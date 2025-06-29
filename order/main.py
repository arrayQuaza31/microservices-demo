from enum import Enum
from bson import ObjectId
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from contextlib import asynccontextmanager
from db_helper import test_connection, close_connection, COLLECTION


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Order Server started...")
    await test_connection()
    yield
    await close_connection()
    print("Order Server closed...")


app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class Status(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    REFUNDED = "refunded"


class OrderIn(BaseModel):
    product_id: str
    price: float
    fee: float
    total: float
    quantity: int
    status: Status


@app.get("/")
async def ping():
    return {"message": "Hello from Order"}
