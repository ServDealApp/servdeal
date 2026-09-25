# ServDeal MVP 1.1

India-first salon booking MVP for Kanpur. This package contains:

- `web/`: responsive Next.js customer website
- `api/`: FastAPI booking API
- `supabase/migrations/`: PostgreSQL/Supabase schema and demo Kanpur data

## MVP scope

- Kanpur only
- Men, women, and unisex salon partners
- At-salon, at-home, or both service modes
- Direct payment to the salon at launch
- Booking status: `requested`, `confirmed`, `rejected`, `completed`, `cancelled`

## 1. Database

Create a new, dedicated Supabase project for ServDeal. Run the files in this order in the Supabase SQL editor:

1. `supabase/migrations/0001_initial.sql`
2. `supabase/migrations/0002_seed_kanpur.sql`

Copy the project connection string into `api/.env` using `api/.env.example`.

## 2. API

```bash
cd api
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

Without `DATABASE_URL`, the API starts in demo mode with in-memory Kanpur salon data. Set `DATABASE_URL` for the real Supabase database.

Open `http://localhost:8000/docs` for interactive API documentation.

## 3. Website

```bash
cd web
cp .env.local.example .env.local
npm install
npm run dev
```

The frontend uses local demo data if `NEXT_PUBLIC_API_URL` is not configured. Set it to `http://localhost:8000` for local API development.

## Production notes

- Deploy `web/` as a dedicated Vercel project for `servdeal.com`.
- Deploy `api/` as a separate FastAPI service and store its URL in `NEXT_PUBLIC_API_URL`.
- Keep this in a new private `ServDealApp/servdeal` repository. Do not share AIMates' database or secrets.
- Do not add platform payments until a merchant/payment agreement exists.
