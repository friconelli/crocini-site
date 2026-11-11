#!/usr/bin/env python3
"""Genera il sito statico di Crocini in dist/ (IT + EN). Nessuna dipendenza.

  SITE_URL=https://crocini.app ./build.py     # dominio canonico (ancora da scegliere: vedi PIANO.md)
Ogni "[da completare: …]" rimasto nel testo viene elencato a fine build.
Il download punta sempre all'ultima release di GitHub (nessun file da ospitare qui).
"""
import html, json, os, re, shutil, subprocess
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.environ.get("SITE_URL", "https://crocini.app").rstrip("/")
REPO = "friconelli/crocini"
NAME = "Crocini"
DL = f"https://github.com/{REPO}/releases/latest/download/Crocini.zip"
REL = f"https://github.com/{REPO}/releases/latest"
GH = f"https://github.com/{REPO}"
GK_CMD = 'xattr -dr com.apple.quarantine "/Applications/Crocini.app"'
TODO = "[da completare:"

def latest_version():
    """Versione dell'ultima release (letta con gh se disponibile; altrimenti la pagina non la mostra)."""
    try:
        out = subprocess.run(["gh", "release", "view", "--repo", REPO, "--json", "tagName"],
                             capture_output=True, text=True, timeout=20)
        return json.loads(out.stdout)["tagName"].lstrip("vV") if out.returncode == 0 else None
    except Exception:
        return None
VERSION = os.environ.get("CROCINI_VERSION") or latest_version()

e = html.escape
def emph(s): return re.sub(r"\*(.+?)\*", r"<em>\1</em>", e(s))

# ---------------------------------------------------------------- contenuti
T = {
"it": {
 "lang": "it", "prefix": "", "alt": "en", "alt_label": "EN",
 "title": "Crocini – impagina biglietti da visita, flyer e locandine per il taglio",
 "desc": "App per Mac che dispone biglietti da visita, flyer e locandine sul foglio di stampa con abbondanza e segni di taglio (crocini) e esporta un PDF pronto per la tipografia.",
 "nav": [("#funzioni", "Funzioni"), ("#prova", "Provalo"), ("#domande", "Domande"), ("#scarica", "Scarica")],
 "eyebrow": "App per Mac",
 "h1": "Il foglio, pronto per il *taglio*",
 "lead": "Crocini dispone biglietti da visita, flyer e locandine sul foglio di stampa, aggiunge abbondanza e segni di taglio e ti consegna un PDF pronto per la tipografia o per la ghigliottina.",
 "cta": "Scarica per Mac", "cta2": "Provalo qui",
 "meta": "macOS 13+ · Apple Silicon e Intel · aggiornamenti integrati",
 "steps_h": "Tre passi, un foglio pronto",
 "steps": [
  ("Trascina la grafica", "Un PNG, un JPEG o un PDF: Crocini lo ripete su tutto il foglio e ne legge la misura reale."),
  ("Imposta il foglio", "Scegli un preset o inserisci le misure: foglio, elemento, abbondanza, distanza, crocini."),
  ("Esporta il PDF", "Un PDF vettoriale con i segni di taglio al loro posto, pronto da stampare."),
 ],
 "demo_h": "Prova il calcolo",
 "demo_p": "Cambia le misure e guarda quanti pezzi entrano sul foglio. È lo stesso calcolo dell’app: se girando gli elementi ne entrano di più, li ruota da solo.",
 "demo_presets": [("Biglietto da visita", 85, 55), ("Cartolina", 100, 150), ("Flyer A6", 105, 148), ("Flyer DL", 99, 210), ("Segnalibro", 50, 150)],
 "demo_paper": "Foglio", "demo_item": "Elemento", "demo_w": "Larghezza", "demo_h2": "Altezza", "demo_bleed": "Abbondanza",
 "demo_marks": "Segni di taglio", "demo_none_bleed": "nessuna", "demo_pieces": "pezzi per foglio", "demo_rot": "ruotati", "demo_nofit": "non entra",
 "demo_note": "Margine 10 mm, nessuna distanza tra gli elementi. L’app permette di cambiare tutto.",
 "feat_h": "Cosa fa",
 "feats": [
  ("spark", "Preset pronti", "Nove configurazioni (biglietti da visita, cartoline, flyer, locandine) e i tuoi preset da salvare."),
  ("bleed", "Abbondanza a modo tuo", "Usa quella già nel file, aggiungila con un colore piatto oppure ingrandendo la grafica."),
  ("marks", "Crocini su misura", "Spessore, lunghezza, colore e distanza dal rifilo: decidi tu come devono apparire."),
  ("ruler", "Tutto in millimetri", "Foglio A4, A3, SRA3, Lettera o misure tue; elemento libero; margini e distanze al decimo di millimetro."),
  ("zoom", "Zoom come negli editor grafici", "Rotella, pinch, lente e mano; barra spaziatrice per spostarti. Controlli ogni dettaglio del taglio."),
  ("rotate", "Rotazione automatica", "Se girando gli elementi ne entrano di più sul foglio, Crocini li ruota da solo."),
  ("chip", "Per ogni Mac", "Una sola app per Mac con Apple Silicon e Intel, da macOS 13 in poi."),
  ("update", "Si aggiorna da sola", "Controlla le novità all’avvio e si aggiorna con un clic, senza riscaricare nulla a mano."),
 ],
 "show_h": "Tutto sotto controllo, in una finestra",
 "show_p": "A sinistra le impostazioni, a destra il foglio in tempo reale: cambi un valore e i pezzi si rimettono in ordine davanti a te.",
 "show_alt": "La finestra di Crocini: a sinistra le impostazioni, a destra un foglio A4 con dieci biglietti da visita e i segni di taglio",
 "faq_h": "Domande frequenti",
 "faq": [
  ("Su quali Mac funziona?", "Su tutti i Mac con macOS 13 Ventura o successivo, sia con Apple Silicon sia con processore Intel."),
  ("Quali file posso impaginare?", "PNG, JPEG, TIFF, HEIC, GIF, WebP e PDF. Dai PDF e dalle immagini con i DPI nel file Crocini legge la misura reale e può impostare l’elemento di conseguenza."),
  ("Come si usano i crocini per tagliare?", "I segni stanno sul bordo della griglia, fuori dall’abbondanza: allinea la ghigliottina o il taglierino ai segni opposti e taglia da un lato all’altro del foglio."),
  ("Perché macOS dice che l’app non è verificata?", "Crocini non è ancora notarizzata da Apple. Al primo avvio fai clic destro sull’app e scegli Apri; in alternativa usa il comando che trovi qui sotto, nella sezione Scarica. Serve una volta sola."),
  ("I miei file restano sul mio Mac?", "Sì. Crocini lavora tutto in locale. L’unica connessione è il controllo degli aggiornamenti, che interroga le release su GitHub."),
  ("Posso salvare le mie configurazioni?", "Sì: dopo aver impostato foglio, elemento, abbondanza e crocini puoi salvare tutto come preset e richiamarlo con un clic."),
 ],
 "dl_h": "Scarica Crocini",
 "dl_p": "Il download è un file zip: aprilo e trascina Crocini nella cartella Applicazioni.",
 "dl_btn": "Scarica per Mac", "dl_gh": "Vedi su GitHub", "dl_ver": "Versione", "dl_req": "macOS 13+ · Apple Silicon e Intel",
 "dl_first_h": "Al primo avvio",
 "dl_first": [
  "Apri lo zip e trascina Crocini nella cartella Applicazioni.",
  "Fai clic destro su Crocini e scegli Apri (macOS chiede conferma una sola volta).",
  "Oppure da Terminale, un comando solo:",
 ],
 "copy": "Copia", "copied": "Copiato",
 "dl_upd": "Dopo il primo avvio non devi più preoccuparti: Crocini controlla gli aggiornamenti e li installa con un clic.",
 "foot_priv": "Il sito non usa cookie né strumenti di statistica. L’app lavora in locale e si collega solo per cercare aggiornamenti.",
 "foot_font": "Carattere: Bricolage Grotesque (SIL Open Font License).",
 "foot_code": "Codice e release su GitHub",
 "skip": "Vai al contenuto", "nf_t": "Pagina non trovata", "nf_p": "Questa pagina non esiste.", "nf_b": "Torna alla home",
 "faq_ld_name": "Domande frequenti su Crocini",
},
"en": {
 "lang": "en", "prefix": "en/", "alt": "it", "alt_label": "IT",
 "title": "Crocini – lay out business cards, flyers and posters for cutting",
 "desc": "Mac app that arranges business cards, flyers and posters on the print sheet with bleed and crop marks, and exports a print-ready PDF.",
 "nav": [("#features", "Features"), ("#try", "Try it"), ("#faq", "FAQ"), ("#download", "Download")],
 "eyebrow": "Mac app",
 "h1": "The sheet, ready for the *cut*",
 "lead": "Crocini arranges business cards, flyers and posters on the print sheet, adds bleed and crop marks and hands you a PDF ready for the print shop or the guillotine.",
 "cta": "Download for Mac", "cta2": "Try it here",
 "meta": "macOS 13+ · Apple Silicon and Intel · built-in updates",
 "steps_h": "Three steps, one sheet ready",
 "steps": [
  ("Drop your artwork", "A PNG, a JPEG or a PDF: Crocini repeats it over the whole sheet and reads its real size."),
  ("Set up the sheet", "Pick a preset or type your sizes: sheet, item, bleed, spacing, crop marks."),
  ("Export the PDF", "A vector PDF with the crop marks right where they belong, ready to print."),
 ],
 "demo_h": "Try the maths",
 "demo_p": "Change the sizes and see how many pieces fit on the sheet. It is the same calculation as the app: if turning the items fits more, it rotates them for you.",
 "demo_presets": [("Business card", 85, 55), ("Postcard", 100, 150), ("A6 flyer", 105, 148), ("DL flyer", 99, 210), ("Bookmark", 50, 150)],
 "demo_paper": "Sheet", "demo_item": "Item", "demo_w": "Width", "demo_h2": "Height", "demo_bleed": "Bleed",
 "demo_marks": "Crop marks", "demo_none_bleed": "none", "demo_pieces": "pieces per sheet", "demo_rot": "rotated", "demo_nofit": "does not fit",
 "demo_note": "10 mm margin, no spacing between items. In the app you can change everything.",
 "feat_h": "What it does",
 "feats": [
  ("spark", "Ready-made presets", "Nine setups (business cards, postcards, flyers, posters) plus your own saved presets."),
  ("bleed", "Bleed, your way", "Use the bleed already in the file, add it with a flat colour or by enlarging the artwork."),
  ("marks", "Custom crop marks", "Thickness, length, colour and distance from the trim: you decide how they look."),
  ("ruler", "Everything in millimetres", "A4, A3, SRA3, Letter or your own sheet; free item size; margins and spacing to a tenth of a millimetre."),
  ("zoom", "Zoom like design editors", "Wheel, pinch, lens and hand; space bar to pan. Check every detail of the cut."),
  ("rotate", "Automatic rotation", "If turning the items fits more on the sheet, Crocini rotates them for you."),
  ("chip", "For every Mac", "One app for Apple Silicon and Intel Macs, from macOS 13 on."),
  ("update", "Updates itself", "It checks for news at launch and updates with one click, no manual re-download."),
 ],
 "show_h": "Everything under control, in one window",
 "show_p": "Settings on the left, the live sheet on the right: change a value and the pieces rearrange right in front of you.",
 "show_alt": "The Crocini window: settings on the left, an A4 sheet with ten business cards and crop marks on the right",
 "faq_h": "Frequently asked questions",
 "faq": [
  ("Which Macs does it run on?", "Any Mac running macOS 13 Ventura or later, both Apple Silicon and Intel."),
  ("Which files can I lay out?", "PNG, JPEG, TIFF, HEIC, GIF, WebP and PDF. From PDFs and from images that carry DPI, Crocini reads the real size and can set the item accordingly."),
  ("How do I cut with the crop marks?", "The marks sit on the edge of the grid, outside the bleed: line up the guillotine or the knife with the opposite marks and cut from one side of the sheet to the other."),
  ("Why does macOS say the app is not verified?", "Crocini is not notarised by Apple yet. On first launch right-click the app and choose Open; or use the command in the Download section below. You only need to do it once."),
  ("Do my files stay on my Mac?", "Yes. Crocini works entirely locally. The only connection is the update check, which asks GitHub for the latest release."),
  ("Can I save my setups?", "Yes: once sheet, item, bleed and crop marks are set you can save everything as a preset and recall it with one click."),
 ],
 "dl_h": "Download Crocini",
 "dl_p": "The download is a zip file: open it and drag Crocini into your Applications folder.",
 "dl_btn": "Download for Mac", "dl_gh": "View on GitHub", "dl_ver": "Version", "dl_req": "macOS 13+ · Apple Silicon and Intel",
 "dl_first_h": "On first launch",
 "dl_first": [
  "Open the zip and drag Crocini into Applications.",
  "Right-click Crocini and choose Open (macOS asks for confirmation just once).",
  "Or from Terminal, a single command:",
 ],
 "copy": "Copy", "copied": "Copied",
 "dl_upd": "After the first launch there is nothing more to do: Crocini checks for updates and installs them with one click.",
 "foot_priv": "This site uses no cookies and no analytics. The app works locally and only connects to look for updates.",
 "foot_font": "Typeface: Bricolage Grotesque (SIL Open Font License).",
 "foot_code": "Code and releases on GitHub",
 "skip": "Skip to content", "nf_t": "Page not found", "nf_p": "This page does not exist.", "nf_b": "Back to home",
 "faq_ld_name": "Crocini frequently asked questions",
},
}
IDS = {"it": ["funzioni", "prova", "domande", "scarica"], "en": ["features", "try", "faq", "download"]}

# ---------------------------------------------------------------- immagini vettoriali
ICONS = {
 "spark": '<path d="M12 3l1.9 5.6L19.5 10l-5.6 1.9L12 17.5l-1.9-5.6L4.5 10l5.6-1.4z"/><path d="M19 16v4M17 18h4"/>',
 "bleed": '<rect x="7" y="7" width="10" height="10" rx="1"/><rect x="3.5" y="3.5" width="17" height="17" rx="1.5" stroke-dasharray="2.2 2"/>',
 "marks": '<path d="M8 3v4M3 8h4M16 3v4M21 8h-4M8 21v-4M3 16h4M16 21v-4M21 16h-4"/><rect x="9" y="9" width="6" height="6" rx=".6"/>',
 "ruler": '<rect x="3" y="8" width="18" height="8" rx="1.5"/><path d="M7 8v3M11 8v4M15 8v3M19 8v4"/>',
 "zoom": '<circle cx="10.5" cy="10.5" r="6"/><path d="M15 15l5.5 5.5M8 10.5h5M10.5 8v5"/>',
 "rotate": '<path d="M20 11a8 8 0 10-2.3 5.7"/><path d="M20 4v7h-7"/>',
 "chip": '<rect x="6.5" y="6.5" width="11" height="11" rx="2"/><rect x="9.5" y="9.5" width="5" height="5" rx=".8"/><path d="M9 3v3M15 3v3M9 18v3M15 18v3M3 9h3M3 15h3M18 9h3M18 15h3"/>',
 "update": '<path d="M12 4v10M8 10.5l4 4 4-4"/><path d="M5 17v2.5A1.5 1.5 0 006.5 21h11a1.5 1.5 0 001.5-1.5V17"/>',
}
def icon(name): return f'<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>'

LOGO = ('<svg class="logo" viewBox="0 0 44 44" aria-hidden="true"><defs><linearGradient id="lg" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0" stop-color="#FF5C9E"/><stop offset=".5" stop-color="#EE2177"/><stop offset="1" stop-color="#BD0A5C"/></linearGradient></defs>'
        '<rect width="44" height="44" rx="11" fill="url(#lg)"/><rect x="11" y="15" width="22" height="14" rx="2.6" fill="#fff"/>'
        '<path d="M7 14V7h7M30 7h7v7M7 30v7h7M30 37h7v-7" fill="none" stroke="#111" stroke-width="3" stroke-linecap="square"/></svg>')

def hero_sheet():
    """Foglio A4 (2 px per mm) con 2×5 biglietti che entrano uno dopo l'altro, poi i crocini che si disegnano."""
    W, H, cw, ch = 420, 594, 170, 110
    x0, y0 = (W - 2 * cw) // 2, (H - 5 * ch) // 2
    cards = []
    for i in range(10):
        c, r = i % 2, i // 2
        x, y = x0 + c * cw, y0 + r * ch
        cards.append(f'<svg class="hc" style="--i:{i}" x="{x}" y="{y}" width="{cw}" height="{ch}" viewBox="0 0 {cw} {ch}" overflow="hidden">'
                     f'<image href="/img/card.webp" x="-6" y="-6" width="{cw+12}" height="{ch+12}" preserveAspectRatio="none"/></svg>')
    off, ln = 6, 9
    d = ""
    for c in range(3):
        x = x0 + c * cw
        d += f"M{x} {y0-off}V{y0-off-ln}M{x} {y0+5*ch+off}V{y0+5*ch+off+ln}"
    for r in range(6):
        y = y0 + r * ch
        d += f"M{x0-off} {y}H{x0-off-ln}M{x0+2*cw+off} {y}H{x0+2*cw+off+ln}"
    return (f'<svg class="sheet" viewBox="0 0 {W} {H}" role="img" aria-label="">'
            f'<rect width="{W}" height="{H}" rx="3" fill="#fff"/>{"".join(cards)}'
            f'<path class="hm" d="{d}" fill="none" stroke="#111" stroke-width="1.4" pathLength="100"/></svg>')

# ---------------------------------------------------------------- stile
CSS = """
@font-face{font-family:"Bricolage Grotesque";src:url(/fonts/bricolage.woff2) format("woff2");font-weight:300 800;font-style:normal;font-display:swap}
:root{--m:#EE2177;--m2:#BD0A5C;--m3:#FF5C9E;--c:#00ADEE;--ink:#1B1118;--ink2:#5B4B55;--paper:#FFF8F5;--card:#fff;--line:rgba(27,17,24,.12);--soft:rgba(238,33,119,.09);--sh:0 18px 50px -20px rgba(120,10,60,.35);--r:22px;color-scheme:light}
@media (prefers-color-scheme:dark){:root{--ink:#F8EEF2;--ink2:#BDA9B4;--paper:#150F17;--card:#221825;--line:rgba(248,238,242,.14);--soft:rgba(255,92,158,.13);--sh:0 18px 50px -20px rgba(0,0,0,.7);color-scheme:dark}}
*{box-sizing:border-box}html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
body{margin:0;background:var(--paper);color:var(--ink);font:400 17px/1.6 "Bricolage Grotesque",system-ui,-apple-system,"Segoe UI",sans-serif;overflow-x:hidden}
img,svg{max-width:100%}a{color:inherit}
.wrap{width:min(1120px,100% - 40px);margin-inline:auto}
.skip{position:absolute;left:-999px;top:8px;background:var(--m);color:#fff;padding:8px 14px;border-radius:10px;z-index:99}.skip:focus{left:8px}
em{font-style:normal;color:var(--m);position:relative;white-space:nowrap}
em::after{content:"";position:absolute;left:-2%;right:-2%;bottom:.04em;height:.14em;background:var(--m);opacity:.22;border-radius:4px;transform:scaleX(0);transform-origin:left;animation:ul .9s .5s cubic-bezier(.2,.8,.2,1) forwards}
@keyframes ul{to{transform:scaleX(1)}}
/* intestazione */
.top{position:sticky;top:0;z-index:20;background:color-mix(in srgb,var(--paper) 82%,transparent);backdrop-filter:saturate(1.4) blur(14px);-webkit-backdrop-filter:saturate(1.4) blur(14px);transition:box-shadow .25s}
.top.scrolled{box-shadow:0 1px 0 var(--line),0 10px 30px -22px rgba(0,0,0,.5)}
.top .wrap{display:flex;align-items:center;gap:22px;height:68px}
.brand{display:flex;align-items:center;gap:11px;text-decoration:none;font-weight:800;font-size:22px;letter-spacing:-.02em}
.brand .logo{width:36px;height:36px;filter:drop-shadow(0 4px 8px rgba(238,33,119,.35));transition:transform .4s cubic-bezier(.3,1.6,.5,1)}.brand:hover .logo{transform:rotate(-8deg) scale(1.08)}
nav{display:flex;gap:4px;margin-left:auto}
nav a{text-decoration:none;font-weight:500;font-size:15px;padding:8px 13px;border-radius:99px;color:var(--ink2);transition:background .2s,color .2s}nav a:hover{background:var(--soft);color:var(--m)}
.lang{font-weight:700;font-size:13px;text-decoration:none;padding:6px 11px;border:1.5px solid var(--line);border-radius:99px;color:var(--ink2)}.lang:hover{border-color:var(--m);color:var(--m)}
.btn{display:inline-flex;align-items:center;gap:9px;text-decoration:none;font-weight:700;font-size:16px;padding:13px 24px;border-radius:99px;border:0;cursor:pointer;color:#fff;background:linear-gradient(135deg,var(--m3),var(--m) 55%,var(--m2));box-shadow:0 10px 26px -10px rgba(238,33,119,.8);transition:transform .25s cubic-bezier(.3,1.5,.5,1),box-shadow .25s}
.btn:hover{transform:translateY(-2px) scale(1.03);box-shadow:0 16px 34px -10px rgba(238,33,119,.9)}.btn:active{transform:scale(.97)}
.btn.ghost{background:transparent;color:var(--m);box-shadow:inset 0 0 0 2px var(--m)}.btn.ghost:hover{background:var(--soft)}
.btn.sm{padding:9px 18px;font-size:14.5px}
.top .btn{margin-left:4px}
.apple{width:18px;height:18px}
/* hero */
.hero{position:relative;padding:56px 0 84px;background:
 radial-gradient(60% 50% at 82% 20%,var(--soft),transparent 70%),
 url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='44' height='44'%3E%3Cpath d='M22 18v8M18 22h8' stroke='%23EE2177' stroke-opacity='.16' stroke-width='1.2'/%3E%3C/svg%3E")}
.hero .wrap{display:grid;grid-template-columns:1.05fr .95fr;gap:48px;align-items:center}
.eyebrow{display:inline-flex;align-items:center;gap:8px;font-weight:700;font-size:13.5px;letter-spacing:.09em;text-transform:uppercase;color:var(--m);background:var(--soft);padding:7px 14px;border-radius:99px}
.eyebrow::before{content:"";width:8px;height:8px;border-radius:50%;background:var(--m);animation:pulse 2s infinite}
@keyframes pulse{50%{transform:scale(1.7);opacity:.35}}
h1{font-size:clamp(40px,6.4vw,76px);line-height:1.02;letter-spacing:-.035em;margin:22px 0 20px;font-weight:800}
.lead{font-size:clamp(18px,2vw,21px);color:var(--ink2);max-width:34em;margin:0 0 30px}
.cta{display:flex;flex-wrap:wrap;gap:14px;align-items:center}
.meta{margin:20px 0 0;font-size:14.5px;color:var(--ink2)}
.sheetwrap{position:relative;justify-self:center;width:min(100%,430px);animation:float 7s ease-in-out infinite}
@keyframes float{50%{transform:translateY(-10px) rotate(.6deg)}}
.sheet{display:block;width:100%;height:auto;filter:drop-shadow(0 30px 40px rgba(120,10,60,.28)) drop-shadow(0 6px 10px rgba(0,0,0,.12));border-radius:3px;transform:rotate(-2.5deg)}
.hc{opacity:0;transform-box:fill-box;transform-origin:center;animation:pop .7s cubic-bezier(.2,1.2,.3,1) forwards;animation-delay:calc(var(--i)*75ms + .35s)}
@keyframes pop{from{opacity:0;transform:scale(.8)}to{opacity:1;transform:none}}
.hm{stroke-dasharray:100;stroke-dashoffset:100;animation:draw 1.1s 1.4s ease-out forwards}
@keyframes draw{to{stroke-dashoffset:0}}
/* sezioni */
section{padding:92px 0;position:relative}
h2{font-size:clamp(30px,4.2vw,50px);line-height:1.06;letter-spacing:-.03em;margin:0 0 14px;font-weight:800}
.sub{color:var(--ink2);max-width:40em;margin:0 0 44px;font-size:18px}
.rv{opacity:0;transform:translateY(22px);transition:opacity .7s cubic-bezier(.2,.8,.2,1),transform .7s cubic-bezier(.2,.8,.2,1);transition-delay:calc(var(--d,0)*90ms)}
html:not(.js) .rv,.rv.in{opacity:1;transform:none}
.steps{display:grid;grid-template-columns:repeat(3,1fr);gap:22px;counter-reset:s}
.step{background:var(--card);border:1px solid var(--line);border-radius:var(--r);padding:30px 28px;box-shadow:var(--sh);position:relative;overflow:hidden}
.step::before{counter-increment:s;content:counter(s);position:absolute;right:-6px;top:-30px;font-size:150px;font-weight:800;color:var(--m);opacity:.09;line-height:1}
.step h3{margin:0 0 8px;font-size:23px;letter-spacing:-.02em}.step p{margin:0;color:var(--ink2)}
/* demo */
.demo-sec{background:linear-gradient(180deg,transparent,var(--soft) 18%,var(--soft) 82%,transparent)}
.demo{display:grid;grid-template-columns:340px 1fr;gap:34px;align-items:start;background:var(--card);border:1px solid var(--line);border-radius:28px;padding:28px;box-shadow:var(--sh)}
.ctl h3{margin:20px 0 9px;font-size:13px;letter-spacing:.09em;text-transform:uppercase;color:var(--ink2)}.ctl h3:first-child{margin-top:0}
.chips{display:flex;flex-wrap:wrap;gap:8px}
.chip{font:600 14px/1 inherit;font-family:inherit;color:var(--m);background:var(--soft);border:1.5px solid transparent;border-radius:99px;padding:9px 13px;cursor:pointer;transition:transform .2s cubic-bezier(.3,1.6,.5,1),background .2s}
.chip:hover{transform:translateY(-2px)}.chip[aria-pressed=true]{background:var(--m);color:#fff}
.row{display:flex;gap:10px;align-items:center}
.fld{display:flex;flex-direction:column;gap:5px;flex:1;font-size:13px;color:var(--ink2)}
.fld input,.fld select{font:600 16px inherit;font-family:inherit;color:var(--ink);background:var(--paper);border:1.5px solid var(--line);border-radius:12px;padding:10px 12px;width:100%;outline:0;transition:border-color .2s,box-shadow .2s}
.fld input:focus,.fld select:focus{border-color:var(--m);box-shadow:0 0 0 4px var(--soft)}
.chk{display:flex;gap:10px;align-items:center;margin-top:14px;font-weight:500;cursor:pointer}.chk input{accent-color:var(--m);width:19px;height:19px}
.stage{display:grid;place-items:center;gap:18px;padding:10px}
#sheet{width:auto;height:min(62vh,560px);max-width:100%;border-radius:3px;box-shadow:0 26px 46px -22px rgba(120,10,60,.5),0 0 0 1px var(--line);background:#fff;overflow:visible}
.pop{animation:pop2 .5s cubic-bezier(.2,1.2,.3,1) backwards;animation-delay:calc(var(--i)*30ms);transform-box:fill-box;transform-origin:center}
@keyframes pop2{from{opacity:0;transform:scale(.85)}}
.count{display:flex;gap:12px;align-items:baseline;flex-wrap:wrap;justify-content:center;font-weight:600;color:var(--ink2)}
.count b{font-size:56px;line-height:1;font-weight:800;color:var(--m);letter-spacing:-.04em;font-variant-numeric:tabular-nums}.count.none b{color:var(--ink2)}
.count small{font-size:14px;background:var(--soft);color:var(--m);padding:5px 11px;border-radius:99px;font-weight:700}
.note{font-size:13.5px;color:var(--ink2);margin:18px 0 0}
/* funzioni */
.feats{display:grid;grid-template-columns:repeat(4,1fr);gap:18px}
.feat{background:var(--card);border:1px solid var(--line);border-radius:20px;padding:24px 22px;transition:transform .35s cubic-bezier(.3,1.4,.5,1),box-shadow .35s,border-color .35s}
.feat:hover{transform:translateY(-6px) rotate(-.4deg);box-shadow:var(--sh);border-color:color-mix(in srgb,var(--m) 45%,transparent)}
.ic{width:46px;height:46px;padding:11px;border-radius:14px;color:#fff;background:linear-gradient(135deg,var(--m3),var(--m2));margin-bottom:16px;box-shadow:0 8px 18px -8px rgba(238,33,119,.8)}
.feat h3{margin:0 0 6px;font-size:19px;letter-spacing:-.015em;line-height:1.2}.feat p{margin:0;color:var(--ink2);font-size:15.5px;line-height:1.5}
/* finestra */
.win{margin-top:8px;border-radius:16px;overflow:hidden;background:var(--card);box-shadow:0 40px 80px -30px rgba(120,10,60,.5),0 0 0 1px var(--line)}
.win .bar{display:flex;gap:8px;padding:13px 16px;background:linear-gradient(var(--card),color-mix(in srgb,var(--card) 92%,#888))}
.win .bar i{width:12px;height:12px;border-radius:50%;background:#FF5F57}.win .bar i:nth-child(2){background:#FEBC2E}.win .bar i:nth-child(3){background:#28C840}
.win img{display:block;width:100%;height:auto}
/* faq */
.faq{max-width:820px}
details{background:var(--card);border:1px solid var(--line);border-radius:18px;margin-bottom:12px;transition:border-color .25s,box-shadow .25s}
details[open]{border-color:color-mix(in srgb,var(--m) 50%,transparent);box-shadow:var(--sh)}
summary{cursor:pointer;list-style:none;padding:20px 56px 20px 24px;font-weight:700;font-size:18px;position:relative;letter-spacing:-.01em}
summary::-webkit-details-marker{display:none}
summary::after{content:"+";position:absolute;right:22px;top:50%;translate:0 -52%;font-size:28px;font-weight:400;color:var(--m);transition:transform .3s}
details[open] summary::after{transform:rotate(45deg)}
details p{margin:0;padding:0 24px 22px;color:var(--ink2)}
/* download */
.dl{background:linear-gradient(135deg,#EE2177,#BD0A5C 70%);color:#fff;border-radius:34px;padding:64px 56px 78px;position:relative;overflow:hidden;box-shadow:0 40px 80px -30px rgba(190,10,90,.75)}
.dl::before{content:"";position:absolute;inset:18px;border:2px solid rgba(255,255,255,.35);border-radius:22px;pointer-events:none;mask:linear-gradient(#000,#000) top left/60px 60px no-repeat,linear-gradient(#000,#000) top right/60px 60px no-repeat,linear-gradient(#000,#000) bottom left/60px 60px no-repeat,linear-gradient(#000,#000) bottom right/60px 60px no-repeat;-webkit-mask:linear-gradient(#000,#000) top left/60px 60px no-repeat,linear-gradient(#000,#000) top right/60px 60px no-repeat,linear-gradient(#000,#000) bottom left/60px 60px no-repeat,linear-gradient(#000,#000) bottom right/60px 60px no-repeat}
.dl h2{color:#fff}.dl .sub{color:rgba(255,255,255,.9);margin-bottom:26px}
.dl .btn{background:#fff;color:var(--m2);box-shadow:0 14px 30px -12px rgba(0,0,0,.5)}.dl .btn.ghost{background:transparent;color:#fff;box-shadow:inset 0 0 0 2px rgba(255,255,255,.8)}.dl .btn.ghost:hover{background:rgba(255,255,255,.14)}
.dl .meta{color:rgba(255,255,255,.88)}
.first{margin-top:38px;padding-top:30px;border-top:1px solid rgba(255,255,255,.3)}
.first h3{margin:0 0 12px;font-size:19px}.first ol{margin:0;padding-left:22px;display:grid;gap:8px;max-width:640px}
code{display:block;font:500 14px/1.5 ui-monospace,SFMono-Regular,Menlo,monospace;background:rgba(0,0,0,.28);padding:13px 16px;border-radius:12px;margin-top:8px;word-break:break-all;user-select:all}
.cp{margin-top:10px;font:700 14px inherit;font-family:inherit;background:rgba(255,255,255,.2);color:#fff;border:0;border-radius:99px;padding:8px 16px;cursor:pointer;transition:background .2s}.cp:hover{background:rgba(255,255,255,.32)}.cp.ok{background:#fff;color:var(--m2)}
.upd{margin:26px 0 0;color:rgba(255,255,255,.92);max-width:640px}
footer{padding:44px 0 60px;color:var(--ink2);font-size:14.5px}
footer .wrap{display:grid;gap:8px}footer a{color:var(--m);text-decoration:none;font-weight:600}footer a:hover{text-decoration:underline}
.nf{min-height:70vh;display:grid;place-items:center;text-align:center;padding:40px 0}
@media (max-width:960px){.hero .wrap{grid-template-columns:1fr}.sheetwrap{width:min(78%,360px)}.feats{grid-template-columns:repeat(2,1fr)}.demo{grid-template-columns:1fr}.steps{grid-template-columns:1fr}nav{display:none}.top .wrap{gap:12px}.top .btn.sm{margin-left:auto}}
@media (max-width:560px){.feats{grid-template-columns:1fr}section{padding:64px 0}.dl{padding:38px 26px;border-radius:26px}.top .btn.sm{display:none}.lang{margin-left:auto}.demo{padding:18px;border-radius:22px}}
@media (prefers-reduced-motion:reduce){*,*::before,*::after{animation:none!important;transition:none!important;scroll-behavior:auto!important}.hc,.hm{opacity:1;stroke-dashoffset:0}em::after{transform:none}}
"""

# ---------------------------------------------------------------- pagine
def url(p): return f"{SITE}/{p}"
def head(t, title, desc, path, alt_path, ld, noindex=False):
    lang = t["lang"]
    og = f"{SITE}/og-crocini{'-en' if lang == 'en' else ''}.png"
    hl = "" if noindex else (f'<link rel="canonical" href="{url(path)}">'
         f'<link rel="alternate" hreflang="{lang}" href="{url(path)}"><link rel="alternate" hreflang="{t["alt"]}" href="{url(alt_path)}">'
         f'<link rel="alternate" hreflang="x-default" href="{url(T["it"]["prefix"] + "")}">')
    return (f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{e(title)}</title><meta name="description" content="{e(desc)}">'
            + ('<meta name="robots" content="noindex">' if noindex else "") + hl +
            f'<meta name="theme-color" content="#EE2177"><link rel="icon" href="/favicon.ico" sizes="48x48"><link rel="icon" type="image/png" sizes="192x192" href="/favicon-192.png"><link rel="apple-touch-icon" href="/apple-touch-icon.png">'
            f'<meta property="og:type" content="website"><meta property="og:site_name" content="{NAME}"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}">'
            f'<meta property="og:url" content="{url(path)}"><meta property="og:image" content="{og}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">'
            f'<meta name="twitter:card" content="summary_large_image">'
            f'<link rel="preload" href="/fonts/bricolage.woff2" as="font" type="font/woff2" crossorigin><script src="/js/boot.js"></script><style>{CSS}</style>'
            + "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld) + "</head>")

APPLE = '<svg class="apple" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12.152 6.896c-.948 0-2.415-1.078-3.96-1.04-2.04.027-3.91 1.183-4.961 3.014-2.117 3.675-.546 9.103 1.519 12.09 1.013 1.454 2.208 3.09 3.792 3.039 1.52-.065 2.09-.987 3.935-.987 1.831 0 2.35.987 3.96.948 1.637-.026 2.676-1.48 3.676-2.948 1.156-1.688 1.636-3.325 1.662-3.415-.039-.013-3.182-1.221-3.22-4.857-.026-3.04 2.48-4.494 2.597-4.559-1.429-2.09-3.623-2.324-4.39-2.376-2-.156-3.675 1.09-4.61 1.09zM15.53 3.83c.843-1.012 1.4-2.427 1.245-3.83-1.207.052-2.662.805-3.532 1.818-.78.896-1.454 2.338-1.273 3.714 1.338.104 2.715-.688 3.559-1.701"/></svg>'

def home(lang):
    t = T[lang]; ids = IDS[lang]; P = "/" + t["prefix"]
    ver = f'<p class="meta">{e(t["dl_ver"])} {e(VERSION)} · {e(t["dl_req"])}</p>' if VERSION else f'<p class="meta">{e(t["dl_req"])}</p>'
    nav = "".join(f'<a href="{h}">{e(l)}</a>' for h, l in t["nav"])
    alt_path = T[t["alt"]]["prefix"]
    feats = "".join(f'<div class="feat rv" style="--d:{i%4}">{icon(k)}<h3>{e(h)}</h3><p>{e(p)}</p></div>' for i, (k, h, p) in enumerate(t["feats"]))
    steps = "".join(f'<div class="step rv" style="--d:{i}"><h3>{e(h)}</h3><p>{e(p)}</p></div>' for i, (h, p) in enumerate(t["steps"]))
    faq = "".join(f'<details class="rv"><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in t["faq"])
    chips = "".join(f'<button class="chip" type="button" data-w="{w}" data-h="{h}" aria-pressed="{"true" if i == 0 else "false"}">{e(n)} {w}×{h}</button>' for i, (n, w, h) in enumerate(t["demo_presets"]))
    body = f'''<body><a class="skip" href="#main">{e(t["skip"])}</a>
<header class="top"><div class="wrap"><a class="brand" href="{P}" aria-label="{NAME}">{LOGO}<span>{NAME}</span></a><nav>{nav}</nav>
<a class="lang" href="/{alt_path}" hreflang="{t["alt"]}">{t["alt_label"]}</a><a class="btn sm" href="{DL}">{e(t["cta"])}</a></div></header>
<main id="main">
<section class="hero"><div class="wrap"><div>
<span class="eyebrow">{e(t["eyebrow"])}</span><h1>{emph(t["h1"])}</h1><p class="lead">{e(t["lead"])}</p>
<div class="cta"><a class="btn" href="{DL}">{APPLE}{e(t["cta"])}</a><a class="btn ghost" href="#{ids[1]}">{e(t["cta2"])}</a></div>
<p class="meta">{e(t["meta"])}</p></div>
<div class="sheetwrap">{hero_sheet()}</div></div></section>

<section><div class="wrap"><h2 class="rv">{e(t["steps_h"])}</h2><div class="steps" style="margin-top:36px">{steps}</div></div></section>

<section class="demo-sec" id="{ids[1]}"><div class="wrap"><h2 class="rv">{e(t["demo_h"])}</h2><p class="sub rv">{e(t["demo_p"])}</p>
<div class="demo rv"><div class="ctl">
<h3>{e(t["demo_paper"])}</h3><div class="chips"><button class="chip" type="button" data-paper="210x297" aria-pressed="true">A4</button><button class="chip" type="button" data-paper="297x420" aria-pressed="false">A3</button></div>
<h3>{e(t["demo_item"])}</h3><div class="chips">{chips}</div>
<div class="row" style="margin-top:12px"><label class="fld">{e(t["demo_w"])} (mm)<input id="demo-w" type="number" inputmode="decimal" min="1" max="420" step="0.5" value="85"></label>
<label class="fld">{e(t["demo_h2"])} (mm)<input id="demo-h" type="number" inputmode="decimal" min="1" max="420" step="0.5" value="55"></label></div>
<h3>{e(t["demo_bleed"])}</h3><label class="fld"><select id="demo-bleed"><option value="0">{e(t["demo_none_bleed"])}</option><option value="2">2 mm</option><option value="3" selected>3 mm</option><option value="5">5 mm</option></select></label>
<label class="chk"><input id="demo-marks" type="checkbox" checked> {e(t["demo_marks"])}</label>
<p class="note">{e(t["demo_note"])}</p></div>
<div class="stage"><svg id="sheet" data-img="/img/card.webp" role="img" aria-label="{e(t["demo_h"])}"></svg>
<div class="count"><b id="demo-n">10</b><span>{e(t["demo_pieces"])}</span><small id="demo-grid" data-rot="{e(t["demo_rot"])}" data-none="{e(t["demo_nofit"])}">2 × 5</small></div></div></div></div></section>

<section id="{ids[0]}"><div class="wrap"><h2 class="rv">{e(t["feat_h"])}</h2><div class="feats" style="margin-top:36px">{feats}</div></div></section>

<section><div class="wrap"><h2 class="rv">{e(t["show_h"])}</h2><p class="sub rv">{e(t["show_p"])}</p>
<div class="win rv"><div class="bar"><i></i><i></i><i></i></div><img src="/img/app.webp" width="1800" height="1231" alt="{e(t["show_alt"])}" loading="lazy" decoding="async"></div></div></section>

<section id="{ids[2]}"><div class="wrap faq"><h2 class="rv">{e(t["faq_h"])}</h2><div style="margin-top:30px">{faq}</div></div></section>

<section id="{ids[3]}"><div class="wrap"><div class="dl rv"><h2>{e(t["dl_h"])}</h2><p class="sub">{e(t["dl_p"])}</p>
<div class="cta"><a class="btn" href="{DL}">{APPLE}{e(t["dl_btn"])}</a><a class="btn ghost" href="{GH}">{e(t["dl_gh"])}</a></div>{ver}
<div class="first"><h3>{e(t["dl_first_h"])}</h3><ol><li>{e(t["dl_first"][0])}</li><li>{e(t["dl_first"][1])}</li><li>{e(t["dl_first"][2])}<code>{e(GK_CMD)}</code>
<button class="cp" type="button" data-copy="{e(GK_CMD)}" data-done="{e(t["copied"])}">{e(t["copy"])}</button></li></ol></div>
<p class="upd">{e(t["dl_upd"])}</p></div></div></section>
</main>
<footer><div class="wrap"><div>{e(t["foot_priv"])}</div><div>{e(t["foot_font"])} · <a href="{GH}">{e(t["foot_code"])}</a></div></div></footer>
<script src="/js/site.js" defer></script></body></html>'''
    ld = [
     {"@context": "https://schema.org", "@type": "SoftwareApplication", "name": NAME, "operatingSystem": "macOS 13+",
      "applicationCategory": "DesignApplication", "description": t["desc"], "url": url(t["prefix"]), "downloadUrl": DL,
      "inLanguage": t["lang"], **({"softwareVersion": VERSION} if VERSION else {}), "image": url("og-crocini.png"),
      "offers": None},
     {"@context": "https://schema.org", "@type": "WebSite", "name": NAME, "url": SITE + "/", "inLanguage": ["it", "en"]},
     {"@context": "https://schema.org", "@type": "FAQPage", "name": t["faq_ld_name"],
      "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in t["faq"]]},
    ]
    ld[0].pop("offers")
    return head(t, t["title"], t["desc"], t["prefix"], alt_path, ld) + body

def not_found():
    t = T["it"]
    return (head(t, f'{t["nf_t"]} – {NAME}', t["nf_p"], "404.html", "en/", [], noindex=True) +
            f'<body><main class="wrap nf"><div><a class="brand" href="/" style="justify-content:center;margin-bottom:24px">{LOGO}<span>{NAME}</span></a>'
            f'<h1 style="font-size:48px">{e(t["nf_t"])}</h1><p class="lead" style="margin-inline:auto">{e(t["nf_p"])}</p><a class="btn" href="/">{e(t["nf_b"])}</a></div></main></body></html>')

# ---------------------------------------------------------------- scrittura
def write(rel, content):
    p = os.path.join(HERE, "dist", rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(content)

def main():
    dist = os.path.join(HERE, "dist")
    shutil.rmtree(dist, ignore_errors=True); os.makedirs(dist)
    src = os.path.join(HERE, "src")
    for name in os.listdir(src):
        s, d = os.path.join(src, name), os.path.join(dist, name)
        shutil.copytree(s, d) if os.path.isdir(s) else shutil.copy2(s, d)
    pages = {"index.html": home("it"), "en/index.html": home("en"), "404.html": not_found()}
    for rel, content in pages.items(): write(rel, content)
    today = date.today().isoformat()
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">'
          + "".join(f'<url><loc>{url(p)}</loc><lastmod>{today}</lastmod><xhtml:link rel="alternate" hreflang="it" href="{url("")}"/><xhtml:link rel="alternate" hreflang="en" href="{url("en/")}"/></url>' for p in ("", "en/"))
          + "</urlset>")
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    write("llms.txt", f"# {NAME}\n\n> App per Mac che dispone biglietti da visita, flyer e locandine sul foglio di stampa con abbondanza e segni di taglio (crocini) ed esporta un PDF pronto per la tipografia.\n\n- Sito: {SITE}/\n- English: {SITE}/en/\n- Download: {DL}\n- Codice e release: {GH}\n- Requisiti: macOS 13+, Apple Silicon e Intel\n")
    left = [r for r, c in pages.items() if TODO in c]
    print(f"Sito generato in dist/ ({SITE}) — versione release: {VERSION or 'non letta'}")
    if left: print("DA COMPLETARE in:", ", ".join(left))
    if "crocini.app" in SITE: print("NOTA: dominio predefinito (crocini.app): da confermare/acquistare, poi SITE_URL=… ./build.py")

if __name__ == "__main__": main()
