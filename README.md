# Orivas Market

Marketplace platform (uy, mashina, telefon, mebel va boshqa mahsulotlar uchun sotish/sotib olish/ijara).

## Stack
FastAPI + SQLAlchemy 2.x + PostgreSQL + Alembic + JWT

## Ishga tushirish (development)

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# .env faylini o'zingizning DB va JWT secret'ingiz bilan to'ldiring

uvicorn app.main:app --reload
```

Swagger UI: http://localhost:8000/docs

## Status
🚧 Loyiha bosqichma-bosqich qurilmoqda. Hozirgi bosqich: Project Setup.
