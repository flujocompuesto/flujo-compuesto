# -*- coding: utf-8 -*-
"""
Genera public/descargas/guia-flujo-compuesto.pdf (content upgrade).

Uso (desde la raíz del repo, con node_modules instalado):
    python3 scripts/descargas/gen_pdf.py

Arma un HTML con la marca (Montserrat embebido) y lo imprime a PDF con
Chrome headless. Si cambias el texto de /guia, actualiza también este
archivo: el PDF es una copia curada de la guía, no se genera de la página.
"""
import base64, pathlib, subprocess

ROOT = pathlib.Path(__file__).resolve().parents[2]
BUILD = ROOT / "scripts/descargas/build"
OUT = ROOT / "public/descargas/guia-flujo-compuesto.pdf"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
FONTS = ROOT / "node_modules/@fontsource/montserrat/files"

def font_b64(w):
    return base64.b64encode((FONTS / f"montserrat-latin-{w}-normal.woff2").read_bytes()).decode()

faces = "".join(
    f"@font-face{{font-family:'Montserrat';font-style:normal;font-weight:{w};"
    f"src:url(data:font/woff2;base64,{font_b64(w)}) format('woff2');}}"
    for w in (400, 600, 700, 800)
)

LOGO = ('<svg width="34" height="34" viewBox="0 0 64 64">'
        '<rect width="64" height="64" rx="14" fill="#24344B"/>'
        '<path d="M12 44 C24 44, 26 20, 52 16" fill="none" stroke="#1DBE60" stroke-width="6" stroke-linecap="round"/>'
        '<circle cx="52" cy="16" r="6" fill="#2EE272"/></svg>')

CSS = """
*{box-sizing:border-box;margin:0;padding:0;-webkit-print-color-adjust:exact;print-color-adjust:exact;}
@page{size:A4;margin:16mm 15mm 20mm;}
html{background:#fff;color-scheme:light;font-family:'Montserrat',sans-serif;color:#3A4A45;font-size:10.5pt;line-height:1.55;}
h1,h2,h3{font-family:'Montserrat',sans-serif;color:#24344B;letter-spacing:-.01em;}
strong{color:#24344B;font-weight:700;}
p{margin:0 0 9px;}
.brand{display:flex;align-items:center;gap:9px;font-weight:800;font-size:13pt;color:#24344B;}
.cover{height:247mm;display:flex;flex-direction:column;justify-content:center;page-break-after:always;}
.cover .eyebrow{display:inline-block;align-self:flex-start;background:#DCF7E8;color:#128A46;font-weight:700;font-size:8.5pt;letter-spacing:.12em;text-transform:uppercase;padding:5px 13px;border-radius:20px;margin:26px 0 16px;}
.cover h1{font-size:33pt;font-weight:800;line-height:1.08;margin-bottom:14px;}
.cover .sub{font-size:12.5pt;color:#45566E;font-weight:500;max-width:150mm;margin-bottom:26px;}
.byline{display:flex;align-items:center;gap:11px;border-top:1px solid #E2E5E9;padding-top:16px;}
.byline .av{width:40px;height:40px;border-radius:50%;background:#24344B;color:#2EE272;font-weight:800;display:flex;align-items:center;justify-content:center;font-size:11pt;}
.cover .url{margin-top:auto;color:#64707F;font-size:9.5pt;font-weight:600;}
h2{font-size:16pt;font-weight:800;margin:20px 0 9px;padding-top:4px;}
.sec{page-break-inside:avoid;}
.lead-in{font-size:11pt;color:#45566E;}
.formula{text-align:center;background:#F0F1F2;border:1px solid #E2E5E9;border-radius:12px;padding:14px;margin:12px 0;}
.formula .lbl{font-size:7.5pt;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#64707F;margin-bottom:6px;}
.formula .eq{font-size:15pt;font-weight:800;color:#128A46;}
.formula .note{font-size:9.5pt;margin-top:5px;}
.two{display:flex;gap:11px;margin:11px 0;}
.box{flex:1;background:#fff;border:1px solid #E2E5E9;border-radius:10px;padding:12px 13px;}
.box.green{border-top:3px solid #1DBE60;}
.box.red{border-top:3px solid #C2544B;}
.box .t{font-weight:800;font-size:10.5pt;margin-bottom:4px;}
.box p{font-size:9.5pt;margin:0;color:#45566E;}
.highlight{background:#24344B;border-radius:12px;padding:16px 18px;margin:13px 0;color:#fff;}
.highlight .q{font-size:14pt;font-weight:800;color:#2EE272;margin-bottom:7px;}
.highlight p{color:rgba(255,255,255,.92);font-size:10pt;margin:0;}
.highlight strong{color:#fff;}
.callout{background:#EAFBF1;border:1px solid #BEEBCF;border-radius:12px;padding:13px 15px;margin:13px 0;}
.callout .t{font-weight:800;color:#128A46;margin-bottom:3px;}
.callout p{color:#24344B;font-size:10pt;margin:0;}
.quote{background:#DCF7E8;border-left:4px solid #1DBE60;border-radius:0 10px 10px 0;padding:11px 16px;margin:12px 0;font-weight:700;color:#24344B;font-size:11.5pt;}
ol,ul{margin:8px 0 10px 20px;}
li{margin-bottom:5px;font-size:10.5pt;}
.err{display:flex;gap:9px;padding:7px 0;border-bottom:1px solid #E2E5E9;}
.err .x{color:#C2544B;font-weight:800;}
.err:last-child{border-bottom:0;}
.foot{position:fixed;bottom:6mm;left:15mm;right:15mm;display:flex;justify-content:space-between;font-size:8pt;color:#9CA3AF;border-top:1px solid #E2E5E9;padding-top:4px;}
.disc{font-size:8.5pt;color:#64707F;border-top:1px solid #E2E5E9;padding-top:10px;margin-top:16px;line-height:1.5;}
.next{background:#F0F1F2;border-radius:12px;padding:14px 16px;margin:14px 0;}
.next .t{font-weight:800;color:#24344B;margin-bottom:6px;}
"""

BODY = f"""
<div class="foot"><span>Flujo Compuesto · De cero a tu primer portafolio, sin miedo</span><span>flujocompuesto.com</span></div>

<section class="cover">
  <div class="brand">{LOGO}<span>Flujo Compuesto</span></div>
  <span class="eyebrow">Guía gratuita</span>
  <h1>De cero a tu primer portafolio, sin miedo</h1>
  <div class="sub">La guía de arranque para empezar a invertir desde Latinoamérica — sin tecnicismos, sin adivinar el mercado y sin promesas de hacerte rico rápido.</div>
  <div class="byline"><div class="av">IH</div><div>Por <strong>Ivan Herrera</strong> · Ingeniero, no financiero<br><span style="color:#64707F;font-size:9.5pt">13 años gestionando su propio patrimonio</span></div></div>
  <div class="url">flujocompuesto.com</div>
</section>

<p class="lead-in">Si ganas bien pero tu dinero lleva años dormido en el banco, esta guía es para ti. No necesitas ser experto, ni tener mucho capital, ni dedicarle horas. Solo necesitas entender <strong>cómo empieza</strong> — y dar el primer paso.</p>
<p>Soy ingeniero, no financiero. Durante 13 años traté mis finanzas como trato mi trabajo de aseguramiento de calidad: como un sistema con datos, reglas y mejora continua. Esto es el método que uso con mi propio dinero, resumido para que empieces hoy.</p>

<div class="sec">
<h2>1. La riqueza no es cuánto ganas</h2>
<p>El error más caro en finanzas personales es confundir <strong>ingreso alto</strong> con <strong>riqueza</strong>. No son lo mismo:</p>
<div class="two">
  <div class="box red"><div class="t">⚙️ Ingresos</div><p>Lo que ganas trabajando. Depende de que <em>tú</em> trabajes. Si te detienes, se detiene. Cambias tiempo por dinero.</p></div>
  <div class="box green"><div class="t">🌱 Patrimonio</div><p>Lo que tu dinero genera por ti. Trabaja 24/7, incluso mientras duermes. Cambia capital por dinero.</p></div>
</div>
<div class="formula"><div class="lbl">La fórmula de la riqueza</div><div class="eq">Riqueza = Patrimonio × Rendimiento</div><div class="note">No importa cuánto ganes. Importa cuánto <strong>conservas</strong> y cuánto <strong>haces crecer</strong>.</div></div>
<div class="two">
  <div class="box red"><div class="t">El profesional atrapado</div><p>Gana $15,000/mes, gasta $14,500. Patrimonio pequeño. Si pierde su trabajo → crisis en 6 meses.</p></div>
  <div class="box green"><div class="t">El constructor de riqueza</div><p>Gana $5,000/mes, invierte $2,000 desde joven. Patrimonio sólido. Si pierde su trabajo → no cambia nada.</p></div>
</div>
<div class="quote">Tu objetivo no es ganar más. Es acumular activos que generen ingresos hasta que superen tus gastos. En ese momento, trabajar se vuelve opcional.</div>
</div>

<div class="sec">
<h2>2. El interés compuesto y la pregunta que lo cambia todo</h2>
<p>El interés compuesto ocurre cuando tus ganancias también generan ganancias. Es dinero creando más dinero, sin que hagas nada. Y su efecto en el tiempo es difícil de creer.</p>
<div class="highlight"><div class="q">¿Puedo permitirme NO invertir?</div><p>Netflix y Spotify cuestan juntos $18/mes. Si los pagaras 50 años, gastarías <strong>$10,800</strong> — casi no lo notarías. Pero si invirtieras esos mismos $18/mes al 10% anual, en 50 años tendrías <strong>$300,000</strong>. Cada año que el dinero está quieto es una pérdida <strong>exponencial</strong>, no lineal.</p></div>
<p>Por eso empezar temprano vale más que empezar con más. Dos personas invierten $200/mes al 7%:</p>
<div class="two">
  <div class="box green"><div class="t">Sofía — empieza a los 20</div><p>Aporta 40 años ($96,000). A los 60: <strong>$525,000</strong>.</p></div>
  <div class="box red"><div class="t">Diego — empieza a los 40</div><p>Aporta 20 años ($48,000). A los 60: <strong>$104,000</strong>.</p></div>
</div>
<p>Sofía aportó exactamente el doble que Diego, pero terminó con <strong>cinco veces más</strong>. La diferencia no fue el monto — fue el <strong>tiempo</strong>.</p>
</div>

<div class="sec">
<h2>3. Gasta con intención (sin culpa)</h2>
<p>Un presupuesto no es una lista de restricciones para sufrir — es un <strong>plan para gastar tu dinero en lo que de verdad te importa</strong>. Todo gasto cae en uno de tres tipos:</p>
<ul>
<li><strong>Apariencia:</strong> lo que compras para que otros te vean de cierta forma. Satisfacción momentánea y vacía.</li>
<li><strong>Obligatorio:</strong> lo necesario para vivir. No da alegría, pero es indispensable.</li>
<li><strong>Valor personal:</strong> lo que te hace genuinamente mejor o más feliz. Satisfacción duradera.</li>
</ul>
<p>El objetivo: <strong>minimiza</strong> el de apariencia, <strong>optimiza</strong> el obligatorio y <strong>maximiza</strong> el de valor. Antes de comprar, tres preguntas: ¿Lo compro por mí o por lo que pensarán? ¿Lo valoraré en 6 meses? ¿Me hace <em>mejor</em> o solo me hace <em>ver</em> mejor?</p>
<p>Y el hábito clave: <strong>págate primero a ti mismo.</strong> Aparta un 10% de tus ingresos en transferencia automática el día de cobro — antes de gastar. Lo que no ves, no lo gastas.</p>
</div>

<div class="sec">
<h2>4. La inflación: por qué el dinero quieto pierde</h2>
<p>Con una inflación de 3.5% anual, esos $100 de hoy tendrán el poder de compra de apenas <strong>$50</strong> en 20 años. No perdiste el dinero — perdiste la mitad de su valor.</p>
<div class="formula"><div class="eq" style="font-size:13pt">Retorno real = Retorno nominal − Inflación</div><div class="note">Una cuenta de ahorros al 1.5% con inflación de 3.5% te da <strong>−2% real</strong>. Pierdes, aunque el número no baje.</div></div>
<p>Creer que tu dinero "está seguro" en el banco es una ilusión: está seguro en número, pero pierde valor en lo que puede comprar. <strong>Guardar sin invertir es, técnicamente, perder.</strong></p>
</div>

<div class="sec">
<h2>5. Invertir sin tecnicismos: acciones y ETFs</h2>
<p>Una <strong>acción</strong> es una fracción de propiedad de una empresa. Invertir no es apostar: es <strong>hacerte socio de buenos negocios</strong>. El <em>precio</em> fluctúa a diario con las emociones; el <em>valor</em> es lo que la empresa realmente vale. A corto plazo el mercado es irracional; a largo plazo, muy racional.</p>
<p>Un <strong>ETF</strong> es una canasta de muchas acciones agrupadas en un solo instrumento. Comprando un ETF del S&amp;P 500 (como VOO) inviertes de golpe en las 500 empresas más grandes de EE.UU. — diversificación instantánea.</p>
<div class="callout"><div class="t">El enfoque Core-Satellite</div><p>70-80% en ETFs diversificados (tu base estable) + 20-30% en acciones de alta convicción. Dato clave: el <strong>90% de los fondos gestionados por profesionales no le gana al S&amp;P 500</strong> a largo plazo. La simplicidad gana.</p></div>
</div>

<div class="sec">
<h2>6. Los errores que te frenan</h2>
<div class="err"><span class="x">✕</span><div><strong>Vender en pánico cuando el mercado cae.</strong> Convierte una pérdida temporal en permanente.</div></div>
<div class="err"><span class="x">✕</span><div><strong>Intentar adivinar el momento.</strong> El tiempo <em>en</em> el mercado le gana al tiempo <em>fuera</em>.</div></div>
<div class="err"><span class="x">✕</span><div><strong>Seguir modas y "tips".</strong> Cuando todos hablan de una acción, ya subió. Eso es especular.</div></div>
<div class="err"><span class="x">✕</span><div><strong>Invertir dinero que necesitas pronto.</strong> Solo invierte lo que puedas dejar 3-5 años.</div></div>
<div class="err"><span class="x">✕</span><div><strong>Esperar a "saber suficiente".</strong> El conocimiento perfecto nunca llega. El error más caro es no empezar.</div></div>
</div>

<div class="sec">
<h2>7. Tu primer paso, en el orden correcto</h2>
<p>Antes de invertir un solo dólar, sigue este orden — no lo saltes:</p>
<ol>
<li><strong>Elimina la deuda de alto interés (+15%).</strong> Ninguna inversión le gana al 24% de una tarjeta.</li>
<li><strong>Arma tu fondo de emergencia:</strong> 3 a 6 meses de gastos en cuenta líquida.</li>
<li><strong>Ahora sí: invierte el excedente cada mes.</strong></li>
</ol>
<p>¿Cómo invertir sin estresarte por el "momento perfecto"? Con <strong>DCA</strong>: inviertes una cantidad fija cada mes, sin importar si el mercado está arriba o abajo. Tu costo promedio se optimiza solo. La cantidad de tu primera inversión importa menos que <strong>empezar</strong>.</p>
</div>

<div class="next">
<div class="t">¿Y ahora qué?</div>
<p style="margin:0;font-size:10pt">Esta guía te dio el <strong>qué</strong> y el <strong>por qué</strong>. Usa la plantilla que viene con esta guía para calcular tu tasa de ahorro y tu número. Y cuando quieras el <strong>cómo</strong> — mi estrategia completa y verla en la práctica cada semana — visita <strong>flujocompuesto.com</strong>.</p>
</div>

<p class="disc">Esta guía es contenido educativo e informativo. No constituye asesoría de inversión, financiera ni fiscal personalizada. Invertir conlleva riesgos, incluida la posible pérdida de capital. Toma tus decisiones considerando tu situación particular. © Flujo Compuesto · flujocompuesto.com</p>
"""

BUILD.mkdir(parents=True, exist_ok=True)
html_path = BUILD / "guia.html"
html_path.write_text(
    f"<!doctype html><html lang='es'><head><meta charset='utf-8'><style>{faces}{CSS}</style></head><body>{BODY}</body></html>",
    encoding="utf-8",
)
subprocess.run(
    [CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
     f"--print-to-pdf={OUT}", html_path.as_uri()],
    check=True, capture_output=True,
)
print(f"PDF: {OUT} ({OUT.stat().st_size // 1024} KB)")
