#!/usr/bin/env python3
"""Static site builder for LowLevel Labs.

Sources:
  content/articles/<slug>.html   article body, with a <!--meta ... --> header
  content/pages/<name>.html      simple pages (about, contact, projects)
Output (committed, served by GitHub Pages):
  index.html, articles.html, topics/<topic>.html, articles/<slug>.html,
  about.html, contact.html, projects.html, sitemap.xml

Run from the repository root:  python3 tools/build.py
"""
import datetime as dt
import html
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://lowlevellabs.in"
CSS_VER = "20261120"

# Topic register: ordered MSB -> LSB; widths sum to 32 bits.
TOPICS = [
    ("boot", "BOOT", 4, "Boot & platform", "Reset vectors, BIOS and UEFI, partition tables, bootloaders and the handoff to the kernel."),
    ("firmware", "FW", 4, "Embedded firmware", "Startup code, interrupts, peripherals, memory technologies and bring-up on real boards."),
    ("c", "C", 4, "C for embedded", "volatile, bit manipulation, memory layout and the parts of C that touch hardware."),
    ("asm", "ASM", 4, "Assembly", "ARM and x86-64 assembly, calling conventions, stack frames and worked programs."),
    ("cpu", "CPU", 4, "CPU internals", "Pipelines, caches, coherence, MMUs, exception levels and multicore communication."),
    ("rtos", "RTOS", 4, "RTOS & VxWorks", "Scheduling, synchronization, priority inversion and VxWorks architecture."),
    ("drivers", "DRV", 5, "Linux device drivers", "Driver model, probe, Device Tree, character devices, ioctl and kernel contexts."),
    ("linux", "LNX", 3, "Linux systems", "User-space system programming: IPC, D-Bus and GDBus."),
]
TOPIC = {t[0]: dict(code=t[1], width=t[2], name=t[3], blurb=t[4]) for t in TOPICS}

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans+Condensed:wght@500;600&'
         'family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;1,400&display=swap" rel="stylesheet">')
HLJS = ("https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/highlight.min.js",
        "https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/languages/armasm.min.js",
        "https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/languages/x86asm.min.js",
        "https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/languages/dts.min.js")
ANALYTICS = ("<script type='module' src='https://static.cloudflareinsights.com/beacon.min.js' "
             "data-cf-beacon='{\"token\": \"65389390692d4a49a738f41ed4240d62\"}'></script>")
THEME_INIT = ("<script>(function(){var t;try{t=localStorage.getItem('ll-theme')}catch(e){}"
              "if(!t&&window.matchMedia&&matchMedia('(prefers-color-scheme: dark)').matches)t='dark';"
              "if(t)document.documentElement.dataset.theme=t})()</script>")
SUN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>'
MENU = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>'
MARK = '<span class="mark" aria-hidden="true"><i></i><i></i><i></i><i></i></span>'

NAV = [("articles.html", "Articles", "articles"), ("topics/index.html", "Topics", "topics"),
       ("projects.html", "Guides", "projects"), ("about.html", "About", "about"), ("contact.html", "Contact", "contact")]


def esc(s):
    return html.escape(s, quote=True)


def layout(*, title, desc, body, depth, path, current="", head_extra="", scripts_extra=""):
    p = "../" * depth
    nav = "".join(
        f'<a href="{p}{href}"{" aria-current=\"page\"" if key == current else ""}>{label}</a>'
        for href, label, key in NAV)
    canonical = SITE + "/" + ("" if path == "index.html" else path)
    full_title = title if title.startswith("LowLevel Labs") else f"{title} | LowLevel Labs"
    year = dt.date.today().year
    foot_topics = "".join(f'<li><a href="{p}topics/{k}.html">{TOPIC[k]["name"]}</a></li>' for k, *_ in TOPICS[:6])
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}">
<meta property="og:type" content="website"><meta property="og:url" content="{canonical}">
<meta name="theme-color" content="#f5f7f9" media="(prefers-color-scheme: light)"><meta name="theme-color" content="#0d1520" media="(prefers-color-scheme: dark)">
<link rel="icon" href="{p}assets/favicon.svg" type="image/svg+xml">
{THEME_INIT}
{FONTS}
<link rel="stylesheet" href="{p}styles.css?v={CSS_VER}">
{head_extra}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="top"><div class="wrap">
<a class="brand" href="{p}index.html" aria-label="LowLevel Labs home">{MARK}<span>LowLevel <b>Labs</b></span></a>
<nav class="nav" id="nav" aria-label="Main">{nav}</nav>
<button class="icon-btn" id="themeBtn" type="button" aria-label="Switch theme">{SUN}</button>
<button class="icon-btn menu-btn" id="menuBtn" type="button" aria-label="Menu" aria-expanded="false" aria-controls="nav">{MENU}</button>
</div></header>
<main id="main">
{body}
</main>
<footer class="foot"><div class="wrap">
<div><a class="brand" href="{p}index.html">{MARK}<span>LowLevel <b>Labs</b></span></a>
<p>Explanations, diagrams and working code for engineers who work below the API.</p>
<p class="muted">© {year} LowLevel Labs</p></div>
<div><h2>Topics</h2><ul>{foot_topics}</ul></div>
<div><h2>Site</h2><ul><li><a href="{p}articles.html">All articles</a></li><li><a href="{p}projects.html">Guides &amp; exercises</a></li><li><a href="{p}about.html">About</a></li><li><a href="{p}contact.html">Contact</a></li><li><a href="https://github.com/Hardik7503/lowlevellabs-site">Source on GitHub</a></li></ul></div>
</div></footer>
{scripts_extra}
<script src="{p}script.js?v={CSS_VER}" defer></script>
{ANALYTICS}
</body>
</html>
"""


def parse(path):
    s = path.read_text()
    m = re.match(r"<!--meta\n(.*?)\n-->\n?", s, re.S)
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    body = s[m.end():]
    # ```lang fenced code blocks -> escaped <pre><code>
    body = re.sub(r"^```(\w*)\n(.*?)\n```\s*$",
                  lambda b: f'<pre><code class="language-{b.group(1) or "plaintext"}">{html.escape(b.group(2), quote=False)}</code></pre>',
                  body, flags=re.S | re.M)
    meta["body"] = body
    meta["slug"] = path.stem
    meta.setdefault("date", "2026-10-22")
    return meta


def slugify(text):
    t = re.sub(r"<[^>]+>", "", text)
    t = html.unescape(t).lower()
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    return t or "section"


def add_heading_ids(body):
    toc, seen = [], set()

    def rep(m):
        attrs, inner = m.group(1), m.group(2)
        if "id=" in attrs:
            hid = re.search(r'id="([^"]+)"', attrs).group(1)
        else:
            hid = slugify(inner)
            base, n = hid, 2
            while hid in seen:
                hid = f"{base}-{n}"; n += 1
            attrs = f'{attrs} id="{hid}"'
        seen.add(hid)
        toc.append((hid, re.sub(r"<[^>]+>", "", inner).strip()))
        return f"<h2{attrs}>{inner}</h2>"

    body = re.sub(r"<h2([^>]*)>(.*?)</h2>", rep, body, flags=re.S)
    return body, toc


def fmt_date(d):
    return dt.date.fromisoformat(d).strftime("%-d %b %Y")


def thumb(topic):
    """Tiny line drawings used on the home page 'Start here' strip."""
    svgs = {
        "rtos": '<svg class="dg" viewBox="0 0 200 110"><rect class="b" x="10" y="14" width="180" height="18" rx="3"/><rect class="cu" x="10" y="14" width="46" height="18" rx="3"/><rect class="b" x="10" y="46" width="180" height="18" rx="3"/><rect class="sg" x="56" y="46" width="64" height="18" rx="3"/><rect class="b" x="10" y="78" width="180" height="18" rx="3"/><rect class="wn" x="120" y="78" width="60" height="18" rx="3"/><text class="m s" x="14" y="27">HIGH</text><text class="m s" x="14" y="59">MED</text><text class="m s" x="14" y="91">LOW</text></svg>',
        "c": '<svg class="dg" viewBox="0 0 200 110"><g>' + "".join(
            f'<rect class="{ "cu" if i in (2,3,4) else "b"}" x="{8+i*23}" y="40" width="21" height="28" rx="2"/><text class="m s" x="{14+i*23}" y="34">{7-i}</text>'
            for i in range(8)) + '</g><text class="m s" x="54" y="90">mask = 0x1C</text></svg>',
        "drivers": '<svg class="dg" viewBox="0 0 200 110"><rect class="b" x="60" y="6" width="80" height="22" rx="4"/><text class="m s" x="76" y="21">open()</text><path class="ln" d="M100 28v12"/><rect class="sg" x="60" y="40" width="80" height="22" rx="4"/><text class="m s" x="88" y="55">VFS</text><path class="ln" d="M100 62v12"/><rect class="cu" x="30" y="74" width="140" height="26" rx="4"/><text class="m s" x="44" y="91">file_operations</text></svg>',
        "cpu": '<svg class="dg" viewBox="0 0 200 110">' + "".join(
            f'<rect class="{c}" x="{8+i*30}" y="{12+i*18}" width="70" height="16" rx="2"/>'
            for i, c in enumerate(["cu", "sg", "b", "b", "b"])) + "</svg>",
        "firmware": '<svg class="dg" viewBox="0 0 200 110"><rect class="ink" x="50" y="6" width="100" height="98" rx="4"/><rect class="cu" x="50" y="6" width="100" height="22" rx="4"/><text class="m s" x="62" y="21">vector table</text><rect class="sg" x="50" y="34" width="100" height="22"/><text class="m s" x="82" y="49">.text</text><rect class="b" x="50" y="60" width="100" height="18"/><text class="m s" x="82" y="73">.data</text><rect class="b" x="50" y="82" width="100" height="18"/><text class="m s" x="84" y="95">.bss</text></svg>',
        "asm": '<svg class="dg" viewBox="0 0 200 110"><rect class="ink" x="40" y="6" width="120" height="98" rx="4"/><rect class="b" x="40" y="6" width="120" height="22"/><text class="m s" x="64" y="21">caller frame</text><rect class="cu" x="40" y="28" width="120" height="20"/><text class="m s" x="62" y="42">return addr</text><rect class="sg" x="40" y="48" width="120" height="20"/><text class="m s" x="70" y="62">saved fp</text><rect class="b" x="40" y="68" width="120" height="36"/><text class="m s" x="78" y="90">locals</text></svg>',
    }
    return svgs.get(topic, svgs["cpu"])


def article_row(a, depth, new_cut):
    p = "../" * depth
    t = TOPIC[a["topic"]]
    new = '<span class="new">New</span>' if a["date"] >= new_cut else ""
    text = esc((a["title"] + " " + a["description"] + " " + t["name"]).lower())
    return (f'<li data-topic="{a["topic"]}" data-text="{text}"><a class="toc-row" href="{p}articles/{a["slug"]}.html">'
            f'<span class="k">{t["name"]}</span>'
            f'<span><span class="t">{esc(a["title"])}</span>{new}<span class="d">{esc(a["description"])}</span></span>'
            f'<span class="r">{esc(a["read"])}</span></a></li>')


def build():
    arts = [parse(f) for f in sorted((ROOT / "content/articles").glob("*.html"))]
    for a in arts:
        assert a["topic"] in TOPIC, f'{a["slug"]}: unknown topic {a["topic"]}'
    order = {k: i for i, (k, *_) in enumerate(TOPICS)}
    arts.sort(key=lambda a: (order[a["topic"]], int(a.get("order", 50)), a["title"]))
    newest = max(a["date"] for a in arts)
    new_cut = (dt.date.fromisoformat(newest) - dt.timedelta(days=45)).isoformat()
    if new_cut < "2026-11-01":
        new_cut = "2026-11-01"
    by_date = sorted(arts, key=lambda a: (a["date"], a.get("order", "50")), reverse=True)
    out_pages = []

    # ---- articles ----
    (ROOT / "articles").mkdir(exist_ok=True)
    for a in arts:
        body, toc = add_heading_ids(a["body"])
        siblings = [x for x in arts if x["topic"] == a["topic"]]
        i = siblings.index(a)
        prev_a = siblings[i - 1] if i > 0 else None
        next_a = siblings[i + 1] if i + 1 < len(siblings) else None
        t = TOPIC[a["topic"]]
        otp = ""
        if len(toc) >= 2 and a.get("toc") != "no":
            otp = ('<aside class="otp" aria-label="On this page"><h2>On this page</h2><ol>' +
                   "".join(f'<li><a href="#{h}">{esc(html.unescape(x))}</a></li>' for h, x in toc) + "</ol></aside>")
        else:
            otp = "<div></div>"
        pn = ""
        if prev_a:
            pn += f'<a class="pn" href="{prev_a["slug"]}.html"><small>Previous in {t["name"]}</small><span>{esc(prev_a["title"])}</span></a>'
        if next_a:
            pn += f'<a class="pn next" href="{next_a["slug"]}.html"><small>Next in {t["name"]}</small><span>{esc(next_a["title"])}</span></a>'
        updated = f' <span>Updated {fmt_date(a["updated"])}</span>' if a.get("updated") else ""
        page = f"""<header class="article-head"><div class="wrap">
<div class="crumbs"><a href="../articles.html">Articles</a> / <a href="../topics/{a["topic"]}.html">{t["name"]}</a></div>
<h1>{esc(a["title"])}</h1>
<p class="lede">{a["lede"]}</p>
<div class="byline"><span>{esc(a["read"])}</span><span>{fmt_date(a["date"])}</span>{updated}</div>
</div></header>
<div class="wrap layout">{otp}
<article class="prose">
{body.strip()}
<nav class="endmatter" aria-label="More in this topic">{pn}</nav>
</article></div>"""
        jsonld = json.dumps({"@context": "https://schema.org", "@type": "TechArticle", "headline": a["title"],
                             "description": a["description"], "datePublished": a["date"],
                             "author": {"@type": "Person", "name": "Hardik"},
                             "publisher": {"@type": "Organization", "name": "LowLevel Labs"}})
        scripts = "".join(f'<script src="{s}" defer></script>' for s in HLJS)
        path = f"articles/{a['slug']}.html"
        (ROOT / path).write_text(layout(title=a["title"], desc=a["description"], body=page, depth=1, path=path,
                                        current="articles", head_extra=f'<script type="application/ld+json">{jsonld}</script>',
                                        scripts_extra=scripts))
        out_pages.append((path, a.get("updated", a["date"])))

    counts = {k: sum(1 for a in arts if a["topic"] == k) for k in TOPIC}

    # ---- register (home hero) ----
    bits, fields, hi = [], [], 31
    for k, code, w, name, _ in TOPICS:
        lo = hi - w + 1
        rng = f"[{hi}:{lo}]" if w > 1 else f"[{hi}]"
        n = counts[k]
        fields.append(f'<a class="reg-field" href="topics/{k}.html" style="grid-column:span {w}">'
                      f'<span class="code">{code}</span><span class="name">{name}</span>'
                      f'<span class="count">{rng} · {n} article{"s" if n != 1 else ""}</span></a>')
        hi = lo - 1
    bits = "".join(f'<span class="reg-bit" aria-hidden="true">{b}</span>' for b in range(31, -1, -1))
    total = len(arts)

    featured = [a for a in by_date if a.get("featured")][:3]
    feat_html = "".join(
        f'<a href="articles/{a["slug"]}.html"><figure aria-hidden="true">{thumb(a["topic"])}</figure>'
        f'<span class="tag">{TOPIC[a["topic"]]["name"]}</span><h3>{esc(a["title"])}</h3><p>{esc(a["description"])}</p></a>'
        for a in featured)
    latest = "".join(article_row(a, 0, new_cut) for a in by_date[:8])
    topic_rows = "".join(
        f'<a class="topic-row" href="topics/{k}.html"><span class="code">{code}</span><span><h3>{name}</h3><p>{blurb}</p></span></a>'
        for k, code, w, name, blurb in TOPICS)
    home = f"""<section class="hero"><div class="wrap">
<h1>Notes from the layer below the API.</h1>
<p class="lede">Explanations, diagrams and working code for embedded firmware, Linux device drivers, C, assembly, CPU internals and real-time operating systems.</p>
<div class="actions"><a class="btn" href="articles.html">Browse all {total} articles</a><a class="btn ghost" href="projects.html">Guides and exercises</a></div>
<div class="reg" role="navigation" aria-label="Topics">
<div class="reg-head"><span><strong>LLL_TOPICS</strong> topic select register</span><span>offset 0x000 · 32-bit · read/click</span></div>
<div class="reg-grid">{bits}{"".join(fields)}</div>
<div class="reg-foot">Each field is a subject area. Pick one to see every article in it.</div>
</div></div></section>
<section class="section"><div class="wrap">
<div class="section-head"><div><h2>Start here</h2><p>Three in-depth pieces, each with diagrams and code you can run.</p></div></div>
<div class="feature">{feat_html}</div>
</div></section>
<section class="section"><div class="wrap">
<div class="section-head"><div><h2>Latest articles</h2></div><a href="articles.html">All articles</a></div>
<ul class="toc-list">{latest}</ul>
</div></section>
<section class="section"><div class="wrap">
<div class="section-head"><div><h2>Topics</h2></div><a href="topics/index.html">Topic index</a></div>
<div class="topic-table">{topic_rows}</div>
</div></section>"""
    (ROOT / "index.html").write_text(layout(title="LowLevel Labs: embedded systems, drivers and CPU internals",
                                            desc="Explanations, diagrams and working code for embedded firmware, Linux device drivers, C, assembly, CPU architecture, RTOS and VxWorks.",
                                            body=home, depth=0, path="index.html"))
    out_pages.append(("index.html", newest))

    # ---- articles listing ----
    chips = '<button class="chip" type="button" data-topic="all">All</button>' + "".join(
        f'<button class="chip" type="button" data-topic="{k}">{name}</button>' for k, code, w, name, _ in TOPICS)
    rows = "".join(article_row(a, 0, new_cut) for a in arts)
    listing = f"""<section class="page-head"><div class="wrap">
<h1>Articles</h1>
<p class="lede">Every article on the site, grouped by topic. Search by title or keyword, or narrow to one topic.</p>
</div></section>
<section><div class="wrap">
<div class="controls"><label class="search"><span class="skip">Search articles</span>
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
<input id="q" type="search" placeholder="Search, e.g. mutex, DMA, AArch64" autocomplete="off"></label>
<span class="muted" id="count" aria-live="polite"></span></div>
<div class="chips" role="group" aria-label="Filter by topic">{chips}</div>
<ul class="toc-list" id="articleList" style="margin-top:18px">{rows}</ul>
<p class="empty" id="empty" hidden>No articles match that search. Try a shorter keyword or choose All.</p>
</div></section>"""
    (ROOT / "articles.html").write_text(layout(title="Articles", desc="All LowLevel Labs articles on embedded firmware, Linux drivers, C, assembly, CPU architecture, RTOS and VxWorks.",
                                               body=listing, depth=0, path="articles.html", current="articles"))
    out_pages.append(("articles.html", newest))

    # ---- topic pages ----
    (ROOT / "topics").mkdir(exist_ok=True)
    for k, code, w, name, blurb in TOPICS:
        items = "".join(article_row(a, 1, new_cut) for a in arts if a["topic"] == k)
        body = f"""<section class="page-head"><div class="wrap">
<div class="crumbs"><a href="index.html">Topics</a> / <span class="mono">{code}</span></div>
<h1>{name}</h1><p class="lede">{blurb}</p></div></section>
<section><div class="wrap"><ul class="toc-list">{items}</ul></div></section>"""
        path = f"topics/{k}.html"
        (ROOT / path).write_text(layout(title=name, desc=blurb, body=body, depth=1, path=path, current="topics"))
        out_pages.append((path, newest))
    trows = "".join(
        f'<a class="topic-row" href="{k}.html"><span class="code">{code}</span><span><h3>{name}</h3><p>{blurb} <span class="muted">({counts[k]})</span></p></span></a>'
        for k, code, w, name, blurb in TOPICS)
    (ROOT / "topics/index.html").write_text(layout(
        title="Topics", desc="Browse LowLevel Labs by subject area.", depth=1, path="topics/", current="topics",
        body=f'<section class="page-head"><div class="wrap"><h1>Topics</h1><p class="lede">Eight subject areas, from the reset vector up to user-space IPC.</p></div></section><section><div class="wrap"><div class="topic-table">{trows}</div></div></section>'))
    out_pages.append(("topics/", newest))

    # ---- simple pages ----
    for f in sorted((ROOT / "content/pages").glob("*.html")):
        pg = parse(f)
        path = f"{f.stem}.html"
        body = f"""<section class="page-head simple"><div class="wrap">
<h1>{esc(pg["title"])}</h1><p class="lede">{pg["lede"]}</p></div></section>
<section class="simple"><div class="wrap"><div class="prose">{pg["body"]}</div></div></section>"""
        (ROOT / path).write_text(layout(title=pg["title"], desc=pg["description"], body=body, depth=0, path=path, current=f.stem))
        out_pages.append((path, pg["date"]))

    # ---- sitemap ----
    urls = "".join(f"<url><loc>{SITE}/{'' if p == 'index.html' else p}</loc><lastmod>{d}</lastmod></url>\n" for p, d in out_pages)
    (ROOT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    print(f"Built {len(arts)} articles, {len(out_pages)} pages.")


if __name__ == "__main__":
    build()
