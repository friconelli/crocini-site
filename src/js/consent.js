/* Consenso ai cookie + Google Tag Manager. GTM (e quindi GA4 e Clarity, configurati come tag dentro GTM)
   si carica SOLO dopo «Accetta»; con «Rifiuta» non parte nessuno script di terze parti. */
(function () {
  'use strict';
  var me = document.currentScript, id = me && me.getAttribute('data-gtm'), cid = me && me.getAttribute('data-clarity');
  if (!id) return;
  var KEY = 'crocini-consent', box = document.getElementById('cookie-banner');
  var store = { get: function () { try { return localStorage.getItem(KEY); } catch (e) { return null; } },
                set: function (v) { try { localStorage.setItem(KEY, v); } catch (e) {} } };

  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  // Consent Mode v2: tutto negato finché l'utente non accetta
  gtag('consent', 'default', { ad_storage: 'denied', analytics_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied', wait_for_update: 500 });

  var loaded = false;
  function load() {
    if (loaded) return; loaded = true;
    gtag('consent', 'update', { analytics_storage: 'granted' });
    window.dataLayer.push({ 'gtm.start': Date.now(), event: 'gtm.js' });
    var s = document.createElement('script');
    s.async = true; s.src = 'https://www.googletagmanager.com/gtm.js?id=' + encodeURIComponent(id);
    document.head.appendChild(s);
    if (cid) {   // Clarity: snippet ufficiale senza codice inline, solo dopo il consenso
      window.clarity = window.clarity || function () { (window.clarity.q = window.clarity.q || []).push(arguments); };
      window.clarity('consentv2', { ad_Storage: 'denied', analytics_Storage: 'granted' });
      var c = document.createElement('script'); c.async = true; c.src = 'https://www.clarity.ms/tag/' + encodeURIComponent(cid);
      document.head.appendChild(c);
    }
  }
  function show() { if (box) box.hidden = false; }
  function hide() { if (box) box.hidden = true; }

  var v = store.get();
  if (v === 'granted') load(); else if (v !== 'denied') show();

  if (box) box.addEventListener('click', function (e) {
    var b = e.target.closest && e.target.closest('[data-ck]'); if (!b) return;
    var grant = b.getAttribute('data-ck') === 'grant';
    store.set(grant ? 'granted' : 'denied'); hide();
    if (grant) load(); else if (loaded) location.reload();   // se ritira il consenso dopo averlo dato, si ricarica senza GTM
  });
  // «Preferenze cookie» nel piè di pagina
  [].forEach.call(document.querySelectorAll('[data-ck-open]'), function (b) { b.addEventListener('click', show); });
})();
