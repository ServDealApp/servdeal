LOOKS_ID = "11111111-1111-1111-1111-111111111111"
GLOW_ID = "33333333-3333-3333-3333-333333333333"


def booking_payload(**overrides):
    payload = {
        "vendor_id": LOOKS_ID,
        "service_id": "s-looks-1",
        "service_mode": "at_salon",
        "booking_date": "2026-10-15",
        "booking_time": "10:00",
        "customer_name": "Saurabh Test",
        "customer_phone": "9876543210",
    }
    payload.update(overrides)
    return payload


def test_health_reports_demo_mode(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "mode": "demo"}


def test_vendor_discovery_detail_and_slots(client):
    vendors = client.get("/vendors", params={"locality": "Kakadeo"})
    assert vendors.status_code == 200
    assert [vendor["slug"] for vendor in vendors.json()] == ["looks-salon-kakadeo"]
    detail = client.get("/vendors/looks-salon-kakadeo")
    assert detail.status_code == 200
    assert detail.json()["services"][0]["id"] == "s-looks-1"
    slots = client.get(f"/vendors/{LOOKS_ID}/slots", params={"booking_date": "2026-10-15"})
    assert slots.status_code == 200
    assert "10:00:00" in slots.json()["slots"]


def test_vendor_filters_at_home_only(client):
    response = client.get("/vendors", params={"service_mode": "at_home"})
    assert response.status_code == 200
    assert {vendor["slug"] for vendor in response.json()} == {"looks-salon-kakadeo", "urban-grooming-swarup-nagar"}


def test_booking_lifecycle_at_salon(client):
    created = client.post("/bookings", json=booking_payload())
    assert created.status_code == 201
    booking = created.json()
    assert booking["booking_reference"].startswith("SD-")
    assert booking["status"] == "requested"
    assert booking["total_amount"] == 599
    confirmed = client.patch(f"/bookings/{booking['id']}/status", json={"status": "confirmed"})
    assert confirmed.status_code == 200
    assert confirmed.json()["status"] == "confirmed"


def test_home_booking_adds_home_service_fee(client):
    response = client.post("/bookings", json=booking_payload(service_mode="at_home", customer_address="Kakadeo, Kanpur"))
    assert response.status_code == 201
    assert response.json()["total_amount"] == 698  # 599 + 99


def test_rejects_invalid_bookings(client):
    missing_address = client.post("/bookings", json=booking_payload(service_mode="at_home"))
    assert missing_address.status_code == 422
    wrong_service = client.post("/bookings", json=booking_payload(service_id="does-not-exist"))
    assert wrong_service.status_code == 400
    unavailable = client.post("/bookings", json=booking_payload(vendor_id=GLOW_ID, service_id="s-glow-1", service_mode="at_home", customer_address="Parade, Kanpur"))
    assert unavailable.status_code == 400


def test_missing_vendor_and_booking_return_404(client):
    assert client.get("/vendors/not-a-salon").status_code == 404
    assert client.patch("/bookings/00000000-0000-0000-0000-000000000000/status", json={"status": "confirmed"}).status_code == 404
