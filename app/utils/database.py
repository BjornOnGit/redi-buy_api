from fastapi import FastAPI
from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine, SyncEngine
import os
from contextlib import asynccontextmanager

def get_database_url():
    environment = os.environ.get("ENVIRONMENT")
    if environment == 'production':
        return MONGODB_URL_PRODUCTION
    return MONGODB_URL

MONGODB_URL = os.environ.get("MONGODB_URL")
MONGODB_URL_PRODUCTION = os.environ.get("MONGODB_URL_PRODUCTION")
client = AsyncIOMotorClient(get_database_url)
database = client.redibuy_db
engine = AIOEngine(client, database='redibuy_db')

async def get_database():
    return database

def get_sync_engine():
    sync_client = MongoClient(get_database_url)
    sync_engine = SyncEngine(sync_client, database='redibuy_db')
    return sync_engine

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