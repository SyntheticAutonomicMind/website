#!/usr/bin/env python3
"""Fix redirect stub titles and standardize template pages."""

import re
from pathlib import Path

SITE_ROOT = Path(__file__).resolve().parent.parent
BASE_URL = 'https://www.syntheticautonomicmind.org'

# Fix redirect stub titles
stub_titles = {
    'ai-coding-assistant-macos.html':   ('Redirecting to SAM...', 'products/sam.html'),
    'clio-terminal-ai.html':            ('Redirecting to CLIO...', 'products/clio.html'),
    'local-ai-assistant-macos.html':    ('Redirecting to SAM...', 'products/sam.html'),
    'stable-diffusion-macos.html':      ('Redirecting to ALICE...', 'products/alice.html'),
}

for filename, (title, target) in stub_titles.items():
    fp = SITE_ROOT / filename
    content = fp.read_text(encoding='utf-8')
    content = re.sub(r'<title>[^<]*</title>', f'<title>{title}</title>', content)
    content = re.sub(r'<meta property="og:title"[^>]*content="[^"]*"', f'<meta property="og:title" content="{title}"', content)
    content = re.sub(r'<meta name="twitter:title"[^>]*content="[^"]*"', f'<meta name="twitter:title" content="{title}"', content)
    fp.write_text(content, encoding='utf-8')
    print(f"Fixed title: {filename} -> {title}")

def get_h1(content):
    m = re.search(r'<h1[^>]*>\s*(.*?)\s*</h1>', content, re.DOTALL)
    if m:
        return re.sub(r'<[^>]+>', '', m.group(1)).strip()
    return None

# Standardize template pages
templates_dir = SITE_ROOT / 'docs' / 'SAM' / 'developer' / 'templates'
templates = sorted(templates_dir.rglob('*.html'))
for fp in templates:
    content = fp.read_text(encoding='utf-8', errors='replace')
    original = content
    rel_path = str(fp.relative_to(SITE_ROOT)).replace('\\', '/')
    page_title = get_h1(content) or fp.stem.replace('-', ' ').title()

    depth = len(fp.relative_to(SITE_ROOT).parts) - 1
    prefix = '../' * depth
    title = f'{page_title} | SAM'
    desc = 'SAM templates for human-AI collaboration: prompts, handoffs, and tools.'
    canonical = f'{BASE_URL}/{rel_path}'

    head = f'''<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{desc}">
    <link rel="canonical" href="{canonical}">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{desc}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{canonical}">
    <meta property="og:image" content="https://www.syntheticautonomicmind.org/images/sam.png">
    <link rel="stylesheet" href="{prefix}css/styles.css?v=13">
</head>'''

    content = re.sub(r'<head>.*?</head>', head, content, count=1, flags=re.DOTALL)

    # Wrap in main/article
    if '<main>' not in content:
        content = re.sub(
            r'(<!--\s*Documentation Content\s*-->\s*\n\s*)<div class="doc-container">',
            r'\1<main>\n        <article class="doc-page" data-product="SAM" data-doc-path="' + rel_path + '">\n    <div class="doc-container">',
            content, count=1, flags=re.DOTALL
        )
        content = re.sub(
            r'(\s*)<div id="footer-placeholder">',
            '</div>\n    </article>\n</main>\n\n    <div id="footer-placeholder">',
            content, count=1
        )

    content = content.replace('css/styles.css?v=12', 'css/styles.css?v=13')

    # Add script tags if missing
    if '<script src=' not in content:
        content = content.replace(
            '<div id="footer-placeholder"></div>',
            '<div id="footer-placeholder"></div>\n    <script src="' + prefix + 'js/main.js?v=13"></script>\n    <script src="' + prefix + 'js/include.js"></script>'
        )

    if content != original:
        fp.write_text(content, encoding='utf-8')
        print(f"Standardized: {rel_path}")

# Also handle the templates index page
fp = templates_dir / 'index.html'
if fp.exists():
    content = fp.read_text(encoding='utf-8', errors='replace')
    original = content
    rel_path = str(fp.relative_to(SITE_ROOT)).replace('\\', '/')
    depth = len(fp.relative_to(SITE_ROOT).parts) - 1
    prefix = '../' * depth

    head = f'''<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Unbroken Method Templates | SAM</title>
    <meta name="description" content="Templates for human-AI collaboration: quick start prompts, full collaboration prompts, handoff templates, and anti-patterns.">
    <link rel="canonical" href="{BASE_URL}/{rel_path}">
    <meta property="og:title" content="Unbroken Method Templates | SAM">
    <meta property="og:description" content="Templates for human-AI collaboration: quick start prompts, full collaboration prompts, handoff templates, and anti-patterns.">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{BASE_URL}/{rel_path}">
    <meta property="og:image" content="https://www.syntheticautonomicmind.org/images/sam.png">
    <link rel="stylesheet" href="{prefix}css/styles.css?v=13">
</head>'''

    content = re.sub(r'<head>.*?</head>', head, content, count=1, flags=re.DOTALL)
    content = content.replace('css/styles.css?v=12', 'css/styles.css?v=13')

    if '<main>' not in content:
        content = re.sub(
            r'(<!--\s*Documentation Content\s*-->\s*\n\s*)<div class="doc-container">',
            r'\1<main>\n        <article class="doc-page" data-product="SAM" data-doc-path="' + rel_path + '">\n    <div class="doc-container">',
            content, count=1, flags=re.DOTALL
        )
        content = re.sub(
            r'(\s*)<div id="footer-placeholder">',
            '</div>\n    </article>\n</main>\n\n    <div id="footer-placeholder">',
            content, count=1
        )

    if '<script src=' not in content:
        content = content.replace(
            '<div id="footer-placeholder"></div>',
            '<div id="footer-placeholder"></div>\n    <script src="' + prefix + 'js/main.js?v=13"></script>\n    <script src="' + prefix + 'js/include.js"></script>'
        )

    if content != original:
        fp.write_text(content, encoding='utf-8')
        print(f"Standardized: {rel_path}")

print("Done!")
