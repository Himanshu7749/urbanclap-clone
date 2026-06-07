import { useState } from 'react'
import Link from 'next/link'
import prisma from '../../lib/prisma'

export default function ProviderProfile({ provider }) {
  const [form, setForm] = useState({
    name: '',
    email: '',
    date: '',
    time: '10:00',
  })
  const [status, setStatus] = useState(null)
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)

  if (!provider) {
    return (
      <div className="p-8">
        <p className="text-gray-600">Provider not found.</p>
      </div>
    )
  }

  const handleChange = (event) => {
    const { name, value } = event.target
    setForm((current) => ({ ...current, [name]: value }))
  }

  const handleSubmit = async (event) => {
    event.preventDefault()
    setLoading(true)
    setError(null)
    setStatus(null)

    const response = await fetch('/api/bookings', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        providerId: provider.id,
        name: form.name,
        email: form.email,
        scheduledAt: `${form.date}T${form.time}:00`,
      }),
    })

    const data = await response.json()
    setLoading(false)

    if (!response.ok) {
      setError(data.error || 'Unable to create booking.')
      return
    }

    setStatus(`Booking confirmed for ${new Date(data.booking.scheduledAt).toLocaleString()}`)
    setForm({ name: '', email: '', date: '', time: '10:00' })
  }

  return (
    <div className="p-8">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-2xl font-bold">{provider.name}</h2>
          <p className="text-sm text-gray-500">Service: {provider.service.name}</p>
          <p className="text-sm text-gray-500">Rating: {provider.rating ?? 'N/A'}</p>
        </div>
        <Link href={`/services/${provider.service.slug}`} className="text-indigo-600">
          Back to service
        </Link>
      </div>

      <div className="max-w-xl space-y-4">
        <div className="rounded-lg border p-4 bg-gray-50">
          <p className="font-semibold">Book this provider</p>
          <p className="text-sm text-gray-600">Submit your info and choose a date/time.</p>
        </div>

        {status && <div className="rounded border border-green-300 bg-green-50 p-4 text-green-700">{status}</div>}
        {error && <div className="rounded border border-red-300 bg-red-50 p-4 text-red-700">{error}</div>}

        <form onSubmit={handleSubmit} className="space-y-4">
          <label className="block">
            <span className="text-sm font-medium text-gray-700">Name</span>
            <input
              type="text"
              name="name"
              value={form.name}
              onChange={handleChange}
              required
              className="mt-1 block w-full rounded border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
            />
          </label>

          <label className="block">
            <span className="text-sm font-medium text-gray-700">Email</span>
            <input
              type="email"
              name="email"
              value={form.email}
              onChange={handleChange}
              required
              className="mt-1 block w-full rounded border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
            />
          </label>

          <div className="grid gap-4 sm:grid-cols-2">
            <label className="block">
              <span className="text-sm font-medium text-gray-700">Date</span>
              <input
                type="date"
                name="date"
                value={form.date}
                onChange={handleChange}
                required
                className="mt-1 block w-full rounded border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
              />
            </label>
            <label className="block">
              <span className="text-sm font-medium text-gray-700">Time</span>
              <input
                type="time"
                name="time"
                value={form.time}
                onChange={handleChange}
                required
                className="mt-1 block w-full rounded border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
              />
            </label>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="inline-flex items-center justify-center rounded bg-indigo-600 px-4 py-2 text-white hover:bg-indigo-700 disabled:cursor-not-allowed disabled:bg-indigo-400"
          >
            {loading ? 'Booking…' : 'Confirm Booking'}
          </button>
        </form>
      </div>
    </div>
  )
}

export async function getServerSideProps({ params }) {
  const provider = await prisma.provider.findUnique({
    where: { id: Number(params.id) },
    include: {
      service: true,
    },
  })

  if (!provider) {
    return { notFound: true }
  }

  return {
    props: {
      provider: {
        id: provider.id,
        name: provider.name,
        rating: provider.rating,
        service: {
          id: provider.service.id,
          name: provider.service.name,
          slug: provider.service.slug,
        },
      },
    },
  }
}
