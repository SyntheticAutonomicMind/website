#!/usr/bin/env python3
"""
Standardize all documentation pages.

Transformations per page:
1. Strip codehilite divs -> clean <pre><code> blocks
2. Standardize <head> metadata (title, description, canonical, OG tags)
3. Replace old breadcrumb div with standardized one
4. Wrap content in <main><article> with data-prev/data-next attributes
5. Bump script version to ?v=13

Usage:  python3 scripts/standardize-docs.py
"""

import re
import html as html_module
from pathlib import Path

SITE_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = SITE_ROOT / 'docs'
BASE_URL = 'https://www.syntheticautonomicmind.org'

PRODUCTS = {
    'SAM':    {'label': 'SAM',   'img': '/images/sam.png',   'desc': 'Native macOS AI assistant with voice control, document RAG, autonomous agents, and multi-provider support.'},
    'CLIO':   {'label': 'CLIO',  'img': '/images/clio.png',  'desc': 'Terminal-native AI development agent with multi-agent coordination, remote execution, and persistent sessions.'},
    'ALICE':  {'label': 'ALICE', 'img': '/images/alice.png', 'desc': 'Local Stable Diffusion and audio generation server with web UI, OpenAI-compatible API, and multi-GPU support.'},
    'shared': {'label': 'Shared', 'img': '/images/sam.png',  'desc': 'The Unbroken Method for human-AI collaboration and ecosystem documentation.'},
}

SECTIONS = {
    'end-user':   'End User',
    'power-user': 'Power User',
    'developer':  'Developer',
    'templates':  'Templates',
}

# Doc pagination: filepath -> (next_title, next_filepath)
DOC_FLOW = {
    'docs/SAM/end-user/getting-started.html':  ('Features Overview',      'docs/SAM/end-user/features-overview.html'),
    'docs/SAM/end-user/features-overview.html': ('Memory & RAG Guide',    'docs/SAM/end-user/memory-and-rag.html'),
    'docs/SAM/end-user/memory-and-rag.html':   ('Shared Topics',         'docs/SAM/end-user/shared-topics.html'),
    'docs/SAM/end-user/shared-topics.html':    ('Use Cases',             'docs/SAM/end-user/use-cases.html'),
    'docs/SAM/end-user/use-cases.html':        ('SAM Web',               'docs/SAM/end-user/sam-web.html'),
    'docs/SAM/end-user/sam-web.html':          (None, None),
    'docs/SAM/power-user/configuration.html':  ('Tools Reference',       'docs/SAM/power-user/tools-reference.html'),
    'docs/SAM/power-user/tools-reference.html':('Advanced Workflows',      'docs/SAM/power-user/advanced-workflows.html'),
    'docs/SAM/power-user/advanced-workflows.html': ('Troubleshooting Guide', 'docs/SAM/power-user/troubleshooting.html'),
    'docs/SAM/power-user/troubleshooting.html':('None', None),
    'docs/SAM/developer/developers-guide.html': ('Architecture',          'docs/SAM/developer/architecture.html'),
    'docs/SAM/developer/architecture.html':    ('API Reference',         'docs/SAM/developer/api-reference.html'),
    'docs/SAM/developer/api-reference.html':   ('Building from Source',  'docs/SAM/developer/building.html'),
    'docs/SAM/developer/building.html':        ('Templates Index',       'docs/SAM/developer/templates/index.html'),
    'docs/SAM/integration-alice.html':         (None, None),
}

CLIO_FLOW = {
    'docs/CLIO/installation.html':       ('Quick Start', 'docs/CLIO/getting-started.html'),
    'docs/CLIO/getting-started.html':    ('Sessions & Memory', 'docs/CLIO/sessions.html'),
    'docs/CLIO/sessions.html':           ('Tools Reference', 'docs/CLIO/tools-reference.html'),
    'docs/CLIO/tools-reference.html':    ('Slash Commands', 'docs/CLIO/slash-commands.html'),
    'docs/CLIO/slash-commands.html':     ('Configuration', 'docs/CLIO/configuration.html'),
    'docs/CLIO/configuration.html':      ('AI Providers', 'docs/CLIO/api-providers.html'),
    'docs/CLIO/api-providers.html':      ('Workflows', 'docs/CLIO/workflows.html'),
    'docs/CLIO/workflows.html':          ('Troubleshooting', 'docs/CLIO/troubleshooting.html'),
    'docs/CLIO/troubleshooting.html':    ('Multi-Agent', 'docs/CLIO/multi-agent.html'),
    'docs/CLIO/multi-agent.html':        ('Remote Execution', 'docs/CLIO/remote-execution.html'),
    'docs/CLIO/remote-execution.html':   ('CLIO + SAM Integration', 'docs/CLIO/integration-sam.html'),
    'docs/CLIO/integration-sam.html':    ('CLIO + ALICE Integration', 'docs/CLIO/integration-alice.html'),
    'docs/CLIO/integration-alice.html':  (None, None),
}

ALICE_FLOW = {
    'docs/ALICE/installation.html':          ('Getting Started', 'docs/ALICE/getting-started.html'),
    'docs/ALICE/getting-started.html':       ('Configuration', 'docs/ALICE/configuration.html'),
    'docs/ALICE/configuration.html':         ('Web Interface', 'docs/ALICE/web-interface.html'),
    'docs/ALICE/web-interface.html':         ('Generation Parameters', 'docs/ALICE/generation-parameters.html'),
    'docs/ALICE/generation-parameters.html': ('Model Management', 'docs/ALICE/model-management.html'),
    'docs/ALICE/model-management.html':      ('Supported Models', 'docs/ALICE/supported-models.html'),
    'docs/ALICE/supported-models.html':      ('Gallery & Privacy', 'docs/ALICE/gallery.html'),
    'docs/ALICE/gallery.html':               ('Performance', 'docs/ALICE/performance.html'),
    'docs/ALICE/performance.html':           ('Privacy Controls', 'docs/ALICE/privacy-controls.html'),
    'docs/ALICE/privacy-controls.html':      ('Authentication', 'docs/ALICE/authentication.html'),
    'docs/ALICE/authentication.html':        ('API Reference', 'docs/ALICE/api-reference.html'),
    'docs/ALICE/api-reference.html':         ('ALICE + SAM Integration', 'docs/ALICE/integration-sam.html'),
    'docs/ALICE/integration-sam.html':       ('ALICE + CLIO Integration', 'docs/ALICE/integration-clio.html'),
    'docs/ALICE/integration-clio.html':      ('Deployment Guide', 'docs/ALICE/deployment.html'),
    'docs/ALICE/deployment.html':            (None, None),
}

SHARED_FLOW = {
    'docs/shared/the-unbroken-method.html': ('The Reflexive Ecosystem', 'docs/shared/the-reflexive-ecosystem.html'),
    'docs/shared/the-reflexive-ecosystem.html': ('Contributing', 'docs/shared/contributing.html'),
    'docs/shared/contributing.html': ('Antipatterns', 'docs/shared/antipatterns.html'),
    'docs/shared/antipatterns.html': (None, None),
}

ALL_FLOW = {**DOC_FLOW, **CLIO_FLOW, **ALICE_FLOW, **SHARED_FLOW}


def get_product_and_section(parts):
    if 'docs' in parts:
        di = parts.index('docs')
        if di + 1 < len(parts) and parts[di + 1] in PRODUCTS:
            prod = parts[di + 1]
            section = parts[di + 2] if di + 2 < len(parts) - 1 else None
            return prod, section
    return None, None


def get_path_prefix(parts):
    """Prefix of '../' to reach site root from this file."""
    return '../' * (len(parts) - 1)


def get_docs_prefix(parts):
    """Prefix of '../' to reach docs/ directory from this file."""
    if 'docs' in parts:
        di = parts.index('docs')
        return '../' * (len(parts) - 1 - di)
    return ''


def extract_h1(content):
    m = re.search(r'<h1[^>]*>\s*(.*?)\s*</h1>', content, re.DOTALL)
    if m:
        title = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        return html_module.unescape(title)
    return None


def extract_description(content):
    # Lead paragraph
    m = re.search(r'<p class="lead">\s*(.*?)\s*</p>', content, re.DOTALL)
    if m:
        d = html_module.unescape(re.sub(r'<[^>]+>', '', m.group(1)).strip())
        if len(d) > 10:
            return d[:160]
    # First <p> in doc-content
    m = re.search(r'class="doc-content">(.*?)</div>\s*</div>\s*</div>', content, re.DOTALL)
    if m:
        p = re.search(r'<p>\s*(.*?)\s*</p>', m.group(1), re.DOTALL)
        if p:
            d = html_module.unescape(re.sub(r'<[^>]+>', '', p.group(1)).strip())
            if len(d) > 10:
                return d[:160]
    return ''


def clean_codehilite(content):
    """Convert <div class="codehilite"><pre>...<span>...</span>...</pre></div> to <pre><code>text</code></pre>"""
    def replacer(m):
        inner = m.group(1)
        # Remove leading empty <span></span>
        inner = re.sub(r'^<span></span>', '', inner)
        # Unwrap all <span> tags iteratively
        prev = None
        while prev != inner:
            prev = inner
            inner = re.sub(r'<span[^>]*>(.*?)</span>', r'\1', inner, flags=re.DOTALL)
        inner = re.sub(r'</?span[^>]*>', '', inner)
        inner = html_module.unescape(inner)
        return f'<pre><code>{inner}</code></pre>'

    content = re.sub(
        r'<div class="codehilite">\s*<pre>(.*?)</pre>\s*</div>',
        replacer, content, flags=re.DOTALL
    )
    return content


def build_breadcrumb(parts, product_key, section, page_title):
    docs_prefix = get_docs_prefix(parts)
    product = PRODUCTS[product_key]
    crumbs = [
        {'label': 'Documentation', 'href': f'{docs_prefix}index.html'},
        {'label': product['label'], 'href': f'{docs_prefix}{product_key}/index.html'},
    ]
    if section and section in SECTIONS and parts[-1] != 'index.html':
        # Only add section crumb if the file is in a subdirectory
        # (not directly in the product root)
        path_depth = len(parts) - parts.index('docs') - 1  # files in docs/
        if path_depth > 2:  # docs/SAM/file.html = depth 2, docs/SAM/sub/file.html = depth 3
            crumbs.append({'label': SECTIONS[section], 'href': ''})

    html = ['<nav class="doc-breadcrumb" aria-label="Breadcrumb">']
    for i, c in enumerate(crumbs):
        if i > 0:
            html.append('<span class="breadcrumb-separator">/</span>')
        if c['href']:
            html.append(f'<a href="{c["href"]}">{c["label"]}</a>')
        else:
            html.append(f'<span>{c["label"]}</span>')
    html.append('<span class="breadcrumb-separator">/</span>')
    html.append(f'<span>{page_title}</span>')
    html.append('</nav>')
    return ''.join(html)


def get_prev_next(rel_path):
    prev_attr, next_attr = '', ''
    for fpath, (ntitle, nnext) in ALL_FLOW.items():
        if fpath == rel_path and nnext:
            next_attr = f' data-next="{nnext}|{ntitle}"'
        if nnext == rel_path and ntitle:
            prev_attr = f' data-prev="{fpath}|{ntitle}"'
    return prev_attr, next_attr


def process_page(filepath):
    content = filepath.read_text(encoding='utf-8', errors='replace')
    original = content
    changes = []
    rel_path = str(filepath.relative_to(SITE_ROOT)).replace('\\', '/')
    parts = filepath.relative_to(SITE_ROOT).parts
    product_key, section = get_product_and_section(parts)
    if not product_key:
        return False, []

    # 1. Clean codehilite
    if 'codehilite' in content:
        content = clean_codehilite(content)
        changes.append('codehilite -> clean pre/code')

    # 2. Get page title
    page_title = extract_h1(content)
    if not page_title:
        return False, []

    # 3. Standardize head
    description = extract_description(content)
    if not description:
        description = PRODUCTS[product_key].get('desc', '')[:160]
    prefix = get_path_prefix(parts)
    product = PRODUCTS[product_key]
    title = f'{page_title} | {product["label"]}'
    canonical = f'{BASE_URL}/{rel_path}'

    head = f'''<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{description}">
    <link rel="canonical" href="{canonical}">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{canonical}">
    <meta property="og:image" content="https://www.syntheticautonomicmind.org{product["img"]}">
    <link rel="stylesheet" href="{prefix}css/styles.css?v=13">
</head>'''

    content = re.sub(r'<head>.*?</head>', head, content, count=1, flags=re.DOTALL)
    changes.append('standardized <head>')

    # 4. Replace breadcrumb
    old_bc = re.search(r'<div class="doc-breadcrumb">.*?</div>', content, re.DOTALL)
    if old_bc:
        new_bc = build_breadcrumb(parts, product_key, section, page_title)
        content = content[:old_bc.start()] + new_bc + content[old_bc.end():]
        changes.append('standardized breadcrumb')

    # 5. Wrap in <main><article> with data attributes
    prev_attr, next_attr = get_prev_next(rel_path)
    article_attrs = f'class="doc-page" data-product="{product_key}" data-doc-path="{rel_path}"'
    if prev_attr:
        article_attrs += prev_attr
    if next_attr:
        article_attrs += next_attr

    # Find the opening: <!-- Documentation Content --> ... <div class="doc-container">
    opening_pattern = re.compile(
        r'(<!--\s*Documentation Content\s*-->\s*\n\s*)<div class="doc-container">',
        re.DOTALL
    )
    if opening_pattern.search(content):
        content = opening_pattern.sub(
            r'\1<main>\n        <article ' + article_attrs + '>\n    <div class="doc-container">',
            content,
            count=1
        )
        changes.append('main/article wrapper (open)')

    # Find the closing: </div>\s*\n\s*<div id="footer-placeholder">
    closing_pattern = re.compile(
        r'</div>\s*\n\s*<div id="footer-placeholder"></div>',
        re.DOTALL
    )
    if closing_pattern.search(content):
        content = closing_pattern.sub(
            '</div>\n    </article>\n</main>\n\n    <div id="footer-placeholder"></div>',
            content,
            count=1
        )
        changes.append('main/article wrapper (close)')

    # 6. Bump script version
    content = content.replace('js/main.js?v=12', 'js/main.js?v=13')

    # 7. Ensure docs.js is not needed in HTML (loaded dynamically by include.js)

    if content != original:
        filepath.write_text(content, encoding='utf-8')
        return True, changes
    return False, changes


def main():
    doc_files = []
    for f in DOCS_DIR.rglob('*.html'):
        if f.name == 'index.html' or f.name == 'clio.html':
            continue
        if 'templates' in f.parts:
            continue
        doc_files.append(f)
    doc_files.sort()

    print(f"Processing {len(doc_files)} doc pages...\n")
    modified = 0
    for fp in doc_files:
        rel = fp.relative_to(SITE_ROOT)
        try:
            changed, changes = process_page(fp)
            status = "  OK " if changed else "  - "
            print(f"{status} {rel}")
            for c in changes:
                print(f"      -> {c}")
            if changed:
                modified += 1
        except Exception as e:
            print(f"  ERR {rel}: {e}")

    print(f"\nDone: {modified} modified, {len(doc_files)} total")


if __name__ == '__main__':
    main()
