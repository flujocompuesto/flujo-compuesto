/**
 * Conecta los formularios de captura de correo con /api/subscribe (Beehiiv).
 * Se aplica a cualquier <form data-subscribe data-source="...">.
 * Dentro del form: input[name="email"], (opcional) input[name="nombre"], y el campo
 * trampa + widget de Turnstile que agrega el componente FormGuard.
 */
function wireForms() {
  const forms = document.querySelectorAll('form[data-subscribe]');
  forms.forEach((form) => {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();

      const emailEl = form.querySelector('input[name="email"]');
      const nombreEl = form.querySelector('input[name="nombre"]');
      const trampa = form.querySelector('input[name="website"]');
      const tsInput = form.querySelector('input[name="cf-turnstile-response"]');
      const btn = form.querySelector('button[type="submit"]');
      if (!emailEl || !btn) return;

      const email = emailEl.value.trim();
      const nombre = nombreEl ? nombreEl.value.trim() : '';
      const source = form.getAttribute('data-source') || 'sitio';

      // Estado: enviando
      const btnLabel = btn.textContent;
      btn.disabled = true;
      btn.textContent = 'Enviando…';
      clearMsg(form);

      try {
        const res = await fetch('/api/subscribe', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            email,
            nombre,
            source,
            website: trampa ? trampa.value : '',
            turnstile: tsInput ? tsInput.value : '',
          }),
        });
        const data = await res.json().catch(() => ({}));

        if (res.ok && data.ok) {
          showSuccess(form, nombre);
        } else if (data.error === 'email_invalido') {
          showMsg(form, 'Revisa tu correo — no parece válido.', 'err');
          resetBtn(btn, btnLabel);
        } else if (data.error === 'verificacion') {
          showMsg(form, 'No pudimos verificar que no eres un robot. Intenta de nuevo.', 'err');
          resetTurnstile(form);
          resetBtn(btn, btnLabel);
        } else {
          showMsg(form, 'Algo falló al suscribirte. Intenta de nuevo en un momento.', 'err');
          resetBtn(btn, btnLabel);
        }
      } catch {
        showMsg(form, 'Sin conexión. Revisa tu internet e intenta otra vez.', 'err');
        resetBtn(btn, btnLabel);
      }
    });
  });
}

// El token de Turnstile es de un solo uso: si el envío falla hay que pedir otro.
function resetTurnstile(form) {
  const w = form.querySelector('.cf-turnstile');
  if (w && window.turnstile) window.turnstile.reset(w);
}

function resetBtn(btn, label) {
  btn.disabled = false;
  btn.textContent = label;
}

function clearMsg(form) {
  const m = form.querySelector('.subscribe-msg');
  if (m) m.remove();
}

function showMsg(form, text, kind) {
  clearMsg(form);
  const p = document.createElement('p');
  p.className = 'subscribe-msg subscribe-msg--' + kind;
  p.setAttribute('role', 'status');
  p.textContent = text;
  form.appendChild(p);
}

function showSuccess(form, nombre) {
  const saludo = nombre ? `¡Listo, ${nombre}! ` : '¡Listo! ';
  // (el saludo se inserta con textContent más abajo, no dentro del HTML)
  form.innerHTML =
    `<div class="subscribe-ok" role="status">` +
    `<div class="subscribe-ok__ic" aria-hidden="true">✓</div>` +
    `<div class="subscribe-ok__title"></div>` +
    `<div class="subscribe-ok__dl">` +
    `<a class="btn btn--primary" href="/descargas/guia-flujo-compuesto.pdf" download>📘 Guía en PDF</a>` +
    `<a class="btn btn--ghost" href="/descargas/plantilla-flujo-compuesto.xlsx" download>📊 Plantilla Excel</a>` +
    `</div>` +
    `<div class="subscribe-ok__sub">También te llegará por correo. Si no lo ves, mira en Promociones o Spam.</div>` +
    `</div>`;
  form.querySelector('.subscribe-ok__title').textContent = `${saludo}Aquí tienes tu guía.`;
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', wireForms);
} else {
  wireForms();
}
