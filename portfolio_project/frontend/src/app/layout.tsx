import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Layout from "../components/Layout";
import { AuthProvider } from "../context/AuthContext";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Amardeep Asode - Professional Stock & Intraday Trader",
  description: "Expert in intraday strategies for consistent results. Transforming trading performance through proven methodologies with 5+ years of market expertise.",
  keywords: "stock trading, intraday trading, trading signals, market analysis, trading mentorship, Amardeep Asode",
  authors: [{ name: "Amardeep Asode" }],
  creator: "Amardeep Asode",
  publisher: "Amardeep Asode",
  formatDetection: {
    email: false,
    address: false,
    telephone: false,
  },
  metadataBase: new URL('https://amardeepasode.com'),
  alternates: {
    canonical: '/',
  },
  openGraph: {
    title: "Amardeep Asode - Professional Stock & Intraday Trader",
    description: "Expert in intraday strategies for consistent results. Transforming trading performance through proven methodologies.",
    url: 'https://amardeepasode.com',
    siteName: 'Amardeep Asode Trading',
    images: [
      {
        url: '/owner_landing_page.jpg',
        width: 1200,
        height: 630,
        alt: 'Amardeep Asode - Professional Trader',
      },
    ],
    locale: 'en_US',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: "Amardeep Asode - Professional Stock & Intraday Trader",
    description: "Expert in intraday strategies for consistent results. Transforming trading performance through proven methodologies.",
    images: ['/owner_landing_page.jpg'],
    creator: '@amardeepasode',
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
  icons: {
    icon: [
      { url: '/favicon.svg', type: 'image/svg+xml' },
      { url: '/favicon.ico', sizes: '32x32' },
    ],
    apple: [
      { url: '/apple-touch-icon.png', sizes: '180x180' },
    ],
    other: [
      {
        rel: 'mask-icon',
        url: '/favicon.svg',
        color: '#00E676',
      },
    ],
  },
  manifest: '/manifest.json',
  themeColor: [
    { media: '(prefers-color-scheme: light)', color: '#ffffff' },
    { media: '(prefers-color-scheme: dark)', color: '#1a1a1a' },
  ],
  viewport: {
    width: 'device-width',
    initialScale: 1,
    maximumScale: 1,
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <head>
        <link rel="icon" href="/favicon.svg" type="image/svg+xml" />
        <link rel="icon" href="/favicon.ico" sizes="32x32" />
        <link rel="apple-touch-icon" href="/apple-touch-icon.png" />
        <link rel="mask-icon" href="/favicon.svg" color="#00E676" />
        <meta name="theme-color" content="#ffffff" media="(prefers-color-scheme: light)" />
        <meta name="theme-color" content="#1a1a1a" media="(prefers-color-scheme: dark)" />
      </head>
      <body className={inter.className}>
        <AuthProvider>
          <Layout>{children}</Layout>
        </AuthProvider>
      </body>
    </html>
  );
}