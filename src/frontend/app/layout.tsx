import type { Metadata } from "next";
import { Inter } from "next/font/google";

import "./globals.css";
import SideNav from "@/components/side-nav";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "HyperPlayground",
  description: "A Hands-on Hyperparameter Tuning Playground",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>
        {
          <div className="flex">
            <SideNav />
            <main className="flex-1">{children}</main>
          </div>
        }
      </body>
    </html>
  );
}
