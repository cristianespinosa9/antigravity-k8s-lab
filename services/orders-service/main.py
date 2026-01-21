from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "orders-service"}

@app.post("/orders/", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(database.get_db)):
    new_order = models.Order(
        user_id=order.user_id,
        item_name=order.item_name,
        quantity=order.quantity,
        price=order.price
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order

@app.get("/orders/", response_model=list[schemas.Order])
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    orders = db.query(models.Order).offset(skip).limit(limit).all()
    return orders
