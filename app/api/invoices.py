from fastapi import APIRouter, HTTPException, status
from ..services.invoice_service import InvoiceService
from fastapi.encoders import jsonable_encoder
import structlog

logger = structlog.get_logger()
router = APIRouter()

# Get invoice by order ID
@router.get("/invoices/{order_id}", status_code=status.HTTP_200_OK)
async def get_invoice(order_id: str):
    try:
        invoices = await InvoiceService.get_invoice_by_order(order_id)
        logger.info(invoices)
        return jsonable_encoder(invoices)
    except HTTPException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invoice not found")

# Download invoice by order ID
@router.get("/invoices/{order_id}/download", status_code=status.HTTP_200_OK)
async def download_invoice(order_id: str):
    try:
        return await InvoiceService.download_invoice(order_id)
    except HTTPException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Couldn't download invoice")
