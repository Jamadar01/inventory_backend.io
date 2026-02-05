# inventory_backend.io
Inventory Management Backend

REST API for inventory management built with FastAPI, SQLAlchemy, and PostgreSQL.
Handles CRUD operations, dashboard analytics, and QR code generation using a third-party API.

🚀 Live URLs

Backend (Railway):
👉 https://inventorybackendio-production.up.railway.app/

Frontend (Vercel):
👉 https://inventory-frontend-io.vercel.app/

🛠 Tech Stack

FastAPI (Python 3.11)

SQLAlchemy 2.0+

Pydantic 2.0+

PostgreSQL (production) / SQLite (local dev)

API Ninjas (QR code generation with free fallback)

Deployed on Railway (Nixpacks)

Database hosted on Neon (serverless PostgreSQL)

📦 Requirements

Python 3.11+

pip

PostgreSQL (optional — SQLite works for local dev)

⚙️ Setup (Local Development)
git clone https://github.com/Jamadar01/inventory_backend.io.git
cd inventory_backend.io

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

cp .env.example .env

uvicorn app.main:app --reload


Server runs at:
👉 http://localhost:8000

API Docs

Swagger UI: http://localhost:8000/docs

ReDoc: http://localhost:8000/redoc

🔐 Environment Variables

Copy .env.example to .env and configure:

Variable	Description	Example
DATABASE_URL	DB connection string	sqlite:///./inventory.db
QR_API_KEY	API Ninjas QR key	Leave empty to use fallback
DEBUG	Debug mode	True
SECRET_KEY	App secret	your-secret-key
ALLOWED_ORIGINS	CORS origins	http://localhost:3000,http://localhost:5173
Database Notes

Local: SQLite auto-creates inventory.db

Production: PostgreSQL (Neon, Supabase, etc.)

Tables auto-created via Base.metadata.create_all() (no Alembic needed)

🔌 API Endpoints
Products
Method	Endpoint	Description
GET	/products/?skip=0&limit=100	List all products
GET	/products/{id}	Get single product
POST	/products/	Create product
PUT	/products/{id}	Update product
DELETE	/products/{id}	Delete product
POST	/products/{id}/generate-qr	Generate QR code
Dashboard
Method	Endpoint	Description
GET	/dashboard/analytics	Inventory analytics
📊 Dashboard Features

Total products

Active products

Inventory quantity & value

Low stock & out-of-stock counts

Category distribution

Top 5 expensive products

Top 5 products by quantity

🔳 QR Code Generation

Generated per product

Encodes JSON with:

Product ID

Name

SKU

Price

Uses API Ninjas QR API

Automatically falls back to qrserver.com if no API key is set

Downloadable as PNG from frontend


🚢 Deployment (Railway)

Start command:

uvicorn app.main:app --host 0.0.0.0 --port $PORT

Steps

Push repo to GitHub

Create Railway project

Connect repository

Set DATABASE_URL and QR_API_KEY

Deploy 🚀

🔗 Related Repository

Frontend (Vercel):
👉 https://inventory-frontend-io.vercel.app/
