// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import mdx from '@astrojs/mdx';

// Dominio de producción — ajústalo cuando conectemos el dominio real.
const SITE = 'https://flujocompuesto.com';

// https://astro.build/config
export default defineConfig({
  site: SITE,
  integrations: [sitemap(), mdx()],
  // Cloudflare Pages sirve output estático desde /dist
  output: 'static',
  build: {
    inlineStylesheets: 'auto',
  },
});
