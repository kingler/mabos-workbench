import '@radix-ui/themes/styles.css' 
import { Theme } from '@radix-ui/themes'
import '../styles/globals.css'

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <Theme accentColor="indigo" grayColor="slate">
          {children}
        </Theme>
      </body>
    </html>
  )
}
