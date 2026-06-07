const { PrismaClient } = require('@prisma/client')
const prisma = new PrismaClient()

async function main() {
  const services = [
    { name: 'Barber', slug: 'barber' },
    { name: 'Plumbing', slug: 'plumbing' },
    { name: 'Cleaning', slug: 'cleaning' },
  ]

  for (const s of services) {
    await prisma.service.upsert({
      where: { slug: s.slug },
      update: {},
      create: s,
    })
  }

  const barber = await prisma.service.findUnique({ where: { slug: 'barber' } })
  const plumbing = await prisma.service.findUnique({ where: { slug: 'plumbing' } })
  const cleaning = await prisma.service.findUnique({ where: { slug: 'cleaning' } })

  const providers = [
    { name: 'Alice the Barber', rating: 4.8, serviceId: barber.id },
    { name: 'Bob the Barber', rating: 4.6, serviceId: barber.id },
    { name: 'Cathy the Plumber', rating: 4.7, serviceId: plumbing.id },
    { name: 'Dinesh the Plumber', rating: 4.4, serviceId: plumbing.id },
    { name: 'Ella the Cleaner', rating: 4.9, serviceId: cleaning.id },
    { name: 'Faisal the Cleaner', rating: 4.5, serviceId: cleaning.id },
  ]

  for (const provider of providers) {
    const existing = await prisma.provider.findFirst({
      where: { name: provider.name },
    })

    if (existing) {
      await prisma.provider.update({
        where: { id: existing.id },
        data: provider,
      })
    } else {
      await prisma.provider.create({
        data: provider,
      })
    }
  }

  console.log('Seed complete')
}

main()
  .catch((e) => {
    console.error(e)
    process.exit(1)
  })
  .finally(async () => {
    await prisma.$disconnect()
  })
