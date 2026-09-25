import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "ServDeal | Salon services in Kanpur",
  description: "Discover and book salon services in Kanpur.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body>{children}</body></html>;
}
