from fastapi import APIRouter, Depends, HTTPException
from typing import List
from datetime import datetime
import hmac
import hashlib

from app.utils.razorpay_config import client, RAZORPAY_KEY_SECRET
from app.models.payment import PaymentRequest, VerifyRequest, PaymentRecord
from app.utils.auth import get_current_user  

router = APIRouter(prefix="/payment", tags=["Payment"],dependencies=[Depends(get_current_user)])

payment_db: List[PaymentRecord] = []

# Add payment record
def add_payment_record(user_id, order_id, amount, currency, status):
    payment_db.append(PaymentRecord(
        user_id=user_id,
        razorpay_order_id=order_id,
        amount=amount,
        currency=currency,
        status=status,
        timestamp=datetime.now()
    ))

# Update payment status
def update_payment_status(order_id, payment_id, status):
    for payment in payment_db:
        if payment.razorpay_order_id == order_id:
            payment.razorpay_payment_id = payment_id
            payment.status = status
            break

# Get all payments (for testing/debug)
def get_all_payments():
    return payment_db


@router.post("/pay")
def create_order(request: PaymentRequest):
    try:
        order = client.order.create({
            "amount": int(request.amount * 100), 
            "currency": request.currency,
            "payment_capture": 1
        })

        add_payment_record(
            user_id=request.user_id,
            order_id=order["id"],
            amount=request.amount,
            currency=request.currency,
            status="created"
        )

        return {
            "order_id": order["id"],
            "currency": request.currency,
            "amount": request.amount,
            "status": "created"
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Payment order creation failed: {str(e)}")


@router.post("/verify")
def verify_payment(data: VerifyRequest):
    body = f"{data.razorpay_order_id}|{data.razorpay_payment_id}"

    expected_signature = hmac.new(
        key=bytes(RAZORPAY_KEY_SECRET, 'utf-8'),
        msg=bytes(body, 'utf-8'),
        digestmod=hashlib.sha256
    ).hexdigest()

    if expected_signature == data.razorpay_signature:
        update_payment_status(
            order_id=data.razorpay_order_id,
            payment_id=data.razorpay_payment_id,
            status="paid"
        )
        return {"status": "Payment verified successfully."}
    else:
        update_payment_status(
            order_id=data.razorpay_order_id,
            payment_id=data.razorpay_payment_id,
            status="failed"
        )
        raise HTTPException(status_code=400, detail="Invalid payment signature.")
