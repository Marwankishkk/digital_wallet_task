from fastapi import APIRouter,Body
from parsers.base import BaseBankParser
from parsers.paytech import PayTechParser
router=APIRouter()

@router.post("/webhooks/paytech")
async def receive_money(data: str = Body(...)):
    lines = data.splitlines()
    parser: BaseBankParser = PayTechParser()
    parsed_transactions = []
    
    for line in lines:
        if line.strip():
            # لازم await هنا عشان الدالة بقت async وبتحفظ في الـ DB
            transaction = await parser.parse(line)
            parsed_transactions.append(transaction)

    print(parsed_transactions)
    return {
        "status": "ok",
        "transactions_received": len(parsed_transactions)
    }