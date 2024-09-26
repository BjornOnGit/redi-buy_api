from fastapi import APIRouter, HTTPException, Depends
from ..models.order import Order
from ..services.payment_service import PaymentService
from ..services.order_service import OrderService
from ..utils.auth import get_current_user
import structlog

logger = structlog.get_logger()

router = APIRouter()

@router.post("/orders/{order_id}/initialize-payment")
async def initialize_payment(order_id: str, user=Depends(get_current_user)):
    order = await OrderService.get_order_by_id(order_id)
    
    if order.user_id != user.id:
        raise HTTPException(status_code=403, detail="You do not have permission to pay for this order.")
    

    payment_service = PaymentService()
    payment_response = await payment_service.initialize_payment(order)
    
    if payment_response.get("status") != True:
        raise HTTPException(status_code=400, detail="Payment initialization failed.")
    
    return {"payment_link": payment_response["data"]["authorization_url"]}

@router.post("/orders/{order_id}/verify-payment")
async def verify_payment(order_id: str, user=Depends(get_current_user)):
    order = await OrderService.get_order_by_id(order_id)

    if order.user_id != user.id:
        raise HTTPException(status_code=403, detail="You do not have permission to pay for this order.")

    payment_service = PaymentService()
    verification_response = await payment_service.verify_payment(reference=str(order.id))

    # logger.info(verification_response)
    
    if verification_response.get("status") != True or verification_response["data"]["status"] != "success":
        raise HTTPException(status_code=400, detail="Payment verification failed.")
    
    if "id" not in verification_response["data"]:
        raise HTTPException(status_code=400, detail="Transaction ID not found in the verification response.")
    
    order.payment_info.transaction_id = str(verification_response["data"]["id"])
    order.status = "paid"
    await OrderService.save_order(order)
    await OrderService.update_order_status(order.id, "paid")
    
    return {"message": "Payment verified successfully", "transaction_id": order.payment_info.transaction_id}
