import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

// Biblioteca "Aprende" — artículos educativos (motor SEO / AI-search).
const aprende = defineCollection({
  loader: glob({ pattern: '**/*.mdx', base: './src/content/aprende' }),
  schema: z.object({
    title: z.string(),          // título SEO (aparece en <title> y H1)
    description: z.string(),    // entradilla visible en la página (y meta description por defecto)
    seoTitle: z.string().max(60).optional(),        // <title> para Google si el título es largo
    seoDescription: z.string().max(155).optional(), // meta description si la entradilla es larga
    category: z.string(),       // ej. "Fundamentos", "Inversión", "Estrategia"
    order: z.number(),          // orden dentro de la biblioteca
    icon: z.string().default('📄'),
    readingTime: z.string().default('5 min'),
    updated: z.coerce.date().optional(),
    draft: z.boolean().default(false),
  }),
});

export const collections = { aprende };
