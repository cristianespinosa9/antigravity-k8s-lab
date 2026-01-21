import os
import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import List

app = FastAPI()

USERS_SERVICE_URL = os.getenv("USERS_SERVICE_URL", "http://localhost:8001")
ORDERS_SERVICE_URL = os.getenv("ORDERS_SERVICE_URL", "http://localhost:8002")

# Schemas
class UserCreate(BaseModel):
    username: str
    email: EmailStr

class User(UserCreate):
    id: int
    is_active: bool

class OrderCreate(BaseModel):
    user_id: int
    item_name: str
    quantity: int
    price: float

class Order(OrderCreate):
    id: int

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "gateway-api"}

# Proxy to Users Service
@app.get("/users/", response_model=List[User])
async def read_users():
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(f"{USERS_SERVICE_URL}/users/")
            resp.raise_for_status()
            return resp.json()
        except httpx.RequestError as exc:
            raise HTTPException(status_code=503, detail=f"Users service not reachable: {exc}")

@app.post("/users/", response_model=User)
async def create_user(user: UserCreate):
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(f"{USERS_SERVICE_URL}/users/", json=user.model_dump())
            if resp.status_code == 400:
                raise HTTPException(status_code=400, detail="Email already registered")
            resp.raise_for_status()
            return resp.json()
        except httpx.RequestError as exc:
             raise HTTPException(status_code=503, detail=f"Users service not reachable: {exc}")

# Proxy to Orders Service
@app.get("/orders/", response_model=List[Order])
async def read_orders():
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(f"{ORDERS_SERVICE_URL}/orders/")
            resp.raise_for_status()
            return resp.json()
        except httpx.RequestError as exc:
             raise HTTPException(status_code=503, detail=f"Orders service not reachable: {exc}")

@app.post("/orders/", response_model=Order)
async def create_order(order: OrderCreate):
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(f"{ORDERS_SERVICE_URL}/orders/", json=order.model_dump())
            resp.raise_for_status()
            return resp.json()
        except httpx.RequestError as exc:
             raise HTTPException(status_code=503, detail=f"Orders service not reachable: {exc}")
