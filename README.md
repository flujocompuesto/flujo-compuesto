# Flujo Compuesto

Sitio web + embudo de **educación financiera e inversión de largo plazo**.
Promesa central: **"De cero a tu primer portafolio"** — filosofía de bajo costo
(Bogleheads / Ben Felix), pensada para quien ya tiene con qué invertir pero le
falta el *cómo*.

## Stack

- **[Astro](https://astro.build)** — sitio estático, rápido y optimizado para SEO.
- **Cloudflare Pages** — hosting (deploy desde `main`).
- SEO + AI-search: JSON-LD (Organization, WebSite, FAQPage), Open Graph, sitemap y `robots.txt`.

## Desarrollo

```bash
npm install
npm run dev      # http://localhost:4321
npm run build    # genera /dist
npm run preview  # previsualiza el build
```

## Estructura

```
src/
  layouts/Base.astro     # <head>, meta SEO, Open Graph, JSON-LD
  pages/index.astro      # landing / embudo
  styles/global.css      # sistema de diseño
public/                  # favicon, robots.txt, imágenes estáticas
```

## Roadmap (fases)

- **Fase 1 (actual)** — Landing + embudo + captura de correo (lead magnet). Arrancar la lista.
- **Fase 2** — Curso self-paced, área de miembros con login, progreso y contenido gated por pago (Next.js + Supabase + Stripe/Whop).
- **Fase 3** — Comunidad (Whop + Discord) y consultoría 1:1.

## Notas

- **Nunca** subir secretos ni datos de clientes al repo (usar variables de entorno / Cloudflare).
- Todo el contenido es educativo — **no** asesoría de inversión personalizada.
