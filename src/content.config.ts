import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const portfolio = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/metadata/portfolio' }),
  schema: ({ image }) =>
    z.object({
      title: z.string(),
      image: image(),
      date: z.coerce.date(),
	  // category: z.enum(['pixel', 'digital', '3d']),
      tags: z.array(z.string()).default([]),
    }),
});

export const collections = { portfolio };
