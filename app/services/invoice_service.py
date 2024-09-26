from ..utils.database import get_engine
from ..models.invoice import Invoice
from ..models.order import Order
from bson import ObjectId
from fastapi import HTTPException
import structlog

logger = structlog.get_logger()

class InvoiceService:

    async def get_invoice_by_order(order_id: str):
        engine = await get_engine()
        invoice = await engine.find_one(Invoice, Invoice.order_id == ObjectId(order_id))
        # logger.info(f"Invoice fetched: {invoice}")
        if not invoice:
            raise HTTPException(status_code=404, detail="Invoice not found for this order.")
        return invoice

    async def download_invoice(order_id: str):
        engine = await get_engine()
        # In a real-world case, you may want to return a PDF or downloadable file
        invoice = await engine.find_one(Invoice, Invoice.order_id == ObjectId(order_id))
        if not invoice:
            raise HTTPException(status_code=404, detail="Invoice not found for this order.")
    
        # Trigger the Celery task to generate the PDF asynchronously
        from ..celery_app import generate_invoice
        generate_invoice.delay(order_id)
    
        # Return a message or the invoice object itself (PDF generation will happen in the background)
        return {
        "message": "Invoice generation in progress. You will receive it shortly.",
        "invoice": invoice
        }
