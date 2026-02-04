from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.api.products import router
from app.api.dashboard import router as dashboard_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Inventory Management API",
    description="A simple CRUD API for inventory management",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
app.include_router(dashboard_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to Inventory Management API",
        "docs": "/docs",
        "redoc": "/redoc"
    }
