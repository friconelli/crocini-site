# Sito di Crocini

Una sola landing page, in italiano (`/`) e in inglese (`/en/`), generata da `build.py` (Python, nessuna dipendenza) in `dist/`. Ispirata al sito di Dolly Projector (`../dolly-site`): stessa struttura (build statico, SEO, hreflang, JSON-LD, sitemap, `llms.txt`, header di sicurezza per Vercel), ma senza statistiche né cookie.

## Contenuto
Hero con il foglio animato (biglietti che entrano uno a uno, poi i crocini si disegnano) → tre passi → **calcolatore interattivo** (stesso calcolo dell'app: griglia centrata, rotazione automatica, margine per i segni) → funzioni → finestra dell'app → FAQ → download con istruzioni del primo avvio → footer (privacy, font, GitHub).

## Download e versione
Il pulsante punta a `https://github.com/friconelli/crocini/releases/latest/download/Crocini.zip`: nessun file da ospitare qui. `build.py` legge la versione dall'ultima release con `gh` (o `CROCINI_VERSION=x.y.z`); ricostruire il sito dopo ogni release per aggiornare il numero.

## Anteprima in locale
```bash
python3 build.py && python3 -m http.server 8099 -d dist     # http://localhost:8099/
```

## Da fare prima di pubblicare
- [ ] **Dominio**: oggi `build.py` usa `https://crocini.app` solo come valore predefinito (canonical, hreflang, sitemap, Open Graph). Scegliere/comprare il dominio, poi `SITE_URL=https://… python3 build.py`.
- [ ] **Hosting**: nuovo progetto Vercel dalla cartella `crocini-site` (`vercel.json` pronto: cartella `dist`, build `python3 build.py`, header di sicurezza, CSP solo con risorse proprie); aggiungere il dominio.
- [ ] Search Console / Bing Webmaster: inviare `/sitemap.xml`.
- [ ] Repository GitHub del sito (non ancora creato).

## Immagini e font
- `src/img/app.webp`: screenshot dell'app (`Crocini --art biglietto.png --snapshot out.png`, ritagliata di 56 px in alto) con il biglietto di esempio generato da `Scripts/make_sample_card.swift` (91×61 mm, 300 dpi).
- `src/og-crocini*.png`: `Scripts/make_og.swift`. Favicon dall'icona dell'app.
- Font: Bricolage Grotesque (OFL), variabile alleggerita in woff2 (Latin).
