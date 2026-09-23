# -*- coding: utf-8 -*-
"""
Genera public/og-default.png (1200x630): la imagen que aparece al compartir
el sitio en WhatsApp, LinkedIn, X, etc.

Uso: python3 scripts/descargas/gen_og.py
"""
import base64, pathlib, subprocess

ROOT = pathlib.Path(__file__).resolve().parents[2]
BUILD = ROOT / "scripts/descargas/build"
OUT = ROOT / "public/og-default.png"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
FONTS = ROOT / "node_modules/@fontsource/montserrat/files"

faces = "".join(
    f"@font-face{{font-family:'Montserrat';font-weight:{w};src:url(data:font/woff2;base64,"
    f"{base64.b64encode((FONTS / f'montserrat-latin-{w}-normal.woff2').read_bytes()).decode()}) format('woff2');}}"
    for w in (600, 800)
)

HTML = f"""<!doctype html><html><head><meta charset="utf-8"><style>{faces}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1200px;height:630px;overflow:hidden}}
body{{font-family:'Montserrat',sans-serif;background:#24344B;color:#fff;position:relative;padding:72px 80px}}
.brand{{display:flex;align-items:center;gap:16px;font-weight:800;font-size:34px}}
h1{{font-weight:800;font-size:76px;line-height:1.04;letter-spacing:-.02em;margin-top:58px;max-width:760px}}
h1 span{{color:#2EE272}}
p{{font-weight:600;font-size:28px;color:rgba(255,255,255,.75);margin-top:26px;max-width:700px;line-height:1.35}}
.url{{position:absolute;left:80px;bottom:60px;font-weight:600;font-size:24px;color:#6FE3A5}}
svg.curve{{position:absolute;right:0;bottom:0}}
</style></head><body>
<div class="brand">
  <svg width="56" height="56" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#fff" fill-opacity=".1"/>
  <path d="M12 44 C24 44, 26 20, 52 16" fill="none" stroke="#1DBE60" stroke-width="6" stroke-linecap="round"/><circle cx="52" cy="16" r="6" fill="#2EE272"/></svg>
  Flujo Compuesto
</div>
<h1>Ganas bien. Ahora aprende a <span>invertir bien.</span></h1>
<p>Educación financiera e inversión de largo plazo, desde Latinoamérica.</p>
<div class="url">flujocompuesto.com</div>
<svg class="curve" width="460" height="630" viewBox="0 0 460 630">
  <defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1DBE60" stop-opacity=".35"/><stop offset="1" stop-color="#1DBE60" stop-opacity="0"/></linearGradient></defs>
  <path d="M0 600 C180 596, 300 540, 370 400 C410 320, 432 220, 440 120 L440 630 L0 630 Z" fill="url(#g)"/>
  <path d="M0 600 C180 596, 300 540, 370 400 C410 320, 432 220, 440 120" fill="none" stroke="#2EE272" stroke-width="8" stroke-linecap="round"/>
  <circle cx="440" cy="120" r="14" fill="#fff"/>
</svg>
</body></html>"""

BUILD.mkdir(parents=True, exist_ok=True)
page = BUILD / "og.html"
page.write_text(HTML, encoding="utf-8")
subprocess.run(
    [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--window-size=1200,630",
     f"--screenshot={OUT}", page.as_uri()],
    check=True, capture_output=True,
)
print(f"OG: {OUT} ({OUT.stat().st_size // 1024} KB)")
