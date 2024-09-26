import httpx
import os
import random
import string
import datetime
from celery import Celery
from .models.order import Order
from .models.invoice import Invoice
from .services.recommendation_service import recommend_products_for_user
from fastapi import HTTPException
from weasyprint import HTML
from jinja2 import Template
from .services.invoice_service import InvoiceService
from bson import ObjectId
from pathlib import Path
from .utils.database import get_sync_engine
from .utils.cache import redis_client

MAILGUN_DOMAIN = os.getenv('MAILGUN_DOMAIN')
MAILGUN_API_KEY = os.getenv('MAILGUN_API_KEY')
MAILGUN_SENDER_EMAIL = os.getenv('MAILGUN_SENDER_EMAIL', 'fhrancorey99@gmail.com')

celery_app = Celery('tasks', broker='redis://localhost:6379/0')

celery_app.conf.task_routes = {
    'app.tasks.*': {'queue': 'main-queue'}
}
celery_app.conf.update(
    broker_connection_retry_on_startup=True
)

@celery_app.task
def send_order_confirmation(order_id: str):
    engine = get_sync_engine()
     # Fetch the order
    order = engine.find_one(Order, {"_id": ObjectId(order_id)})
    if not order:
        raise HTTPException(status_code=404, detail="Order not found.")
    
    # Email settings
    receiver = order.email
    subject = 'Order Confirmation'

    # Mailgun API request URL
    mailgun_api_url = f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages"

    # Prepare the request data, including template variables
    data = {
        "from": f"Your Company <{MAILGUN_SENDER_EMAIL}>",
        "to": receiver,
        "subject": subject,
        "template": "order_confirmation_template",  # Use your Mailgun template name
        "h:X-Mailgun-Variables": {
            "order_id": order_id,
            "user_email": order.email,
            "order_date": str(order.created_at),
            # Add any other variables needed in the template
        }
    }

    # Send the request using httpx
    try:
        response = httpx.post(
            mailgun_api_url,
            auth=("api", MAILGUN_API_KEY),
            data=data
        )

        if response.status_code == 200:
            print(f"Order confirmation email sent to {receiver}.")
        else:
            print(f"Failed to send email: {response.status_code} {response.text}")

    except Exception as e:
        print(f"Error sending email: {str(e)}")

@celery_app.task
def create_invoice(order_id: str):
    engine = engine = get_sync_engine()
    
    # Fetch the relevant order
    order = engine.find_one(Order, {"_id": ObjectId(order_id)})
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Generate a unique invoice number
    invoice_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    
    # Create and store the invoice
    invoice = Invoice(
        order_id=order.id,
        invoice_number=invoice_number,
        total_amount=order.total_amount,
        created_at=datetime.datetime.now()
    )
    
    engine.save(invoice)
    return invoice
@celery_app.task
def generate_invoice(order_id: str):
    engine = engine = get_sync_engine()
    # Fetch the order and invoice
    order = engine.find_one(Order, {"_id": ObjectId(order_id)})
    if not order:
        raise HTTPException(status_code=404, detail="Order not found.")
    
    invoice = engine.find_one(Invoice, {"order_id": ObjectId(order_id)})
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found.")
    
    # Invoice template using Jinja2 (you can place this in a separate .html file)
    html_template = Template("""
    <html>
        <body>
            <h1>Invoice</h1>
            <p>Invoice Number: {{ invoice.invoice_number }}</p>
            <p>Order ID: {{ order.id }}</p>
            <p>Total Amount: {{ invoice.total_amount }}</p>
            <p>Date: {{ invoice.created_at }}</p>
        </body>
    </html>
    """)
    
    # Render the HTML
    html_content = html_template.render(order=order, invoice=invoice)
    
    # Generate PDF from the rendered HTML
    pdf_file_path = f"invoices/invoice_{invoice.invoice_number}.pdf"
    Path("invoices").mkdir(parents=True, exist_ok=True)  # Ensure the directory exists
    HTML(string=html_content).write_pdf(pdf_file_path)
    
    print(f"Invoice PDF generated at: {pdf_file_path}")
    
    return pdf_file_path

@celery_app.task
def update_user_recommendations(user_id: str):
    engine = get_sync_engine()
    recommended_products = recommend_products_for_user(ObjectId(user_id))
    # Save or cache recommendations in Redis or DB for fast retrieval
    redis_client.set(f"user:{user_id}:recommendations", recommended_products)