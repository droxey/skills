---
name: nextjs-nebula-miniapp
description: Next.js + Nebula Miniapps best practices. Read when building, reviewing, or optimizing Next.js apps in the Nebula sandbox. Covers Server Components architecture, streaming/caching, data fetching, design compliance (shadcn/ui, spacing, touch targets), proxy integration, and production checklist.
---

# Next.js + Nebula Miniapps: Best Practices

**Next.js 16.2.6 (App Router) | May 2026**

## 1. Architecture: Server Components First

**Golden Rule:** Default to Server Components. Push `"use client"` as far down the tree as possible.

Server Components:
- Run on the server, zero JS shipped to the client
- Fetch data close to the source (databases, APIs, ORMs)
- Keep secrets (API keys, tokens) out of the client bundle
- Improve First Contentful Paint (FCP)
- Rendered result is cached in the static shell

Add `"use client"` ONLY when you need:
- `useState`, `useEffect`, event handlers (`onClick`, `onChange`)
- Browser APIs (`localStorage`, `window`, `geolocation`)
- Custom hooks requiring React state

### Client Boundary Rule

When a file is marked `"use client"`, ALL imports and components it directly renders become part of the client bundle. Minimize by passing Server Components as children:

```tsx
// layout.tsx — Server Component (default)
import Search from './search'  // Client Component
import Logo from './logo'      // Server Component

export default function Layout({ children }) {
  return (
    <nav>
      <Logo />        {/* stays on server */}
      <Search />      {/* only this ships to client */}
    </nav>
  )
}
```

### Children Slot Pattern

```tsx
// modal.tsx — Client Component
'use client'
export default function Modal({ children }) {
  return <div>{children}</div>
}

// page.tsx — Server Component
export default function Page() {
  return (
    <Modal>
      <Cart />  {/* Server Component — zero JS */}
    </Modal>
  )
}
```

### Props: Serializable Only

Data passed from Server to Client Components must be serializable. Use props for plain values. For streaming data, use React's `use` API.

---

## 2. Performance: Streaming, Caching, and PPR

### Streaming Architecture

Two streams work together:
1. **HTML Stream:** Progressive chunks of rendered HTML. The static shell (layouts, nav, Suspense fallbacks) is sent immediately. Async components stream in as they resolve.
2. **Component Payload (RSC):** A compact binary representation of the Server Component tree. On initial load, embedded in the HTML stream. On client-side navigation, only the payload is fetched — zero HTML transferred.

### The Static Shell

Everything above the first `<Suspense>` boundary forms the static shell — sent to the browser instantly. With Cache Components enabled, this is prerendered at build time and served from edge.

**The static shell is what the user sees first. Make it count.**

### Defer Dynamic Access

Push dynamic access down. If you `await cookies()`, `headers()`, `params`, or `searchParams` at the top of a layout or page, everything below becomes dynamic:

```tsx
// BAD: Blocks the entire page
export default async function Dashboard() {
  const cookieStore = await cookies()  // dynamic, blocks everything
  return <div>...</div>
}

// GOOD: Defer to the component that needs it
export default function Layout({ children }) {
  const cookieStore = cookies()  // Start but DON'T await
  return (
    <Nav>
      <Suspense fallback={<p>Loading...</p>}>
        <UserMenu cookiePromise={cookieStore} />
      </Suspense>
    </Nav>
    {children}
  )
}
```

### Granular `<Suspense>` vs `loading.js`

| | `loading.js` | `<Suspense>` |
|---|---|---|
| Scope | Entire page | Any component |
| Setup | Drop in a file | Wrap components explicitly |
| Navigation | Prefetched as instant fallback | Not prefetched by default |
| Best for | Pages where nothing renders without data | **Most pages — prefer this** |

**Prefer explicit `<Suspense>` boundaries close to the dynamic work.**

### Parallel Streaming

Each `<Suspense>` boundary streams independently:

```tsx
export default function Dashboard() {
  return (
    <div>
      <h1>Dashboard</h1>
      <div className="grid grid-cols-2 gap-4">
        <Suspense fallback={<Skeleton />}>
          <Revenue />       {/* resolves in 200ms */}
        </Suspense>
        <Suspense fallback={<Skeleton />}>
          <RecentOrders />  {/* resolves in 1s */}
        </Suspense>
      </div>
      <Suspense fallback={<Skeleton />}>
        <Recommendations /> {/* resolves in 3s */}
      </Suspense>
    </div>
  )
}
```

### Cache Components (Next.js 16)

Enable in `next.config.ts`:
```ts
const nextConfig: NextConfig = {
  cacheComponents: true,
}
```

**Data-level** — Cache a function:
```ts
export async function getUsers() {
  'use cache'
  cacheLife('hours')
  return db.query('SELECT * FROM users')
}
```

**UI-level** — Cache an entire component:
```ts
export default async function Page() {
  'use cache'
  cacheLife('hours')
  const users = await db.query('SELECT * FROM users')
  return <ul>{users.map(u => <li key={u.id}>{u.name}</li>)}</ul>
}
```

For fresh data on every request: DON'T use `"use cache"`. Wrap in `<Suspense>` instead.

**Runtime APIs** (cookies, headers, searchParams, params) should be wrapped in `<Suspense>`. Extract values and pass as arguments to cached functions:

```ts
async function ProfileContent() {
  const session = (await cookies()).get('session')?.value
  return <CachedContent sessionId={session} />
}

async function CachedContent({ sessionId }) {
  'use cache'
  const data = await fetchUserData(sessionId)
  return <div>{data}</div>
}
```

---

## 3. Data Fetching: The Right Way

### Server Components: Direct Access

```tsx
export default async function Page() {
  const data = await fetch('https://api.example.com/posts')
  const posts = await data.json()
  return <ul>{posts.map(p => <li key={p.id}>{p.title}</li>)}</ul>
}
```

With an ORM:
```tsx
import { db, posts } from '@/lib/db'
export default async function Page() {
  const allPosts = await db.select().from(posts)
  return <ul>{allPosts.map(p => <li key={p.id}>{p.title}</li>)}</ul>
}
```

Key facts:
- Identical `fetch` requests in a React tree are automatically memoized
- `fetch` is NOT cached by default in Next.js 16 — use `"use cache"` to cache, or `<Suspense>` to stream
- Credentials and queries are NEVER exposed to the client

### Client Components: TanStack Query

Nebula miniapps ship with TanStack Query pre-installed:

```tsx
'use client'
import { useQuery } from '@tanstack/react-query'

export function PostList() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['posts'],
    queryFn: () => fetch('/api/posts').then(r => r.json()),
  })
}
```

Create a providers wrapper:
```tsx
'use client'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { useState } from 'react'

export function Providers({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(() => new QueryClient())
  return <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
}
```

### Forms: Server Actions

```tsx
export default function Page() {
  async function createInvoice(formData: FormData) {
    'use server'
    const session = await auth()
    if (!session?.user) throw new Error('Unauthorized')
    const rawFormData = {
      customerId: formData.get('customerId'),
      amount: formData.get('amount'),
      status: formData.get('status'),
    }
    // mutate data, revalidate cache
  }
  return <form action={createInvoice}>...</form>
}
```

With Zod validation:
```ts
'use server'
import { z } from 'zod'

const schema = z.object({ email: z.string().email() })

export async function createUser(formData: FormData) {
  const validated = schema.safeParse({ email: formData.get('email') })
  if (!validated.success) {
    return { errors: validated.error.flatten().fieldErrors }
  }
}
```

### Optimistic Updates

```tsx
const [optimisticMessages, addOptimisticMessage] = useOptimistic(
  messages,
  (state, newMessage) => [...state, { message: newMessage }]
)
```

---

## 4. Design: Nebula Miniapp Visual Rules

### The 400px Constraint

Miniapps display in a ~400px sidebar by default. Design for 400px first; layouts must expand to full screen. **Dense and functional beats spacious and decorative.**

### 12-Point Compliance Checklist

Before EVERY `rebuild_miniapp`:
```
[ ] Every interactive element is at least h-11 (44px touch target)
[ ] EVERY button is shadcn <Button>, input is shadcn <Input>, label is shadcn <Label>
[ ] All spacing values are from {1, 2, 4, 6, 8, 12, 16, 20, 24} — never 3, 5, 7, 9, 11
[ ] No hardcoded colors — only semantic tokens (bg-background, text-foreground, etc.)
[ ] No multi-color gradients
[ ] No emoji as iconography — lucide-react or plain text
[ ] No vh units — dvh only
[ ] Page title names the SPECIFIC app, not "Miniapp" or "My App"
[ ] No centered placeholder hero with do-nothing CTA
[ ] Loading state uses shadcn <Skeleton> shaped like eventual content
[ ] Error state shows message + retry button in bg-destructive/5
[ ] Empty state is signaled deliberately (label + hint), no emoji
```

### Hard Rules

**1. Touch Targets: `h-11 min-w-[44px]`**
Every clickable element must have `h-11`. `h-9` and `h-10` are mobile accessibility violations.

**2. shadcn/ui ALWAYS**
```tsx
// BAD
<button className="px-3 py-2 bg-primary">Save</button>
<input type="text" className="border rounded px-2" />
<div className="animate-pulse h-4 w-3/4 bg-muted rounded" />

// GOOD
<Button>Save</Button>
<Input type="text" />
<Skeleton className="h-4 w-3/4" />
```

**3. Semantic Tokens Only**
No `bg-gray-*`, `bg-blue-*`, `text-red-*`, or literal hex colors. Use:
- `bg-background`, `text-foreground`, `text-muted-foreground`
- `bg-primary`, `bg-destructive`, `bg-muted`, `border`

Exception: three status pairs — `text-green-600 dark:text-green-400` (success), `text-yellow-600 dark:text-yellow-400` (warning), `text-destructive` (error).

**4. Spacing Scale**
Allowed: `1, 2, 4, 6, 8, 12, 16, 20, 24`
Forbidden: `3, 5, 7, 9, 10, 11, 13, 14, 15`

### Copyable Patterns

**Page Header:**
```tsx
<header className="border-b">
  <div className="mx-auto max-w-3xl px-4 py-4">
    <h1 className="text-xl font-semibold tracking-tight">{appTitle}</h1>
    <p className="mt-1 text-sm text-muted-foreground">{description}</p>
  </div>
</header>
```

**Loading State:**
```tsx
<div className="space-y-3">
  <Skeleton className="h-5 w-3/4" />
  <Skeleton className="h-5 w-1/2" />
  <Skeleton className="h-5 w-2/3" />
</div>
```

**Error State:**
```tsx
<div className="rounded-md border border-destructive/30 bg-destructive/5 p-4">
  <p className="text-sm font-medium text-destructive">{error.message}</p>
  <Button variant="ghost" size="sm" className="mt-2" onClick={refetch}>
    Try again
  </Button>
</div>
```

**Empty State:**
```tsx
<div className="flex flex-col items-center justify-center py-12 px-4 text-center">
  <p className="text-sm font-medium">No items yet</p>
  <p className="mt-1 text-sm text-muted-foreground">{actionableHint}</p>
  <Button className="mt-4" onClick={...}>{primaryAction}</Button>
</div>
```

### Typography Scale

- Page titles: `text-2xl sm:text-3xl font-semibold tracking-tight`
- Section headings: `text-lg font-medium`
- Body text: `text-sm leading-relaxed text-muted-foreground`
- Emphasised body: `text-sm font-medium text-foreground`

### Tailwind v4 Notes

- NO `tailwind.config.ts` — use CSS `@theme` blocks in `globals.css`
- Custom colors and fonts are CSS custom properties inside `@theme { }`
- The scaffold's globals.css has design tokens pre-configured

---

## 5. Platform Integration: Proxies, Auth, and Callbacks

### Environment Variables

- `NEBULA_PROXY_URL` — base URL of the Nebula backend (set by runtime)
- `SANDBOX_AUTH_TOKEN` — short-lived JWT (SERVER-SIDE ONLY, never `NEXT_PUBLIC_`)

### Proxy Pattern (All Endpoints)

```ts
// src/app/api/<name>/route.ts
const PROXY_URL = process.env.NEBULA_PROXY_URL
const AUTH_TOKEN = process.env.SANDBOX_AUTH_TOKEN

const resp = await fetch(`${PROXY_URL}/internal/proxy/<endpoint>`, {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${AUTH_TOKEN}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ /* endpoint-specific payload */ }),
})
```

Client calls the API route:
```tsx
const { data } = useQuery({
  queryKey: ['feature'],
  queryFn: () => fetch('/api/<name>').then(r => r.json()),
})
```

### Endpoints

- `/internal/proxy/oauth` — call user-connected OAuth apps (GitHub, Gmail, Linear, etc.)
- `/internal/proxy/messages` — post a message back to the agent from the miniapp
- `/internal/proxy/llm` — call an LLM via the user's selected model

### Security

- `SANDBOX_AUTH_TOKEN` is server-side only
- Never expose proxy URLs or tokens to the browser bundle
- Sanitize third-party error messages before returning to client

---

## 6. Production Checklist

### Automatic Optimizations (No Config Required)

- Server Components by default → zero client JS for static parts
- Automatic code-splitting by route segment
- `<Link>` prefetching when links enter the viewport
- Prerendering at build time
- Caching of rendered results, data, and static assets

### Image Optimization

Use `next/image` for ALL images:
```tsx
import Image from 'next/image'

// Local images — auto width/height/blurDataURL
import heroImage from './hero.png'
<Image src={heroImage} alt="Hero" />

// Remote images — define remotePatterns in next.config.ts
<Image src="https://cdn.example.com/photo.jpg" alt="" width={500} height={500} />
```

### Font Optimization

Use `next/font` for zero-layout-shift, self-hosted fonts:
```tsx
import { Geist } from 'next/font/google'
const geist = Geist({ subsets: ['latin'] })

export default function RootLayout({ children }) {
  return <html lang="en" className={geist.className}><body>{children}</body></html>
}
```

Prefer variable fonts for the best performance.

### Core Web Vitals Targets

- LCP (Largest Contentful Paint): < 2.5s
- INP (Interaction to Next Paint): < 200ms
- CLS (Cumulative Layout Shift): < 0.1

---

## 7. Infrastructure Considerations

### Streaming Gotchas

- Once streaming begins, HTTP response headers (including status code) have already been sent. **You cannot change the status code after streaming starts.**
- When a `<Suspense>` fallback renders or a component suspends, the server commits to `200 OK`. If `notFound()` fires mid-stream, Next.js injects `<meta name="robots" content="noindex">` instead of changing to 404.
- Safari requires ~1024 bytes of HTML before rendering. Ensure the static shell exceeds this threshold.
- Nginx buffers streaming responses by default. Configure `proxy_buffering off` for true streaming.
- CDNs must support chunked transfer encoding for streaming to work through the edge.

### Early Resource Discovery

The static shell includes `<link>` and `<script>` tags in the very first HTML chunk. The browser discovers and starts fetching CSS, JavaScript, and fonts immediately, while the server is still generating content.
