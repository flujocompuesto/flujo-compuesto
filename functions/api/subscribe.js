/**
 * Cloudflare Pages Function — POST /api/subscribe
 *
 * Recibe { nombre, email, source } desde los formularios del sitio y crea
 * la suscripción en Beehiiv usando la API v2.
 *
 * Secretos (se configuran como variables de entorno en Cloudflare Pages —
 * NUNCA en el código):
 *   - BEEHIIV_API_KEY          (secreto, cifrado)
 *   - BEEHIIV_PUBLICATION_ID   (ej. pub_xxxxxxxx)
 */

const json = (data, status = 200) =>
  new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });

const isEmail = (v) => typeof v === 'string' && /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v);

export async function onRequestPost({ request, env }) {
  // 1) Configuración presente
  if (!env.BEEHIIV_API_KEY || !env.BEEHIIV_PUBLICATION_ID) {
    return json({ ok: false, error: 'config' }, 500);
  }

  // 2) Parsear y validar el body
  let body;
  try {
    body = await request.json();
  } catch {
    return json({ ok: false, error: 'bad_request' }, 400);
  }

  const email = (body.email || '').trim().toLowerCase();
  const nombre = (body.nombre || '').trim();
  const source = (body.source || 'sitio').toString().slice(0, 60);

  if (!isEmail(email)) {
    return json({ ok: false, error: 'email_invalido' }, 422);
  }

  // 3) Llamada a Beehiiv
  const endpoint = `https://api.beehiiv.com/v2/publications/${env.BEEHIIV_PUBLICATION_ID}/subscriptions`;
  const base = {
    email,
    reactivate_existing: true,
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
    // Primer intento: con el nombre como custom field.
    let res = post(nombre ? { ...base, custom_fields: [{ name: 'Nombre', value: nombre }] } : base);
    res = await res;

    // Si falla (p.ej. el custom field "Nombre" no existe aún), reintenta sin él
    // para que al menos el correo siempre quede capturado.
    if (!res.ok && nombre) {
      res = await post(base);
    }

    if (!res.ok) {
      const detail = await res.text().catch(() => '');
      return json({ ok: false, error: 'beehiiv', status: res.status, detail: detail.slice(0, 200) }, 502);
    }

    return json({ ok: true });
  } catch {
    return json({ ok: false, error: 'network' }, 502);
  }
}
// Nota: al exportar solo onRequestPost, cualquier otro método → 405 automático.
