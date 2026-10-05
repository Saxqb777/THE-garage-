import type { Metadata, Viewport } from 'next';
import { Barlow_Condensed, IBM_Plex_Mono } from 'next/font/google';
import './globals.css';

// condensed grotesk for labels and headings (workshop signage), mono for codes and readouts
const display = Barlow_Condensed({ subsets: ['latin'], weight: ['500', '600', '700'], variable: '--font-display', display: 'swap' });
const mono = IBM_Plex_Mono({ subsets: ['latin'], weight: ['400', '500', '600'], variable: '--font-mono', display: 'swap' });

export const metadata: Metadata = {
  title: 'The Garage',
  description: 'A photoreal 3D garage for a 2005 Toyota Land Cruiser 100.',
};

export const viewport: Viewport = {
  themeColor: '#0b0c0e',
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en" className={`${display.variable} ${mono.variable}`}>
      <body>{children}</body>
    </html>
  );
}
