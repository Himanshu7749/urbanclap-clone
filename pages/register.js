import { useState } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/router'

const PYTHON_API = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export default function Register() {
  const router = useRouter()
  const [form, setForm] = useState({ name: '', email: '', password: '', confirm: '' })
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleChange = (e) => setForm(c => ({ ...c, [e.target.name]: e.target.value }))

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (form.password !== form.confirm) {
      setError('Passwords do not match.')
      return
    }
    setLoading(true)
    setError(null)

    const res = await fetch(`${PYTHON_API}/api/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: form.name, email: form.email, password: form.password }),
    })
    const data = await res.json()
    setLoading(false)

    if (!res.ok) {
      setError(data.detail || 'Registration failed.')
      return
    }

    localStorage.setItem('token', data.access_token)
    localStorage.setItem('user', JSON.stringify(data.user))
    router.push('/')
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-purple-50 flex items-center justify-center px-4">
      <div className="w-full max-w-md">
        <div className="mb-8 text-center">
          <Link href="/" className="inline-flex items-center gap-2 text-2xl font-bold text-indigo-700">
            <span>🏙️</span> UrbanServe
          </Link>
          <h1 className="mt-4 text-3xl font-extrabold text-gray-900">Create an account</h1>
          <p className="mt-2 text-sm text-gray-500">Already have one? <Link href="/login" className="text-indigo-600 font-medium hover:underline">Sign in</Link></p>
        </div>

        <div className="card">
          {error && (
            <div className="mb-4 flex items-center gap-3 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-red-700">
              <span>❌</span>
              <span className="text-sm font-medium">{error}</span>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <label className="block">
              <span className="text-sm font-semibold text-gray-700">Full Name</span>
              <input type="text" name="name" value={form.name} onChange={handleChange} required placeholder="John Doe" className="input" />
            </label>
            <label className="block">
              <span className="text-sm font-semibold text-gray-700">Email</span>
              <input type="email" name="email" value={form.email} onChange={handleChange} required placeholder="john@example.com" className="input" />
            </label>
            <label className="block">
              <span className="text-sm font-semibold text-gray-700">Password</span>
              <input type="password" name="password" value={form.password} onChange={handleChange} required placeholder="Min 6 characters" className="input" />
            </label>
            <label className="block">
              <span className="text-sm font-semibold text-gray-700">Confirm Password</span>
              <input type="password" name="confirm" value={form.confirm} onChange={handleChange} required placeholder="Repeat password" className="input" />
            </label>
            <button type="submit" disabled={loading} className="btn-primary w-full py-3 mt-2">
              {loading ? 'Creating account…' : 'Create Account'}
            </button>
          </form>
        </div>
      </div>
    </div>
  )
}
