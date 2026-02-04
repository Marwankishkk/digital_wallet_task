from fastapi import FastAPI
from api.webhooks import router as webhooks_router

app = FastAPI()
app.include_router(webhooks_router, prefix="/api")
