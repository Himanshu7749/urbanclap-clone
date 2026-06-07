# UrbanClap Clone (Next.js + Tailwind + Prisma)

Quick starter scaffold for an UrbanClap-like services marketplace.

Getting started

1. Install dependencies

```bash
npm install
```

2. Generate Prisma client and run migrations (creates SQLite DB)

```bash
npx prisma generate
npx prisma migrate dev --name init
node prisma/seed.js
```

3. Run dev server

```bash
npm run dev
```

What's included

- Next.js app with basic pages (home, services, provider profile)
- Tailwind CSS setup
- Prisma schema (SQLite) + seed script

Next steps

- Add authentication, provider dashboards, booking flow, payments.
