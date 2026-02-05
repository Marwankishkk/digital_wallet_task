from fastapi import APIRouter, Body, BackgroundTasks
from tasks import process_webhook_task  
import uuid

router = APIRouter()

@router.post("/webhooks/paytech")
async def receive_paytech_webhook(data: str = Body(...)):
    request_id = str(uuid.uuid4())
    process_webhook_task.delay(data, request_id, "paytech")
    return {
        "status": "accepted",
        "request_id": request_id,
        "message": "Webhook received and queued for processing"
    }

@router.post("/webhooks/acme")
async def receive_acme_webhook(data: str = Body(...)):
    request_id = str(uuid.uuid4())
    process_webhook_task.delay(data, request_id, "acme")
    return {
        "status": "accepted",
        "request_id": request_id,
        "message": "Webhook received and queued for processing"
    }