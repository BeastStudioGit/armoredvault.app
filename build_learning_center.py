#!/usr/bin/env python3
"""
Convert Armored Vault Learning Center markdown to HTML pages for armoredvault.app.
Mirrors the SwiftUI parser semantics: H1/H2/H3, bullets, numbered lists,
fenced code, tables, horizontal rules, paragraphs, and inline **bold**, *italic*, `code`.
"""
import os
import re
import html
from pathlib import Path

SRC_DIR = Path("/Volumes/Mac Studio Swap/Armored Vault/ArmoredVault/LearningCenter")
OUT_DIR = Path("/Volumes/Mac Studio Swap/armoredvault.app/learning")

ARTICLES = [
    ("01-how-encryption-works",
     "How Armored Vault Encrypts Your Files",
     "AES-256-GCM, PBKDF2, KEK-wrapped MFEK, UUID filenames — the architecture, in plain language.",
     "01",
     "01-encryption.svg",
     "Plaintext file names dissolving into encrypted ciphertext blocks",
     "April 6, 2026"),
    ("02-choosing-a-strong-passphrase",
     "Choosing a Strong Passphrase",
     "Why a 10-word Diceware passphrase is the right answer, and how Face ID still keeps you safe.",
     "02",
     "02-passphrase.svg",
     "Three dice surrounded by floating Diceware words",
     "April 9, 2026"),
    ("03-what-armored-vault-doesnt-protect-against",
     "What Armored Vault Doesn't Protect Against",
     "The honest list of limits — and the common-sense moves that defeat each one.",
     "03",
     "03-limits.svg",
     "A shield with cracks symbolizing the limits of protection",
     "April 12, 2026"),
    ("04-your-files-outside-the-vault",
     "Your Files Outside the Vault",
     "Importing, exporting, and the boundary between vaulted and unvaulted state.",
     "04",
     "04-boundary.svg",
     "A boundary line dividing vaulted files from unvaulted ones",
     "April 15, 2026"),
    ("05-why-i-dont-collect-your-data",
     "Why I Don't Collect Your Data",
     "Zero analytics, zero telemetry, zero servers — and how you can verify it.",
     "05",
     "05-no-data.svg",
     "A device with all outbound network requests blocked",
     "April 18, 2026"),
]

NUMBERED_RE = re.compile(r'^(\d+)\.\s+(.*)$')

def strip_frontmatter(md):
    lines = md.split("\n")
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                return "\n".join(lines[i+1:])
    return md

def inline_md(s):
    """Escape HTML, then apply inline markdown: **bold**, *italic*, `code`."""
    s = html.escape(s)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    s = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'(?<![*\w])\*([^*\n]+)\*(?!\w)', r'<em>\1</em>', s)
    return s

def parse_blocks(md):
    """Yield (kind, payload) tuples."""
    lines = md.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        t = line.strip()

        # Fenced code block
        if t.startswith("```"):
            buf = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                buf.append(lines[i])
                i += 1
            i += 1  # consume closing fence
            yield ("code", "\n".join(buf))
            continue

        # Table
        if t.startswith("|") and t.endswith("|"):
            rows = []
            while i < len(lines):
                tt = lines[i].strip()
                if tt.startswith("|") and tt.endswith("|"):
                    cells = [c.strip() for c in tt[1:-1].split("|")]
                    rows.append(cells)
                    i += 1
                else:
                    break
            if len(rows) >= 2:
                header = rows[0]
                body = rows[2:] if len(rows) >= 3 else []
                yield ("table", (header, body))
            continue

        # Horizontal rule (after frontmatter strip — `---` between paragraphs)
        if t == "---":
            yield ("rule", None)
            i += 1
            continue

        # Headings
        if t.startswith("### "):
            yield ("h3", t[4:])
            i += 1
            continue
        if t.startswith("## "):
            yield ("h2", t[3:])
            i += 1
            continue
        if t.startswith("# "):
            yield ("h1", t[2:])
            i += 1
            continue

        # Bullets — group consecutive
        if t.startswith("- "):
            items = []
            while i < len(lines):
                tt = lines[i].strip()
                if tt.startswith("- "):
                    items.append(tt[2:])
                    i += 1
                else:
                    break
            yield ("ul", items)
            continue

        # Numbered list — group consecutive
        m = NUMBERED_RE.match(t)
        if m:
            items = []
            while i < len(lines):
                tt = lines[i].strip()
                mm = NUMBERED_RE.match(tt)
                if mm:
                    items.append(mm.group(2))
                    i += 1
                else:
                    break
            yield ("ol", items)
            continue

        # Empty line
        if t == "":
            i += 1
            continue

        # Paragraph
        para = [t]
        i += 1
        while i < len(lines):
            tt = lines[i].strip()
            if (tt == "" or tt.startswith("#") or tt.startswith("- ")
                    or tt.startswith("|") or tt.startswith("```")
                    or tt == "---" or NUMBERED_RE.match(tt)):
                break
            para.append(tt)
            i += 1
        yield ("p", " ".join(para))

def render_blocks(blocks):
    out = []
    for kind, payload in blocks:
        if kind == "h1":
            # Skip the H1 — we render the article title in the page hero.
            continue
        elif kind == "h2":
            out.append(f"<h2>{inline_md(payload)}</h2>")
        elif kind == "h3":
            out.append(f"<h3>{inline_md(payload)}</h3>")
        elif kind == "p":
            out.append(f"<p>{inline_md(payload)}</p>")
        elif kind == "ul":
            items = "".join(f"<li>{inline_md(it)}</li>" for it in payload)
            out.append(f"<ul>{items}</ul>")
        elif kind == "ol":
            items = "".join(f"<li>{inline_md(it)}</li>" for it in payload)
            out.append(f"<ol>{items}</ol>")
        elif kind == "code":
            out.append(f"<pre><code>{html.escape(payload)}</code></pre>")
        elif kind == "table":
            header, body = payload
            ths = "".join(f"<th>{inline_md(c)}</th>" for c in header)
            trs = []
            for row in body:
                tds = "".join(f"<td>{inline_md(c)}</td>" for c in row)
                trs.append(f"<tr>{tds}</tr>")
            out.append(
                "<div class=\"table-wrap\"><table>"
                f"<thead><tr>{ths}</tr></thead>"
                f"<tbody>{''.join(trs)}</tbody>"
                "</table></div>"
            )
        elif kind == "rule":
            out.append("<hr>")
    return "\n".join(out)

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} — Armored Vault Learning Center</title>
    <meta name="description" content="{summary}">
    <link rel="icon" type="image/png" href="../assets/app-icon.png">
    <link rel="apple-touch-icon" href="../assets/app-icon.png">
    <link rel="stylesheet" href="../style.css?v=20260426e">
</head>
<body>

<header class="nav">
    <div class="nav-inner">
        <a href="../index.html#top" class="nav-brand">
            <img class="nav-icon" src="../assets/app-icon.png" alt="">
            <span>Armored Vault</span>
        </a>
        <button class="nav-toggle" aria-label="Toggle menu" aria-expanded="false">
            <span></span><span></span><span></span>
        </button>
        <nav class="nav-links">
            <a href="../index.html#features">Features</a>
            <a href="../index.html#security">Security</a>
            <a href="../learning-center.html">Learning Center</a>
            <a href="../support.html">Support</a>
            <a href="../index.html#download" class="nav-cta">Download</a>
        </nav>
    </div>
</header>

<section class="support-hero article-hero">
    <div class="support-hero-inner">
        <a href="../learning-center.html" class="article-back">&larr; Learning Center</a>
        <span class="eyebrow">LEARNING CENTER &middot; ARTICLE {num}</span>
        <h1>{title}</h1>
        <p class="article-meta">By Robert Lewis &middot; {date}</p>
    </div>
</section>

<div class="article-hero-image">
    <img src="images/{image}" alt="{image_alt}" loading="lazy">
</div>

<article class="article-section">
    <div class="article-inner">
        <div class="article-body">
{body}
        </div>
        {nav_block}
    </div>
</article>

<footer class="footer">
    <div class="footer-inner">
        <div class="footer-brand">
            <img class="nav-icon" src="../assets/app-icon.png" alt="">
            <strong>Armored Vault</strong>
            <p>Encrypted Vault for iPad</p>
        </div>
        <nav class="footer-links">
            <a href="../learning-center.html">Learning Center</a>
            <a href="../support.html">Support</a>
            <a href="../privacy.html">Privacy Policy</a>
            <a href="../index.html#features">Features</a>
        </nav>
    </div>
    <div class="footer-legal">
        <p>&copy; 2026 Beast Studio. All rights reserved.</p>
    </div>
</footer>

<script src="../assets/nav.js"></script>
</body>
</html>
"""

def nav_block(prev_a, next_a):
    parts = ['<div class="article-pager">']
    if prev_a:
        parts.append(f'<a class="pager prev" href="{prev_a[0]}.html"><span class="pager-label">&larr; Previous</span><span class="pager-title">{html.escape(prev_a[1])}</span></a>')
    else:
        parts.append('<span class="pager pager-empty"></span>')
    if next_a:
        parts.append(f'<a class="pager next" href="{next_a[0]}.html"><span class="pager-label">Next &rarr;</span><span class="pager-title">{html.escape(next_a[1])}</span></a>')
    else:
        parts.append('<span class="pager pager-empty"></span>')
    parts.append('</div>')
    return "\n".join(parts)

def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for idx, (slug, title, summary, num, image, image_alt, date) in enumerate(ARTICLES):
        src = SRC_DIR / f"{slug}.md"
        md = strip_frontmatter(src.read_text(encoding="utf-8"))
        blocks = list(parse_blocks(md))
        body = render_blocks(blocks)
        prev_a = ARTICLES[idx-1][:2] if idx > 0 else None
        next_a = ARTICLES[idx+1][:2] if idx < len(ARTICLES)-1 else None
        page = PAGE.format(
            title=html.escape(title),
            summary=html.escape(summary),
            body=body,
            nav_block=nav_block(prev_a, next_a),
            num=num,
            image=image,
            image_alt=html.escape(image_alt),
            date=html.escape(date),
        )
        out_path = OUT_DIR / f"{slug}.html"
        out_path.write_text(page, encoding="utf-8")
        print(f"wrote {out_path}")

if __name__ == "__main__":
    main()
