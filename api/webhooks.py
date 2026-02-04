from fastapi import APIRouter,Body

router=APIRouter()

@router.post("/receive_money")
async def receive_money(data: str = Body(...)):
    print(data)
    return {"data" : data}