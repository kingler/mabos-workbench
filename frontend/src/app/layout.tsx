import React from 'react'
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'MABOS - Multi-Agent Business Operating System',
  description: 'Revolutionary synthesis of theoretical BDI architecture with practical workflow orchestration, delivering intelligent, adaptive business automation at enterprise scale.',
  keywords: ['BDI', 'Multi-Agent', 'Workflow', 'Automation', 'Business Process', 'AI'],
  authors: [{ name: 'MABOS Development Team', url: 'https://mabos.ai' }],
  creator: 'MABOS Development Team',
  publisher: 'MABOS',
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
  openGraph: {
    type: 'website',
    locale: 'en_US',
    url: 'https://mabos.ai',
    title: 'MABOS - Multi-Agent Business Operating System',
    description: 'Revolutionary synthesis of theoretical BDI architecture with practical workflow orchestration',
    siteName: 'MABOS',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'MABOS - Multi-Agent Business Operating System',
    description: 'Revolutionary synthesis of theoretical BDI architecture with practical workflow orchestration',
    creator: '@mabos_ai',
  },
  viewport: {
    width: 'device-width',
    initialScale: 1,
    maximumScale: 1,
  },
  themeColor: [
    { media: '(prefers-color-scheme: light)', color: '#ffffff' },
    { media: '(prefers-color-scheme: dark)', color: '#000000' },
  ],
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <link rel="icon" href="/favicon.ico" />
        <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png" />
        <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png" />
        <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png" />
        <link rel="manifest" href="/site.webmanifest" />
      </head>
      <body className={inter.className}>
        <div id="root">
          {children}
        </div>
      </body>
    </html>
  )
} 