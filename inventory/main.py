from bson import ObjectId
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from contextlib import asynccontextmanager
from db_helper import test_connection, close_connection, COLLECTION


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Inventory Server started...")
    await test_connection()
    yield
    await close_connection()
    print("Inventory Server closed...")


app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ProductIn(BaseModel):
    name: str
    price: float
    quantity: int


class ProductOut(BaseModel):
    id: str = Field(..., alias="_id")
    name: str
    price: float
    quantity: int

    class Config:
        validate_by_name = True


class UpdateProductIn(BaseModel):
    quantity: int


def format_product(product: dict):
    product["_id"] = str(product["_id"])
    return ProductOut(**product)


@app.get("/")
async def ping():
    return {"message": "Hello from Inventory"}


@app.get("/products/list")
async def list_all_products():
    return [format_product(product) async for product in COLLECTION.find()]


@app.get("/products/list/{uid}")
async def list_all_products(uid: str):
    return format_product(await COLLECTION.find_one(filter={"_id": ObjectId(oid=uid)}))


@app.post("/products/create")
async def create_new_product(product: ProductIn):
    inserted_product = await COLLECTION.insert_one(document=product.model_dump())
    return {"message": f"Product with ID '{inserted_product.inserted_id}' inserted"}


@app.delete("/products/delete/{uid}")
async def delete_product(uid: str):
    deleted_product = await COLLECTION.delete_one(filter={"_id": ObjectId(oid=uid)})
    return {"message": f"{deleted_product.deleted_count} product deleted"}


@app.patch("/products/update/{uid}")
async def update_product(uid: str, update_data: UpdateProductIn):
    updated_product = await COLLECTION.update_one(
        filter={"_id": ObjectId(oid=uid)},
        update={"$set": update_data.model_dump()},
    )
    return {"message": f"{updated_product.modified_count} product modified"}
