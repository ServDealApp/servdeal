export type ServiceMode = "at_salon" | "at_home";

export function displayPrice(price: number, offerPrice?: number | null) {
  return offerPrice || price;
}

export function bookingMessage(reference: string) {
  return `Booking ${reference} requested. The salon will confirm it.`;
}

export function homeServiceTotal(price: number, homeServiceFee: number, mode: ServiceMode) {
  return price + (mode === "at_home" ? homeServiceFee : 0);
}
