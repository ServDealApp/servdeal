import { describe, expect, it } from "vitest";

import { bookingMessage, displayPrice, homeServiceTotal } from "../../lib/booking";

describe("booking helpers", () => {
  it("uses the offer price when it exists", () => {
    expect(displayPrice(799, 599)).toBe(599);
    expect(displayPrice(799, null)).toBe(799);
  });

  it("adds the fee only for home service", () => {
    expect(homeServiceTotal(599, 99, "at_salon")).toBe(599);
    expect(homeServiceTotal(599, 99, "at_home")).toBe(698);
  });

  it("returns the customer confirmation text", () => {
    expect(bookingMessage("SD-1234ABCD")).toContain("SD-1234ABCD");
  });
});
