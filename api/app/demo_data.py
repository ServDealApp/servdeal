from datetime import date, time


CATEGORIES = [
    {"slug": "men-salon", "name": "Men's Salon", "audience": "men"},
    {"slug": "women-salon", "name": "Women's Salon", "audience": "women"},
    {"slug": "unisex-salon", "name": "Unisex Salon", "audience": "unisex"},
]

VENDORS = [
    {
        "id": "11111111-1111-1111-1111-111111111111",
        "slug": "looks-salon-kakadeo",
        "name": "Looks Salon",
        "salon_type": "unisex",
        "locality": "Kakadeo",
        "city": "Kanpur",
        "rating": 4.6,
        "review_count": 128,
        "home_service_available": True,
        "cover_image": "https://images.unsplash.com/photo-1560066984-138dadb4c035?auto=format&fit=crop&w=900&q=80",
        "services": [
            {"id": "s-looks-1", "name": "Hair Cut + Blow Dry", "price": 799, "offer_price": 599, "duration_minutes": 60, "service_mode": "both", "home_service_fee": 99},
            {"id": "s-looks-2", "name": "Hair Spa", "price": 1499, "offer_price": 1199, "duration_minutes": 90, "service_mode": "at_salon", "home_service_fee": 0},
        ],
    },
    {
        "id": "22222222-2222-2222-2222-222222222222",
        "slug": "urban-grooming-swarup-nagar",
        "name": "Urban Grooming Studio",
        "salon_type": "men",
        "locality": "Swarup Nagar",
        "city": "Kanpur",
        "rating": 4.5,
        "review_count": 84,
        "home_service_available": True,
        "cover_image": "https://images.unsplash.com/photo-1621605815971-fbc98d665033?auto=format&fit=crop&w=900&q=80",
        "services": [
            {"id": "s-urban-1", "name": "Haircut + Beard Styling", "price": 499, "offer_price": 399, "duration_minutes": 45, "service_mode": "both", "home_service_fee": 79},
            {"id": "s-urban-2", "name": "Facial", "price": 899, "offer_price": None, "duration_minutes": 60, "service_mode": "at_salon", "home_service_fee": 0},
        ],
    },
    {
        "id": "33333333-3333-3333-3333-333333333333",
        "slug": "glow-women-parade",
        "name": "Glow Women Salon",
        "salon_type": "women",
        "locality": "Parade",
        "city": "Kanpur",
        "rating": 4.7,
        "review_count": 65,
        "home_service_available": False,
        "cover_image": "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?auto=format&fit=crop&w=900&q=80",
        "services": [
            {"id": "s-glow-1", "name": "Haircut + Hair Wash", "price": 699, "offer_price": 549, "duration_minutes": 60, "service_mode": "at_salon", "home_service_fee": 0},
            {"id": "s-glow-2", "name": "Party Makeup", "price": 2999, "offer_price": None, "duration_minutes": 120, "service_mode": "at_salon", "home_service_fee": 0},
        ],
    },
]


def slots_for(_: date) -> list[str]:
    return [time(10, 0).isoformat(), time(11, 0).isoformat(), time(12, 0).isoformat(), time(15, 0).isoformat(), time(16, 0).isoformat(), time(17, 0).isoformat()]
