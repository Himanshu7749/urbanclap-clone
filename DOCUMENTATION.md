# UrbanServe — Project Documentation

> A full-stack home-services marketplace built with **Next.js 14**, **React 18**, **Tailwind CSS**, and **Prisma ORM** (SQLite).

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Tech Stack](#2-tech-stack)
3. [Project Structure](#3-project-structure)
4. [Database Schema](#4-database-schema)
5. [Pages](#5-pages)
6. [API Routes](#6-api-routes)
7. [Library / Utilities](#7-library--utilities)
8. [Styles](#8-styles)
9. [Configuration Files](#9-configuration-files)
10. [Database Seed](#10-database-seed)
11. [NPM Scripts](#11-npm-scripts)
12. [User Flow](#12-user-flow)
13. [How to Run](#13-how-to-run)

---

## 1. Project Overview

UrbanServe is a clone of the UrbanClap / Urban Company app — a platform where users can:

- Browse home service categories (Barber, Plumbing, Cleaning)
- View verified service providers for each category with star ratings
- Book an appointment with a provider by entering their name, email, date and time
- View all their bookings with status tracking (pending / confirmed / cancelled)

The app uses **server-side rendering (SSR)** for all data-heavy pages so that search engines and users always get fresh data. Bookings are created via a **REST API route** and stored in an **SQLite database** managed by Prisma ORM.

---

## 2. Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Framework | Next.js 14 | Routing, SSR, API routes |
| UI Library | React 18 | Component-based UI |
| Styling | Tailwind CSS 3 | Utility-first CSS |
| ORM | Prisma 5 | Database access and migrations |
| Database | SQLite | Local file-based relational database |
| CSS Processing | PostCSS + Autoprefixer | Cross-browser CSS compatibility |

---

## 3. Project Structure

```
urbanclap-clone/
│
├── pages/                          # Next.js pages (each file = a route)
│   ├── _app.js                     # Root app wrapper — imports global CSS
│   ├── index.js                    # Home page — lists service categories
│   ├── bookings.js                 # Bookings list page — shows all bookings
│   ├── api/
│   │   └── bookings.js             # POST /api/bookings — creates a booking
│   ├── services/
│   │   └── [slug].js               # /services/barber, /services/plumbing etc.
│   └── providers/
│       └── [id].js                 # /providers/1, /providers/2 etc.
│
├── lib/
│   └── prisma.js                   # Prisma client singleton (shared DB connection)
│
├── prisma/
│   ├── schema.prisma               # Database models definition
│   ├── seed.js                     # Script to populate DB with sample data
│   ├── dev.db                      # SQLite database file (auto-created)
│   └── migrations/
│       └── 20260607172656_init/
│           └── migration.sql       # Initial SQL migration
│
├── styles/
│   └── globals.css                 # Global CSS — Tailwind directives + custom classes
│
├── next.config.js                  # Next.js configuration
├── tailwind.config.js              # Tailwind CSS configuration
├── postcss.config.js               # PostCSS plugin configuration
├── package.json                    # Dependencies and scripts
└── README.md                       # Basic project readme
```

---

## 4. Database Schema

File: `prisma/schema.prisma`

The database has **4 models** (tables):

---

### Model: `User`

Stores customer information. A user is created or updated automatically when they make a booking — they do not need to register separately.

| Field | Type | Description |
|---|---|---|
| `id` | Int (PK) | Auto-incremented primary key |
| `name` | String? | Customer's full name (optional) |
| `email` | String (unique) | Customer's email — used as unique identifier |
| `bookings` | Booking[] | All bookings made by this user |

---

### Model: `Service`

Represents a service category (e.g. Barber, Plumbing, Cleaning).

| Field | Type | Description |
|---|---|---|
| `id` | Int (PK) | Auto-incremented primary key |
| `name` | String | Display name (e.g. "Barber") |
| `slug` | String (unique) | URL-safe identifier (e.g. "barber") used in routes |
| `providers` | Provider[] | All providers who offer this service |

---

### Model: `Provider`

Represents a professional/vendor who offers a specific service.

| Field | Type | Description |
|---|---|---|
| `id` | Int (PK) | Auto-incremented primary key |
| `name` | String | Provider's full name |
| `rating` | Float? | Star rating out of 5 (optional) |
| `serviceId` | Int (FK) | Links to the `Service` this provider belongs to |
| `service` | Service | The related service object |
| `bookings` | Booking[] | All bookings made with this provider |

---

### Model: `Booking`

Records a scheduled appointment between a user and a provider.

| Field | Type | Description |
|---|---|---|
| `id` | Int (PK) | Auto-incremented primary key |
| `userId` | Int? (FK) | Links to the `User` who made the booking |
| `providerId` | Int (FK) | Links to the `Provider` being booked |
| `scheduledAt` | DateTime | Date and time of the appointment |
| `status` | String | Booking status — default is `"pending"` |
| `user` | User? | The related user object |
| `provider` | Provider | The related provider object |

---

### Relationships Diagram

```
Service ──< Provider ──< Booking >── User
```

- One **Service** has many **Providers**
- One **Provider** has many **Bookings**
- One **User** has many **Bookings**

---

## 5. Pages

### `pages/_app.js` — App Wrapper

**Route:** N/A (wraps all pages)

**What it does:**
- This is the root component Next.js uses to initialize every page.
- Imports `styles/globals.css` so Tailwind and custom component styles are available globally.
- Renders the active page component via `<Component {...pageProps} />`.

**Props:**
| Prop | Description |
|---|---|
| `Component` | The current page component being rendered |
| `pageProps` | Props fetched by `getServerSideProps` or `getStaticProps` on that page |

---

### `pages/index.js` — Home Page

**Route:** `/`

**What it does:**
- Displays the landing page with a sticky navbar, hero section, and service cards.
- The `services` array is hardcoded with 3 items: Barber, Plumbing, and Cleaning — each with a name, icon, description, and gradient color.
- Each service card links to `/services/[slug]` for that category.
- The navbar has a "My Bookings" button linking to `/bookings`.

**Key elements:**
| Element | Description |
|---|---|
| Navbar | Sticky top bar with logo and bookings link |
| Hero section | Large heading, subtext, and "Explore Services" CTA button |
| Services grid | 3 cards in a responsive grid (1 col mobile, 3 col desktop) |
| Footer | Simple copyright footer |

**Data source:** Static — no database queries, no `getServerSideProps`.

---

### `pages/bookings.js` — My Bookings Page

**Route:** `/bookings`

**What it does:**
- Fetches all bookings from the database and renders them in a list.
- Each booking card shows: provider name, service category, customer name & email, booking status (with color-coded badge), and scheduled date/time.
- If there are no bookings, shows an empty state with a CTA to explore services.

**`getServerSideProps` function:**
- Runs on the server before the page is sent to the browser.
- Calls `prisma.booking.findMany()` with includes for `provider → service` and `user`.
- Orders results by `scheduledAt` descending (newest first).
- Converts `scheduledAt` DateTime to an ISO string so it can be safely passed as a React prop.

**Status badge colors:**
| Status | Color |
|---|---|
| `PENDING` | Yellow |
| `CONFIRMED` | Green |
| `CANCELLED` | Red |

---

### `pages/services/[slug].js` — Service Detail Page

**Route:** `/services/barber`, `/services/plumbing`, `/services/cleaning`

**What it does:**
- Dynamic page — the `[slug]` in the filename means the URL segment becomes `params.slug`.
- Fetches the service matching the slug, along with all its providers.
- Renders each provider as a card showing name, star rating, and a "Book Now" button.
- Clicking "Book Now" navigates to `/providers/[id]` for that provider.
- Returns a 404 if the slug does not match any service in the database.

**`StarRating` component (local):**
- Accepts a `rating` number (e.g. `4.8`).
- Renders 5 SVG star icons — filled yellow for stars up to the rounded rating, grey for the rest.
- Displays the numeric rating value next to the stars.
- Shows "N/A" if rating is null.

**`getServerSideProps` function:**
- Calls `prisma.service.findUnique({ where: { slug } })` with providers included.
- Returns `{ notFound: true }` if no service found — Next.js shows the 404 page.

---

### `pages/providers/[id].js` — Provider Profile & Booking Page

**Route:** `/providers/1`, `/providers/2`, etc.

**What it does:**
- Dynamic page — fetches a single provider by numeric `id` from the URL.
- Displays a provider profile card (avatar with first letter, name, service type, star rating).
- Below the profile, renders a booking form with fields: Full Name, Email, Date, and Time.
- On form submit, calls `POST /api/bookings` with the booking data.
- Shows a green success message or a red error message depending on the API response.
- Resets the form on successful booking.

**`StarRating` component (local — same as in services page):**
- Renders 5 star SVG icons with fill based on the rounded rating value.

**React state variables:**
| State | Type | Description |
|---|---|---|
| `form` | Object | Holds `name`, `email`, `date`, `time` field values |
| `status` | String/null | Success message text after booking |
| `error` | String/null | Error message text on failure |
| `loading` | Boolean | True while the API request is in flight |

**`handleChange` function:**
- Updates the `form` state when any input field changes.
- Uses the input's `name` attribute to know which field to update.

**`handleSubmit` function:**
- Prevents the default form submission.
- Sets `loading = true` and clears previous status/error.
- Sends a `POST` request to `/api/bookings` with `providerId`, `name`, `email`, and `scheduledAt` (combined date + time string).
- On success: sets the success message and resets the form.
- On failure: sets the error message from the API response.

**`getServerSideProps` function:**
- Calls `prisma.provider.findUnique({ where: { id: Number(params.id) } })` with service included.
- Returns `{ notFound: true }` if provider doesn't exist.

---

## 6. API Routes

### `pages/api/bookings.js` — Create Booking

**Endpoint:** `POST /api/bookings`

**What it does:**
Creates a new booking by finding or creating the user (by email) and then creating the booking record linked to both the user and provider.

**Request Body (JSON):**
| Field | Type | Required | Description |
|---|---|---|---|
| `providerId` | Number | Yes | ID of the provider to book |
| `name` | String | Yes | Customer's full name |
| `email` | String | Yes | Customer's email address |
| `scheduledAt` | String | Yes | ISO date-time string (e.g. `"2026-06-15T10:00:00"`) |

**Response:**
| Scenario | HTTP Status | Response Body |
|---|---|---|
| Success | `201 Created` | `{ booking: { ...bookingData } }` |
| Wrong HTTP method | `405 Method Not Allowed` | Plain text error |
| Missing fields | `400 Bad Request` | `{ error: "Missing booking details" }` |
| Provider not found | `404 Not Found` | `{ error: "Provider not found" }` |

**Step-by-step logic:**

1. **Method check** — Rejects any non-POST request with a 405 response.
2. **Validation** — Checks that `providerId`, `name`, `email`, and `scheduledAt` are all present in the request body. Returns 400 if any are missing.
3. **Provider lookup** — Queries the database for a provider with the given `providerId`. Returns 404 if not found.
4. **User upsert** — Uses `prisma.user.upsert()`:
   - If a user with the given `email` exists → updates their `name`.
   - If no user exists → creates a new user with the `name` and `email`.
   - This means users are automatically registered on their first booking.
5. **Booking creation** — Creates a new `Booking` record linking the user ID and provider ID with the scheduled time and a default status of `"pending"`.
6. **Response** — Returns the created booking (with provider and user included) as JSON with a 201 status.

---

## 7. Library / Utilities

### `lib/prisma.js` — Prisma Client Singleton

**What it does:**
Exports a single shared instance of the Prisma database client. This prevents the app from creating a new database connection on every hot-reload during development.

**Why this pattern is needed:**
In Next.js development mode, the module cache is cleared on every file change. Without this singleton pattern, each hot-reload would create a new `PrismaClient` instance, quickly exhausting the SQLite connection pool.

**Logic:**
- In **production**: creates a new `PrismaClient` instance normally.
- In **development**: stores the instance on the `global` object (`global.prisma`). If it already exists (from a previous hot-reload), reuses it. Otherwise, creates a new one and stores it.

**Usage across the project:**
```js
import prisma from '../lib/prisma'
const data = await prisma.booking.findMany()
```

---

## 8. Styles

### `styles/globals.css` — Global Stylesheet

**What it does:**
- Loads the three Tailwind CSS layers: `base` (resets), `components` (pre-built classes), and `utilities` (atomic classes).
- Sets `height: 100%` on `html`, `body`, and `#__next` so full-height layouts work.
- Defines reusable custom component classes using `@layer components`.

**Custom component classes:**

| Class | Description |
|---|---|
| `.btn-primary` | Indigo filled button with shadow, hover darkening, and press animation |
| `.btn-outline` | Indigo outlined button with hover background |
| `.card` | White rounded card with subtle shadow and ring border |
| `.input` | Styled text input with focus ring and border transitions |

These classes are used throughout pages to keep styling consistent without repeating long Tailwind class strings.

---

## 9. Configuration Files

### `next.config.js` — Next.js Configuration

Currently empty (uses all Next.js defaults). Can be extended to add image domains, environment variables, redirects, rewrites, etc.

---

### `tailwind.config.js` — Tailwind CSS Configuration

- `content`: Tells Tailwind to scan `pages/` and `components/` directories for class names so unused styles are removed in production builds.
- `theme.extend`: Empty — uses the default Tailwind design system (colors, spacing, fonts, etc.).
- `plugins`: None added.

---

### `postcss.config.js` — PostCSS Configuration

Runs two PostCSS plugins on every CSS file:
- **tailwindcss**: Processes Tailwind directives (`@tailwind`, `@layer`, `@apply`) into real CSS.
- **autoprefixer**: Automatically adds vendor prefixes (e.g. `-webkit-`) to CSS properties for cross-browser compatibility.

---

## 10. Database Seed

### `prisma/seed.js` — Sample Data Seeder

**Run with:** `npm run seed`

**What it does:**
Populates the database with sample services and providers so the app has content to display. Uses upsert operations so running the seed multiple times is safe and idempotent.

**Data seeded:**

**Services (3):**
| Name | Slug |
|---|---|
| Barber | barber |
| Plumbing | plumbing |
| Cleaning | cleaning |

**Providers (6 — 2 per service):**
| Name | Rating | Service |
|---|---|---|
| Alice the Barber | 4.8 | Barber |
| Bob the Barber | 4.6 | Barber |
| Cathy the Plumber | 4.7 | Plumbing |
| Dinesh the Plumber | 4.4 | Plumbing |
| Ella the Cleaner | 4.9 | Cleaning |
| Faisal the Cleaner | 4.5 | Cleaning |

**Logic:**
1. Loops through the service list, upserting each by `slug` (creates if not exists, skips if already there).
2. Looks up each service by slug to get its database `id`.
3. Loops through providers. For each provider, checks if a provider with that `name` already exists — updates if yes, creates if no.
4. Disconnects the Prisma client when done.

---

## 11. NPM Scripts

Defined in `package.json`:

| Script | Command | Description |
|---|---|---|
| `npm run dev` | `next dev` | Start the development server at `http://localhost:3000` with hot-reload |
| `npm run build` | `next build` | Build the app for production (optimized bundle) |
| `npm run start` | `next start` | Start the production server (requires `npm run build` first) |
| `npm run migrate` | `prisma migrate dev --name init` | Create and apply a new database migration |
| `npm run prisma:generate` | `prisma generate` | Regenerate the Prisma client after schema changes |
| `npm run seed` | `node prisma/seed.js` | Populate the database with sample data |

---

## 12. User Flow

```
Home Page (/)
    │
    ├── Click "My Bookings" ──────────────────────────► Bookings Page (/bookings)
    │                                                        Shows all bookings with status
    │
    └── Click a Service Card
            │
            ▼
    Service Page (/services/[slug])
    Shows list of providers for that service
            │
            └── Click "Book Now"
                    │
                    ▼
            Provider Page (/providers/[id])
            Shows provider profile + booking form
                    │
                    └── Fill form and submit
                            │
                            ▼
                    POST /api/bookings
                    Creates user (upsert) + booking record
                            │
                            ▼
                    Success message shown on page
                    Booking appears on /bookings page
```

---

## 13. How to Run

### Prerequisites
- Node.js 18 or higher
- npm

### Steps

```bash
# 1. Install dependencies
npm install

# 2. Generate Prisma client (needed after fresh install)
npx prisma generate

# 3. Create the SQLite database and apply migrations
npx prisma migrate deploy

# 4. Seed the database with sample data
npm run seed

# 5. Start the development server
npm run dev
```

Open `http://localhost:3000` in your browser.

### Environment
No `.env` file is required. The database connection is hardcoded in `prisma/schema.prisma` as `file:./dev.db` (a local SQLite file inside the `prisma/` folder).

---

*Documentation generated for UrbanServe — UrbanClap Clone*
