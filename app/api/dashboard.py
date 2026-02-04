from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.product import Product

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/analytics")
def get_dashboard_analytics(db: Session = Depends(get_db)):
    total_products = db.query(func.count(Product.id)).scalar()
    active_products = db.query(func.count(Product.id)).filter(Product.is_active == True).scalar()
    inactive_products = db.query(func.count(Product.id)).filter(Product.is_active == False).scalar()
    total_value = db.query(func.sum(Product.price * Product.quantity)).scalar() or 0
    total_quantity = db.query(func.sum(Product.quantity)).scalar() or 0
    low_stock_count = db.query(func.count(Product.id)).filter(Product.quantity <= 10).scalar()
    out_of_stock_count = db.query(func.count(Product.id)).filter(Product.quantity == 0).scalar()

    category_breakdown = db.query(
        Product.category,
        func.count(Product.id).label('count')
    ).group_by(Product.category).all()

    categories = [
        {"category": cat or "Uncategorized", "count": count}
        for cat, count in category_breakdown
    ]

    stock_status = [
        {"status": "In Stock", "count": db.query(func.count(Product.id)).filter(Product.quantity > 10).scalar()},
        {"status": "Low Stock", "count": low_stock_count - out_of_stock_count},
        {"status": "Out of Stock", "count": out_of_stock_count}
    ]

    top_expensive = db.query(Product).order_by(Product.price.desc()).limit(5).all()
    top_expensive_products = [
        {
            "id": p.id,
            "name": p.name,
            "sku": p.sku,
            "price": float(p.price),
            "quantity": p.quantity
        }
        for p in top_expensive
    ]

    top_quantity = db.query(Product).order_by(Product.quantity.desc()).limit(5).all()
    top_quantity_products = [
        {
            "id": p.id,
            "name": p.name,
            "sku": p.sku,
            "price": float(p.price),
            "quantity": p.quantity
        }
        for p in top_quantity
    ]

    products_with_qr = db.query(func.count(Product.id)).filter(Product.qr_code.isnot(None)).scalar()
    products_without_qr = total_products - products_with_qr
    
    return {
        "summary": {
            "total_products": total_products,
            "active_products": active_products,
            "inactive_products": inactive_products,
            "total_inventory_value": round(float(total_value), 2),
            "total_quantity": total_quantity,
            "low_stock_count": low_stock_count,
            "out_of_stock_count": out_of_stock_count,
            "products_with_qr": products_with_qr,
            "products_without_qr": products_without_qr
        },
        "category_breakdown": categories,
        "stock_status": stock_status,
        "top_expensive_products": top_expensive_products,
        "top_quantity_products": top_quantity_products
    }
