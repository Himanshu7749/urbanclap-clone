import Link from 'next/link'
import prisma from '../lib/prisma'

export default function Bookings({ bookings }) {
  return (
    <div className="min-h-screen p-8">
      <div className="max-w-4xl mx-auto">
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-3xl font-bold">Your Bookings</h1>
          <Link href="/" className="text-indigo-600">
            Home
          </Link>
        </div>

        {bookings.length === 0 ? (
          <p className="text-gray-600">No bookings yet. Select a provider and schedule your first service.</p>
        ) : (
          <div className="space-y-4">
            {bookings.map((booking) => (
              <div key={booking.id} className="p-4 border rounded">
                <div className="font-semibold">{booking.provider.name}</div>
                <div className="text-sm text-gray-500">Service: {booking.provider.service.name}</div>
                <div className="text-sm">Customer: {booking.user.name} ({booking.user.email})</div>
                <div className="text-sm">When: {new Date(booking.scheduledAt).toLocaleString()}</div>
                <div className="text-sm">Status: {booking.status}</div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export async function getServerSideProps() {
  const bookings = await prisma.booking.findMany({
    include: {
      provider: {
        include: { service: true },
      },
      user: true,
    },
    orderBy: { scheduledAt: 'desc' },
  })

  return {
    props: {
      bookings: bookings.map((booking) => ({
        ...booking,
        scheduledAt: booking.scheduledAt.toISOString(),
      })),
    },
  }
}
