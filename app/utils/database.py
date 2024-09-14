from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine
import os
from contextlib import asynccontextmanager

MONGODB_URL = os.environ.get("MONGODB_URL")
client = AsyncIOMotorClient(MONGODB_URL)
database = client.redibuy_db
engine = AIOEngine(client, database='redibuy_db')

async def get_database():
    return database

async def get_engine():
    return engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    await startup_db_client(app)
    yield

    await shutdown_db_client(app)

async def startup_db_client(app: FastAPI):
    app.mongodb_client = client
    app.mongodb = app.mongodb_client.get_database('redibuy_db')
    print("RediBuyDB connected")

async def shutdown_db_client(app: FastAPI):
    app.mongodb_client.close()
    print("RediBuyDB connected")