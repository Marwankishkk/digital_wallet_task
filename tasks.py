# tasks.py
import asyncio
from celery import Celery
from celery.signals import worker_process_init
from core.database import db_instance, connect_to_mongo  
from parsers import get_parser

# Initialize Celery app with Redis as the message broker
app = Celery('webhook_tasks', broker='redis://localhost:6379/0')

@worker_process_init.connect
def init_worker(**kwargs):
    """
    Signal receiver that runs when each worker process starts.
    Ensures that MongoDB connection is established for the worker.
    Without this, db_instance.db would remain None.
    """
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    # Run the async connection function in the worker's event loop
    loop.run_until_complete(connect_to_mongo())
    print("Worker Connected to MongoDB successfully! 🚀")

@app.task(name="process_webhook_task")
def process_webhook_task(data, request_id, bank_name="paytech"):
    """
    Main Celery task that receives the webhook data and executes 
    the asynchronous parsing logic.
    
    Args:
        data: Raw webhook data string
        request_id: Unique identifier for this request
        bank_name: Name of the bank (defaults to "paytech" for backward compatibility)
    """
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
    return loop.run_until_complete(handle_parsing(data, request_id, bank_name))

async def handle_parsing(data, request_id, bank_name="paytech"):
    """
    Logic to split incoming data into lines and parse each line 
    using the appropriate parser based on bank_name.
    
    Args:
        data: Raw webhook data string
        request_id: Unique identifier for this request
        bank_name: Name of the bank to determine which parser to use
    """
    lines = [line.strip() for line in data.splitlines() if line.strip()]
    
    # Get the appropriate parser for the bank
    try:
        parser = get_parser(bank_name)
    except ValueError as e:
        print(f"Task {request_id} - {e}")
        return {"request_id": request_id, "processed_count": 0, "error": str(e)}
    
    results = []
    for line in lines:
        try:
            # The parser can now perform insert_one safely since DB is initialized
            transaction = await parser.parse(line)
            if transaction:
                print(f"Task {request_id} - Processed line: {line[:30]}...")
                # Extracting ID to confirm successful database insertion
                results.append(str(transaction.get('_id', 'inserted')))
            else:
                print(f"Task {request_id} - Line parsed as None: {line[:30]}...")
        except Exception as e:
            # Catching errors per line to prevent the entire worker from crashing
            print(f"Task {request_id} - Error parsing line: {e}")
            
    return {"request_id": request_id, "processed_count": len(results)}