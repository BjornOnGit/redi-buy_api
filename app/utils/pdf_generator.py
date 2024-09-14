from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from ..models.order import OrderModel

def generate_invoice_pdf(order: OrderModel, filename: str):
    c = canvas.Canvas(filename, pagesize=letter)
    c.setFont("Helvetica", 12)
    c.drawString(100, 750, f"Invoice for Order {order.id}")
    # Add more invoice details...
    c.save()