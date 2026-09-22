#!/usr/bin/env python3
"""
Render eula.md -> eula.html in the site's legal-page layout (same shell as privacy.html).
GitHub Pages used to do this via Jekyll; Cloudflare serves files as-is, so rerun this
after every eula.md edit and commit both files.
"""
import html
from pathlib import Path

from build_learning_center import parse_blocks, render_blocks

BASE_DIR = Path(__file__).resolve().parent
BR = "\u0000BR\u0000"  # survives html.escape; swapped for <br> after rendering


def keep_line_breaks(md):
    """Preserve single newlines inside paragraphs (lettered clauses, address block)."""
    lines = md.split("\n")
    out = []
    for i, line in enumerate(lines):
        nxt = lines[i + 1].strip() if i + 1 < len(lines) else ""
        t = line.strip()
        is_text = t and not t.startswith(("#", "- ", "|", "```")) and t != "---"
        nxt_is_text = nxt and not nxt.startswith(("#", "- ", "|", "```")) and nxt != "---"
        out.append(line + BR if is_text and nxt_is_text else line)
    return "\n".join(out)


PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Armored Vault — End-User License Agreement</title>
    <meta name="description" content="Armored Vault End-User License Agreement between you and Beast Studio Dev LLC.">
    <link rel="icon" type="image/png" href="assets/app-icon.png">
    <link rel="apple-touch-icon" href="assets/app-icon.png">
    <link rel="stylesheet" href="style.css?v=20260701a">
</head>
<body>

<!-- ═══════════════════ NAV ═══════════════════ -->
<header class="nav">
    <div class="nav-inner">
        <a href="index.html#top" class="nav-brand">
            <img class="nav-icon" src="assets/app-icon.png" alt="">
            <span>Armored Vault</span>
        </a>
        <button class="nav-toggle" aria-label="Toggle menu" aria-expanded="false">
            <span></span><span></span><span></span>
        </button>
        <nav class="nav-links">
            <a href="index.html#features">Features</a>
            <a href="index.html#security">Security</a>
            <a href="learning-center.html">Learning Center</a>
            <a href="support.html">Support</a>
            <a href="index.html#download" class="nav-cta">Download</a>
        </nav>
    </div>
</header>

<!-- ═══════════════════ EULA HERO ═══════════════════ -->
<section class="support-hero">
    <div class="support-hero-inner">
        <span class="eyebrow">LICENSE AGREEMENT</span>
        <h1>End-User License Agreement</h1>
    </div>
</section>

<!-- ═══════════════════ EULA BODY (generated from eula.md by build_eula.py) ═══════════════════ -->
<section class="legal">
    <div class="legal-inner">
{body}
    </div>
</section>

<!-- ═══════════════════ FOOTER ═══════════════════ -->
<footer class="footer">
    <div class="footer-inner">
        <div class="footer-brand">
            <img class="nav-icon" src="assets/app-icon.png" alt="">
            <strong>Armored Vault</strong>
            <p>Encrypted Vault for iPad and Mac</p>
        </div>
        <nav class="footer-links">
            <a href="learning-center.html">Learning Center</a>
            <a href="support.html">Support</a>
            <a href="privacy.html">Privacy Policy</a>
            <a href="security.html">Security Model</a>
            <a href="index.html#features">Features</a>
            <a href="support.html#faq">FAQ</a>
        </nav>
    </div>
    <div class="footer-legal">
        <p>&copy; 2026 Beast Studio. All rights reserved.</p>
    </div>
</footer>

<script src="assets/nav.js"></script>
</body>
</html>
"""


def main():
    md = (BASE_DIR / "eula.md").read_text(encoding="utf-8")
    body = render_blocks(parse_blocks(keep_line_breaks(md)))
    body = body.replace(html.escape(BR), "<br>").replace(BR, "<br>")
    out = BASE_DIR / "eula.html"
    out.write_text(PAGE.format(body=body), encoding="utf-8")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
