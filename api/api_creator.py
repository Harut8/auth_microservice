import asyncio

from fastapi import FastAPI

from amqp_service.rabbit_app.rabbit_app import RabbitMQ
from api.user_api import user_router
from uvicorn import run
from repository.core.core import DbConnection

app = FastAPI(version="1.0.0")
app.include_router(user_router, prefix="/api/v1")


@app.on_event("startup")
async def on_start_server():
    await DbConnection.create_connection()
    await RabbitMQ.connect("pcassa_")
    asyncio.ensure_future(RabbitMQ.consume('harut','harut'))


@app.get("/")
async def ping():
    await RabbitMQ.publish('harut', 'harut_message', 'harut')
    return {"status": "SERVER RUNNING"}


def run_server():
    run(app)
