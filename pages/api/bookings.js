import prisma from '../../lib/prisma'

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    res.setHeader('Allow', ['POST'])
    return res.status(405).end(`Method ${req.method} Not Allowed`)
  }

  const { providerId, name, email, scheduledAt } = req.body

  if (!providerId || !name || !email || !scheduledAt) {
    return res.status(400).json({ error: 'Missing booking details' })
  }

  const provider = await prisma.provider.findUnique({
    where: { id: Number(providerId) },
  })

  if (!provider) {
    return res.status(404).json({ error: 'Provider not found' })
  }

  const user = await prisma.user.upsert({
    where: { email },
    update: { name },
    create: { name, email },
  })

  const booking = await prisma.booking.create({
    data: {
      providerId: Number(providerId),
      userId: user.id,
      scheduledAt: new Date(scheduledAt),
      status: 'pending',
    },
    include: {
      provider: true,
      user: true,
    },
  })

  return res.status(201).json({ booking })
}
