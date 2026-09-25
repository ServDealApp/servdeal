from contextlib import asynccontextmanager
from datetime import date
from uuid import uuid4

import asyncpg
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .demo_data import CATEGORIES, VENDORS, slots_for
from .schemas import BookingCreate, BookingOut, BookingStatus, BookingStatusUpdate, ServiceMode, VendorDetail, VendorSummary


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.pool = await asyncpg.create_pool(settings.database_url) if settings.database_url else None
    app.state.demo_bookings = {}
    yield
    if app.state.pool:
        await app.state.pool.close()


app = FastAPI(title="ServDeal API", version="0.1.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=settings.origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])


def demo_vendor(vendor_id: str):
    return next((vendor for vendor in VENDORS if vendor["id"] == vendor_id), None)


@app.get("/health")
async def health():
    return {"status": "ok", "mode": "database" if app.state.pool else "demo"}


@app.get("/categories")
async def categories():
    return CATEGORIES


@app.get("/vendors", response_model=list[VendorSummary])
async def list_vendors(locality: str | None = None, service_mode: ServiceMode | None = None):
    if app.state.pool:
        rows = await app.state.pool.fetch("""
            SELECT v.id::text, v.slug, v.name, v.salon_type, l.name AS locality, c.name AS city,
                   v.rating, v.review_count, v.home_service_available, v.cover_image
            FROM vendor_profiles v
            JOIN localities l ON l.id = v.locality_id
            JOIN cities c ON c.id = l.city_id
            WHERE v.is_active = true
              AND ($1::text IS NULL OR l.name ILIKE $1)
              AND ($2::text IS NULL OR ($2 IN ('at_home','both') AND v.home_service_available))
            ORDER BY v.rating DESC
        """, locality, service_mode.value if service_mode else None)
        return [dict(row) for row in rows]

    vendors = VENDORS
    if locality:
        vendors = [v for v in vendors if v["locality"].lower() == locality.lower()]
    if service_mode == ServiceMode.at_home:
        vendors = [v for v in vendors if v["home_service_available"]]
    return [{key: value for key, value in vendor.items() if key != "services"} for vendor in vendors]


@app.get("/vendors/{slug}", response_model=VendorDetail)
async def get_vendor(slug: str):
    if app.state.pool:
        row = await app.state.pool.fetchrow("""
            SELECT v.id::text, v.slug, v.name, v.salon_type, l.name AS locality, c.name AS city,
                   v.rating, v.review_count, v.home_service_available, v.cover_image
            FROM vendor_profiles v JOIN localities l ON l.id=v.locality_id JOIN cities c ON c.id=l.city_id
            WHERE v.slug=$1 AND v.is_active=true
        """, slug)
        if not row:
            raise HTTPException(404, "Vendor not found")
        services = await app.state.pool.fetch("""
            SELECT id::text, name, price, offer_price, duration_minutes, service_mode::text, home_service_fee
            FROM services WHERE vendor_id=$1 AND is_active=true ORDER BY display_order, name
        """, row["id"])
        return {**dict(row), "services": [dict(service) for service in services]}

    vendor = next((v for v in VENDORS if v["slug"] == slug), None)
    if not vendor:
        raise HTTPException(404, "Vendor not found")
    return vendor


@app.get("/vendors/{vendor_id}/slots")
async def available_slots(vendor_id: str, booking_date: date = Query(default_factory=date.today)):
    if not demo_vendor(vendor_id) and not app.state.pool:
        raise HTTPException(404, "Vendor not found")
    return {"vendor_id": vendor_id, "booking_date": booking_date, "slots": slots_for(booking_date)}


@app.post("/bookings", response_model=BookingOut, status_code=201)
async def create_booking(payload: BookingCreate):
    if app.state.pool:
        service = await app.state.pool.fetchrow("""
            SELECT s.id, s.name, s.price, s.offer_price, s.service_mode::text, s.home_service_fee, v.name AS vendor_name
            FROM services s JOIN vendor_profiles v ON v.id=s.vendor_id
            WHERE s.id=$1 AND s.vendor_id=$2 AND s.is_active=true
        """, payload.service_id, payload.vendor_id)
        if not service:
            raise HTTPException(400, "Service does not belong to this vendor")
        if service["service_mode"] not in (payload.service_mode.value, "both"):
            raise HTTPException(400, "Selected mode is unavailable for this service")
        total = (service["offer_price"] or service["price"]) + (service["home_service_fee"] if payload.service_mode == ServiceMode.at_home else 0)
        reference = f"SD-{uuid4().hex[:8].upper()}"
        row = await app.state.pool.fetchrow("""
            INSERT INTO bookings (booking_reference, vendor_id, service_id, service_mode, booking_date, booking_time,
              customer_name, customer_phone, customer_email, customer_address, landmark, customer_notes, total_amount)
            VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13) RETURNING id::text, status::text
        """, reference, payload.vendor_id, payload.service_id, payload.service_mode.value, payload.booking_date, payload.booking_time,
             payload.customer_name, payload.customer_phone, payload.customer_email, payload.customer_address, payload.landmark,
             payload.customer_notes, total)
        return {"id": row["id"], "booking_reference": reference, "status": row["status"], "vendor_name": service["vendor_name"], "service_name": service["name"], "booking_date": payload.booking_date, "booking_time": payload.booking_time, "service_mode": payload.service_mode, "total_amount": total}

    vendor = demo_vendor(str(payload.vendor_id))
    if not vendor:
        raise HTTPException(400, "Vendor not found")
    service = next((item for item in vendor["services"] if item["id"] == payload.service_id), None)
    if not service:
        raise HTTPException(400, "Service not found")
    if service["service_mode"] not in (payload.service_mode.value, "both"):
        raise HTTPException(400, "Selected mode is unavailable for this service")
    booking_id = str(uuid4())
    total = (service["offer_price"] or service["price"]) + (service["home_service_fee"] if payload.service_mode == ServiceMode.at_home else 0)
    result = {"id": booking_id, "booking_reference": f"SD-{booking_id[:8].upper()}", "status": BookingStatus.requested, "vendor_name": vendor["name"], "service_name": service["name"], "booking_date": payload.booking_date, "booking_time": payload.booking_time, "service_mode": payload.service_mode, "total_amount": total}
    app.state.demo_bookings[booking_id] = result
    return result


@app.patch("/bookings/{booking_id}/status", response_model=BookingOut)
async def update_booking_status(booking_id: str, payload: BookingStatusUpdate):
    if app.state.pool:
        row = await app.state.pool.fetchrow("""
            UPDATE bookings SET status=$2, updated_at=now() WHERE id=$1
            RETURNING id::text, booking_reference, status::text, booking_date, booking_time, service_mode::text, total_amount
        """, booking_id, payload.status.value)
        if not row:
            raise HTTPException(404, "Booking not found")
        details = await app.state.pool.fetchrow("""
            SELECT v.name AS vendor_name, s.name AS service_name FROM bookings b
            JOIN vendor_profiles v ON v.id=b.vendor_id JOIN services s ON s.id=b.service_id WHERE b.id=$1
        """, booking_id)
        return {**dict(row), **dict(details)}
    booking = app.state.demo_bookings.get(booking_id)
    if not booking:
        raise HTTPException(404, "Booking not found")
    booking["status"] = payload.status
    return booking
