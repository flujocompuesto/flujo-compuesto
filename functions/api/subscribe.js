/**
 * Cloudflare Pages Function — POST /api/subscribe
 *
 * Recibe { nombre, email, source, website, turnstile } desde los formularios
 * del sitio y crea la suscripción en Beehiiv usando la API v2.
 *
 * Protección anti-abuso (en este orden):
 *   1. Origen: solo se aceptan peticiones hechas desde el propio sitio.
 *   2. Campo trampa ("website"): si viene lleno es un bot → se descarta en
 *      silencio (respondemos ok para no darle pistas).
 *   3. Cloudflare Turnstile: si existe TURNSTILE_SECRET_KEY, el token es
 *      obligatorio y se valida contra Cloudflare.
 *
 * Variables de entorno en Cloudflare Pages (NUNCA en el código):
 *   - BEEHIIV_API_KEY          (secreto, cifrado)
 *   - BEEHIIV_PUBLICATION_ID   (ej. pub_xxxxxxxx)
 *   - TURNSTILE_SECRET_KEY     (secreto, opcional; va junto con la variable de
 *                               build PUBLIC_TURNSTILE_SITE_KEY)
 */

const json = (data, status = 200) =>
  new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });

const isEmail = (v) => typeof v === 'string' && v.length <= 254 && /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v);

// Hosts desde los que se permite suscribir.
function origenPermitido(request) {
  const origen = request.headers.get('Origin') || request.headers.get('Referer');
  if (!origen) return false;
  let host;
  try {
    host = new URL(origen).hostname;
  } catch {
    return false;
  }
  return (
    host === 'flujocompuesto.com' ||
    host === 'www.flujocompuesto.com' ||
    host === 'flujo-compuesto.pages.dev' ||
    host.endsWith('.flujo-compuesto.pages.dev') || // despliegues de preview
    host === 'localhost' ||
    host === '127.0.0.1'
  );
}

async function turnstileValido(token, secret, ip) {
  if (!token) return false;
  const form = new FormData();
  form.append('secret', secret);
  form.append('response', token);
  if (ip) form.append('remoteip', ip);
  try {
    const res = await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', { method: 'POST', body: form });
    const data = await res.json();
    return data.success === true;
  } catch {
    return false;
  }
}

export async function onRequestPost({ request, env }) {
  // 1) Configuración presente
  if (!env.BEEHIIV_API_KEY || !env.BEEHIIV_PUBLICATION_ID) {
    return json({ ok: false, error: 'config' }, 500);
  }

  // 2) Solo desde el propio sitio
  if (!origenPermitido(request)) {
    return json({ ok: false, error: 'origen' }, 403);
  }

  // 3) Parsear y validar el body
  let body;
  try {
    body = await request.json();
  } catch {
    return json({ ok: false, error: 'bad_request' }, 400);
  }

  // Campo trampa lleno → bot. Respondemos como si todo fuera bien y no llamamos a Beehiiv.
  if (typeof body.website === 'string' && body.website.trim() !== '') {
    return json({ ok: true });
  }

  const email = String(body.email || '').trim().toLowerCase();
  const nombre = String(body.nombre || '').trim().slice(0, 80);
  const source = String(body.source || 'sitio').slice(0, 60);

  if (!isEmail(email)) {
    return json({ ok: false, error: 'email_invalido' }, 422);
  }

  // 4) Turnstile (solo si está configurado)
  if (env.TURNSTILE_SECRET_KEY) {
    const ip = request.headers.get('CF-Connecting-IP');
    if (!(await turnstileValido(body.turnstile, env.TURNSTILE_SECRET_KEY, ip))) {
      return json({ ok: false, error: 'verificacion' }, 403);
    }
  }

  // 5) Llamada a Beehiiv
  const endpoint = `https://api.beehiiv.com/v2/publications/${env.BEEHIIV_PUBLICATION_ID}/subscriptions`;
  const base = {
    email,
    // false: si alguien se dio de baja, nadie puede volver a suscribirlo sin su consentimiento.
    reactivate_existing: false,
    send_welcome_email: true,
    utm_source: 'flujocompuesto',
    utm_medium: source,
    referring_site: 'flujocompuesto.com',
  };

  const post = (payload) =>
    fetch(endpoint, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${env.BEEHIIV_API_KEY}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    });

  try {
    // Primer intento: con el nombre en el campo nativo "First Name" de Beehiiv.
    let res = await post(nombre ? { ...base, custom_fields: [{ name: 'First Name', value: nombre }] } : base);

    // Si falla (p.ej. el nombre del campo no calza), reintenta sin él para que
    // al menos el correo siempre quede capturado.
    if (!res.ok && nombre) {
      res = await post(base);
    }

    if (!res.ok) {
      // El detalle de Beehiiv se queda en los logs del servidor, no va al navegador.
      console.error('beehiiv', res.status, (await res.text().catch(() => '')).slice(0, 300));
      return json({ ok: false, error: 'beehiiv' }, 502);
    }

    return json({ ok: true });
  } catch (err) {
    console.error('beehiiv network', err);
    return json({ ok: false, error: 'network' }, 502);
  }
}
// Nota: al exportar solo onRequestPost, cualquier otro método → 405 automático.
