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
# ID del contenitore Google Tag Manager (GTM-XXXXXXX): se manca, il sito resta senza statistiche e senza banner.
GTM_ID = os.environ.get("GTM_ID", "").strip()
REPO = "friconelli/crocini"
NAME = "Crocini"
DL = f"https://github.com/{REPO}/releases/latest/download/Crocini.zip"
REL = f"https://github.com/{REPO}/releases/latest"
GH = f"https://github.com/{REPO}"
GK_CMD = 'xattr -dr com.apple.quarantine "/Applications/Crocini.app"'
TODO = "[da completare:"

def latest_version():
    """Versione dell'ultima release: con gh se c'è, altrimenti dall'API pubblica di GitHub (serve sul build di Vercel)."""
    try:
        out = subprocess.run(["gh", "release", "view", "--repo", REPO, "--json", "tagName"],
                             capture_output=True, text=True, timeout=20)
        if out.returncode == 0: return json.loads(out.stdout)["tagName"].lstrip("vV")
    except Exception:
        pass
    try:
        from urllib.request import urlopen, Request
        r = urlopen(Request(f"https://api.github.com/repos/{REPO}/releases/latest", headers={"User-Agent": "crocini-site-build"}), timeout=10)
        return json.loads(r.read())["tag_name"].lstrip("vV")
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
 "desc": "App per Mac che dispone biglietti da visita, flyer e locandine sul foglio di stampa con abbondanza e segni di taglio (crocini), anche fronte-retro e fustella per plotter, ed esporta un PDF pronto per la tipografia.",
 "nav": [("#funzioni", "Funzioni"), ("#prova", "Provalo"), ("#domande", "Domande"), ("#scarica", "Scarica")],
 "eyebrow": "App per Mac",
 "h1": "Il foglio, pronto per il *taglio*",
 "lead": "Crocini dispone biglietti da visita, flyer e locandine sul foglio di stampa, aggiunge abbondanza e segni di taglio e ti consegna un PDF pronto per la tipografia, per la ghigliottina o per il plotter; anche fronte-retro.",
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
  ("between", "Crocini anche tra gli elementi", "Con una distanza tra i pezzi, i segni di taglio compaiono anche nelle fessure, non solo sul bordo del foglio."),
  ("duplex", "Fronte-retro", "Carichi fronte e retro e ottieni un PDF a due pagine, con il retro già specchiato per la stampa su due lati e un’opzione per correggerne l’allineamento al millimetro."),
  ("plotter", "Fustella per il plotter", "Un secondo PDF con la linea di taglio (colore spot CutContour) e i segni di registrazione: per Summa, Roland, Graphtec (anche con iMark) e la maggior parte dei plotter."),
  ("shape", "Forma di taglio tua", "Carichi un SVG e la fustella segue quella forma: biglietti con angoli speciali, etichette tonde o sagomate."),
  ("number", "Numero progressivo", "Per abbonamenti e tessere: parti dal numero che vuoi, scegli font, posizione e formato, e produci più fogli di fila."),
  ("ruler", "Tutto in millimetri", "Foglio A4, A3, SRA3, Super B/A3, Lettera o misure tue; elemento libero; margini e distanze al decimo di millimetro."),
  ("zoom", "Zoom come negli editor grafici", "Rotella, pinch, lente e mano; barra spaziatrice per spostarti. Controlli ogni dettaglio del taglio."),
  ("rotate", "Rotazione automatica", "Se girando gli elementi ne entrano di più sul foglio, Crocini li ruota da solo."),
  ("update", "Si aggiorna da sola", "Controlla le novità all’avvio e si aggiorna con un clic, senza riscaricare nulla a mano."),
 ],
 "show_h": "Tutto sotto controllo, in una finestra",
 "show_p": "A sinistra le impostazioni, a destra il foglio in tempo reale: cambi un valore e i pezzi si rimettono in ordine davanti a te.",
 "show_alt": "La finestra di Crocini: a sinistra le impostazioni, a destra un foglio A4 con dieci biglietti da visita e i segni di taglio",

 "sc_kick": "Dentro l’app", "sc_h": "Scorri, e guarda il foglio cambiare",
 "sc_p": "Ogni funzione, vista sul foglio: la pagina si muove con te.", "sc_unit": "pezzi", "sc_alt": "Un foglio A4 che cambia mentre scorri: biglietti, abbondanza, segni di taglio, zoom, rotazione, numerazione, fustella e fronte-retro",
 "sc_steps": [
  ("Un preset e il foglio è pronto", "Biglietti, cartoline, flyer, etichette: scegli un formato e Crocini calcola subito quanti pezzi entrano. I tuoi preset li salvi e li richiami con un clic.", ""),
  ("L’abbondanza a modo tuo", "Il file ce l’ha già? La usi. Altrimenti la aggiungi con un colore piatto o ingrandendo la grafica: stampa a vivo senza strisce bianche.", "Abbondanza 3 mm"),
  ("Crocini su misura", "Spessore, lunghezza, colore e distanza dal rifilo. Stanno sul bordo della griglia, pronti per la ghigliottina.", "Segni di taglio"),
  ("Zoom come negli editor grafici", "Rotella, pinch, lente e mano; barra spaziatrice per spostarti. Controlli ogni dettaglio del taglio prima di stampare.", "Zoom"),
  ("Gira i pezzi da solo", "Se ruotando gli elementi ne entrano di più sul foglio, Crocini li gira per te: da 3 a 5 segnalibri, senza toccare nulla.", ""),
  ("Crocini anche tra gli elementi", "Con una distanza tra i pezzi, i segni di taglio compaiono anche nelle fessure: tagli ogni pezzo con precisione, non solo sul bordo del foglio.", "Segni tra gli elementi"),
  ("Numero progressivo", "Per abbonamenti e tessere: parti dal numero che vuoi, scegli font, posizione e formato, e produci più fogli di fila.", "Numerazione"),
  ("Fustella per il plotter", "Un secondo PDF con la linea di taglio, anche con una forma tua da SVG, e i segni di registrazione negli angoli.", "Fustella"),
  ("Fronte-retro", "Carichi il retro e il PDF ha due pagine: il retro è già specchiato e lo allinei al millimetro se la stampante sposta.", "Fronte / Retro"),
 ],
 "faq_h": "Domande frequenti",
 "faq": [
  ("Su quali Mac funziona?", "Su tutti i Mac con macOS 13 Ventura o successivo, sia con Apple Silicon sia con processore Intel."),
  ("Quali file posso impaginare?", "PNG, JPEG, TIFF, HEIC, GIF, WebP e PDF. Dai PDF e dalle immagini con i DPI nel file Crocini legge la misura reale e può impostare l’elemento di conseguenza."),
  ("Come si usano i crocini per tagliare?", "I segni stanno sul bordo della griglia, fuori dall’abbondanza (e anche tra gli elementi, se c’è una distanza): allinea la ghigliottina o il taglierino ai segni opposti e taglia da un lato all’altro del foglio."),
  ("Come funziona il fronte-retro?", "Attivi «Fronte-retro», carichi la grafica del retro ed esporti: il PDF ha due pagine e la seconda è specchiata, così stampando fronte-retro sul lato lungo i retri combaciano con i fronti."),
  ("Posso tagliare con un plotter?", "Sì: attiva «Esporta anche la fustella». Il PDF di stampa riceve quattro segni di registrazione negli angoli e un secondo PDF contiene la linea di taglio (colore spot CutContour) con gli stessi segni, nella stessa posizione. Il formato è generico: alcuni plotter vogliono i propri segni, e conviene fare una prova su un foglio. Per i Graphtec con iMark c’è un profilo che esporta solo la linea di taglio, su un livello a parte, e lascia i segni a iMark."),
  ("Posso numerare gli elementi?", "Sì: nella scheda «Numerazione» scegli da che numero partire, il passo, le cifre con gli zeri davanti, un testo prima e dopo, il font, la posizione e la rotazione. Con più fogli i numeri continuano da un foglio all’altro nello stesso PDF."),
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
 "foot_priv_stats": "Il sito usa cookie di statistica (Google Analytics e Microsoft Clarity) solo se li accetti. L’app lavora in locale e si collega solo per cercare aggiornamenti.",
 "ck_text": "Usiamo cookie di statistica (Google Analytics e Microsoft Clarity) per capire come viene usato il sito. Partono solo se accetti.", "ck_accept": "Accetta", "ck_reject": "Rifiuta", "ck_prefs": "Preferenze cookie",
 "foot_font": "Carattere: Bricolage Grotesque (SIL Open Font License).",
 "foot_code": "Codice e release su GitHub",
 "skip": "Vai al contenuto", "nf_t": "Pagina non trovata", "nf_p": "Questa pagina non esiste.", "nf_b": "Torna alla home",
 "faq_ld_name": "Domande frequenti su Crocini",
},
"en": {
 "lang": "en", "prefix": "en/", "alt": "it", "alt_label": "IT",
 "title": "Crocini – lay out business cards, flyers and posters for cutting",
 "desc": "Mac app that arranges business cards, flyers and posters on the print sheet with bleed and crop marks, double-sided and plotter cut files, and exports a print-ready PDF.",
 "nav": [("#features", "Features"), ("#try", "Try it"), ("#faq", "FAQ"), ("#download", "Download")],
 "eyebrow": "Mac app",
 "h1": "The sheet, ready for the *cut*",
 "lead": "Crocini arranges business cards, flyers and posters on the print sheet, adds bleed and crop marks and hands you a PDF ready for the print shop, the guillotine or the plotter; double-sided too.",
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
  ("between", "Crop marks between items too", "With a gap between the pieces, crop marks also appear in the gutters, not only on the edge of the sheet."),
  ("duplex", "Double-sided", "Load front and back and get a two-page PDF, with the back already mirrored for double-sided printing and an option to fine-tune its alignment to the millimetre."),
  ("plotter", "Cut file for the plotter", "A second PDF with the cut line (CutContour spot colour) and registration marks: for Summa, Roland, Graphtec (iMark too) and most cutting plotters."),
  ("shape", "Your own cut shape", "Load an SVG and the die follows that shape: cards with special corners, round or contoured labels."),
  ("number", "Sequential numbering", "For memberships and passes: start from any number, pick font, position and format, and produce several sheets in a row."),
  ("ruler", "Everything in millimetres", "A4, A3, SRA3, Super B/A3, Letter or your own sheet; free item size; margins and spacing to a tenth of a millimetre."),
  ("zoom", "Zoom like design editors", "Wheel, pinch, lens and hand; space bar to pan. Check every detail of the cut."),
  ("rotate", "Automatic rotation", "If turning the items fits more on the sheet, Crocini rotates them for you."),
  ("update", "Updates itself", "It checks for news at launch and updates with one click, no manual re-download."),
 ],
 "show_h": "Everything under control, in one window",
 "show_p": "Settings on the left, the live sheet on the right: change a value and the pieces rearrange right in front of you.",
 "show_alt": "The Crocini window: settings on the left, an A4 sheet with ten business cards and crop marks on the right",

 "sc_kick": "Inside the app", "sc_h": "Scroll, and watch the sheet change",
 "sc_p": "Every feature, shown on the sheet: the page moves with you.", "sc_unit": "pieces", "sc_alt": "An A4 sheet that changes as you scroll: cards, bleed, crop marks, zoom, rotation, numbering, cut file and double-sided",
 "sc_steps": [
  ("A preset and the sheet is ready", "Business cards, postcards, flyers, labels: pick a format and Crocini instantly works out how many pieces fit. Save your own presets and recall them with one click.", ""),
  ("Bleed, your way", "Already in the file? Use it. Otherwise add it with a flat colour or by enlarging the artwork: full-bleed printing without white edges.", "Bleed 3 mm"),
  ("Custom crop marks", "Thickness, length, colour and distance from the trim. They sit on the edge of the grid, ready for the guillotine.", "Crop marks"),
  ("Zoom like design editors", "Wheel, pinch, lens and hand; space bar to pan. Check every detail of the cut before printing.", "Zoom"),
  ("It turns the pieces for you", "If turning the items fits more on the sheet, Crocini rotates them for you: from 3 to 5 bookmarks, without touching a thing.", ""),
  ("Crop marks between items too", "With a gap between the pieces, crop marks also appear in the gutters: cut every piece precisely, not only along the edge of the sheet.", "Marks between items"),
  ("Sequential numbering", "For memberships and passes: start from any number, pick font, position and format, and produce several sheets in a row.", "Numbering"),
  ("Cut file for the plotter", "A second PDF with the cut line, even with your own shape from an SVG, and registration marks in the corners.", "Cut file"),
  ("Double-sided", "Load the back and the PDF has two pages: the back is already mirrored, and you can align it to the millimetre if your printer shifts.", "Front / Back"),
 ],
 "faq_h": "Frequently asked questions",
 "faq": [
  ("Which Macs does it run on?", "Any Mac running macOS 13 Ventura or later, both Apple Silicon and Intel."),
  ("Which files can I lay out?", "PNG, JPEG, TIFF, HEIC, GIF, WebP and PDF. From PDFs and from images that carry DPI, Crocini reads the real size and can set the item accordingly."),
  ("How do I cut with the crop marks?", "The marks sit on the edge of the grid, outside the bleed (and between the items too, when there is a gap): line up the guillotine or the knife with the opposite marks and cut from one side of the sheet to the other."),
  ("How does double-sided work?", "Turn on “Double-sided”, load the back artwork and export: the PDF has two pages and the second one is mirrored, so printing double-sided on the long edge the backs line up with the fronts."),
  ("Can I cut with a plotter?", "Yes: turn on “Also export the cut file”. The print PDF gets four registration marks in the corners and a second PDF holds the cut line (CutContour spot colour) with the same marks in the same position. The format is generic: some plotters want their own marks, so do a test sheet first. For Graphtec with iMark there is a profile that exports only the cut line, on its own layer, and leaves the marks to iMark."),
  ("Can I number the items?", "Yes: in the “Numbering” card pick the starting number, the step, digits with leading zeros, text before and after, the font, position and rotation. With several sheets the numbers carry on from one sheet to the next in the same PDF."),
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
 "foot_priv_stats": "This site uses analytics cookies (Google Analytics and Microsoft Clarity) only if you accept them. The app works locally and only connects to look for updates.",
 "ck_text": "We use analytics cookies (Google Analytics and Microsoft Clarity) to understand how the site is used. They only start if you accept.", "ck_accept": "Accept", "ck_reject": "Reject", "ck_prefs": "Cookie preferences",
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
 "between": '<rect x="3" y="5" width="7" height="14" rx="1"/><rect x="14" y="5" width="7" height="14" rx="1"/><path d="M12 2.5v3M12 18.5v3"/>',
 "duplex": '<rect x="3.5" y="6" width="11" height="14" rx="1.5"/><path d="M8 3.5h9.5A1.5 1.5 0 0119 5v11"/><path d="M7 11h4M7 14h3"/>',
 "plotter": '<rect x="3" y="3" width="3.2" height="3.2"/><rect x="17.8" y="17.8" width="3.2" height="3.2"/><rect x="8" y="8" width="8" height="8" rx="2.5" stroke-dasharray="2 1.6"/>',
 "lang": '<circle cx="12" cy="12" r="8.5"/><path d="M3.5 12h17M12 3.5c-3 3-3 14 0 17M12 3.5c3 3 3 14 0 17"/>',
 "shape": '<path d="M5 6h14a2.5 2.5 0 002.5 2.5v7A2.5 2.5 0 0019 18H5a2.5 2.5 0 00-2.5-2.5v-7A2.5 2.5 0 005 6z" stroke-dasharray="2.4 1.8"/><path d="M12 9v6M9 12h6"/>',
 "number": '<path d="M9.5 4L7.5 20M16.5 4l-2 16M5 9h15M4 15h15"/>',
 "chip": '<rect x="6.5" y="6.5" width="11" height="11" rx="2"/><rect x="9.5" y="9.5" width="5" height="5" rx=".8"/><path d="M9 3v3M15 3v3M9 18v3M15 18v3M3 9h3M3 15h3M18 9h3M18 15h3"/>',
 "update": '<path d="M12 4v10M8 10.5l4 4 4-4"/><path d="M5 17v2.5A1.5 1.5 0 006.5 21h11a1.5 1.5 0 001.5-1.5V17"/>',
}
def icon(name): return f'<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>'

LOGO = ('<svg class="logo" viewBox="0 0 44 44" aria-hidden="true"><defs><linearGradient id="lg" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0" stop-color="#FF3DA8"/><stop offset=".55" stop-color="#EC008C"/><stop offset="1" stop-color="#C70075"/></linearGradient></defs>'
        '<rect width="44" height="44" rx="11" fill="url(#lg)"/><rect x="11" y="15" width="22" height="14" rx="2.6" fill="#fff"/>'
        '<path d="M7 14V7h7M30 7h7v7M7 30v7h7M30 37h7v-7" fill="none" stroke="#FFF200" stroke-width="3" stroke-linecap="square"/></svg>')

REG = ('<svg class="reg" viewBox="0 0 58 58" aria-hidden="true" fill="none" stroke="#141414" stroke-width="2.4">'
       '<circle cx="29" cy="29" r="15"/><circle cx="29" cy="29" r="7" fill="#EC008C" stroke="none"/><path d="M29 2v18M29 38v18M2 29h18M38 29h18"/></svg>')

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
            f'<path class="hm" d="{d}" fill="none" stroke="#141414" stroke-width="1.6" pathLength="100"/></svg>')

# ---------------------------------------------------------------- stile
CSS = """
@font-face{font-family:"Bricolage Grotesque";src:url(/fonts/bricolage.woff2) format("woff2");font-weight:300 800;font-style:normal;font-display:swap}
:root{--c:#00AEEF;--m:#EC008C;--y:#FFF200;--k:#141414;--m2:#C70075;--ink:#141414;--ink2:#55565B;--line:#E3E3E8;--paper:#fff;--soft:#F6F6F8;--r:20px;color-scheme:light}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
html.lenis,html.lenis body{height:auto}.lenis:not(.lenis-autoToggle).lenis-stopped{overflow:clip}.lenis [data-lenis-prevent]{overscroll-behavior:contain}
body{margin:0;background:#fff;color:var(--ink);font:400 17px/1.6 "Bricolage Grotesque",system-ui,-apple-system,"Segoe UI",sans-serif;overflow-x:hidden}
img,svg{max-width:100%}a{color:inherit}
.wrap{width:min(1120px,100% - 40px);margin-inline:auto}
.skip{position:absolute;left:-999px;top:8px;background:var(--k);color:#fff;padding:8px 14px;border-radius:10px;z-index:99}.skip:focus{left:8px}
/* scrollbar: i quattro colori di stampa, come la barra in alto */
::-webkit-scrollbar{width:14px;height:14px}
::-webkit-scrollbar-track{background:var(--soft);border-left:2px solid var(--k)}
::-webkit-scrollbar-thumb{background:linear-gradient(180deg,var(--c) 0 25%,var(--m) 25% 50%,var(--y) 50% 75%,var(--k) 75% 100%);border:2px solid var(--k);border-radius:99px;min-height:56px;background-clip:padding-box}
::-webkit-scrollbar-thumb:hover{border-color:var(--m)}
@supports not selector(::-webkit-scrollbar){html{scrollbar-color:var(--m) var(--soft);scrollbar-width:auto}}
.ck{position:fixed;left:16px;bottom:16px;z-index:60;max-width:380px;background:#fff;border:2px solid var(--k);border-radius:18px;padding:16px 18px;box-shadow:5px 5px 0 var(--y)}
.ck[hidden]{display:none}.ck p{margin:0 0 12px;font-size:14.5px;line-height:1.45;color:var(--ink2)}
.ckb{display:flex;gap:10px}.ckb button{font:700 14px inherit;font-family:inherit;border:2px solid var(--k);border-radius:99px;padding:8px 16px;cursor:pointer;background:#fff;color:var(--k)}
.ckb .cky{background:var(--m);color:#fff;box-shadow:3px 3px 0 var(--k)}
button.lnk{font:inherit;color:inherit;background:none;border:0;padding:0;margin-left:6px;text-decoration:underline;cursor:pointer}
@media (max-width:560px){.ck{left:12px;right:12px;bottom:12px;max-width:none}}
.bar4{height:6px;background:linear-gradient(90deg,var(--c) 0 25%,var(--m) 25% 50%,var(--y) 50% 75%,var(--k) 75% 100%)}
/* evidenziatore giallo, come un pennarello sul foglio di prova */
em{font-style:normal;color:var(--m);position:relative;white-space:nowrap;z-index:0}
em::before{content:"";position:absolute;left:-.08em;right:-.08em;bottom:.02em;height:.46em;background:var(--y);z-index:-1;transform:scaleX(var(--u,0));transform-origin:left;border-radius:2px}
html:not(.js) em,html.nogsap em{--u:1}
/* intestazione */
.top{position:sticky;top:0;z-index:20;background:rgba(255,255,255,.92);backdrop-filter:saturate(1.4) blur(12px);-webkit-backdrop-filter:saturate(1.4) blur(12px);border-bottom:2px solid transparent;transition:border-color .25s}
.top.scrolled{border-bottom-color:var(--k)}
.top .wrap{display:flex;align-items:center;gap:22px;height:66px}
.brand{display:flex;align-items:center;gap:11px;text-decoration:none;font-weight:800;font-size:23px;letter-spacing:-.025em}
.brand .logo{width:36px;height:36px;transition:transform .4s cubic-bezier(.3,1.6,.5,1)}.brand:hover .logo{transform:rotate(-8deg) scale(1.08)}
nav{display:flex;gap:2px;margin-left:auto}
nav a{text-decoration:none;font-weight:600;font-size:15px;padding:8px 13px;border-radius:99px;transition:background .15s}
nav a:nth-child(1):hover{background:var(--c)}nav a:nth-child(2):hover{background:var(--m);color:#fff}nav a:nth-child(3):hover{background:var(--y)}nav a:nth-child(4):hover{background:var(--k);color:#fff}
.lang{font-weight:700;font-size:13px;text-decoration:none;padding:6px 11px;border:2px solid var(--k);border-radius:99px}.lang:hover{background:var(--y)}
/* pulsanti: colore pieno e ombra dura, come una lastra sfalsata */
.btn{display:inline-flex;align-items:center;gap:9px;text-decoration:none;font-weight:700;font-size:16px;padding:12px 24px;border-radius:99px;border:2px solid var(--k);cursor:pointer;color:#fff;background:var(--m);box-shadow:4px 4px 0 var(--k);transition:transform .15s,box-shadow .15s}
.btn:hover{transform:translate(-2px,-2px);box-shadow:6px 6px 0 var(--k)}.btn:active{transform:translate(3px,3px);box-shadow:1px 1px 0 var(--k)}
.btn.ghost{background:#fff;color:var(--k);box-shadow:4px 4px 0 var(--c)}.btn.ghost:hover{box-shadow:6px 6px 0 var(--c)}
.btn.sm{padding:8px 18px;font-size:14.5px;box-shadow:3px 3px 0 var(--k)}
.top .btn{margin-left:4px}
.apple{width:18px;height:18px}
/* hero: retino di punti C M Y leggermente sfalsati */
.hero{position:relative;padding:56px 0 92px;overflow:hidden}
.hero::before{content:"";position:absolute;inset:0;z-index:0;pointer-events:none;
 background-image:radial-gradient(circle,rgba(0,174,239,.55) 1.5px,transparent 2px),radial-gradient(circle,rgba(236,0,140,.45) 1.5px,transparent 2px),radial-gradient(circle,rgba(255,242,0,.95) 1.7px,transparent 2.2px);
 background-size:26px 26px;background-position:0 0,9px 9px,18px 4px;
 -webkit-mask-image:radial-gradient(60% 75% at 88% 18%,#000,transparent 72%);mask-image:radial-gradient(60% 75% at 88% 18%,#000,transparent 72%)}
.hero .wrap{position:relative;z-index:1;display:grid;grid-template-columns:minmax(0,1.05fr) minmax(0,.95fr);gap:48px;align-items:center}
.eyebrow{display:inline-flex;align-items:center;gap:10px;font-weight:700;font-size:13.5px;letter-spacing:.09em;text-transform:uppercase;border:2px solid var(--k);padding:6px 14px;border-radius:99px;background:#fff}
.eyebrow i{display:inline-flex;gap:3px}.eyebrow i b{width:9px;height:9px;border-radius:50%;display:block;}
.eyebrow i b:nth-child(1){background:var(--c)}.eyebrow i b:nth-child(2){background:var(--m);animation-delay:.2s}.eyebrow i b:nth-child(3){background:var(--y);box-shadow:inset 0 0 0 1px rgba(0,0,0,.25);animation-delay:.4s}.eyebrow i b:nth-child(4){background:var(--k);animation-delay:.6s}
h1{font-size:clamp(40px,6.4vw,76px);line-height:1.02;letter-spacing:-.035em;margin:22px 0 20px;font-weight:800}
.lead{font-size:clamp(18px,2vw,21px);color:var(--ink2);max-width:34em;margin:0 0 30px}
.cta{display:flex;flex-wrap:wrap;gap:16px;align-items:center}
.meta{margin:22px 0 0;font-size:14.5px;color:var(--ink2)}
/* il foglio con due "lastre" sfalsate dietro, come un errore di registro */
.sheetwrap{position:relative;justify-self:center;width:min(100%,430px)}
.sheetwrap::before,.sheetwrap::after{content:"";position:absolute;inset:0;border-radius:3px;transform:rotate(-2.5deg)}
.sheetwrap::before{background:var(--c);translate:-16px 12px;opacity:.9}
.sheetwrap::after{background:var(--y);translate:16px 18px;box-shadow:0 0 0 2px var(--k)}
.sheet{position:relative;z-index:1;display:block;width:100%;height:auto;border-radius:3px;transform:rotate(-2.5deg);box-shadow:0 0 0 2px var(--k),8px 8px 0 var(--m)}
.hc{transform-box:fill-box;transform-origin:center}html.js:not(.nogsap) .hc{opacity:0}
.hm{stroke-dasharray:100;stroke-dashoffset:0}html.js:not(.nogsap) .hm{stroke-dashoffset:100}
.reg{position:absolute;right:-6px;top:-26px;width:58px;height:58px;z-index:2}
/* sezioni */
section{padding:92px 0;position:relative}
h2{font-size:clamp(30px,4.2vw,50px);line-height:1.06;letter-spacing:-.03em;margin:0 0 14px;font-weight:800}
.sub{color:var(--ink2);max-width:40em;margin:0 0 44px;font-size:18px}
.kick{display:inline-block;font-weight:800;font-size:13px;letter-spacing:.12em;text-transform:uppercase;margin-bottom:12px;padding:3px 10px;background:var(--y)}
html.js:not(.nogsap) .rv:not(.in){opacity:0}
.steps{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:26px;counter-reset:s}
.step{background:#fff;border:2px solid var(--k);border-radius:var(--r);padding:30px 28px;position:relative;overflow:hidden;transition:transform .2s,box-shadow .2s}
.step:nth-child(1){box-shadow:7px 7px 0 var(--c)}.step:nth-child(2){box-shadow:7px 7px 0 var(--m)}.step:nth-child(3){box-shadow:7px 7px 0 var(--y)}
.step:hover{transform:translate(-3px,-3px)}.step:nth-child(1):hover{box-shadow:10px 10px 0 var(--c)}.step:nth-child(2):hover{box-shadow:10px 10px 0 var(--m)}.step:nth-child(3):hover{box-shadow:10px 10px 0 var(--y)}
.step::before{counter-increment:s;content:counter(s);display:grid;place-items:center;width:42px;height:42px;border-radius:50%;border:2px solid var(--k);font-weight:800;font-size:20px;margin-bottom:16px}
.step:nth-child(1)::before{background:var(--c)}.step:nth-child(2)::before{background:var(--m);color:#fff}.step:nth-child(3)::before{background:var(--y)}
.step h3{margin:0 0 8px;font-size:23px;letter-spacing:-.02em}.step p{margin:0;color:var(--ink2)}
/* demo */
.demo-sec{background:#fff;border-block:2px solid var(--k)}
.demo{display:grid;grid-template-columns:minmax(0,340px) minmax(0,1fr);gap:34px;align-items:start;background:#fff;border:2px solid var(--k);border-radius:26px;padding:28px;box-shadow:9px 9px 0 var(--c)}
.ctl h3{margin:20px 0 9px;font-size:13px;letter-spacing:.1em;text-transform:uppercase;color:var(--ink2)}.ctl h3:first-child{margin-top:0}
.chips{display:flex;flex-wrap:wrap;gap:8px}
.chip{font:600 14px/1 inherit;font-family:inherit;color:var(--k);background:#fff;border:2px solid var(--k);border-radius:99px;padding:8px 13px;cursor:pointer;transition:transform .15s,background .15s}
.chip:hover{transform:translateY(-2px);background:var(--y)}.chip[aria-pressed=true]{background:var(--m);color:#fff}
.row{display:flex;gap:10px;align-items:center}
.fld{display:flex;flex-direction:column;gap:5px;flex:1;font-size:13px;color:var(--ink2)}
.fld input,.fld select{font:600 16px inherit;font-family:inherit;color:var(--ink);background:#fff;border:2px solid var(--k);border-radius:12px;padding:9px 12px;width:100%;outline:0;transition:box-shadow .15s}
.fld input:focus,.fld select:focus{box-shadow:4px 4px 0 var(--c)}
.chk{display:flex;gap:10px;align-items:center;margin-top:14px;font-weight:600;cursor:pointer}.chk input{accent-color:var(--m);width:19px;height:19px}
.stage{display:grid;place-items:center;gap:18px;padding:10px;min-width:0}
#sheet{width:auto;height:min(62vh,560px);max-width:100%;border-radius:2px;box-shadow:0 0 0 2px var(--k),7px 7px 0 var(--y);background:#fff;overflow:visible}
.pop{animation:pop2 .5s cubic-bezier(.2,1.2,.3,1) backwards;animation-delay:calc(var(--i)*30ms);transform-box:fill-box;transform-origin:center}
@keyframes pop2{from{opacity:0;transform:scale(.85)}}
.count{display:flex;gap:12px;align-items:baseline;flex-wrap:wrap;justify-content:center;font-weight:600;color:var(--ink2)}
.count b{font-size:60px;line-height:1;font-weight:800;color:var(--k);letter-spacing:-.04em;font-variant-numeric:tabular-nums;background:linear-gradient(transparent 62%,var(--y) 62%);padding:0 6px}.count.none b{background:none;color:var(--ink2)}
.count small{font-size:14px;background:var(--c);color:var(--k);padding:4px 11px;border-radius:99px;font-weight:700;border:2px solid var(--k)}
.note{font-size:13.5px;color:var(--ink2);margin:18px 0 0}
/* funzioni */
.feats{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:20px}
.feat{background:#fff;border:2px solid var(--k);border-radius:18px;padding:24px 22px;transition:transform .2s,box-shadow .2s}
.feat:nth-child(3n+1):hover{box-shadow:6px 6px 0 var(--c)}.feat:nth-child(3n+2):hover{box-shadow:6px 6px 0 var(--m)}.feat:nth-child(3n):hover{box-shadow:6px 6px 0 var(--y)}
.feat:hover{transform:translate(-3px,-3px)}
.ic{width:48px;height:48px;padding:11px;border-radius:50%;color:var(--k);border:2px solid var(--k);margin-bottom:16px}
.feat:nth-child(3n+1) .ic{background:var(--c)}.feat:nth-child(3n+2) .ic{background:var(--m)}.feat:nth-child(3n) .ic{background:var(--y)}
.feat h3{margin:0 0 6px;font-size:19px;letter-spacing:-.015em;line-height:1.2}.feat p{margin:0;color:var(--ink2);font-size:15.5px;line-height:1.5}
/* sezione a scorrimento: il foglio resta fermo, i passi scorrono */
.scrolly-sec{padding-bottom:30px}
.scrolly{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:64px;align-items:start;margin-top:10px}
.stage-col{position:sticky;top:78px;height:calc(100vh - 100px);display:grid;place-items:center}
.stagebox{position:relative;width:min(100%,430px)}
#scene{display:block;width:100%;height:auto;max-height:calc(100vh - 190px);aspect-ratio:210/297;margin-inline:auto;background:#fff;border:2px solid var(--k);border-radius:3px;box-shadow:9px 9px 0 var(--y);overflow:hidden}
#cam{transform-origin:0 0}
#scene .ring{fill:var(--m);fill-rule:evenodd;opacity:0;transition:opacity .6s}#scene.s1 .ring{opacity:.45}
#scene .bd{opacity:0;transition:opacity .6s}#scene.s1 .bd{opacity:1}
#scene .mk{transition:stroke-width .6s,stroke .6s}
.chipbar{position:absolute;left:-12px;top:-16px;z-index:3;display:flex;gap:8px;align-items:baseline;background:#fff;border:2px solid var(--k);border-radius:99px;padding:6px 14px;font-weight:700;font-size:14px;box-shadow:3px 3px 0 var(--c);max-width:calc(100% + 24px)}
.chipbar b{font-size:20px;line-height:1;font-variant-numeric:tabular-nums;background:linear-gradient(transparent 58%,var(--y) 58%);padding:0 3px}.chipbar small{font-size:12px;color:var(--ink2);font-weight:600}
.zoompill{position:absolute;right:-12px;bottom:-14px;z-index:3;background:var(--m);color:#fff;border:2px solid var(--k);border-radius:99px;padding:4px 14px;font-weight:800;font-size:15px;box-shadow:3px 3px 0 var(--k);opacity:0;transform:translateY(8px);transition:opacity .4s,transform .4s;font-variant-numeric:tabular-nums}
.stagebox[data-step="3"] .zoompill{opacity:1;transform:none}
.steps-col{padding-bottom:12vh}
.st{min-height:78vh;display:flex;flex-direction:column;justify-content:center;opacity:.28;transition:opacity .5s}
.st.on{opacity:1}
.st .num{display:grid;place-items:center;width:44px;height:44px;border-radius:50%;border:2px solid var(--k);font-weight:800;font-size:20px;margin-bottom:18px}
.st .n0{background:var(--c)}.st .n1{background:var(--m);color:#fff}.st .n2{background:var(--y)}.st .n3{background:var(--k);color:#fff}
.st h3{margin:0 0 12px;font-size:clamp(26px,3.2vw,40px);line-height:1.08;letter-spacing:-.03em}
.st p{margin:0;color:var(--ink2);font-size:18px;max-width:30em}
/* faq */
.faq{max-width:820px}
details{background:#fff;border:2px solid var(--k);border-radius:16px;margin-bottom:14px;transition:box-shadow .2s,transform .2s}
details:hover{transform:translate(-2px,-2px);box-shadow:5px 5px 0 var(--c)}
details[open]{box-shadow:6px 6px 0 var(--y);transform:none}
summary{cursor:pointer;list-style:none;padding:19px 56px 19px 24px;font-weight:700;font-size:18px;position:relative;letter-spacing:-.01em}
summary::-webkit-details-marker{display:none}
summary::after{content:"+";position:absolute;right:20px;top:50%;translate:0 -52%;font-size:24px;font-weight:700;line-height:1;width:30px;height:30px;display:grid;place-items:center;border-radius:50%;background:var(--m);color:#fff;transition:transform .3s}
details[open] summary::after{transform:rotate(45deg)}
details p{margin:0;padding:0 24px 22px;color:var(--ink2)}
/* download */
.dl{background:#fff;border:3px solid var(--k);border-radius:28px;position:relative;overflow:hidden;box-shadow:12px 12px 0 var(--m)}
.dl .bar4{height:14px}
.dl-in{padding:52px 56px 60px}
.dl h2{margin-bottom:10px}.dl .sub{margin-bottom:26px}
.first{margin-top:38px;padding-top:30px;border-top:2px dashed var(--k)}
.first h3{margin:0 0 12px;font-size:19px}.first ol{margin:0;padding-left:22px;display:grid;gap:8px;max-width:640px}
code{display:block;font:500 14px/1.5 ui-monospace,SFMono-Regular,Menlo,monospace;background:var(--k);color:#fff;padding:13px 16px;border-radius:12px;margin-top:8px;word-break:break-all;user-select:all}
.cp{margin-top:10px;font:700 14px inherit;font-family:inherit;background:var(--y);color:var(--k);border:2px solid var(--k);border-radius:99px;padding:7px 16px;cursor:pointer;transition:transform .15s,background .15s}.cp:hover{transform:translateY(-2px)}.cp.ok{background:var(--c)}
.upd{margin:26px 0 0;color:var(--ink2);max-width:640px}
footer{padding:0 0 56px;color:var(--ink2);font-size:14.5px}
footer .bar4{margin-bottom:34px}
footer .wrap{display:grid;gap:8px}footer a{color:var(--m2);text-decoration:none;font-weight:700}footer a:hover{text-decoration:underline}
.nf{min-height:70vh;display:grid;place-items:center;text-align:center;padding:40px 0}
@media (max-width:960px){.scrolly{grid-template-columns:minmax(0,1fr);gap:0}.stage-col{top:64px;height:46vh;background:#fff;z-index:5;padding:14px 0 10px;border-bottom:2px solid var(--k)}.stagebox{width:min(100%,250px)}#scene{max-height:38vh}.st{min-height:56vh}.steps-col{padding-bottom:6vh}.chipbar{left:-6px;font-size:12.5px}.hero .wrap{grid-template-columns:minmax(0,1fr)}.sheetwrap{width:min(78%,360px);margin-top:10px}.feats{grid-template-columns:repeat(2,minmax(0,1fr))}.demo{grid-template-columns:minmax(0,1fr)}.steps{grid-template-columns:minmax(0,1fr)}nav{display:none}.top .wrap{gap:12px}.top .btn.sm{margin-left:auto}}
@media (max-width:560px){.feats{grid-template-columns:minmax(0,1fr)}section{padding:64px 0}.dl-in{padding:34px 24px 40px}.dl{border-radius:22px}.top .btn.sm{display:none}.lang{margin-left:auto}.demo{padding:18px;border-radius:20px}}
@media (prefers-reduced-motion:reduce){*,*::before,*::after{animation:none!important;transition:none!important;scroll-behavior:auto!important}.hc,.hm{opacity:1;stroke-dashoffset:0}em::before{transform:none}}
"""

# ---------------------------------------------------------------- pagine
def url(p): return f"{SITE}/{p}"
def head(t, title, desc, path, alt_path, ld, noindex=False):
    lang = t["lang"]
    og = f"{SITE}/og-crocini{'-en' if lang == 'en' else ''}.jpg"
    hl = "" if noindex else (f'<link rel="canonical" href="{url(path)}">'
         f'<link rel="alternate" hreflang="{lang}" href="{url(path)}"><link rel="alternate" hreflang="{t["alt"]}" href="{url(alt_path)}">'
         f'<link rel="alternate" hreflang="x-default" href="{url(T["it"]["prefix"] + "")}">')
    return (f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{e(title)}</title><meta name="description" content="{e(desc)}">'
            + ('<meta name="robots" content="noindex">' if noindex else "") + hl +
            f'<meta name="theme-color" content="#ffffff"><link rel="icon" href="/favicon.ico" sizes="48x48"><link rel="icon" type="image/png" sizes="192x192" href="/favicon-192.png"><link rel="apple-touch-icon" href="/apple-touch-icon.png">'
            f'<meta property="og:type" content="website"><meta property="og:site_name" content="{NAME}"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}">'
            f'<meta property="og:url" content="{url(path)}"><meta property="og:image" content="{og}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">'
            f'<meta name="twitter:card" content="summary_large_image">'
            f'<link rel="preload" href="/fonts/bricolage.woff2" as="font" type="font/woff2" crossorigin><script src="/js/boot.js"></script><style>{CSS}</style>'
            + "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld) + "</head>")

APPLE = '<svg class="apple" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12.152 6.896c-.948 0-2.415-1.078-3.96-1.04-2.04.027-3.91 1.183-4.961 3.014-2.117 3.675-.546 9.103 1.519 12.09 1.013 1.454 2.208 3.09 3.792 3.039 1.52-.065 2.09-.987 3.935-.987 1.831 0 2.35.987 3.96.948 1.637-.026 2.676-1.48 3.676-2.948 1.156-1.688 1.636-3.325 1.662-3.415-.039-.013-3.182-1.221-3.22-4.857-.026-3.04 2.48-4.494 2.597-4.559-1.429-2.09-3.623-2.324-4.39-2.376-2-.156-3.675 1.09-4.61 1.09zM15.53 3.83c.843-1.012 1.4-2.427 1.245-3.83-1.207.052-2.662.805-3.532 1.818-.78.896-1.454 2.338-1.273 3.714 1.338.104 2.715-.688 3.559-1.701"/></svg>'

def consent_html(t):
    if not GTM_ID: return ""
    return (f'<div id="cookie-banner" class="ck" role="dialog" aria-live="polite" aria-label="{e(t["ck_prefs"])}" hidden><p>{e(t["ck_text"])}</p>'
            f'<div class="ckb"><button type="button" class="ckn" data-ck="deny">{e(t["ck_reject"])}</button><button type="button" class="cky" data-ck="grant">{e(t["ck_accept"])}</button></div></div>'
            f'<script src="/js/consent.js" data-gtm="{e(GTM_ID)}" defer></script>')

def home(lang):
    t = T[lang]; ids = IDS[lang]; P = "/" + t["prefix"]
    ver = f'<p class="meta">{e(t["dl_ver"])} {e(VERSION)} · {e(t["dl_req"])}</p>' if VERSION else f'<p class="meta">{e(t["dl_req"])}</p>'
    nav = "".join(f'<a href="{h}">{e(l)}</a>' for h, l in t["nav"])
    alt_path = T[t["alt"]]["prefix"]
    feats = "".join(f'<div class="feat rv" style="--d:{i%4}">{icon(k)}<h3>{e(h)}</h3><p>{e(p)}</p></div>' for i, (k, h, p) in enumerate(t["feats"]))
    steps = "".join(f'<div class="step rv" style="--d:{i}"><h3>{e(h)}</h3><p>{e(p)}</p></div>' for i, (h, p) in enumerate(t["steps"]))
    sc_steps = "".join(f'<article class="st{" on" if i == 0 else ""}" data-chip="{e(c)}"><span class="num n{i % 4}">{i+1}</span><h3>{e(h)}</h3><p>{e(p)}</p></article>' for i, (h, p, c) in enumerate(t["sc_steps"]))
    faq = "".join(f'<details class="rv"><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in t["faq"])
    chips = "".join(f'<button class="chip" type="button" data-w="{w}" data-h="{h}" aria-pressed="{"true" if i == 0 else "false"}">{e(n)} {w}×{h}</button>' for i, (n, w, h) in enumerate(t["demo_presets"]))
    body = f'''<body><a class="skip" href="#main">{e(t["skip"])}</a>
<div class="bar4" aria-hidden="true"></div>
<header class="top"><div class="wrap"><a class="brand" href="{P}" aria-label="{NAME}">{LOGO}<span>{NAME}</span></a><nav>{nav}</nav>
<a class="lang" href="/{alt_path}" hreflang="{t["alt"]}">{t["alt_label"]}</a><a class="btn sm" href="{DL}">{e(t["cta"])}</a></div></header>
<main id="main">
<section class="hero"><div class="wrap"><div>
<span class="eyebrow"><i aria-hidden="true"><b></b><b></b><b></b><b></b></i>{e(t["eyebrow"])}</span><h1>{emph(t["h1"])}</h1><p class="lead">{e(t["lead"])}</p>
<div class="cta"><a class="btn" href="{DL}">{APPLE}{e(t["cta"])}</a><a class="btn ghost" href="#{ids[1]}">{e(t["cta2"])}</a></div>
<p class="meta">{e(t["meta"])}</p></div>
<div class="sheetwrap">{hero_sheet()}{REG}</div></div></section>

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
<div class="stage"><svg id="sheet" data-img="/img/card.webp" data-img2="/img/tile.webp" role="img" aria-label="{e(t["demo_h"])}"></svg>
<div class="count"><b id="demo-n">10</b><span>{e(t["demo_pieces"])}</span><small id="demo-grid" data-rot="{e(t["demo_rot"])}" data-none="{e(t["demo_nofit"])}">2 × 5</small></div></div></div></div></section>

<section id="{ids[0]}"><div class="wrap"><h2 class="rv">{e(t["feat_h"])}</h2><div class="feats" style="margin-top:36px">{feats}</div></div></section>

<section class="scrolly-sec"><div class="wrap"><span class="kick rv">{e(t["sc_kick"])}</span><h2 class="rv">{e(t["sc_h"])}</h2><p class="sub rv" style="margin-bottom:10px">{e(t["sc_p"])}</p>
<div class="scrolly"><div class="stage-col"><div class="stagebox" id="stagebox"><div class="chipbar"><span id="sc-label"></span><b id="sc-n">10</b><small>{e(t["sc_unit"])}</small></div>
<svg id="scene" viewBox="0 0 210 297" data-img="/img/card.webp" data-img2="/img/tile.webp" data-presets="{e(json.dumps([[n, w, h] for n, w, h in t["demo_presets"]], ensure_ascii=False))}" role="img" aria-label="{e(t["sc_alt"])}"></svg>
<div class="zoompill" id="sc-zoom">100%</div></div></div>
<div class="steps-col">{sc_steps}</div></div></div></section>

<section id="{ids[2]}"><div class="wrap faq"><h2 class="rv">{e(t["faq_h"])}</h2><div style="margin-top:30px">{faq}</div></div></section>

<section id="{ids[3]}"><div class="wrap"><div class="dl rv"><div class="bar4" aria-hidden="true"></div><div class="dl-in"><h2>{e(t["dl_h"])}</h2><p class="sub">{e(t["dl_p"])}</p>
<div class="cta"><a class="btn" href="{DL}">{APPLE}{e(t["dl_btn"])}</a><a class="btn ghost" href="{GH}">{e(t["dl_gh"])}</a></div>{ver}
<div class="first"><h3>{e(t["dl_first_h"])}</h3><ol><li>{e(t["dl_first"][0])}</li><li>{e(t["dl_first"][1])}</li><li>{e(t["dl_first"][2])}<code>{e(GK_CMD)}</code>
<button class="cp" type="button" data-copy="{e(GK_CMD)}" data-done="{e(t["copied"])}">{e(t["copy"])}</button></li></ol></div>
<p class="upd">{e(t["dl_upd"])}</p></div></div></div></section>
</main>
<footer><div class="bar4" aria-hidden="true"></div><div class="wrap"><div>{e(t["foot_priv_stats"] if GTM_ID else t["foot_priv"])}{(" <button type=\"button\" class=\"lnk\" data-ck-open>" + e(t["ck_prefs"]) + "</button>") if GTM_ID else ""}</div><div>{e(t["foot_font"])} · <a href="{GH}">{e(t["foot_code"])}</a></div></div></footer>
<script src="/js/vendor/gsap.min.js" defer></script><script src="/js/vendor/ScrollTrigger.min.js" defer></script><script src="/js/vendor/lenis.min.js" defer></script><script src="/js/site.js" defer></script>{consent_html(t)}</body></html>'''
    ld = [
     {"@context": "https://schema.org", "@type": "SoftwareApplication", "name": NAME, "operatingSystem": "macOS 13+",
      "applicationCategory": "DesignApplication", "description": t["desc"], "url": url(t["prefix"]), "downloadUrl": DL,
      "inLanguage": t["lang"], **({"softwareVersion": VERSION} if VERSION else {}), "image": url("og-crocini.jpg"),
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
