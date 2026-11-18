#!/usr/bin/env python3
"""Builds the static pages from src/*.html (body only) + one shared shell.
Front matter: first lines 'key: value' until a blank line. Run: python tools/build.py"""
import pathlib, html

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / 'src'
BASE = 'https://thebifold-site.vercel.app'
BOOK = 'https://www.thebifold.com/event/bi-one-get-one-black-friday/#em-event-booking-form'

NAV_L = [('events', '/events', 'The next party'), ('about', '/about', 'Your hosts'), ('guide', '/guide', 'Before you go')]
NAV_R = [('faq', '/faq', 'FAQ'), ('contact', '/contact', 'Contact')]
ARROW = '<svg viewBox="0 0 16 16" aria-hidden="true" focusable="false"><path d="M2 8h11M9 4l4 4-4 4" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'


def nav(items, cur):
    return ''.join(f'<a href="{h}"{" aria-current=\"page\"" if k == cur else ""}>{t}</a>' for k, h, t in items)


def shell(meta, body):
    cur = meta.get('nav', '')
    title = meta['title']
    desc = meta['description']
    path = meta['path']
    url = BASE + (path if path != '/' else '/')
    gate = '' if meta.get('gate') == 'no' else GATE
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="The BiFold">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}/assets/img/welcome-table-1200.webp">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#f6e9e2">
<meta name="rating" content="adult">
<link rel="icon" href="/assets/img/favicon-32.webp" type="image/webp">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="preload" href="/assets/fonts/bodoni-moda-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/instrument-sans-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/site.css">
<script src="/assets/head.js"></script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{gate}<header class="masthead" id="site-header">
  <div class="wrap masthead__row">
    <nav class="nav nav--left" aria-label="Main">{nav(NAV_L, cur)}</nav>
    <a class="wordmark" href="/"><span class="wordmark__name">The <i>Bi</i>Fold</span><span class="wordmark__tag">Open on both sides</span></a>
    <nav class="nav nav--right" aria-label="More">{nav(NAV_R, cur)}<a class="btn btn--small masthead__cta" href="{BOOK}">Request access</a></nav>
    <button class="menu-btn" id="menu-btn" type="button" aria-expanded="false" aria-controls="mobile-nav"><i class="menu-btn__mark" aria-hidden="true"></i><span>Menu</span></button>
  </div>
  <nav class="wrap mobile-nav" id="mobile-nav" aria-label="Mobile">{nav(NAV_L + NAV_R, cur)}<a class="mobile-nav__cta" href="{BOOK}">Request access</a></nav>
</header>
<main id="main">
{body}
</main>
{FOOTER.replace('{PARTNERS}', PARTNERS)}
<aside class="dock" id="dock" aria-label="Next party"><p><b>Fri, Nov 27 · Bi One, Get One</b>Screened · 21+ · Design District</p><a class="btn btn--small" href="{BOOK}">Request access</a></aside>
<script src="/assets/site.js" defer></script>
</body>
</html>
'''


PARTNERS = ''

TARIFF = '''<ul class="tariff" aria-label="Donation to attend, by guest type">
          <li><span class="tariff__name">Couple</span><span class="tariff__dots"></span><span class="tariff__price num">$150</span><span class="tariff__help">One donation per couple.</span></li>
          <li><span class="tariff__name">Single man</span><span class="tariff__dots"></span><span class="tariff__price num">$175</span><span class="tariff__help">One donation per person.</span></li>
          <li><span class="tariff__name">Single woman</span><span class="tariff__dots"></span><span class="tariff__price num">$0.01</span><span class="tariff__help">Not a fee — just so we can screen every guest.</span></li>
          <li><span class="tariff__name">Cabana add-on</span><span class="tariff__dots"></span><span class="tariff__price num">$50</span><span class="tariff__help">Add-on — you still need an entry donation. Only 3.</span></li>
        </ul>'''

GATE = '''<div class="gate" id="gate" role="dialog" aria-modal="true" aria-label="The BiFold — adults only" hidden>
  <span class="gate__space" aria-hidden="true"></span>
  <div class="gate__mark wordmark" aria-hidden="true"><span class="wordmark__name">The <i>Bi</i>Fold</span></div>
  <div class="gate__choices">
    <button class="gate__btn gate__btn--yes" id="gate-yes" type="button"><span class="gate__big">I'm 21<span class="plus">+</span></span><span class="gate__small">Adult bi parties</span></button>
    <a class="gate__btn gate__btn--no" id="gate-no" href="https://google.com" rel="nofollow"><span class="gate__big">Leave</span></a>
  </div>
</div>
'''

FOOTER = f'''<footer class="colophon" id="site-footer">
  <div class="flap" aria-hidden="true"><span class="seal seal--mono">B</span></div>
  <div class="wrap colophon__card">
    <p class="wordmark colophon__mark"><span class="wordmark__name">The <i>Bi</i>Fold</span><span class="wordmark__tag">Open on both sides</span></p>
    <p class="colophon__blurb">Monthly, screened, consent-first parties for bisexual and bi&#8209;curious adults in the Dallas Design District.</p>
    <nav class="colophon__links" aria-label="Site index"><a href="/events">The next party</a> <a href="/about">Your hosts</a> <a href="/guide">Before you go</a> <a href="/faq">FAQ</a> <a href="/standards">Standards</a> <a href="/dress-code">Dress code</a> <a href="/privacy">Privacy</a> <a href="/terms">Terms</a> <a href="/partners">Partners</a> <a href="/contact">Contact</a></nav>
    <ul class="colophon__contact"><li>Design District, Dallas</li><li>Typically 9 pm to 2 am</li><li><a href="tel:+12146999655">(214)&nbsp;699-9655</a></li><li><a href="mailto:admin@thebifold.com">admin@thebifold.com</a></li></ul>
    <div class="colophon__fine"><p>© 2026 The BiFold. Adults only.</p><p>Spots, donations and approval are handled on our <a class="nowrap" href="{BOOK}">secure booking page</a>.</p></div>
  </div>
</footer>'''


def parse(p):
    raw = p.read_text(encoding='utf-8')
    head, _, body = raw.partition('\n\n')
    meta = {}
    for line in head.splitlines():
        k, _, v = line.partition(':')
        meta[k.strip()] = v.strip()
    body = body.replace('{TARIFF}', TARIFF).replace('{BOOK}', BOOK).replace('{ARROW}', ARROW)
    return meta, body


def main():
    for p in sorted(SRC.glob('*.html')):
        meta, body = parse(p)
        out = ROOT / meta['file']
        out.write_text(shell(meta, body.rstrip() + '\n'), encoding='utf-8', newline='\n')
        print('built', out.name)


if __name__ == '__main__':
    main()
