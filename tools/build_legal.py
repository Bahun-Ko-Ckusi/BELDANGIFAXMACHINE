"""Writes the Terms of Service, EULA, Privacy Policy and 18+ notice into BOTH sites from one text,
so the game site and the company site never say different things. Also writes plain-text copies
for pasting into Steamworks (steam/ in the company repo).

Run: python3 tools/build_legal.py ~/toadstoolweblink ~/BELDANGIFAXMACHINE
"""
import html as htmllib
import pathlib
import re
import sys

UPDATED = "November 20, 2026"
EMAIL = "beldangifaxmachine@gmail.com"
MAIL = f'<a href="mailto:{EMAIL}">{EMAIL}</a>'
GAME_SITE = "https://bahun-ko-ckusi.github.io/toadstoolweblink/"
CO_SITE = "https://beldangifaxmachine.com/"

# ── sections, shared between the Terms and the EULA ─────────────────────────
# Each section is (id, heading, body). Pages pick the ones they need and get numbered when built.

AGE = ("age", "You must be 18 or older", """
<p>Toadstool is made for adults aged 18 and over. You may only buy, download or play it if you
are at least 18 and old enough to enter into a binding agreement where you live. If you are under
18, do not buy, download or play the game.</p>
""")

AGE_NOTICE = ("age-notice", "How we tell players about the age limit", """
<p>We make the age limit clear before anyone pays and every time the game starts:</p>
<ul>
  <li><strong>Before you buy.</strong> Our websites and the game&rsquo;s store page state that
  Toadstool is for adults 18 and over and describe its mature content. Our
  <a href="age.html">18+ content notice</a> lists what is in the game.</li>
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
""")

CONTENT = ("content", "Drug content is fiction, not advice", """
<p>Toadstool is a psychology and mycology simulation. It depicts the growing and use of
psilocybin (&ldquo;magic&rdquo;) mushrooms and other drugs.</p>
<p>Psilocybin is a Schedule I controlled substance under United States federal law and is
illegal in many other countries. The game does not encourage, promote or condone illegal
activity. Nothing in it is a real guide, recipe or set of instructions, and nothing in it is
medical, legal or scientific advice. Know and follow the laws where you live.</p>
""")

MUSHROOMS = ("mushrooms", "Do not use the game to identify real mushrooms", """
<p>Mushrooms in the game are not accurate enough to identify real ones. Many wild mushrooms are
poisonous, and some deadly species look very similar to edible or psilocybin species.
<strong>Never pick, eat or give anyone a wild mushroom because of anything you saw in the
game.</strong> If someone may have eaten a poisonous mushroom, get medical help immediately (in
the US, call Poison Control at 1-800-222-1222 or 911).</p>
""")

HEALTH = ("health", "Photosensitivity and health warnings", """
<p><strong>Photosensitive seizures.</strong> Some scenes have intense flashing colours, glitches
and heavy visual distortion. A small number of people may have seizures when exposed to certain
lights or patterns, even with no history of epilepsy. If you or anyone in your family has had a
seizure or epilepsy, talk to a doctor before playing. Stop playing immediately and see a doctor
if you have dizziness, altered vision, eye or muscle twitching, loss of awareness,
disorientation, or any involuntary movement.</p>
<p><strong>Motion sickness and discomfort.</strong> The game includes swaying, distorted and
moving visuals. If you feel sick, dizzy or uncomfortable, stop and rest.</p>
<p><strong>Disturbing themes.</strong> The game deals with altered states of mind and
psychological themes that some players may find upsetting. Take breaks, and stop playing if it
affects you.</p>
""")

LICENSE = ("license", "Your licence to play", """
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
  <li>cheat, hack or interfere with online play, our servers or other players&rsquo; games;</li>
  <li>remove or change any copyright, trademark, age or content notice in the game;</li>
  <li>let anyone under 18 play the game, or use the game for anything unlawful.</li>
</ul>
<p>Mods you make for your own single-player use are fine. Please don&rsquo;t distribute mods that
include our code or assets.</p>
""")

STEAM = ("steam", "Buying through Steam, and refunds", """
<p>Toadstool is sold through Steam, operated by Valve Corporation. Your purchase, payment,
account and download are handled by Steam and covered by the Steam Subscriber Agreement and
Steam&rsquo;s refund policy. Refund requests go through Steam. We never receive or store your
payment details. Valve is not responsible for the game or for these terms.</p>
""")

ONLINE = ("online", "Online play and conduct", """
<p>Toadstool has online features. When Steam is running you can play with your Steam friends in
a friends-only lobby. Other players in your session can see your frog&rsquo;s name and look,
where your frog is and what it does. Our <a href="privacy.html">Privacy Policy</a> explains what
is sent and stored.</p>
<p>Don&rsquo;t use a frog name, bug note or anything else you put in the game that is hateful,
harassing, threatening, sexual, or that shares anyone&rsquo;s personal information. We may remove
anything like that, and we may block anyone who abuses online play. Online features may change,
be limited or be turned off at any time, especially during early access.</p>
""")

EARLY = ("early-access", "Early access", """
<p>Early access means the game is unfinished. You should expect bugs, missing features and
changes. During early access:</p>
<ul>
  <li>features, content, balance and price may change, be added or be removed;</li>
  <li>updates may reset or break saved games;</li>
  <li>planned features, including the full storyline, are our current plan and not a promise.
  Timelines can move.</li>
</ul>
<p>Please buy the game for what it is today, not for what we hope to add.</p>
""")

VIDEOS = ("videos", "Videos and streaming", """
<p>You can stream, record and share videos and screenshots of your own gameplay, including on
monetised channels, as long as you follow the rules of the platform you post on, including its
rules for mature and drug-related content. Please don&rsquo;t present our footage or assets as
your own work, and don&rsquo;t share builds of the game.</p>
""")

FEEDBACK = ("feedback", "Feedback", """
<p>If you send us ideas, suggestions or bug reports, we may use them to improve the game without
owing you anything for them.</p>
""")

IP = ("ip", "Our property", """
<p>The game, its name, code, art, models, audio, text and our websites belong to Beldangi Fax
Machine LC or our licensors and are protected by copyright and other laws. All rights not
expressly given to you are kept by us. Toadstool is built with the Godot Engine and uses other
third-party tools and assets, each used under its own licence.</p>
""")

COPYRIGHT = ("copyright", "Copyright complaints", f"""
<p>If you believe something in the game or on our websites infringes your copyright, email us at
{MAIL} with: a description of the work you own; where the material is; your name and contact
details; a statement that you believe in good faith the use is not authorised by you, your agent
or the law; a statement, under penalty of perjury, that your notice is accurate and that you are
the owner or authorised to act for the owner; and your physical or electronic signature.</p>
""")

WARRANTY = ("warranty", "No warranty", """
<p>The game and our websites are provided &ldquo;as is&rdquo; and &ldquo;as available&rdquo;. To
the fullest extent the law allows, we make no warranties of any kind, express or implied,
including warranties of merchantability, fitness for a particular purpose and non-infringement,
or that the game will be error-free or uninterrupted.</p>
""")

LIABILITY = ("liability", "Limit of liability", """
<p>To the fullest extent the law allows, we are not liable for any indirect, incidental, special,
punitive or consequential damages, or for lost data, saves or profits, arising from the game or
our websites. Our total liability to you for any claim is limited to the amount you paid for the
game. Some places don&rsquo;t allow some of these limits, so they may not all apply to you.</p>
""")

ENDING = ("ending", "Ending your licence", """
<p>You can stop using the game at any time by uninstalling it. If you break these terms, your
licence ends and you must stop playing and delete the game. Sections that by their nature should
last after the licence ends, such as ownership, no warranty, limit of liability and governing
law, keep applying.</p>
""")

LAW = ("law", "Governing law", """
<p>These terms are governed by the laws of the State of Vermont, USA, without regard to its
conflict-of-law rules. Any dispute that is not handled by Steam will be heard in the state or
federal courts located in Vermont, unless the consumer laws of the country where you live give
you the right to bring it where you live. Nothing here takes away rights you have under those
consumer laws.</p>
""")

GENERAL = ("general", "General", """
<ul>
  <li><strong>Whole agreement.</strong> These terms, our Privacy Policy and the terms of the
  store you bought from are the whole agreement between you and us about the game.</li>
  <li><strong>Severability.</strong> If any part of these terms can&rsquo;t be enforced, the rest
  still applies, and that part is applied as far as the law allows.</li>
  <li><strong>No waiver.</strong> If we don&rsquo;t enforce a part of these terms right away, we
  can still enforce it later.</li>
  <li><strong>Transfer.</strong> You can&rsquo;t transfer your rights under these terms. We may
  transfer ours, for example if the game or the company is sold.</li>
  <li><strong>Export and sanctions.</strong> You may not download or use the game where United
  States export or sanctions laws forbid it.</li>
</ul>
""")

CHANGES = ("changes", "Changes to these terms", """
<p>We may update these terms, for example when the game leaves early access. The latest version
is always on this page, with the date it last changed at the top. If you keep playing after an
update, the new terms apply.</p>
""")

CONTACT = ("contact", "Contact", f"""
<p>Beldangi Fax Machine LC, Vermont, USA. Questions about these terms: {MAIL}</p>
""")

TERMS_INTRO = f"""
<p>These terms cover the video game <strong>Toadstool</strong>, also shown in the game as
&ldquo;Toadstool Labs&rdquo; (the &ldquo;game&rdquo;), including early access and its online
features, and our websites: the <a href="{GAME_SITE}">Toadstool site</a> and the
<a href="{CO_SITE}">Beldangi Fax Machine LC site</a>. The game and the sites are made and
published by <strong>Beldangi Fax Machine LC</strong>, a Vermont limited liability company
(&ldquo;we&rdquo;, &ldquo;us&rdquo;). The <a href="eula.html">End User License Agreement</a> is
part of these terms.</p>
<p>By buying, installing or playing the game, or by using our websites, you agree to these
terms. If you don&rsquo;t agree, don&rsquo;t play the game or use the sites.</p>

<div class="notice" role="note">
  <p><strong>Adults only (18+).</strong> Toadstool depicts the growing and use of psilocybin
  mushrooms and other drugs, and some scenes have intense flashing colours and heavy visual
  distortion. It is a work of fiction. Never eat a wild mushroom because of anything you saw in
  the game.</p>
</div>
"""

EULA_INTRO = """
<p>This End User License Agreement (&ldquo;EULA&rdquo;) is between you and <strong>Beldangi Fax
Machine LC</strong>, a Vermont limited liability company (&ldquo;we&rdquo;, &ldquo;us&rdquo;),
and covers the video game <strong>Toadstool</strong>, also shown in the game as &ldquo;Toadstool
Labs&rdquo; (the &ldquo;game&rdquo;). It is part of our <a href="terms.html">Terms of
Service</a>. By installing or playing the game you agree to this EULA. If you don&rsquo;t agree,
don&rsquo;t install or play the game.</p>

<div class="notice" role="note">
  <p><strong>Adults only (18+).</strong> Toadstool depicts the growing and use of psilocybin
  mushrooms and other drugs, and some scenes have intense flashing colours and heavy visual
  distortion. It is a work of fiction. Never eat a wild mushroom because of anything you saw in
  the game.</p>
</div>
"""

TERMS = [AGE, AGE_NOTICE, CONTENT, MUSHROOMS, HEALTH, LICENSE, STEAM, ONLINE, EARLY, VIDEOS,
         FEEDBACK, IP, COPYRIGHT, WARRANTY, LIABILITY, ENDING, LAW, GENERAL, CHANGES, CONTACT]
EULA = [AGE, CONTENT, MUSHROOMS, HEALTH, LICENSE, ONLINE, STEAM, EARLY, IP, WARRANTY, LIABILITY,
        ENDING, LAW, GENERAL, CHANGES, CONTACT]

# ── privacy policy ─────────────────────────────────────────────────────────
PRIVACY_INTRO = f"""
<p>This policy explains what information <strong>Beldangi Fax Machine LC</strong> (&ldquo;we&rdquo;,
&ldquo;us&rdquo;) collects through the video game <strong>Toadstool</strong> (also shown in the game
as &ldquo;Toadstool Labs&rdquo;) and our websites: the <a href="{GAME_SITE}">Toadstool site</a> and
the <a href="{CO_SITE}">Beldangi Fax Machine LC site</a>. The short version: the game sends only
what its online features need, most of it is deleted within a day, we run no ads or tracking,
and we don&rsquo;t sell anything about you.</p>
"""

PRIVACY = [
    ("on-your-computer", "What stays on your computer", """
<p>Your saves, settings and frog are stored on your own computer. The game also makes a random
player number the first time it runs and keeps it there. It is not linked to your name or your
Steam account. The game&rsquo;s content warning does not record anything about you.</p>
"""),
    ("online", "What the game sends online", """
<p>The game&rsquo;s online features use a server we run on Supabase, a database hosting
company. When the game is connected to the internet:</p>
<ul>
  <li><strong>Character looks.</strong> At start the game downloads the looks of the
  game&rsquo;s townsfolk from our server. Like any internet request, the server receives your IP
  address and basic technical information to answer it.</li>
  <li><strong>Player record.</strong> While you are in a world, the game saves a small record on
  our server with a player ID (your Steam ID when Steam is running, otherwise a random number),
  your frog&rsquo;s name, your frog&rsquo;s look and the time you were last seen. It is deleted
  automatically about 24 hours after you stop playing.</li>
  <li><strong>Friendships with townsfolk.</strong> How friendly the game&rsquo;s characters are
  with you is saved on our server under your random player number, so it carries over between
  sessions. It is deleted automatically after 24 hours without a change.</li>
  <li><strong>Bug notes.</strong> If you leave a note with the in-game Bug Clipboard, we receive
  the text you write, your frog&rsquo;s name and where in the game you were. We keep notes until
  we have dealt with them. Please don&rsquo;t put personal information in a bug note.</li>
  <li><strong>Playing together.</strong> With Steam running, your frog&rsquo;s name, look,
  position and actions are sent to the friends in your lobby through Steam&rsquo;s network.
  Without Steam, the game shares the same things through our server with other players who are
  online at the same time. These live updates are not stored, apart from the player record
  above.</li>
</ul>
<p>Player records, friendship records and bug notes are shared by the game&rsquo;s online
features, so other copies of the game can read them. Use a frog name you are happy for other
players to see.</p>
"""),
    ("steam", "Steam", """
<p>The game is sold and delivered through Steam and uses Steam features such as friends,
lobbies and invites. Your Steam account, date of birth, purchases, payments and achievements are
handled by Valve under the Steam Privacy Policy. We don&rsquo;t receive your payment details or
your date of birth. Steam gives developers combined sales and usage reports that don&rsquo;t
identify you personally.</p>
"""),
    ("websites", "Our websites", """
<ul>
  <li>No account is needed, and we run no analytics, ads or tracking cookies.</li>
  <li>Both sites are hosted on GitHub Pages. GitHub may log technical data such as your IP address
  and browser type to run and secure the service.</li>
  <li>Fonts load from Google Fonts, which may receive your IP address when a page loads.</li>
</ul>
"""),
    ("email", "If you email us", """
<p>If you email us, we receive your email address and whatever you write. We use it only to
reply to you and keep it only as long as we need to. Ask us and we&rsquo;ll delete it.</p>
"""),
    ("use", "How we use information", """
<p>We use the information above only to run the game&rsquo;s online features, fix bugs, keep
online play safe and reply to you. We don&rsquo;t use it for advertising or build profiles of
players.</p>
"""),
    ("sharing", "Who we share it with", """
<p>We don&rsquo;t sell or rent your personal information. It is handled for us by the services
named above (Supabase for the game&rsquo;s server, Valve for Steam, GitHub for website hosting,
Google for fonts), which may process it in the United States and other countries. We share it
with anyone else only if the law requires us to.</p>
"""),
    ("age", "Adults only", """
<p>Toadstool contains mature content and is for adults aged 18 and over. The game and our
websites are not directed at children, and we don&rsquo;t knowingly collect information from
anyone under 18. If you think someone under 18 has sent us information, contact us and
we&rsquo;ll delete it.</p>
"""),
    ("rights", "Your choices", """
<p>You can play without any of the online features by playing with your computer offline. You
can ask what information we hold about you, or ask us to correct or delete it, by emailing us.
Tell us your frog&rsquo;s name or Steam ID so we can find it. Depending on where you live, you may
have further rights under laws such as the GDPR or US state privacy laws, and we&rsquo;ll honour
them.</p>
"""),
    ("security", "Security", """
<p>We take reasonable steps to protect the information we hold, but no method of sending or
storing data is completely secure.</p>
"""),
    ("links", "Other sites", """
<p>Our sites link to other services, including Steam, Instagram, TikTok and Linktree. Their
privacy practices are their own.</p>
"""),
    ("changes", "Changes", """
<p>We may update this policy, for example if we add online features. The latest version is always
on this page, with the date it last changed at the top. If a change affects what the game sends,
we&rsquo;ll update this policy before that game update ships.</p>
"""),
    ("contact", "Contact", f"""
<p>Beldangi Fax Machine LC, Vermont, USA. Privacy questions or requests: {MAIL}</p>
"""),
]

# ── 18+ content notice ─────────────────────────────────────────────────────
# The quoted warning must match the in-game screen word for word
# (charatercontrol/menu/scripts/boot_intro.gd, _build_warning).
IN_GAME_WARNING = """
<div class="notice" role="note">
  <p><strong>CONTENT WARNING &ndash; 18+</strong></p>
  <p>Toadstool Labs is a work of fiction made for adults aged 18 or older.</p>
  <p>It shows the growing and use of psilocybin mushrooms and other drugs. Psilocybin is a
  Schedule I controlled substance in the United States and is illegal in many other countries.</p>
  <p>The game does not encourage, promote or condone illegal activity, and nothing in it is a real
  guide or set of instructions. Mushrooms in the game are not accurate enough to identify real ones:
  never eat a wild mushroom because of anything you saw here.</p>
  <p>PHOTOSENSITIVITY: some scenes have intense flashing colours, glitches and heavy visual
  distortion that may affect people with photosensitive epilepsy.</p>
</div>
"""

# Short description for the Steam content survey; also shown on the 18+ page.
MATURE_TEXT = ("Toadstool is for adults 18+. It depicts the growing and use of psilocybin "
               "(\"magic\") mushrooms and other drugs, including drug-induced hallucinations shown "
               "with heavy visual distortion and intense flashing colours. Drug use is fictional and "
               "not presented as a guide. The game does not encourage illegal activity. Some scenes "
               "may affect players with photosensitive epilepsy.")

AGE_PAGE = f"""
<p><strong>Toadstool is for adults aged 18 and over.</strong> If you are under 18, do not buy,
download or play it. This page lists the mature content in the game so you can decide before you
buy. It is part of our <a href="terms.html">Terms of Service</a>.</p>

<h2 id="contains">What the game contains</h2>
<ul>
  <li><strong>Drug content.</strong> Growing, harvesting, preparing and taking psilocybin
  (&ldquo;magic&rdquo;) mushrooms and other drugs, and the hallucinations that follow.</li>
  <li><strong>Flashing lights.</strong> Intense flashing colours, glitches and heavy visual
  distortion, especially during trips. This may affect people with photosensitive epilepsy.</li>
  <li><strong>Motion.</strong> Swaying, warping and moving visuals that can cause motion
  sickness.</li>
  <li><strong>Mature themes.</strong> Altered states of mind and psychological themes that some
  players may find upsetting.</li>
  <li><strong>Online play.</strong> Playing with Steam friends, where other players can see your
  frog&rsquo;s name and look.</li>
</ul>

<h2 id="summary">Short description</h2>
<p>{htmllib.escape(MATURE_TEXT, quote=False)}</p>

<h2 id="in-game">The warning shown every time the game starts</h2>
<p>Before the main menu, every time the game starts, players see this screen:</p>
{IN_GAME_WARNING}

<h2 id="fiction">It is fiction, not advice</h2>
<p>Psilocybin is a Schedule I controlled substance under United States federal law and is
illegal in many other countries. Nothing in the game is a real guide, recipe or set of
instructions, or medical, legal or scientific advice. Mushrooms in the game are not accurate
enough to identify real ones. <strong>Never pick, eat or give anyone a wild mushroom because of
anything you saw in the game.</strong> If someone may have eaten a poisonous mushroom, get medical
help immediately (in the US, call Poison Control at 1-800-222-1222 or 911).</p>

<h2 id="parents">Parents and guardians</h2>
<p>Toadstool is marked as mature content on Steam. Steam asks for a date of birth before showing
mature store pages and lets you block mature games with Steam&rsquo;s family and parental
controls. We don&rsquo;t verify anyone&rsquo;s age ourselves, so please use those controls to keep
the game away from children.</p>

<h2 id="contact">Contact</h2>
<p>Questions: {MAIL}</p>
"""


# Numbers each section and joins it into one page body.
def numbered(sections):
    parts = []
    for n, (sid, title, body) in enumerate(sections, 1):
        parts.append(f'<h2 id="{sid}">{n}. {title}</h2>\n{body.strip()}')
    return "\n\n".join(parts)


def indent(text, n):
    pad = " " * n
    return "\n".join((pad + line) if line.strip() else line for line in text.strip("\n").splitlines())


# Turns a page body into plain text for pasting into Steamworks.
def plain(body):
    text = re.sub(r"<h2[^>]*>(.*?)</h2>", lambda m: "\n" + m.group(1).upper() + "\n", body, flags=re.S)
    text = re.sub(r"</p>", "</p>\n\n", text)   # every paragraph gets its own block
    text = re.sub(r"<li>", "- ", text)
    text = re.sub(r"<a href=\"([^\"]+)\">(.*?)</a>",
                  lambda m: m.group(2) if m.group(1).startswith("mailto:") else f"{m.group(2)} ({full_url(m.group(1))})",
                  text, flags=re.S)
    text = re.sub(r"<[^>]+>", "", text)
    text = htmllib.unescape(text)
    paragraphs = [" ".join(p.split()) for p in re.split(r"\n\s*\n", text)]
    # list items sit on their own lines inside one paragraph
    paragraphs = [p.replace(" - ", "\n- ") if p.startswith("- ") else p for p in paragraphs]
    return "\n\n".join(p for p in paragraphs if p).strip() + "\n"


# Relative page links in the legal text point at the company site in the plain-text copies.
def full_url(href):
    return href if href.startswith("http") else CO_SITE + href


# One entry per generated page: file name, title, body.
def pages():
    return [
        ("terms.html", "Terms of Service", TERMS_INTRO.strip() + "\n\n" + numbered(TERMS)),
        ("eula.html", "End User License Agreement", EULA_INTRO.strip() + "\n\n" + numbered(EULA)),
        ("privacy.html", "Privacy Policy", PRIVACY_INTRO.strip() + "\n\n" + numbered(PRIVACY)),
        ("age.html", "18+ Content Notice", AGE_PAGE.strip()),
    ]


# ── game site (toadstoolweblink): keep its own chrome ─────────────────────
def game_page(title, body):
    links = """<a href="index.html">Home</a>
            <a href="terms.html">Terms</a>
            <a href="eula.html">EULA</a>
            <a href="privacy.html">Privacy</a>
            <a href="age.html">18+</a>"""
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
            {links}
        </nav>
    </header>

    <main class="block narrow doc">
        <p class="label">Last updated: {UPDATED}</p>
        <h1>{title}</h1>
{indent(body, 8)}
    </main>

    <footer class="footer">
        <nav>
            {links}
        </nav>
        <p class="fine">&copy; 2026 <a href="{CO_SITE}">Beldangi Fax Machine LC</a>. Toadstool is for adults 18+.</p>
    </footer>

</body>
</html>
"""


# ── company site (BELDANGIFAXMACHINE) ─────────────────────────────────
def co_page(title, body):
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
    <a href="eula.html">EULA</a>
    <a href="privacy.html">Privacy</a>
    <a href="age.html">18+</a>
  </nav>
</header>

<main class="doc">
  <h1>{title}</h1>
  <p class="updated">Last updated {UPDATED}</p>
{indent(body, 2)}
</main>

<footer class="foot">
  <nav class="foot-links" aria-label="Legal">
    <a href="./">Home</a>
    <a href="terms.html">Terms of Service</a>
    <a href="eula.html">EULA</a>
    <a href="privacy.html">Privacy Policy</a>
    <a href="age.html">18+ Notice</a>
  </nav>
  <p>&copy; 2026 Beldangi Fax Machine LC. All rights reserved.</p>
</footer>
</body>
</html>
"""


game, co = map(pathlib.Path, sys.argv[1:3])
for name, title, body in pages():
    (game / name).write_text(game_page(title, body))
    (co / name).write_text(co_page(title, body))

# plain-text copies for Steamworks (EULA text box, mature content survey)
steam = co / "steam"
steam.mkdir(exist_ok=True)
eula_body = EULA_INTRO + "\n\n" + numbered(EULA)
(steam / "eula.txt").write_text(f"END USER LICENSE AGREEMENT - TOADSTOOL\nLast updated {UPDATED}\n\n" + plain(eula_body))
(steam / "mature_content.txt").write_text(MATURE_TEXT + "\n")
print("wrote terms, eula, privacy, 18+ notice to both sites, and steam/ text copies")
