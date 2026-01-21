from pydantic import BaseModel

class OrderBase(BaseModel):
    user_id: int
    item_name: str
    quantity: int
    price: float

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int

    class Config:
        from_attributes = True
