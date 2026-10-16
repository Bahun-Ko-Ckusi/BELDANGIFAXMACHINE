"""Writes the Terms of Service and Privacy Policy into BOTH sites from one text,
so the game site and the company site never say different things."""
import pathlib, sys

UPDATED = "October 16, 2026"
MAIL = '<a href="mailto:beldangifaxmachine@gmail.com">beldangifaxmachine@gmail.com</a>'
GAME_SITE = "https://bahun-ko-ckusi.github.io/toadstoolweblink/"
CO_SITE = "https://beldangifaxmachine.com/"

TERMS = f"""
<p>These terms cover the video game <strong>Toadstool</strong>, also shown in the game as
&ldquo;Toadstool Labs&rdquo; (the &ldquo;game&rdquo;), including early access, and our websites:
the <a href="{GAME_SITE}">Toadstool site</a> and the <a href="{CO_SITE}">Beldangi Fax Machine LC
site</a>. The game and the sites are made and published by <strong>Beldangi Fax Machine LC</strong>,
a Vermont limited liability company (&ldquo;we&rdquo;, &ldquo;us&rdquo;).</p>
<p>By buying, installing or playing the game, or by using our websites, you agree to these
terms. If you don&rsquo;t agree, don&rsquo;t play the game or use the sites.</p>

<div class="notice" role="note">
  <p><strong>Adults only (18+).</strong> Toadstool depicts the growing and use of psilocybin
  mushrooms and other drugs, and some scenes have intense flashing colours and heavy visual
  distortion. It is a work of fiction. Never eat a wild mushroom because of anything you saw in
  the game.</p>
</div>

<h2 id="age">1. You must be 18 or older</h2>
<p>Toadstool is made for adults aged 18 and over. You may only buy, download or play it if you
are at least 18 and old enough to enter into these terms where you live. If you are under 18,
do not play the game.</p>

<h2 id="age-notice">2. How we tell players about the age limit</h2>
<p>We make the age limit clear before anyone pays and every time the game starts:</p>
<ul>
  <li><strong>Before you buy.</strong> Our websites and the game&rsquo;s store page state that
  Toadstool is for adults 18 and over and describe its mature content.</li>
  <li><strong>On Steam.</strong> Toadstool is marked as mature content on Steam. Steam asks for
  a date of birth before showing mature store pages, lets parents and guardians block mature
  games with Steam&rsquo;s family and parental controls, and may require extra age checks in
  some countries. Purchases and accounts are also subject to the Steam Subscriber Agreement.</li>
  <li><strong>Every time the game starts.</strong> Before the main menu, the game shows a
  &ldquo;Content Warning &ndash; 18+&rdquo; screen stating that the game is for adults aged 18
  or older, that it depicts psilocybin and other drugs, that it does not encourage illegal
  activity, and that it contains intense flashing effects.</li>
</ul>
<p>We do not collect ID or verify anyone&rsquo;s age ourselves, and Steam&rsquo;s checks rely in
part on information people give about themselves. Account holders are responsible for who uses
their Steam account. Parents and guardians: please use Steam&rsquo;s family controls to keep
mature games away from children.</p>

<h2 id="content">3. Drug content is fiction, not advice</h2>
<p>Toadstool is a realistic psychology and mycology simulation. It depicts the growing and use of
psilocybin (&ldquo;magic&rdquo;) mushrooms and other drugs.</p>
<p>Psilocybin is a Schedule I controlled substance under United States federal law and is
illegal in many other countries. The game does not encourage, promote or condone illegal
activity. Nothing in it is a real guide, recipe or set of instructions, and nothing in it is
medical, legal or scientific advice. Know and follow the laws where you live.</p>

<h2 id="mushrooms">4. Do not use the game to identify real mushrooms</h2>
<p>Mushrooms in the game are not accurate enough to identify real ones. Many wild mushrooms are
poisonous, and some deadly species look very similar to edible or psilocybin species.
<strong>Never pick, eat or give anyone a wild mushroom because of anything you saw in the
game.</strong> If someone may have eaten a poisonous mushroom, get medical help immediately (in
the US, call Poison Control at 1-800-222-1222 or 911).</p>

<h2 id="health">5. Photosensitivity and health warnings</h2>
<p><strong>Photosensitive seizures.</strong> Some scenes have intense flashing colours, glitches
and heavy visual distortion. A small number of people may have seizures when exposed to certain
lights or patterns, even with no history of epilepsy. If you or anyone in your family has had a
seizure or epilepsy, talk to a doctor before playing. Stop playing immediately and see a doctor
if you have dizziness, altered vision, eye or muscle twitching, loss of awareness,
disorientation, or any involuntary movement.</p>
<p><strong>Motion sickness and discomfort.</strong> The game is played in first person and
includes swaying, distorted and moving visuals. If you feel sick, dizzy or uncomfortable, stop
and rest.</p>
<p><strong>Disturbing themes.</strong> The game deals with altered states of mind and
psychological themes that some players may find upsetting. Take breaks, and stop playing if it
affects you.</p>

<h2 id="license">6. Your licence to play</h2>
<p>When you buy Toadstool you get a licence to play it, not ownership of it. We give you a
personal, non-exclusive, non-transferable, revocable licence to install and play the game for
your own non-commercial entertainment, under these terms and the terms of the store you bought
it from.</p>
<p>You may not:</p>
<ul>
  <li>copy, sell, rent, sublicense or redistribute the game or any part of it;</li>
  <li>extract, reuse or redistribute the game&rsquo;s code, art, models, audio or other assets,
  including in other games or products;</li>
  <li>reverse engineer, decompile or disassemble the game, except where the law allows it;</li>
  <li>remove or change any copyright, trademark, age or content notice in the game;</li>
  <li>let anyone under 18 play the game, or use the game for anything unlawful.</li>
</ul>
<p>Mods you make for your own single-player use are fine. Please don&rsquo;t distribute mods that
include our code or assets.</p>

<h2 id="steam">7. Buying through Steam, and refunds</h2>
<p>Toadstool is sold through Steam, operated by Valve Corporation. Your purchase, payment,
account and download are handled by Steam and covered by the Steam Subscriber Agreement and
Steam&rsquo;s refund policy. Refund requests go through Steam. We never receive or store your
payment details.</p>

<h2 id="early-access">8. Early access</h2>
<p>Early access means the game is unfinished. You should expect bugs, missing features and
changes. During early access:</p>
<ul>
  <li>features, content, balance and price may change, be added or be removed;</li>
  <li>updates may reset or break saved games;</li>
  <li>planned features, including the full storyline, are our current plan and not a promise.
  Timelines can move.</li>
</ul>
<p>Please buy the game for what it is today, not for what we hope to add.</p>

<h2 id="videos">9. Videos and streaming</h2>
<p>You can stream, record and share videos and screenshots of your own gameplay, including on
monetised channels, as long as you follow the rules of the platform you post on, including its
rules for mature and drug-related content. Please don&rsquo;t present our footage or assets as
your own work, and don&rsquo;t share builds of the game.</p>

<h2 id="feedback">10. Feedback</h2>
<p>If you send us ideas, suggestions or bug reports, we may use them to improve the game without
owing you anything for them.</p>

<h2 id="ip">11. Our property</h2>
<p>The game, its name, code, art, models, audio, text and our websites belong to Beldangi Fax
Machine LC or our licensors and are protected by copyright and other laws. Toadstool is built
with the Godot Engine, which is used under its own open-source licence.</p>

<h2 id="warranty">12. No warranty</h2>
<p>The game and our websites are provided &ldquo;as is&rdquo; and &ldquo;as available&rdquo;. To
the fullest extent the law allows, we make no warranties of any kind, express or implied,
including that they will be error-free, uninterrupted, or fit for a particular purpose.</p>

<h2 id="liability">13. Limit of liability</h2>
<p>To the fullest extent the law allows, we are not liable for any indirect, incidental, special
or consequential damages, or for lost data, saves or profits, arising from the game or our
websites. Our total liability to you for any claim is limited to the amount you paid for the
game. Some places don&rsquo;t allow some of these limits, so they may not all apply to you.</p>

<h2 id="ending">14. Ending your licence</h2>
<p>You can stop using the game at any time by uninstalling it. If you break these terms, your
licence ends and you must stop playing and delete the game.</p>

<h2 id="law">15. Governing law</h2>
<p>These terms are governed by the laws of the State of Vermont, USA, without regard to its
conflict-of-law rules. Nothing here takes away rights you have under the consumer laws of the
country where you live.</p>

<h2 id="changes">16. Changes to these terms</h2>
<p>We may update these terms, for example when the game leaves early access. The latest version
is always on this page, with the date it last changed at the top. If you keep playing after an
update, the new terms apply.</p>

<h2 id="contact">17. Contact</h2>
<p>Beldangi Fax Machine LC, Vermont, USA. Questions about these terms: {MAIL}</p>
"""

PRIVACY = f"""
<p>This policy explains what information <strong>Beldangi Fax Machine LC</strong> (&ldquo;we&rdquo;,
&ldquo;us&rdquo;) collects through the video game <strong>Toadstool</strong> (also shown in the game
as &ldquo;Toadstool Labs&rdquo;) and our websites: the <a href="{GAME_SITE}">Toadstool site</a> and
the <a href="{CO_SITE}">Beldangi Fax Machine LC site</a>. The short version: we collect as little
as we can, we don&rsquo;t track you, and we don&rsquo;t sell anything about you.</p>

<h2 id="game">1. The game</h2>
<p>Toadstool does not send us your personal information. Your saves and settings are stored on
your own computer. The game&rsquo;s content warning does not record anything about you.</p>
<p>If we add online features later, such as crash reports or anything else that sends data to
us, we will update this policy before that update ships and explain what is collected.</p>

<h2 id="steam">2. Steam</h2>
<p>The game is sold and delivered through Steam. Your Steam account, date of birth, purchases,
payments, achievements and any Steam features are handled by Valve under the Steam Privacy
Policy. We don&rsquo;t receive your payment details or your date of birth. Steam gives developers
combined sales and usage reports that don&rsquo;t identify you personally.</p>

<h2 id="websites">3. Our websites</h2>
<ul>
  <li>No account is needed, and we run no analytics, ads or tracking cookies.</li>
  <li>Both sites are hosted on GitHub Pages. GitHub may log technical data such as your IP address
  and browser type to run and secure the service.</li>
  <li>Fonts load from Google Fonts, which may receive your IP address when a page loads.</li>
</ul>

<h2 id="email">4. If you email us</h2>
<p>If you email us, we receive your email address and whatever you write. We use it only to
reply to you and keep it only as long as we need to. Ask us and we&rsquo;ll delete it.</p>

<h2 id="sharing">5. Sharing</h2>
<p>We don&rsquo;t sell or rent your personal information. We share it only if the law requires
us to.</p>

<h2 id="age">6. Adults only</h2>
<p>Toadstool contains mature content and is for adults aged 18 and over. Our websites are not
directed at children, and we don&rsquo;t knowingly collect information from anyone under 18. If
you think someone under 18 has sent us information, contact us and we&rsquo;ll delete it.</p>

<h2 id="rights">7. Your choices</h2>
<p>You can ask what information we hold about you, or ask us to correct or delete it, by emailing
us. Depending on where you live, you may have further rights under laws such as the GDPR or US
state privacy laws, and we&rsquo;ll honour them.</p>

<h2 id="links">8. Other sites</h2>
<p>Our sites link to other services, including Steam, Instagram, TikTok and Linktree. Their
privacy practices are their own.</p>

<h2 id="changes">9. Changes</h2>
<p>We may update this policy. The latest version is always on this page, with the date it last
changed at the top.</p>

<h2 id="contact">10. Contact</h2>
<p>Beldangi Fax Machine LC, Vermont, USA. Privacy questions or requests: {MAIL}</p>
"""

def indent(html, n):
    pad = " " * n
    return "\n".join((pad + l) if l.strip() else l for l in html.strip("\n").splitlines())

# ── game site (toadstoolweblink): keep its own chrome ─────────────────────
def game_page(title, h1, body):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Toadstool</title>
    <meta name="description" content="{title} for Toadstool, an 18+ game by Beldangi Fax Machine LC.">
    <link rel="icon" type="image/png" href="gallery/character.png">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&family=Space+Grotesk:wght@500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="styles.css">
</head>
<body class="legal">

    <header class="nav nav-solid">
        <a class="wordmark" href="index.html">Toadstool</a>
        <nav>
            <a href="index.html">Home</a>
            <a href="terms.html">Terms</a>
            <a href="privacy.html">Privacy</a>
        </nav>
    </header>

    <main class="block narrow doc">
        <p class="label">Last updated: {UPDATED}</p>
        <h1>{h1}</h1>
{indent(body, 8)}
    </main>

    <footer class="footer">
        <nav>
            <a href="index.html">Home</a>
            <a href="terms.html">Terms</a>
            <a href="privacy.html">Privacy</a>
        </nav>
        <p class="fine">&copy; 2026 Beldangi Fax Machine LC. Toadstool is for adults 18+.</p>
    </footer>

</body>
</html>
"""

# ── company site (BELDANGIFAXMACHINE) ─────────────────────────────────
def co_page(title, h1, body):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#0e0c0a">
<meta name="color-scheme" content="dark">
<title>{title} — Beldangi Fax Machine LC</title>
<meta name="description" content="{title} for Toadstool and the Beldangi Fax Machine LC websites.">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css">
</head>
<body>
<header class="top">
  <a class="studio" href="./">Beldangi Fax Machine LC</a>
  <nav aria-label="Pages">
    <a href="./#toadstool">Toadstool</a>
    <a href="terms.html">Terms</a>
    <a href="privacy.html">Privacy</a>
  </nav>
</header>

<main class="doc">
  <h1>{h1}</h1>
  <p class="updated">Last updated {UPDATED}</p>
{indent(body, 2)}
</main>

<footer class="foot">
  <nav class="foot-links" aria-label="Legal">
    <a href="./">Home</a>
    <a href="terms.html">Terms of Service</a>
    <a href="privacy.html">Privacy Policy</a>
  </nav>
  <p>&copy; 2026 Beldangi Fax Machine LC. All rights reserved.</p>
</footer>
</body>
</html>
"""

game, co = map(pathlib.Path, sys.argv[1:3])
(game / "terms.html").write_text(game_page("Terms of Service", "Terms of Service", TERMS))
(game / "privacy.html").write_text(game_page("Privacy Policy", "Privacy Policy", PRIVACY))
(co / "terms.html").write_text(co_page("Terms of Service", "Terms of Service", TERMS))
(co / "privacy.html").write_text(co_page("Privacy Policy", "Privacy Policy", PRIVACY))
print("wrote terms + privacy to both sites")
