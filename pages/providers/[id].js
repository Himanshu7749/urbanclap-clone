import { useState } from 'react'
import Link from 'next/link'

const PYTHON_API = process.env.PYTHON_API_URL || 'http://localhost:8000'

function StarRating({ rating }) {
  const stars = Math.round(rating ?? 0)
  return (
    <span className="flex items-center gap-0.5 text-yellow-400">
      {Array.from({ length: 5 }).map((_, i) => (
        <svg key={i} className={`h-4 w-4 ${i < stars ? 'fill-current' : 'fill-gray-200'}`} viewBox="0 0 20 20">
          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
        </svg>
      ))}
      <span className="ml-1 text-sm font-medium text-gray-600">{rating ? rating.toFixed(1) : 'N/A'}</span>
    </span>
  )
}

export default function ProviderProfile({ provider }) {
  const [form, setForm] = useState({ name: '', email: '', date: '', time: '10:00' })
  const [status, setStatus] = useState(null)
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)

  if (!provider) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-gray-50">
        <p className="text-gray-500">Provider not found.</p>
      </div>
    )
  }

  const handleChange = (e) => {
    const { name, value } = e.target
    setForm((c) => ({ ...c, [name]: value }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setStatus(null)

    const res = await fetch(`${PYTHON_API}/api/bookings`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        provider_id: provider.id,
        name: form.name,
        email: form.email,
        scheduled_at: `${form.date}T${form.time}:00`,
      }),
    })

    const data = await res.json()
    setLoading(false)

    if (!res.ok) {
      setError(data.detail || 'Unable to create booking.')
      return
    }

    setStatus(`Booking confirmed for ${new Date(data.scheduled_at).toLocaleString()}`)
    setForm({ name: '', email: '', date: '', time: '10:00' })
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-purple-50">
      <nav className="sticky top-0 z-50 border-b border-white/60 bg-white/80 backdrop-blur-md">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
          <Link href="/" className="flex items-center gap-2">
            <span className="text-2xl">🏙️</span>
            <span className="text-xl font-bold text-indigo-700">UrbanServe</span>
          </Link>
          <Link href={`/services/${provider.service.slug}`} className="btn-outline text-sm py-2 px-4">
            ← Back to {provider.service.name}
          </Link>
        </div>
      </nav>

      <main className="mx-auto max-w-2xl px-6 py-12">
        <div className="card mb-8 flex items-center gap-6">
          <div className="flex h-20 w-20 flex-shrink-0 items-center justify-center rounded-3xl bg-gradient-to-br from-indigo-400 to-purple-500 text-4xl font-bold text-white shadow-lg">
            {provider.name[0]}
          </div>
          <div>
            <h1 className="text-2xl font-extrabold text-gray-900">{provider.name}</h1>
            <p className="mt-0.5 text-sm text-gray-500">{provider.service.name} Specialist</p>
            <div className="mt-2">
              <StarRating rating={provider.rating} />
            </div>
          </div>
        </div>

        <div className="card">
          <h2 className="mb-1 text-xl font-bold text-gray-900">Book an Appointment</h2>
          <p className="mb-6 text-sm text-gray-500">Fill in your details and pick a time slot.</p>

          {status && (
            <div className="mb-4 flex items-center gap-3 rounded-xl border border-green-200 bg-green-50 px-4 py-3 text-green-700">
              <span className="text-xl">✅</span>
              <span className="text-sm font-medium">{status}</span>
            </div>
          )}
          {error && (
            <div className="mb-4 flex items-center gap-3 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-red-700">
              <span className="text-xl">❌</span>
              <span className="text-sm font-medium">{error}</span>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-5">
            <label className="block">
              <span className="text-sm font-semibold text-gray-700">Full Name</span>
              <input type="text" name="name" value={form.name} onChange={handleChange} required placeholder="John Doe" className="input" />
            </label>

            <label className="block">
              <span className="text-sm font-semibold text-gray-700">Email Address</span>
              <input type="email" name="email" value={form.email} onChange={handleChange} required placeholder="john@example.com" className="input" />
            </label>

            <div className="grid gap-4 sm:grid-cols-2">
              <label className="block">
                <span className="text-sm font-semibold text-gray-700">Date</span>
                <input type="date" name="date" value={form.date} onChange={handleChange} required className="input" />
              </label>
              <label className="block">
                <span className="text-sm font-semibold text-gray-700">Time</span>
                <input type="time" name="time" value={form.time} onChange={handleChange} required className="input" />
              </label>
            </div>

            <button type="submit" disabled={loading} className="btn-primary w-full py-3">
              {loading ? (
                <>
                  <svg className="h-4 w-4 animate-spin" viewBox="0 0 24 24" fill="none">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z" />
                  </svg>
                  Booking…
                </>
              ) : (
                'Confirm Booking'
              )}
            </button>
          </form>
        </div>
      </main>
    </div>
  )
}

export async function getServerSideProps({ params }) {
  try {
    const res = await fetch(`${PYTHON_API}/api/providers/${params.id}`)
    if (!res.ok) return { notFound: true }
    const provider = await res.json()
    return { props: { provider } }
  } catch {
    return { notFound: true }
  }
}
