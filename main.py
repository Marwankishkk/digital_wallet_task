from fastapi import FastAPI
from api.webhooks import router as webhooks_router
from core.database import connect_to_mongo, close_mongo_connection

app = FastAPI()
app.include_router(webhooks_router, prefix="/api")
# app/main.py

@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()