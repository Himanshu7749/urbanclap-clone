import { useEffect, useState } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/router'

const services = [
  { slug: 'barber',   name: 'Barber',       icon: '✂️', description: 'Haircuts, styling, beard trims and more at your doorstep.', color: 'from-orange-400 to-pink-500' },
  { slug: 'plumbing', name: 'Plumbing',      icon: '🔧', description: 'Leaks, clogs, installations — certified plumbers on demand.', color: 'from-blue-400 to-cyan-500' },
  { slug: 'cleaning', name: 'Home Cleaning', icon: '🧹', description: 'Deep cleaning, sanitization and tidy-up for every room.', color: 'from-green-400 to-emerald-500' },
]

export default function Home() {
  const router = useRouter()
  const [user, setUser] = useState(null)

  useEffect(() => {
    const stored = localStorage.getItem('user')
    if (stored) setUser(JSON.parse(stored))
  }, [])

  const logout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    setUser(null)
    router.push('/')
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-purple-50">
      <nav className="sticky top-0 z-50 border-b border-white/60 bg-white/80 backdrop-blur-md">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
          <div className="flex items-center gap-2">
            <span className="text-2xl">🏙️</span>
            <span className="text-xl font-bold text-indigo-700">UrbanServe</span>
          </div>
          <div className="flex items-center gap-3">
            <Link href="/bookings" className="btn-outline text-sm py-2 px-4">My Bookings</Link>
            {user ? (
              <>
                <span className="text-sm text-gray-600">Hi, <span className="font-semibold text-gray-900">{user.name}</span></span>
                <button onClick={logout} className="btn-outline text-sm py-2 px-4">Logout</button>
              </>
            ) : (
              <>
                <Link href="/login" className="btn-outline text-sm py-2 px-4">Sign In</Link>
                <Link href="/register" className="btn-primary text-sm py-2 px-4">Sign Up</Link>
              </>
            )}
          </div>
        </div>
      </nav>

      <section className="mx-auto max-w-6xl px-6 py-20 text-center">
        <div className="mb-4 inline-block rounded-full bg-indigo-100 px-4 py-1.5 text-sm font-medium text-indigo-700">
          Trusted by 10,000+ customers
        </div>
        <h1 className="mb-5 text-5xl font-extrabold leading-tight tracking-tight text-gray-900 md:text-6xl">
          Home services,{' '}
          <span className="bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">delivered</span>
        </h1>
        <p className="mx-auto mb-10 max-w-xl text-lg text-gray-500">
          Book verified professionals for barber, plumbing, cleaning and more — right from your phone.
        </p>
        <Link href="#services" className="btn-primary">Explore Services</Link>
      </section>

      <section id="services" className="mx-auto max-w-6xl px-6 pb-24">
        <h2 className="mb-10 text-center text-3xl font-bold text-gray-800">Our Services</h2>
        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {services.map((s) => (
            <Link key={s.slug} href={`/services/${s.slug}`} className="card group flex flex-col gap-4 overflow-hidden">
              <div className={`flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br ${s.color} text-3xl shadow-md transition group-hover:scale-110`}>
                {s.icon}
              </div>
              <div>
                <h3 className="text-lg font-bold text-gray-900">{s.name}</h3>
                <p className="mt-1 text-sm text-gray-500">{s.description}</p>
              </div>
              <span className="mt-auto text-sm font-semibold text-indigo-600 group-hover:underline">Browse providers →</span>
            </Link>
          ))}
        </div>
      </section>

      <footer className="border-t border-gray-100 bg-white py-8 text-center text-sm text-gray-400">
        © 2026 UrbanServe — All rights reserved.
      </footer>
    </div>
  )
}
