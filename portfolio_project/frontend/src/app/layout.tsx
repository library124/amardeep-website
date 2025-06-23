import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Layout from "../components/Layout";
import { AuthProvider } from "../context/AuthContext";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Trader Portfolio",
  description: "A portfolio website for an intraday trader.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <AuthProvider>
          <Layout>{children}</Layout>
        </AuthProvider>
      </body>
    </html>
  );
}
