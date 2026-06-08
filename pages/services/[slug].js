import Link from 'next/link'
import prisma from '../../lib/prisma'

function StarRating({ rating }) {
  const stars = Math.round(rating ?? 0)
  return (
    <span className="flex items-center gap-0.5 text-yellow-400">
      {Array.from({ length: 5 }).map((_, i) => (
        <svg key={i} className={`h-4 w-4 ${i < stars ? 'fill-current' : 'fill-gray-200'}`} viewBox="0 0 20 20">
          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
        </svg>
      ))}
      <span className="ml-1 text-sm text-gray-500">{rating ? rating.toFixed(1) : 'N/A'}</span>
    </span>
  )
}

export default function ServicePage({ service, providers }) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-purple-50">
      {/* Navbar */}
      <nav className="sticky top-0 z-50 border-b border-white/60 bg-white/80 backdrop-blur-md">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
          <Link href="/" className="flex items-center gap-2">
            <span className="text-2xl">🏙️</span>
            <span className="text-xl font-bold text-indigo-700">UrbanServe</span>
          </Link>
          <Link href="/" className="btn-outline text-sm py-2 px-4">
            ← Back
          </Link>
        </div>
      </nav>

      <main className="mx-auto max-w-4xl px-6 py-12">
        <div className="mb-10">
          <p className="mb-1 text-sm font-medium text-indigo-600">Available Professionals</p>
          <h1 className="text-4xl font-extrabold text-gray-900">{service.name}</h1>
          <p className="mt-2 text-gray-500">Choose a verified provider and book your slot instantly.</p>
        </div>

        {providers.length === 0 ? (
          <div className="card flex flex-col items-center gap-4 py-20 text-center">
            <span className="text-6xl">🔍</span>
            <h2 className="text-xl font-bold text-gray-800">No providers yet</h2>
            <p className="text-gray-500">We're onboarding professionals — check back soon!</p>
          </div>
        ) : (
          <div className="grid gap-4 sm:grid-cols-2">
            {providers.map((p) => (
              <div key={p.id} className="card flex flex-col gap-4">
                <div className="flex items-center gap-4">
                  <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-gradient-to-br from-indigo-400 to-purple-500 text-2xl font-bold text-white shadow">
                    {p.name[0]}
                  </div>
                  <div>
                    <p className="font-bold text-gray-900">{p.name}</p>
                    <StarRating rating={p.rating} />
                  </div>
                </div>
                <Link href={`/providers/${p.id}`} className="btn-primary w-full justify-center">
                  Book Now
                </Link>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  )
}

export async function getServerSideProps({ params }) {
  const service = await prisma.service.findUnique({
    where: { slug: params.slug },
    include: {
      providers: { select: { id: true, name: true, rating: true } },
    },
  })

  if (!service) return { notFound: true }

  return {
    props: {
      service: { id: service.id, name: service.name, slug: service.slug },
      providers: service.providers,
    },
  }
}
