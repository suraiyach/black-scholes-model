export const metadata = { title: "NSE Options Dashboard" };
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body style={{ fontFamily: 'Inter, system-ui, sans-serif', background: '#0b1220', color: '#e5e7eb' }}>
        <div style={{ maxWidth: 1200, margin: '0 auto', padding: 16 }}>
          <h1 style={{ fontSize: 28, fontWeight: 700, margin: '16px 0' }}>NSE Options Dashboard (Black–Scholes)</h1>
          {children}
        </div>
      </body>
    </html>
  );
}
