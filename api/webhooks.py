from fastapi import APIRouter, Body, BackgroundTasks
from tasks import process_webhook_task  # هنكريت الفايل ده حالا
import uuid

router = APIRouter()

@router.post("/webhooks/paytech")
async def receive_money(data: str = Body(...)):
    request_id = str(uuid.uuid4())
    
    process_webhook_task.delay(data, request_id)
    return {
        "status": "accepted",
        "request_id": request_id,
        "message": "Webhook received and queued for processing"
    }