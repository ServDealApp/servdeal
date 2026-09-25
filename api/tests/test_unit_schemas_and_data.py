from datetime import date

import pytest
from pydantic import ValidationError

from app.demo_data import slots_for
from app.schemas import BookingCreate, ServiceMode


def valid_payload(**overrides):
    payload = {
        "vendor_id": "11111111-1111-1111-1111-111111111111",
        "service_id": "s-looks-1",
        "service_mode": "at_salon",
        "booking_date": "2026-10-15",
        "booking_time": "10:00",
        "customer_name": "Test Customer",
        "customer_phone": "9876543210",
    }
    payload.update(overrides)
    return payload


def test_slots_are_stable_and_ordered():
    assert slots_for(date(2026, 10, 15)) == [
        "10:00:00", "11:00:00", "12:00:00", "15:00:00", "16:00:00", "17:00:00",
    ]


def test_at_home_booking_requires_address():
    with pytest.raises(ValidationError, match="customer_address is required"):
        BookingCreate(**valid_payload(service_mode=ServiceMode.at_home))


def test_at_salon_booking_does_not_require_address():
    booking = BookingCreate(**valid_payload())
    assert booking.service_mode is ServiceMode.at_salon


def test_name_must_not_be_single_character():
    with pytest.raises(ValidationError):
        BookingCreate(**valid_payload(customer_name="A"))
