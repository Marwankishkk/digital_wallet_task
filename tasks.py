# tasks.py
import asyncio
from celery import Celery
from celery.signals import worker_process_init
from core.database import db_instance, connect_to_mongo  
from parsers.paytech import PayTechParser

app = Celery('webhook_tasks', broker='redis://localhost:6379/0')

@worker_process_init.connect
def init_worker(**kwargs):
    
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    loop.run_until_complete(connect_to_mongo())
    print("Worker Connected to MongoDB successfully! 🚀")

@app.task(name="process_webhook_task")
def process_webhook_task(data, request_id):
    """
    الـ Task دي بتستلم الـ Webhook وبتشغل الـ Async logic بتاعك.
    """
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
    return loop.run_until_complete(handle_parsing(data, request_id))

async def handle_parsing(data, request_id):
    lines = [line.strip() for line in data.splitlines() if line.strip()]
    parser = PayTechParser()
    
    results = []
    for line in lines:
        try:
            # دلوقتي الـ parser هيقدر يعمل insert_one من غير Error
            transaction = await parser.parse(line)
            if transaction:
                print(f"Task {request_id} - Processed line: {line[:30]}...")
                results.append(str(transaction.get('_id', 'inserted')))
            else:
                print(f"Task {request_id} - Line parsed as None: {line[:30]}...")
        except Exception as e:
            # هنا بنمسك أي Error عشان الـ Worker ميتوقفش
            print(f"Task {request_id} - Error parsing line: {e}")
            
    return {"request_id": request_id, "processed_count": len(results)}