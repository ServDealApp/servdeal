insert into countries (id, name, code, currency_code)
values ('00000000-0000-0000-0000-000000000001', 'India', 'IN', 'INR')
on conflict (code) do nothing;

insert into cities (id, country_id, name, slug)
values ('00000000-0000-0000-0000-000000000010', '00000000-0000-0000-0000-000000000001', 'Kanpur', 'kanpur')
on conflict (slug) do nothing;

insert into localities (id, city_id, name, slug) values
('00000000-0000-0000-0000-000000000101', '00000000-0000-0000-0000-000000000010', 'Kakadeo', 'kakadeo'),
('00000000-0000-0000-0000-000000000102', '00000000-0000-0000-0000-000000000010', 'Swarup Nagar', 'swarup-nagar'),
('00000000-0000-0000-0000-000000000103', '00000000-0000-0000-0000-000000000010', 'Parade', 'parade')
on conflict (city_id, slug) do nothing;

insert into vendor_profiles (id, slug, name, salon_type, locality_id, contact_name, contact_phone, address, home_service_available, rating, review_count, cover_image, is_active) values
('11111111-1111-1111-1111-111111111111', 'looks-salon-kakadeo', 'Looks Salon', 'unisex', '00000000-0000-0000-0000-000000000101', 'Demo Owner', '9000000001', 'Kakadeo, Kanpur', true, 4.6, 128, 'https://images.unsplash.com/photo-1560066984-138dadb4c035?auto=format&fit=crop&w=900&q=80', true),
('22222222-2222-2222-2222-222222222222', 'urban-grooming-swarup-nagar', 'Urban Grooming Studio', 'men', '00000000-0000-0000-0000-000000000102', 'Demo Owner', '9000000002', 'Swarup Nagar, Kanpur', true, 4.5, 84, 'https://images.unsplash.com/photo-1621605815971-fbc98d665033?auto=format&fit=crop&w=900&q=80', true),
('33333333-3333-3333-3333-333333333333', 'glow-women-parade', 'Glow Women Salon', 'women', '00000000-0000-0000-0000-000000000103', 'Demo Owner', '9000000003', 'Parade, Kanpur', false, 4.7, 65, 'https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?auto=format&fit=crop&w=900&q=80', true)
on conflict (slug) do nothing;

insert into services (vendor_id, name, price, offer_price, duration_minutes, service_mode, home_service_fee, display_order) values
('11111111-1111-1111-1111-111111111111', 'Hair Cut + Blow Dry', 799, 599, 60, 'both', 99, 1),
('11111111-1111-1111-1111-111111111111', 'Hair Spa', 1499, 1199, 90, 'at_salon', 0, 2),
('22222222-2222-2222-2222-222222222222', 'Haircut + Beard Styling', 499, 399, 45, 'both', 79, 1),
('22222222-2222-2222-2222-222222222222', 'Facial', 899, null, 60, 'at_salon', 0, 2),
('33333333-3333-3333-3333-333333333333', 'Haircut + Hair Wash', 699, 549, 60, 'at_salon', 0, 1),
('33333333-3333-3333-3333-333333333333', 'Party Makeup', 2999, null, 120, 'at_salon', 0, 2);
