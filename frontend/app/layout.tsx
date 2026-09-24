import './globals.css'

export const metadata = { title: 'NZ Commercial Property Intelligence' }

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en-NZ"><body>{children}</body></html>
}
