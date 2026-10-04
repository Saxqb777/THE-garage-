import type { Metadata, Viewport } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'The Garage',
  description: 'A photoreal 3D garage for a 2005 Toyota Land Cruiser 100.',
};

export const viewport: Viewport = {
  themeColor: '#0f1013',
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
