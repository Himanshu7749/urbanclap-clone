import Link from 'next/link'

const PYTHON_API = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

const statusColors = {
  pending: 'bg-yellow-100 text-yellow-700',
  confirmed: 'bg-green-100 text-green-700',
  cancelled: 'bg-red-100 text-red-700',
}

export default function Bookings({ bookings }) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-purple-50">
      <nav className="sticky top-0 z-50 border-b border-white/60 bg-white/80 backdrop-blur-md">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
          <Link href="/" className="flex items-center gap-2">
            <span className="text-2xl">🏙️</span>
            <span className="text-xl font-bold text-indigo-700">UrbanServe</span>
          </Link>
          <Link href="/" className="btn-outline text-sm py-2 px-4">
            ← Home
          </Link>
        </div>
      </nav>

      <main className="mx-auto max-w-4xl px-6 py-12">
        <div className="mb-10">
          <h1 className="text-4xl font-extrabold text-gray-900">My Bookings</h1>
          <p className="mt-2 text-gray-500">Track all your scheduled services in one place.</p>
        </div>

        {bookings.length === 0 ? (
          <div className="card flex flex-col items-center gap-4 py-20 text-center">
            <span className="text-6xl">📅</span>
            <h2 className="text-xl font-bold text-gray-800">No bookings yet</h2>
            <p className="text-gray-500">Browse our services and book your first professional.</p>
            <Link href="/" className="btn-primary mt-2">
              Explore Services
            </Link>
          </div>
        ) : (
          <div className="space-y-4">
            {bookings.map((booking) => (
              <div key={booking.id} className="card flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                <div className="flex items-center gap-4">
                  <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-indigo-100 text-2xl">
                    🔖
                  </div>
                  <div>
                    <p className="font-bold text-gray-900">{booking.provider.name}</p>
                    <p className="text-sm text-gray-500">{booking.provider.service.name}</p>
                    <p className="text-sm text-gray-400">
                      {booking.user.name} · {booking.user.email}
                    </p>
                  </div>
                </div>
                <div className="flex flex-col items-end gap-2">
                  <span className={`rounded-full px-3 py-1 text-xs font-semibold ${statusColors[booking.status] || 'bg-gray-100 text-gray-600'}`}>
                    {booking.status}
                  </span>
                  <p className="text-sm text-gray-500">
                    {new Date(booking.scheduled_at).toLocaleString()}
                  </p>
                </div>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  )
}

export async function getServerSideProps() {
  try {
    const res = await fetch(`${PYTHON_API}/api/bookings`)
    if (!res.ok) return { props: { bookings: [] } }
    const bookings = await res.json()
    return { props: { bookings } }
  } catch {
    return { props: { bookings: [] } }
  }
}
