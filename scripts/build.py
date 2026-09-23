from datetime import date
from pathlib import Path
import html
import json
import shutil

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'dist'
BASE = 'https://luongnv.com/time-echo-website/'
EMAIL = 'lamnv260398@gmail.com'
ISSUES = 'https://github.com/nguyenvanlamm/time-echo-website/issues'


def page(name, title, description, body, json_ld=None, noindex=False):
    nav = ''.join(f'<a href="{url}"' + (' aria-current="page"' if url == name else '') + f'>{label}</a>' for url, label in [('index.html#how-it-works', 'How to play'), ('support.html', 'Support'), ('changelog.html', 'Changelog')])
    path = '' if name == 'index.html' else name
    robots = '<meta name="robots" content="noindex">' if noindex else ''
    ld = ''.join(f'<script type="application/ld+json">{json.dumps(block, ensure_ascii=False)}</script>' for block in (json_ld or []))
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)} — Time Echo</title><meta name="description" content="{html.escape(description, quote=True)}">{robots}
<meta name="theme-color" content="#0b0e14"><link rel="canonical" href="{BASE}{path}">
<meta property="og:type" content="website"><meta property="og:site_name" content="Time Echo"><meta property="og:locale" content="en_US"><meta property="og:title" content="{html.escape(title, quote=True)} — Time Echo"><meta property="og:description" content="{html.escape(description, quote=True)}"><meta property="og:url" content="{BASE}{path}"><meta property="og:image" content="{BASE}assets/social.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="Time Echo preview: your violet echo holds a switch while you head for the golden exit."><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{html.escape(title, quote=True)} — Time Echo"><meta name="twitter:description" content="{html.escape(description, quote=True)}"><meta name="twitter:image" content="{BASE}assets/social.png"><meta name="twitter:image:alt" content="Time Echo preview: your violet echo holds a switch while you head for the golden exit.">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="assets/app-icon.png"><link rel="preload" href="assets/Baloo2-Regular.ttf" as="font" type="font/ttf" crossorigin><link rel="stylesheet" href="assets/site.css"><script src="assets/site.js" defer></script>{ld}</head>
<body><a class="skip" href="#main">Skip to content</a><header class="header wrap"><a class="brand" href="index.html" aria-label="Time Echo home"><span class="brand-mark" aria-hidden="true"><i></i><i></i></span>time echo<span class="brand-dot">.</span></a><nav aria-label="Main navigation">{nav}</nav><span class="nav-status"><i></i> Coming soon</span></header>
<main id="main">{body}</main><footer class="wrap footer"><a class="brand" href="index.html">time echo<span class="brand-dot">.</span></a><p>A little planning. A few past selves.</p><nav aria-label="Footer navigation"><a href="support.html">Support & feedback</a><a href="privacy.html">Privacy & data</a><a href="changelog.html">Changelog</a></nav><small>© 2026 Time Echo</small></footer></body></html>'''


def intro(kicker, heading, desc):
    return f'<section class="page-intro wrap"><p class="eyebrow">{kicker}</p><h1>{heading}</h1><p class="lead">{desc}</p></section>'


def board():
    # Reconstructed from the game's level 03, not a screenshot or a separate game engine.
    rows = ['#########', '#S..b...#', '#####D###', '#......F#', '#########']
    tiles = ''
    for y, row in enumerate(rows):
        for x, cell in enumerate(row):
            kind = {'#':'wall', 'b':'switch', 'D':'door', 'F':'goal'}.get(cell, 'floor')
            tiles += f'<span class="tile {kind}" data-x="{x}" data-y="{y}">' + ('<i></i>' if cell in 'bDF' else '') + '</span>'
    return f'''<div class="board-scene" id="preview"><div class="scene-heading"><span><i class="live-dot"></i> THE DOOR KEEPER</span><span>LEVEL 03 / 80</span></div><div class="board" role="img" aria-label="Level 3 illustration. Your violet echo holds a switch while your cyan character passes through the door to the golden exit.">{tiles}<span class="actor echo" aria-hidden="true"></span><span class="actor player" aria-hidden="true"></span></div><div class="board-legend"><span><i class="cyan"></i>You, now</span><span><i class="violet"></i>Your echo</span><span><i class="gold"></i>The way out</span></div><div class="demo-caption"><span class="step-counter">01 / 03</span><p id="demo-caption">First, walk to the switch.</p><button id="demo-next" class="round-button" aria-label="Show the next step of the gameplay preview">→</button></div><p class="preview-note">An illustrated loop. Tap the arrow to see what happens.</p></div>'''

faqs = [
('What is Time Echo?', 'A single-player puzzle game where you cooperate with recordings of your own moves. Each rewind creates an echo that retraces your previous route.'),
('Do I need quick reflexes?', 'No. Each move advances the board by one step. You have a limited number of steps per loop, but you can take as long as you like to choose them.'),
('Can I play without the internet?', 'Yes. All 80 levels work offline. Progress and settings are saved on your device.'),
('What if I make a mistake?', 'Undo a move or rewind and try a different plan. You can also choose another unlocked level and come back later.'),
('When can I download it?', 'Time Echo is coming to iOS and Android. A release date has not been announced. Download links will appear here when available.'),
('Does the game have ads or accounts?', 'The current version has no ads, in-app purchases, or accounts. You can simply play.')]

home = f'''<section class="hero wrap"><div class="hero-copy"><p class="eyebrow"><span class="tiny-orbit"></span> A PUZZLE GAME ABOUT YOU. AND YOU.</p><h1>Your best<br>teammate is<br>your <em>past self.</em></h1><p class="lead">Make your move. Rewind time. Team up with your echoes to find a way through.</p><div class="hero-actions"><span class="coming"><span aria-hidden="true">◷</span><span>Coming soon<small>for iOS & Android</small></span></span><a class="text-link" href="#how-it-works">Discover the loop <span aria-hidden="true">↘</span></a></div><p class="hero-footnote">Made for curious minds. Played at your own pace.</p></div><div class="hero-art"><div class="orbit orbit-one"></div><div class="orbit orbit-two"></div><span class="art-label">A LITTLE HELP FROM YESTERDAY</span>{board()}<span class="floating-note"><span aria-hidden="true">↶</span> This time, you have backup.</span></div></section>
<section class="facts wrap" aria-label="Game at a glance"><div><strong>80</strong><span>handcrafted levels</span></div><div><strong>12</strong><span>chapters to unravel</span></div><div><strong>100%</strong><span>playable offline</span></div><div><span class="fact-symbol" aria-hidden="true">∞</span><span>time to think</span></div></section>
<section class="section wrap premise"><div><p class="eyebrow">ONE PLAYER. A WHOLE TEAM OF YOU.</p><h2>Leave yourself<br>a helping hand.</h2></div><div><p class="large-copy">That door needs someone on the switch.<br>Luckily, you’ve been here before.</p><p>Every rewind turns your last run into an echo that repeats your moves. Let your past self hold the door while you head for the exit. Then take that idea a few loops further.</p><a class="text-link" href="#how-it-works">See how it works <span aria-hidden="true">↗</span></a></div></section>
<section class="section wrap"><div class="section-heading"><p class="eyebrow">SMALL MOVES. SATISFYING POSSIBILITIES.</p><h2>For the joy of<br><em>figuring it out.</em></h2></div><div class="benefits"><article><span class="feature-art path-art" aria-hidden="true">···<b>●</b>···<i>◎</i></span><h3>Think one self ahead.</h3><p>Layer your routes across time. Buttons, boxes, keys, and pits turn a simple path into a shared plan.</p></article><article><span class="feature-art echo-art" aria-hidden="true"><i></i><i></i><i></i></span><h3>Let the idea click.</h3><p>Learn one rule at a time, then combine them across twelve chapters. Later puzzles bring up to five echoes along.</p></article><article><span class="feature-art pause-art" aria-hidden="true">Ⅱ</span><h3>Take your time.</h3><p>The board moves when you do. Undo a step, rethink a route, or put your phone down. No connection needed.</p></article></div></section>
<section class="section how-section" id="how-it-works"><div class="wrap"><div class="section-heading"><p class="eyebrow">MEET YOUR NEXT GOOD IDEA</p><h2>Move. Rewind. <em>Rethink.</em></h2><p>Three little steps. A whole new way through.</p></div><ol class="steps"><li><span class="step-icon">01 <b aria-hidden="true">→</b></span><h3>Make a move.</h3><p>Walk to a switch or put a box in place. Every step becomes part of your echo’s route.</p></li><li><span class="step-icon">02 <b aria-hidden="true">↶</b></span><h3>Leave an echo.</h3><p>Rewind to the start. Your past self now repeats the moves you just made.</p></li><li><span class="step-icon">03 <b aria-hidden="true">◎</b></span><h3>Find your way out.</h3><p>Move alongside your echo. Let it do its part while you take the next step toward the goal.</p></li></ol><a class="text-link" href="#preview">Explore the illustrated loop <span aria-hidden="true">↑</span></a></div></section>
<section class="section wrap faq"><div><p class="eyebrow">BEFORE YOUR FIRST LOOP</p><h2>A few good<br>questions.</h2><p>Still curious? <a href="support.html">Get in touch.</a></p></div><div class="questions">''' + ''.join(f'<details><summary>{q}<span aria-hidden="true">+</span></summary><p>{a}</p></details>' for q,a in faqs) + '''</div></section><section class="wrap final-cta"><span class="tiny-orbit" aria-hidden="true"></span><p class="eyebrow">SEE YOU IN THE NEXT LOOP</p><h2>Good things take <em>a little time.</em></h2><p>Time Echo is coming soon to iOS & Android.</p><a class="button" href="changelog.html">Explore what’s coming <span aria-hidden="true">↗</span></a></section>'''

support = intro('WE’RE HERE TO HELP', 'Every good loop<br>starts with <em>feedback.</em>', 'A stuck puzzle, an unexpected bug, or an idea for the next chapter. Tell us what’s on your mind.') + f'''<section class="wrap support-grid"><div><h2>Start a conversation.</h2><p>These guided forms open in our website’s GitHub repository. You’ll need a free GitHub account. Reports are public, so keep personal information out of them.</p><div class="support-options"><a href="{ISSUES}/new?template=bug_report.yml"><span class="option-icon">↯</span><span><strong>Report a bug</strong><small>Help us retrace what happened.</small></span><span>↗</span></a><a href="{ISSUES}/new?template=feature_request.yml"><span class="option-icon">✧</span><span><strong>Suggest a feature</strong><small>A little idea for a future loop.</small></span><span>↗</span></a><a href="{ISSUES}/new?template=feedback.yml"><span class="option-icon">◎</span><span><strong>Share feedback</strong><small>Questions and thoughts are welcome.</small></span><span>↗</span></a></div><div class="help-note"><h3>Stuck on a level?</h3><p>Try planning where your echo should end its route. Sometimes its job is simply to stay on a switch. Include the level number if you’d like help.</p></div><p class="small">You can also <a href="{ISSUES}">browse existing reports</a>.</p></div><div class="email-panel"><p class="eyebrow">PREFER EMAIL?</p><h2>Send us a note.</h2><p>No GitHub account needed. This form prepares a draft in your email app; you review and send it yourself.</p><form id="support-form"><label for="topic">What’s it about?</label><select id="topic" name="topic"><option>Game support</option><option>Bug report</option><option>Feature idea</option><option>General feedback</option><option>Privacy request</option></select><label for="device">Device & app version <span>(optional)</span></label><input id="device" name="device" maxlength="120" placeholder="e.g. iPhone 15, iOS 26, Time Echo 1.0.0"><label for="message">Your message</label><textarea id="message" name="message" rows="6" required minlength="10" maxlength="1800" placeholder="Tell us what happened, or share your idea…"></textarea><p class="small">Your message is not stored by this website. See our <a href="privacy.html#support-data">support privacy details</a>.</p><button class="button" type="submit">Prepare email <span aria-hidden="true">↗</span></button><p id="form-status" role="status" class="small"></p><a id="email-draft" hidden>Open email draft</a><button class="text-link" type="button" id="copy-message">Copy message instead</button><noscript><p>This form needs JavaScript to prepare a draft. Email us directly using the link below.</p></noscript></form><p class="email-direct">Or email <a href="mailto:{EMAIL}">{EMAIL}</a></p></div></section>'''

privacy = intro('YOUR GAME. YOUR DEVICE.', 'Privacy, <em>plain and simple.</em>', 'The Time Echo game works offline. Your progress belongs on your device.') + f'''<div class="wrap document-layout"><aside><p class="eyebrow">ON THIS PAGE</p><a href="#game-data">The game</a><a href="#local-data">Local data</a><a href="#website-data">This website</a><a href="#support-data">Support messages</a><a href="#your-choices">Your choices</a><a href="#contact">Contact</a></aside><article class="prose"><p class="policy-meta">Last updated: September 22, 2026 · Applies to Time Echo and this website</p><div class="privacy-summary"><strong>No game accounts. No advertising. No analytics in the app.</strong><p>The game does not send your gameplay or personal information to us. Visiting this website or choosing to contact us involves the services described below.</p></div><h2 id="game-data">1. Data in the game</h2><p>Time Echo is an offline puzzle game, identified on Android as <code>com.nguyenvanlam.time_echo</code>. The app does not collect or transmit personal information, device identifiers, location, or gameplay analytics to the developer. It has no accounts, advertising services, or tracking SDKs.</p><h2 id="local-data">2. What stays on your device</h2><p>The app saves completed levels and best loop counts, tutorial completion, your language preference, and sound and haptic settings in local app storage. This lets you continue playing and keep your preferences between sessions.</p><p>We do not operate a server that receives this data. Device or operating-system backups may include app data according to your device settings; those backups are managed by your platform provider.</p><p>The game does not ask to access your contacts, photos, camera, microphone, or location.</p><h2 id="website-data">3. Visiting this website</h2><p>This website does not add analytics, advertising trackers, cookies, or browser storage. Fonts and artwork are hosted with the site.</p><p>The website is hosted on GitHub Pages. GitHub logs visitors’ IP addresses for security purposes and processes technical information under its own <a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement">privacy statement</a>. See <a href="https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages">GitHub Pages hosting information</a>.</p><h2 id="support-data">4. Support, reports, and feedback</h2><p>Contacting us is optional. If you send an email, we receive your email address, the message, and any attachments you choose to send. We use this information to respond and investigate your request. Email is handled by our email provider, Gmail, under <a href="https://policies.google.com/privacy">Google’s privacy policy</a>.</p><p>The email form builds a draft locally in your browser. It does not upload your message to a website server or send email automatically. Your email provider processes the draft and message when you use it.</p><p>If you open a GitHub issue, your username, report, comments, and any attachments are public. GitHub processes them under its privacy statement. Do not include passwords, private contact details, or sensitive personal information in a public issue.</p><p>Support correspondence is kept while needed to handle your request and any follow-up, or where required by law. Public issues remain visible as a record of reports and fixes unless removed. You can request deletion of correspondence or personal information you have shared by emailing us; GitHub and email providers manage their own retention and backups.</p><h2 id="your-choices">5. Your choices and deletion</h2><p>You can reset game progress in the game’s Settings. To remove local app data and preferences, delete the app (rather than offloading it on iOS), or clear its app data where your operating system supports that. Manage device backups separately in your platform’s settings.</p><p>There is no game account to delete. To ask about, correct, or request deletion of personal information in support messages, contact <a href="mailto:{EMAIL}">{EMAIL}</a>. For information GitHub processes, use GitHub’s privacy controls or contact GitHub.</p><h2>6. Children’s privacy</h2><p>The game does not collect personal information from any player, including children. A parent or guardian should help a child contact support, and can contact us about personal information shared in a support request.</p><h2>7. Changes to this policy</h2><p>We will update this page and its date when our data practices change. Any future app features that change how data is handled will be reflected here.</p><h2 id="contact">8. Contact</h2><p>For Time Echo privacy questions, contact the developer at <a href="mailto:{EMAIL}">{EMAIL}</a>. You can also use the email form on our <a href="support.html">support page</a>.</p></article></div>'''

changelog = intro('THE STORY SO FAR', 'Every loop,<br><em>a little better.</em>', 'New puzzles, thoughtful refinements, and the details that make a difference.') + '''<section class="wrap changelog"><div class="release-meta"><span class="release-status">IN PREPARATION</span><p>Version 1.0.0</p><small>Public release coming soon</small></div><article class="release"><p class="eyebrow">THE FIRST CHAPTER</p><h2>Your past self has your back.</h2><p>Our initial release brings the full Time Echo campaign to your pocket. These are the features in the current build; the app is not yet publicly available.</p><h3>A puzzle that remembers your moves</h3><ul><li>80 handcrafted levels across twelve chapters.</li><li>Time loops that turn your previous routes into helpful echoes.</li><li>Switches, doors, boxes, keys, and pits to plan around.</li><li>Later levels with up to six loops and five echoes.</li></ul><h3>Room to think</h3><ul><li>Step-by-step movement, undo, and manual rewind.</li><li>An introductory tutorial and local progress saving.</li><li>Portrait and landscape layouts.</li><li>English and Vietnamese language options.</li><li>Sound and haptic settings.</li><li>Offline play without accounts, ads, or in-app purchases.</li></ul><a class="text-link" href="support.html">Share an idea for the next loop <span aria-hidden="true">↗</span></a></article></section>'''

def crumbs(label, name):
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': BASE},
        {'@type': 'ListItem', 'position': 2, 'name': label, 'item': BASE + name}]}

home_ld = [
    {'@context': 'https://schema.org', '@type': 'Organization', 'name': 'Time Echo', 'url': BASE,
     'logo': BASE + 'assets/app-icon.png', 'email': EMAIL,
     'sameAs': ['https://github.com/nguyenvanlamm/time-echo-website']},
    {'@context': 'https://schema.org', '@type': 'WebSite', 'name': 'Time Echo', 'url': BASE},
    {'@context': 'https://schema.org', '@type': 'VideoGame', 'name': 'Time Echo', 'url': BASE,
     'description': 'An offline puzzle game about teaming up with your past selves. 80 levels, twelve chapters. Coming soon to iOS and Android.',
     'applicationCategory': 'GameApplication', 'operatingSystem': 'iOS, Android',
     'gamePlatform': ['iOS', 'Android'], 'playMode': 'SinglePlayer',
     'image': BASE + 'assets/social.png',
     'author': {'@type': 'Organization', 'name': 'Time Echo', 'url': BASE}},
    {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faqs]}]

pages = [('index.html', 'Your best teammate is your past self', 'An offline puzzle game about teaming up with your past selves. 80 levels, twelve chapters. Coming soon to iOS and Android.', home, home_ld), ('support.html', 'Support & feedback', 'Get help with Time Echo, report a bug, suggest a feature, or contact the developer by email.', support, [crumbs('Support', 'support.html')]), ('privacy.html', 'Privacy & data', 'How Time Echo handles local game progress, preferences, website visits, and support messages.', privacy, [crumbs('Privacy & data', 'privacy.html')]), ('changelog.html', 'Changelog', 'Explore what is coming in Time Echo 1.0.0 and follow future game updates.', changelog, [crumbs('Changelog', 'changelog.html')])]
if OUT.exists():
    shutil.rmtree(OUT)
OUT.mkdir()
shutil.copytree(ROOT / 'assets', OUT / 'assets')
for name, title, description, body, ld in pages:
    (OUT / name).write_text(page(name, title, description, body, ld))
(OUT / '404.html').write_text(page('404.html', 'Page not found', 'The page you are looking for could not be found. Head back to the Time Echo homepage.', intro('A SMALL DETOUR', 'This loop leads<br><em>somewhere else.</em>', 'That page could not be found. Head back to the beginning.') + '<div class="wrap"><a class="button" href="/time-echo-website/">Return to Time Echo</a></div>', [crumbs('Page not found', '404.html')], noindex=True))
# Absolute assets make the fallback work for unknown nested URLs on GitHub Pages.
p = OUT / '404.html'
p.write_text(p.read_text().replace('href="assets/', 'href="/time-echo-website/assets/').replace('src="assets/', 'src="/time-echo-website/assets/').replace('href="index.html', 'href="/time-echo-website/index.html').replace('href="support.html', 'href="/time-echo-website/support.html').replace('href="privacy.html', 'href="/time-echo-website/privacy.html').replace('href="changelog.html', 'href="/time-echo-website/changelog.html'))
(OUT / '.nojekyll').touch()
(OUT / 'robots.txt').write_text(f'''User-agent: *
Allow: /

# AI search, retrieval, and training crawlers are explicitly allowed.
User-agent: GPTBot
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Claude-SearchBot
Allow: /

User-agent: Claude-User
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Perplexity-User
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: Applebot-Extended
Allow: /

User-agent: Meta-ExternalAgent
Allow: /

User-agent: CCBot
Allow: /

User-agent: Bytespider
Allow: /

User-agent: Amazonbot
Allow: /

User-agent: DuckAssistBot
Allow: /

User-agent: MistralAI-User
Allow: /

User-agent: DeepSeekBot
Allow: /

User-agent: cohere-training-data-crawler
Allow: /

Sitemap: {BASE}sitemap.xml
''')
(OUT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join(f'<url><loc>{BASE}{"" if p[0] == "index.html" else p[0]}</loc><lastmod>{date.today()}</lastmod></url>' for p in pages) + '</urlset>')
(OUT / 'llms.txt').write_text(f'''# Time Echo

> Official website for Time Echo — an offline puzzle game where you team up with echoes of your past moves. 80 handcrafted levels across twelve chapters. Coming soon to iOS and Android.

## Pages

- [Time Echo]({BASE}): Game overview, how the time-loop mechanic works, and FAQ
- [Support & feedback]({BASE}support.html): Report bugs, suggest features, or email the developer at {EMAIL}
- [Privacy & data]({BASE}privacy.html): What the game and this website store, and your choices
- [Changelog]({BASE}changelog.html): What is coming in version 1.0.0

## Optional

- [Source repository](https://github.com/nguyenvanlamm/time-echo-website): Static site generated by scripts/build.py, deployed via GitHub Pages
''')
print(f'Built {len(pages) + 1} pages in {OUT}')
