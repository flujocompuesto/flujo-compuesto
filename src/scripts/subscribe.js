/**
 * Conecta los formularios de captura de correo con /api/subscribe (Beehiiv).
 * Se aplica a cualquier <form data-subscribe data-source="...">.
 * Dentro del form debe haber un input[type="email"] y (opcional) un input[type="text"].
 */
function wireForms() {
  const forms = document.querySelectorAll('form[data-subscribe]');
  forms.forEach((form) => {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();

      const emailEl = form.querySelector('input[type="email"]');
      const nombreEl = form.querySelector('input[type="text"]');
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
          body: JSON.stringify({ email, nombre, source }),
        });
        const data = await res.json().catch(() => ({}));

        if (res.ok && data.ok) {
          showSuccess(form, nombre);
        } else if (data.error === 'email_invalido') {
          showMsg(form, 'Revisa tu correo — no parece válido.', 'err');
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
  form.innerHTML =
    `<div class="subscribe-ok" role="status">` +
    `<div class="subscribe-ok__ic" aria-hidden="true">✓</div>` +
    `<div class="subscribe-ok__title">${saludo}Revisa tu correo.</div>` +
    `<div class="subscribe-ok__sub">Te envié el acceso. Si no lo ves, mira en Promociones o Spam.</div>` +
    `</div>`;
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', wireForms);
} else {
  wireForms();
}
