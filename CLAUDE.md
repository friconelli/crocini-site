# Sito di Crocini
Landing statica IT/EN generata da `build.py` → `dist/` (vedi PIANO.md). Anteprima: `python3 build.py && python3 -m http.server 8099 -d dist`.
- Niente cookie né banner: solo Vercel Web Analytics (script `/_vercel/insights/script.js`, coda `window.va` in boot.js). I clic su Download diventano la pagina vista virtuale `/download/mac` (eventi personalizzati non inclusi nel piano Hobby). CSP `script-src 'self'`: gli script stanno in `src/js` (boot.js, site.js), mai inline.
- Testi in `T` (it/en) dentro build.py: ogni modifica va fatta in entrambe le lingue.
- Per le prove con screenshot: Chrome headless (`--headless=new --force-prefers-reduced-motion`); le animazioni `.rv` a scroll compaiono sbiadite negli screenshot senza reduced-motion.
- Online: https://crocini.vercel.app (Vercel, progetto `crocini`); repo github.com/friconelli/crocini-site. Dominio proprio non ancora scelto: variabile `SITE_URL`. App: ../crocini (repo github.com/friconelli/crocini).
- Sezione a scorrimento: i testi dei passi sono in `sc_steps` (it/en) dentro build.py; la scena è SVG disegnato da `site.js` (ultimo blocco), il passo attivo è quello più vicino al centro dello schermo (listener di scroll, non IntersectionObserver). Per provarla in Chrome headless serve un iframe + `scrollTo({behavior:'instant'})` perché `html{scroll-behavior:smooth}`.
