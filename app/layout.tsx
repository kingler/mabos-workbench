import '@radix-ui/themes/styles.css' 
import { Theme } from '@radix-ui/themes'
// Add this line

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <Theme>
          {children}
        </Theme>
      </body>
    </html>
  )
}