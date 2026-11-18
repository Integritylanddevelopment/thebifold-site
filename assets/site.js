/* The BiFold — small, additive behaviour. No network calls, nothing stored but the two gate keys. */
(function () {
  'use strict';
  var KEY_OPENED = 'crapp:thebifold:opened';
  var KEY_MODE = 'crapp:thebifold:mode';
  var EMAIL = 'admin@thebifold.com';
  var doc = document.documentElement;

  function read(k) { try { return window.localStorage.getItem(k); } catch (e) { return null; } }
  function write(k, v) { try { window.localStorage.setItem(k, v); } catch (e) { /* storage blocked: gate shows next visit, which is correct */ } }

  doc.classList.add('js');

  /* ---------- Age gate (first-open screen: two buttons) ---------- */
  var gate = document.getElementById('gate');
  var shell = ['site-header', 'main', 'site-footer', 'dock'];
  function setInert(on) {
    shell.forEach(function (id) {
      var el = document.getElementById(id);
      if (!el) return;
      if (on) { el.setAttribute('inert', ''); el.setAttribute('aria-hidden', 'true'); }
      else { el.removeAttribute('inert'); el.removeAttribute('aria-hidden'); }
    });
  }
  function closeGate() {
    write(KEY_OPENED, '1');
    write(KEY_MODE, 'adult');
    gate.hidden = true;
    doc.classList.remove('gate-open');
    doc.classList.remove('gate-pending');
    setInert(false);
    var main = document.getElementById('main');
    if (main) { main.setAttribute('tabindex', '-1'); main.focus({ preventScroll: true }); }
  }
  if (gate) {
    var passed = read(KEY_OPENED) === '1' && read(KEY_MODE) === 'adult';
    if (!passed) {
      gate.hidden = false;
      doc.classList.add('gate-open');
      setInert(true);
      var yes = document.getElementById('gate-yes');
      var no = document.getElementById('gate-no');
      if (yes) { yes.addEventListener('click', closeGate); yes.focus(); }
      gate.addEventListener('keydown', function (e) {
        if (e.key !== 'Tab' || !yes || !no) return;
        if (e.shiftKey && document.activeElement === yes) { e.preventDefault(); no.focus(); }
        else if (!e.shiftKey && document.activeElement === no) { e.preventDefault(); yes.focus(); }
      });
    }
  }

  /* ---------- Hero unfold (class added by JS only; content visible without it) ---------- */
  var spread = document.querySelector('[data-unfold]');
  if (spread) {
    spread.classList.add('unfold');
    /* once unfolded, drop the class so a resize or re-layout can never replay it */
    window.setTimeout(function () { spread.classList.remove('unfold'); }, 900);
  }

  /* ---------- Mobile dock: only once the first screen has scrolled away ---------- */
  var dock = document.getElementById('dock');
  var first = document.querySelector('main > section');
  if (dock && first && 'IntersectionObserver' in window) {
    doc.classList.add('dock-managed');
    new IntersectionObserver(function (en) { dock.classList.toggle('is-on', !en[0].isIntersecting); }, { rootMargin: '-120px 0px 0px 0px' }).observe(first);
  }

  /* ---------- Mobile menu ---------- */
  var btn = document.getElementById('menu-btn');
  var panel = document.getElementById('mobile-nav');
  if (btn && panel) {
    btn.addEventListener('click', function () {
      var open = btn.getAttribute('aria-expanded') === 'true';
      btn.setAttribute('aria-expanded', open ? 'false' : 'true');
      btn.querySelector('span').textContent = open ? 'Menu' : 'Close';
      panel.classList.toggle('is-open', !open);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && btn.getAttribute('aria-expanded') === 'true') { btn.click(); btn.focus(); }
    });
  }

  /* ---------- Mail-composer forms (guest list + contact) ---------- */
  var EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
  function val(form, name) { var el = form.elements[name]; return el ? String(el.value || '').trim() : ''; }
  function say(form, kind, text) {
    var s = form.querySelector('.status');
    if (!s) return;
    s.setAttribute('data-kind', kind);
    s.textContent = text;
  }
  Array.prototype.forEach.call(document.querySelectorAll('form[data-mail]'), function (form) {
    var radios = form.querySelectorAll('input[name="intent"]');
    function sync() {
      var r = form.querySelector('input[name="intent"]:checked'); if (!r) return;
      Array.prototype.forEach.call(form.querySelectorAll('[data-for]'), function (el) { el.hidden = el.getAttribute('data-for') !== r.value; });
      var b = form.querySelector('button[type="submit"]');
      if (b && b.getAttribute('data-label-' + r.value)) b.textContent = b.getAttribute('data-label-' + r.value);
    }
    Array.prototype.forEach.call(radios, function (r) { r.addEventListener('change', sync); });
    sync();
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var email = form.elements.email;
      var v = val(form, 'email');
      if (!v) { email.setAttribute('aria-invalid', 'true'); email.focus(); say(form, 'err', 'Add your email so we can reach you.'); return; }
      if (!EMAIL_RE.test(v)) { email.setAttribute('aria-invalid', 'true'); email.focus(); say(form, 'err', 'That email looks off — check for a typo.'); return; }
      email.removeAttribute('aria-invalid');
      var intent = form.querySelector('input[name="intent"]:checked');
      var kind = intent ? (intent.value === 'question' ? 'contact' : 'guestlist') : form.getAttribute('data-mail');
      var lines = [];
      Array.prototype.forEach.call(form.querySelectorAll('input, textarea'), function (el) {
        if (!el.name || el.type === 'hidden' || el.type === 'radio') return;
        if (el.closest('[hidden]')) return;
        var label = el.getAttribute('data-label') || el.name;
        var x = String(el.value || '').trim();
        lines.push(label + ': ' + (x || '—'));
      });
      var subject = kind === 'guestlist' ? 'Guest list — please add me' : 'Question for the hosts';
      var body = (kind === 'guestlist' ? 'Hi Summer & Mike, please add me to The BiFold guest list.\n\n' : 'Hi Summer & Mike,\n\n') + lines.join('\n') + '\n';
      var href = 'mailto:' + EMAIL + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
      say(form, 'ok', kind === 'guestlist'
        ? 'Your email app should open with your details filled in. Press send and you’re on the list.'
        : 'Your email app should open with your message filled in. Press send and we’ll reply.');
      var fallback = form.querySelector('.mail-fallback');
      if (fallback) { fallback.hidden = false; }
      window.location.href = href;
    });
  });
})();
