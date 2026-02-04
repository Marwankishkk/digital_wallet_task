import asyncio
from fastapi import APIRouter,Body
from parsers.base import BaseBankParser
from parsers.paytech import PayTechParser
import logging
from datetime import datetime

router = APIRouter()
logger = logging.getLogger("uvicorn.error")

@router.post("/webhooks/paytech")
async def receive_money(data: str = Body(...)):
    start_time = datetime.now()
    lines = [line.strip() for line in data.splitlines() if line.strip()]
    
    parser: BaseBankParser = PayTechParser()
    success_count = 0
    failed_lines = [] 
    results = []
    for line in lines:
        try:
            transaction = await parser.parse(line)
            if transaction:
                results.append(transaction)
                success_count += 1
            else:
                failed_lines.append({"line": line, "reason": "Parsed as None/Empty"})
        except Exception as e:
            failed_lines.append({"line": line, "reason": str(e)})

    elapsed_seconds = (datetime.now() - start_time).total_seconds()
    
    return {
        "status": "completed" if not failed_lines else "partial_success",
        "summary": {
            "total_received": len(lines),
            "successfully_processed": success_count,
            "failed_count": len(failed_lines)
        },
        "errors": failed_lines, 
        "meta": {
            "execution_time_sec": round(elapsed_seconds, 4),
            "timestamp": datetime.now().isoformat()
        }
    }