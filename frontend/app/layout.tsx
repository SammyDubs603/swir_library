export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body style={{ fontFamily: 'Arial, sans-serif', margin: 24 }}>
        <h1>SWIR Spectra Library</h1>
        <nav style={{ marginBottom: 16 }}>
          <a href="/" style={{ marginRight: 12 }}>Search</a>
          <a href="/attribution">Attribution</a>
        </nav>
        {children}
      </body>
    </html>
  )
}
