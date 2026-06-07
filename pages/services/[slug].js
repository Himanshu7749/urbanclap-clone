import Link from 'next/link'
import prisma from '../../lib/prisma'

export default function ServicePage({ service, providers }) {
  return (
    <div className="p-8">
      <h2 className="text-2xl font-bold mb-4">{service.name} Providers</h2>
      {providers.length === 0 ? (
        <p className="text-gray-600">No providers are available for this service yet.</p>
      ) : (
        <ul className="space-y-3">
          {providers.map((p) => (
            <li
              key={p.id}
              className="p-4 border rounded flex justify-between items-center"
            >
              <div>
                <div className="font-medium">{p.name}</div>
                <div className="text-sm text-gray-500">Rating: {p.rating ?? 'N/A'}</div>
              </div>
              <Link href={`/providers/${p.id}`} className="text-indigo-600">
                View
              </Link>
            </li>
          ))}
        </ul>
      )}

      <div className="mt-6">
        <Link href="/" className="text-sm text-gray-600">
          Back
        </Link>
      </div>
    </div>
  )
}

export async function getServerSideProps({ params }) {
  const service = await prisma.service.findUnique({
    where: { slug: params.slug },
    include: {
      providers: {
        select: { id: true, name: true, rating: true },
      },
    },
  })

  if (!service) {
    return { notFound: true }
  }

  return {
    props: {
      service: {
        id: service.id,
        name: service.name,
        slug: service.slug,
      },
      providers: service.providers,
    },
  }
}
