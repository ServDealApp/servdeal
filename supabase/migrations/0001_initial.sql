create extension if not exists pgcrypto;

create type salon_type as enum ('men', 'women', 'unisex');
create type service_mode as enum ('at_salon', 'at_home', 'both');
create type booking_status as enum ('requested', 'confirmed', 'rejected', 'completed', 'cancelled');

create table countries (
  id uuid primary key default gen_random_uuid(),
  name text not null unique,
  code char(2) not null unique,
  currency_code char(3) not null default 'INR',
  created_at timestamptz not null default now()
);

create table cities (
  id uuid primary key default gen_random_uuid(),
  country_id uuid not null references countries(id),
  name text not null,
  slug text not null unique,
  is_active boolean not null default true,
  created_at timestamptz not null default now()
);

create table localities (
  id uuid primary key default gen_random_uuid(),
  city_id uuid not null references cities(id) on delete cascade,
  name text not null,
  slug text not null,
  created_at timestamptz not null default now(),
  unique(city_id, slug)
);

create table vendor_profiles (
  id uuid primary key default gen_random_uuid(),
  slug text not null unique,
  name text not null,
  salon_type salon_type not null,
  locality_id uuid not null references localities(id),
  contact_name text not null,
  contact_phone text not null,
  manager_email text,
  address text not null,
  opening_time time not null default '10:00',
  closing_time time not null default '20:00',
  home_service_available boolean not null default false,
  rating numeric(2,1) not null default 0,
  review_count integer not null default 0,
  cover_image text,
  is_active boolean not null default false,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table vendor_service_areas (
  id uuid primary key default gen_random_uuid(),
  vendor_id uuid not null references vendor_profiles(id) on delete cascade,
  locality_id uuid not null references localities(id) on delete cascade,
  unique(vendor_id, locality_id)
);

create table services (
  id uuid primary key default gen_random_uuid(),
  vendor_id uuid not null references vendor_profiles(id) on delete cascade,
  name text not null,
  description text,
  price integer not null check (price >= 0),
  offer_price integer check (offer_price is null or offer_price >= 0),
  duration_minutes integer not null check (duration_minutes between 15 and 360),
  service_mode service_mode not null default 'at_salon',
  home_service_fee integer not null default 0 check (home_service_fee >= 0),
  display_order integer not null default 0,
  is_active boolean not null default true,
  created_at timestamptz not null default now()
);

create table bookings (
  id uuid primary key default gen_random_uuid(),
  booking_reference text not null unique,
  vendor_id uuid not null references vendor_profiles(id),
  service_id uuid not null references services(id),
  service_mode service_mode not null,
  booking_date date not null,
  booking_time time not null,
  status booking_status not null default 'requested',
  customer_name text not null,
  customer_phone text not null,
  customer_email text,
  customer_address text,
  landmark text,
  customer_notes text,
  total_amount integer not null check (total_amount >= 0),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  check ((service_mode = 'at_home') = (customer_address is not null))
);

create index bookings_vendor_status_idx on bookings(vendor_id, status, booking_date);
create index services_vendor_idx on services(vendor_id, is_active);
create index vendor_profiles_locality_idx on vendor_profiles(locality_id, is_active);

alter table countries enable row level security;
alter table cities enable row level security;
alter table localities enable row level security;
alter table vendor_profiles enable row level security;
alter table vendor_service_areas enable row level security;
alter table services enable row level security;
alter table bookings enable row level security;

create policy "public can read active cities" on cities for select using (is_active = true);
create policy "public can read localities" on localities for select using (true);
create policy "public can read active vendors" on vendor_profiles for select using (is_active = true);
create policy "public can read active services" on services for select using (is_active = true);
