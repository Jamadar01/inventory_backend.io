from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.product import Product, ProductCreate, ProductUpdate
from app.crud.product import (
    get_product,
    get_products,
    create_product,
    update_product,
    delete_product
)
from app.utils.qr_generator import generate_qr_code

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=List[Product])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_products(db, skip=skip, limit=limit)


@router.get("/{product_id}", response_model=Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@router.post("/", response_model=Product)
def create_new_product(product: ProductCreate, db: Session = Depends(get_db)):
    return create_product(db=db, product=product)


@router.put("/{product_id}", response_model=Product)
def update_existing_product(
    product_id: int, product: ProductUpdate, db: Session = Depends(get_db)
):
    db_product = update_product(db, product_id=product_id, product=product)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@router.delete("/{product_id}")
def delete_existing_product(product_id: int, db: Session = Depends(get_db)):
    success = delete_product(db, product_id=product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}


@router.post("/{product_id}/generate-qr")
def regenerate_qr_code(product_id: int, db: Session = Depends(get_db)):
    db_product = get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    qr_code_data = generate_qr_code({
        'id': db_product.id,
        'name': db_product.name,
        'sku': db_product.sku,
        'price': float(db_product.price)
    })

    db_product.qr_code = qr_code_data
    db.commit()
    db.refresh(db_product)

    return {
        "message": "QR code regenerated successfully",
        "qr_code": qr_code_data
    }
