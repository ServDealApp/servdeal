from datetime import date, time
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, model_validator


class ServiceMode(str, Enum):
    at_salon = "at_salon"
    at_home = "at_home"
    both = "both"


class BookingStatus(str, Enum):
    requested = "requested"
    confirmed = "confirmed"
    rejected = "rejected"
    completed = "completed"
    cancelled = "cancelled"


class ServiceOut(BaseModel):
    id: str
    name: str
    price: int
    offer_price: int | None = None
    duration_minutes: int
    service_mode: ServiceMode
    home_service_fee: int = 0


class VendorSummary(BaseModel):
    id: str
    slug: str
    name: str
    salon_type: str
    locality: str
    city: str
    rating: float
    review_count: int
    home_service_available: bool
    cover_image: str | None = None


class VendorDetail(VendorSummary):
    services: list[ServiceOut]


class BookingCreate(BaseModel):
    vendor_id: UUID
    service_id: str
    service_mode: ServiceMode
    booking_date: date
    booking_time: time
    customer_name: str = Field(min_length=2, max_length=100)
    customer_phone: str = Field(min_length=8, max_length=20)
    customer_email: EmailStr | None = None
    customer_address: str | None = Field(default=None, max_length=500)
    landmark: str | None = Field(default=None, max_length=160)
    customer_notes: str | None = Field(default=None, max_length=500)

    @model_validator(mode="after")
    def require_address_for_home_service(self):
        if self.service_mode == ServiceMode.at_home and not self.customer_address:
            raise ValueError("customer_address is required for at-home service")
        return self


class BookingOut(BaseModel):
    id: str
    booking_reference: str
    status: BookingStatus
    vendor_name: str
    service_name: str
    booking_date: date
    booking_time: time
    service_mode: ServiceMode
    total_amount: int


class BookingStatusUpdate(BaseModel):
    status: BookingStatus
