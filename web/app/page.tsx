"use client";

import { FormEvent, useEffect, useState } from "react";

type Service = { id: string; name: string; price: number; offer_price?: number | null; duration_minutes: number; service_mode: "at_salon" | "at_home" | "both"; home_service_fee: number };
type Vendor = { id: string; slug: string; name: string; salon_type: string; locality: string; city: string; rating: number; review_count: number; home_service_available: boolean; cover_image?: string; services?: Service[] };

const apiUrl = process.env.NEXT_PUBLIC_API_URL;
const fallback: Vendor[] = [
  { id: "11111111-1111-1111-1111-111111111111", slug: "looks-salon-kakadeo", name: "Looks Salon", salon_type: "unisex", locality: "Kakadeo", city: "Kanpur", rating: 4.6, review_count: 128, home_service_available: true, cover_image: "https://images.unsplash.com/photo-1560066984-138dadb4c035?auto=format&fit=crop&w=900&q=80", services: [{id:"s-looks-1",name:"Hair Cut + Blow Dry",price:799,offer_price:599,duration_minutes:60,service_mode:"both",home_service_fee:99}] },
  { id: "22222222-2222-2222-2222-222222222222", slug: "urban-grooming-swarup-nagar", name: "Urban Grooming Studio", salon_type: "men", locality: "Swarup Nagar", city: "Kanpur", rating: 4.5, review_count: 84, home_service_available: true, cover_image: "https://images.unsplash.com/photo-1621605815971-fbc98d665033?auto=format&fit=crop&w=900&q=80", services: [{id:"s-urban-1",name:"Haircut + Beard Styling",price:499,offer_price:399,duration_minutes:45,service_mode:"both",home_service_fee:79}] },
  { id: "33333333-3333-3333-3333-333333333333", slug: "glow-women-parade", name: "Glow Women Salon", salon_type: "women", locality: "Parade", city: "Kanpur", rating: 4.7, review_count: 65, home_service_available: false, cover_image: "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?auto=format&fit=crop&w=900&q=80", services: [{id:"s-glow-1",name:"Haircut + Hair Wash",price:699,offer_price:549,duration_minutes:60,service_mode:"at_salon",home_service_fee:0}] },
];

export default function HomePage() {
  const [vendors, setVendors] = useState<Vendor[]>(fallback);
  const [selected, setSelected] = useState<Vendor | null>(null);
  const [mode, setMode] = useState<"at_salon" | "at_home">("at_salon");
  const [message, setMessage] = useState("");

  useEffect(() => { if (apiUrl) fetch(`${apiUrl}/vendors`).then((r) => r.ok ? r.json() : fallback).then(setVendors).catch(() => setVendors(fallback)); }, []);

  async function openVendor(vendor: Vendor) {
    setMessage("");
    if (!apiUrl || vendor.services?.length) {
      setSelected(vendor);
      setMode("at_salon");
      return;
    }
    const response = await fetch(`${apiUrl}/vendors/${vendor.slug}`);
    setSelected(response.ok ? await response.json() : vendor);
    setMode("at_salon");
  }

  async function requestBooking(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!selected) return;
    const form = new FormData(event.currentTarget);
    const service = selected.services?.[0];
    if (!service) return;
    const payload = { vendor_id: selected.id, service_id: service.id, service_mode: mode, booking_date: form.get("date"), booking_time: form.get("time"), customer_name: form.get("name"), customer_phone: form.get("phone"), customer_address: mode === "at_home" ? form.get("address") : null };
    if (!apiUrl) { setMessage("Demo booking created. Connect the API to submit real bookings."); return; }
    const response = await fetch(`${apiUrl}/bookings`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) });
    const data = await response.json();
    setMessage(response.ok ? `Booking ${data.booking_reference} requested. The salon will confirm it.` : data.detail || "Booking could not be created.");
  }

  return <main>
    <nav><div className="brand">Serv<span>Deal</span></div><div className="navlinks"><a href="#salons">Explore</a><a href="#how">How it works</a><button className="outline">For Partners</button></div></nav>
    <section className="hero"><div><p className="eyebrow">KANPUR SALON BOOKINGS</p><h1>Salon services and great deals, around you.</h1><p className="lead">Book trusted men, women and unisex salons—at the salon or in your home.</p><div className="search"><span>⌕</span><input placeholder="Search hair cut, facial, makeup..."/><button>Search</button></div><p className="note">Services are provided directly by listed salon partners.</p></div><aside><div className="map"><span>Kakadeo</span><span>Swarup Nagar</span><span>Parade</span><strong>Kanpur</strong></div><div className="stat"><b>4–5</b><small>trusted salon partners at launch</small></div></aside></section>
    <section id="salons" className="section"><div className="section-heading"><div><p className="eyebrow">EXPLORE</p><h2>Choose your salon</h2></div><div className="chips"><button className="active">All</button><button>Men</button><button>Women</button><button>Unisex</button><button onClick={() => setMode("at_home")}>At home</button></div></div><div className="cards">{vendors.map((vendor) => <article className="card" key={vendor.id}><img src={vendor.cover_image} alt=""/><div className="card-body"><div className="row"><h3>{vendor.name}</h3><b>★ {vendor.rating}</b></div><p>{vendor.salon_type} salon · {vendor.locality}, Kanpur</p><p>{vendor.home_service_available ? "At salon or at home" : "At salon service"}</p><div className="row"><strong>{vendor.services?.[0] ? `From ₹${vendor.services[0].offer_price || vendor.services[0].price}` : "View services"}</strong><button onClick={() => openVendor(vendor)}>Book now</button></div></div></article>)}</div></section>
    <section id="how" className="how"><p className="eyebrow">SIMPLE BOOKING</p><h2>Find. Book. Feel good.</h2><div><article><b>1</b><h3>Choose a salon</h3><p>Compare services, offers and localities.</p></article><article><b>2</b><h3>Select a slot</h3><p>Choose at-salon or home service where available.</p></article><article><b>3</b><h3>Get confirmation</h3><p>Your salon partner accepts your booking.</p></article></div></section>
    {selected && <div className="modal-backdrop"><section className="booking"><button className="close" onClick={() => setSelected(null)}>×</button><p className="eyebrow">BOOKING REQUEST</p><h2>{selected.name}</h2><p>{selected.services?.[0]?.name} · ₹{selected.services?.[0]?.offer_price || selected.services?.[0]?.price}</p><form onSubmit={requestBooking}><label>Service mode<select value={mode} onChange={(e) => setMode(e.target.value as "at_salon" | "at_home")}><option value="at_salon">At salon</option>{selected.home_service_available && <option value="at_home">At home</option>}</select></label><label>Your name<input name="name" required/></label><label>Phone number<input name="phone" required inputMode="tel"/></label><label>Date<input name="date" required type="date"/></label><label>Time<select name="time"><option>10:00</option><option>11:00</option><option>15:00</option><option>16:00</option></select></label>{mode === "at_home" && <label>Home address<textarea name="address" required/></label>}<button type="submit">Request booking</button></form>{message && <p className="success">{message}</p>}</section></div>}
  </main>;
}
