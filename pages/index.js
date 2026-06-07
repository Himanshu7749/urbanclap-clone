import Link from 'next/link'

export default function Home() {
  const services = [
    { slug: 'barber', name: 'Barber' },
    { slug: 'plumbing', name: 'Plumbing' },
    { slug: 'cleaning', name: 'Home Cleaning' },
  ]

  return (
    <div className="min-h-screen p-8">
      <header className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-6">UrbanClap Clone</h1>
        <p className="text-gray-600 mb-6">
          Discover services and book a provider directly through the app.
        </p>
      </header>

      <main className="max-w-4xl mx-auto">
        <section className="grid gap-4 mb-6">
          {services.map((s) => (
            <Link
              key={s.slug}
              href={`/services/${s.slug}`}
              className="p-4 border rounded hover:bg-gray-50"
            >
              {s.name}
            </Link>
          ))}
        </section>

        <Link href="/bookings" className="inline-block px-4 py-3 bg-indigo-600 text-white rounded hover:bg-indigo-700">
          View Bookings
        </Link>
      </main>
    </div>
  )
}
