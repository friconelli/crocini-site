# Sito di Crocini
Landing statica IT/EN generata da `build.py` → `dist/` (vedi PIANO.md). Anteprima: `python3 build.py && python3 -m http.server 8099 -d dist`.
- Niente cookie né statistiche; CSP `script-src 'self'`: gli script stanno in `src/js` (boot.js, site.js), mai inline.
- Testi in `T` (it/en) dentro build.py: ogni modifica va fatta in entrambe le lingue.
- Per le prove con screenshot: Chrome headless (`--headless=new --force-prefers-reduced-motion`); le animazioni `.rv` a scroll compaiono sbiadite negli screenshot senza reduced-motion.
- Dominio non ancora scelto: `SITE_URL`. App: ../crocini (repo github.com/friconelli/crocini).
