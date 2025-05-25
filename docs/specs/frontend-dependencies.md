# MABOS Frontend Dependencies Specification

## Core Framework & Build Tools

Based on the reference codebases (AgentDock_MABOS and Suna), we'll use **Next.js 14+** with **TypeScript** for optimal performance and developer experience.

### Core Dependencies (package.json)

```json
{
  "name": "mabos-frontend",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "type-check": "tsc --noEmit",
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage",
    "e2e": "playwright test",
    "storybook": "storybook dev -p 6006",
    "build-storybook": "storybook build"
  },
  "dependencies": {
    // Core Framework (Next.js 14+ like AgentDock_MABOS and Suna)
    "next": "^14.2.0",
    "react": "^18.3.0",
    "react-dom": "^18.3.0",
    
    // TypeScript
    "typescript": "^5.4.0",
    "@types/react": "^18.3.0",
    "@types/react-dom": "^18.3.0",
    "@types/node": "^20.12.0",
    
    // Styling (Tailwind CSS like AgentDock_MABOS and Suna)
    "tailwindcss": "^3.4.0",
    "postcss": "^8.4.0",
    "autoprefixer": "^10.4.0",
    "@tailwindcss/forms": "^0.5.0",
    "@tailwindcss/typography": "^0.5.0",
    
    // UI Components (Radix UI like AgentDock_MABOS)
    "@radix-ui/react-alert-dialog": "^1.0.5",
    "@radix-ui/react-avatar": "^1.0.4",
    "@radix-ui/react-checkbox": "^1.0.4",
    "@radix-ui/react-collapsible": "^1.0.3",
    "@radix-ui/react-dialog": "^1.0.5",
    "@radix-ui/react-dropdown-menu": "^2.0.6",
    "@radix-ui/react-form": "^0.0.3",
    "@radix-ui/react-hover-card": "^1.0.7",
    "@radix-ui/react-label": "^2.0.2",
    "@radix-ui/react-menubar": "^1.0.4",
    "@radix-ui/react-navigation-menu": "^1.1.4",
    "@radix-ui/react-popover": "^1.0.7",
    "@radix-ui/react-progress": "^1.0.3",
    "@radix-ui/react-radio-group": "^1.1.3",
    "@radix-ui/react-scroll-area": "^1.0.5",
    "@radix-ui/react-select": "^2.0.0",
    "@radix-ui/react-separator": "^1.0.3",
    "@radix-ui/react-slider": "^1.1.2",
    "@radix-ui/react-switch": "^1.0.3",
    "@radix-ui/react-tabs": "^1.0.4",
    "@radix-ui/react-toast": "^1.1.5",
    "@radix-ui/react-toggle": "^1.0.3",
    "@radix-ui/react-toggle-group": "^1.0.4",
    "@radix-ui/react-tooltip": "^1.0.7",
    
    // State Management (Zustand like reference codebases)
    "zustand": "^4.5.0",
    "immer": "^10.0.0",
    
    // Workflow Designer (React Flow for drag-and-drop like Kestra-KB patterns)
    "@xyflow/react": "^12.0.0",
    "reactflow": "^11.11.0",
    "@xyflow/system": "^0.0.32",
    
    // Data Fetching & API
    "@tanstack/react-query": "^5.28.0",
    "@tanstack/react-query-devtools": "^5.28.0",
    "axios": "^1.6.0",
    "ky": "^1.2.0",
    
    // Real-time Communication (WebSockets)
    "socket.io-client": "^4.7.0",
    "ws": "^8.16.0",
    
    // Form Handling
    "react-hook-form": "^7.51.0",
    "@hookform/resolvers": "^3.3.0",
    
    // Validation (Zod like AgentDock_MABOS)
    "zod": "^3.22.0",
    
    // Date Handling
    "date-fns": "^3.6.0",
    "@date-io/date-fns": "^3.0.0",
    
    // Icons
    "lucide-react": "^0.367.0",
    "@heroicons/react": "^2.1.0",
    
    // Utilities
    "clsx": "^2.1.0",
    "class-variance-authority": "^0.7.0",
    "tailwind-merge": "^2.2.0",
    "cmdk": "^1.0.0",
    
    // Charts and Visualization
    "recharts": "^2.12.0",
    "d3": "^7.9.0",
    "@types/d3": "^7.4.0",
    
    // File Upload
    "react-dropzone": "^14.2.0",
    
    // Rich Text Editor
    "@tiptap/react": "^2.2.0",
    "@tiptap/starter-kit": "^2.2.0",
    "@tiptap/extension-placeholder": "^2.2.0",
    
    // Code Editor (Monaco like Kestra-KB)
    "@monaco-editor/react": "^4.6.0",
    "monaco-editor": "^0.47.0",
    
    // Internationalization
    "next-intl": "^3.11.0",
    "react-i18next": "^14.1.0",
    "i18next": "^23.10.0",
    
    // Animation
    "framer-motion": "^11.0.0",
    "react-transition-group": "^4.4.0",
    
    // Error Handling
    "@sentry/nextjs": "^7.108.0",
    "react-error-boundary": "^4.0.0",
    
    // PDF Generation
    "jspdf": "^2.5.0",
    "html2canvas": "^1.4.0",
    
    // CSV Export
    "papaparse": "^5.4.0",
    "@types/papaparse": "^5.3.0"
  },
  "devDependencies": {
    // Linting & Code Quality
    "eslint": "^8.57.0",
    "eslint-config-next": "^14.2.0",
    "@typescript-eslint/eslint-plugin": "^7.5.0",
    "@typescript-eslint/parser": "^7.5.0",
    "eslint-plugin-react": "^7.34.0",
    "eslint-plugin-react-hooks": "^4.6.0",
    "eslint-plugin-jsx-a11y": "^6.8.0",
    "eslint-plugin-import": "^2.29.0",
    
    // Prettier
    "prettier": "^3.2.0",
    "prettier-plugin-tailwindcss": "^0.5.0",
    
    // Testing
    "jest": "^29.7.0",
    "jest-environment-jsdom": "^29.7.0",
    "@testing-library/react": "^14.2.0",
    "@testing-library/jest-dom": "^6.4.0",
    "@testing-library/user-event": "^14.5.0",
    
    // E2E Testing
    "@playwright/test": "^1.42.0",
    "playwright": "^1.42.0",
    
    // Visual Testing
    "@storybook/nextjs": "^8.0.0",
    "@storybook/react": "^8.0.0",
    "@storybook/addon-essentials": "^8.0.0",
    "@storybook/addon-a11y": "^8.0.0",
    "storybook": "^8.0.0",
    
    // Bundle Analysis
    "@next/bundle-analyzer": "^14.2.0",
    
    // Type Checking
    "tsc-files": "^1.1.0",
    
    // Mocking
    "msw": "^2.2.0",
    
    // Development
    "cross-env": "^7.0.0",
    "dotenv": "^16.4.0"
  }
}
```

## Configuration Files

### TypeScript Configuration (tsconfig.json)
```json
{
  "compilerOptions": {
    "target": "es5",
    "lib": ["dom", "dom.iterable", "es6"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "forceConsistentCasingInFileNames": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [
      {
        "name": "next"
      }
    ],
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"],
      "@/components/*": ["./src/components/*"],
      "@/lib/*": ["./src/lib/*"],
      "@/hooks/*": ["./src/hooks/*"],
      "@/types/*": ["./src/types/*"],
      "@/styles/*": ["./src/styles/*"]
    }
  },
  "include": [
    "next-env.d.ts",
    "**/*.ts",
    "**/*.tsx",
    ".next/types/**/*.ts"
  ],
  "exclude": ["node_modules"]
}
```

### Tailwind Configuration (tailwind.config.ts)
```typescript
import type { Config } from 'tailwindcss'

const config: Config = {
  darkMode: ["class"],
  content: [
    './pages/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}',
    './app/**/*.{ts,tsx}',
    './src/**/*.{ts,tsx}',
  ],
  theme: {
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
    extend: {
      colors: {
        // MABOS Brand Colors
        primary: {
          50: '#e6f2ff',
          100: '#b3d9ff',
          200: '#80c0ff',
          300: '#4da6ff',
          400: '#1a8cff',
          500: '#0066cc', // MABOS Blue
          600: '#0052a3',
          700: '#003d7a',
          800: '#002952',
          900: '#001429',
        },
        secondary: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          200: '#bae6fd',
          300: '#7dd3fc',
          400: '#38bdf8',
          500: '#0ea5e9',
          600: '#0284c7',
          700: '#0369a1',
          800: '#075985',
          900: '#0c4a6e',
        },
        // Design System Colors
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      spacing: {
        '18': '4.5rem',
        '88': '22rem',
      },
      keyframes: {
        "accordion-down": {
          from: { height: "0" },
          to: { height: "var(--radix-accordion-content-height)" },
        },
        "accordion-up": {
          from: { height: "var(--radix-accordion-content-height)" },
          to: { height: "0" },
        },
      },
      animation: {
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
      },
    },
  },
  plugins: [
    require("tailwindcss-animate"),
    require("@tailwindcss/forms"),
    require("@tailwindcss/typography"),
  ],
}

export default config
```

### Next.js Configuration (next.config.ts)
```typescript
/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    appDir: true,
    serverComponentsExternalPackages: ["@xyflow/react"],
  },
  images: {
    domains: ['localhost', 'api.mabos.dev'],
  },
  webpack: (config: any) => {
    config.externals.push({
      'utf-8-validate': 'commonjs utf-8-validate',
      'bufferutil': 'commonjs bufferutil',
    })
    return config
  },
  eslint: {
    dirs: ['pages', 'app', 'components', 'lib', 'src'],
  },
  env: {
    CUSTOM_KEY: process.env.CUSTOM_KEY,
  },
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'X-Frame-Options',
            value: 'DENY',
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'Referrer-Policy',
            value: 'origin-when-cross-origin',
          },
        ],
      },
    ]
  },
}

module.exports = nextConfig
```

## Project Structure

```
src/
├── app/                    # Next.js App Router
│   ├── (auth)/            # Auth route group
│   ├── (dashboard)/       # Dashboard route group
│   ├── api/               # API routes
│   ├── globals.css        # Global styles
│   ├── layout.tsx         # Root layout
│   └── page.tsx           # Home page
├── components/            # React components
│   ├── ui/               # Base UI components (shadcn/ui)
│   ├── layout/           # Layout components
│   ├── workflow/         # Workflow designer components
│   ├── auth/             # Authentication components
│   └── dashboard/        # Dashboard components
├── hooks/                # Custom React hooks
├── lib/                  # Utility functions
│   ├── utils.ts          # Common utilities
│   ├── api.ts            # API client
│   ├── auth.ts           # Auth utilities
│   └── validators.ts     # Zod schemas
├── stores/               # Zustand stores
├── types/                # TypeScript type definitions
└── styles/               # Additional CSS files
```

## Key Technologies & Rationale

### Core Framework: Next.js 14+
- **Why**: Based on AgentDock_MABOS and Suna analysis showing excellent performance
- **Features**: App Router, Server Components, streaming, built-in optimization

### UI Framework: Radix UI + Tailwind CSS
- **Why**: AgentDock_MABOS uses Radix UI extensively for accessibility
- **Benefits**: Unstyled, accessible components with Tailwind for rapid styling

### State Management: Zustand
- **Why**: Lightweight, TypeScript-friendly, used across reference codebases
- **Benefits**: Simple API, great DevTools integration, minimal boilerplate

### Workflow Designer: React Flow / XyFlow
- **Why**: Industry standard for node-based editors, similar to Kestra-KB patterns
- **Features**: Drag-and-drop, customizable nodes, performance optimized

### Data Fetching: TanStack Query
- **Why**: Best-in-class data fetching with caching and synchronization
- **Features**: Background updates, optimistic updates, infinite queries

### Forms: React Hook Form + Zod
- **Why**: AgentDock_MABOS pattern, excellent performance and validation
- **Benefits**: Minimal re-renders, TypeScript integration, schema validation

This frontend architecture provides:
- **Enterprise-ready** performance and scalability
- **Accessibility** compliance (WCAG 2.1 AA)
- **Modern development** experience with TypeScript
- **Component reusability** across all interfaces
- **Real-time collaboration** capabilities
- **Comprehensive testing** framework 