#!/usr/bin/env python3
"""
Fix breadcrumb links and process templates pages.
Run AFTER standardize-docs.py to correct path calculations.
"""

import re
import html as html_module
from pathlib import Path

SITE_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = SITE_ROOT / 'docs'

PRODUCTS = {
    'SAM':    {'label': 'SAM',   'color': 'sam',   'img': '/images/sam.png',   'desc': 'Native macOS AI assistant with voice control, document RAG, autonomous agents, and multi-provider support.'},
    'CLIO':   {'label': 'CLIO',  'color': 'clio',  'img': '/images/clio.png',  'desc': 'Terminal-native AI development agent with multi-agent coordination, remote execution, and persistent sessions.'},
    'ALICE':  {'label': 'ALICE', 'color': 'alice', 'img': '/images/alice.png', 'desc': 'Local Stable Diffusion and audio generation server with web UI, OpenAI-compatible API, and multi-GPU support.'},
    'shared': {'label': 'Shared', 'color': 'shared', 'img': '/images/sam.png',  'desc': 'The Unbroken Method for human-AI collaboration and ecosystem documentation.'},
}

SECTIONS = {
    'end-user':   'End User',
    'power-user': 'Power User',
    'developer':  'Developer',
    'templates':  'Templates',
}

def get_product_and_section(parts):
    if 'docs' in parts:
        di = parts.index('docs')
        if di + 1 < len(parts) and parts[di + 1] in PRODUCTS:
            prod = parts[di + 1]
            section = parts[di + 2] if di + 2 < len(parts) - 1 else None
            return prod, section, di
    return None, None, -1

def docs_prefix(parts, di):
    """Prefix of '../' to reach docs/ directory from file's directory."""
    # Number of directory components between 'docs' and the file's parent dir
    levels_in_docs = len(parts) - 2 - di  # -1 for filename, -1 for 'docs' itself
    return '../' * levels_in_docs

def build_breadcrumb(parts, product_key, section, di, page_title):
    """Build correct breadcrumb HTML."""
    dp = docs_prefix(parts, di)
    product = PRODUCTS[product_key]

    crumbs = []
    crumbs.append({'label': 'Documentation', 'href': f'{dp}index.html'})

    # For shared pages, there's no shared/index.html — just show the label
    has_product_index = product_key != 'shared'
    if has_product_index:
        crumbs.append({'label': product['label'], 'href': f'{dp}{product_key}/index.html'})

    # Section crumb (only if the file is in a subdirectory, not directly in product dir)
    levels_in_docs = len(parts) - 2 - di  # same as docs_prefix multiplier
    if section and section in SECTIONS and levels_in_docs > 1:
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

def clean_codehilite(content):
    def replacer(m):
        inner = m.group(1)
        inner = re.sub(r'^<span></span>', '', inner)
        prev = None
        while prev != inner:
            prev = inner
            inner = re.sub(r'<span[^>]*>(.*?)</span>', r'\1', inner, flags=re.DOTALL)
        inner = re.sub(r'</?span[^>]*>', '', inner)
        inner = html_module.unescape(inner)
        return f'<pre><code>{inner}</code></pre>'
    content = re.sub(r'<div class="codehilite">\s*<pre>(.*?)</pre>\s*</div>', replacer, content, flags=re.DOTALL)
    return content

def fix_breadcrumb(content, filepath, rel_path):
    parts = filepath.relative_to(SITE_ROOT).parts
    product_key, section, di = get_product_and_section(parts)
    if not product_key:
        return False, 'no product'

    page_title = extract_h1(content)
    if not page_title:
        return False, 'no h1 title'

    # Replace existing breadcrumb (match both <div> and <nav> versions)
    new_bc = build_breadcrumb(parts, product_key, section, di, page_title)
    old_pattern = r'<nav class="doc-breadcrumb".*?</nav>|<div class="doc-breadcrumb">.*?</div>'
    new_content, count = re.subn(old_pattern, new_bc, content, count=1, flags=re.DOTALL)
    if count == 0:
        return False, 'no breadcrumb found'
    return True, new_content

def extract_h1(content):
    m = re.search(r'<h1[^>]*>\s*(.*?)\s*</h1>', content, re.DOTALL)
    if m:
        title = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        return html_module.unescape(title)
    return None

def fix_codeblocks(filepath):
    """Clean codehilite divs on a single file."""
    content = filepath.read_text(encoding='utf-8', errors='replace')
    if 'codehilite' not in content:
        return False, 'no codehilite'
    content = clean_codehilite(content)
    filepath.write_text(content, encoding='utf-8')
    return True, 'cleaned'

def main():
    # 1. Fix breadcrumbs on all processed doc pages (excluding index, templates, clio.html)
    doc_files = []
    for f in DOCS_DIR.rglob('*.html'):
        if f.name in ('index.html', 'clio.html'):
            continue
        doc_files.append(f)
    doc_files.sort()

    print("=== Fixing breadcrumbs ===")
    for fp in doc_files:
        rel = fp.relative_to(SITE_ROOT)
        content = fp.read_text(encoding='utf-8', errors='replace')
        success, result = fix_breadcrumb(content, fp, str(rel).replace('\\', '/'))
        if success:
            fp.write_text(result, encoding='utf-8')
            print(f"  OK  {rel}")
        else:
            print(f"  SKIP {rel} ({result})")

    # 2. Clean codehilite on templates pages (were skipped by standardize-docs.py)
    print("\n=== Cleaning codehilite in templates ===")
    tpl_files = sorted(DOCS_DIR.rglob('*.html'))
    tpl_files = [f for f in tpl_files if 'templates' in f.parts]
    for fp in tpl_files:
        rel = fp.relative_to(SITE_ROOT)
        success, msg = fix_codeblocks(fp)
        print(f"  {'OK' if success else 'SKIP'} {rel} ({msg})")

    # 3. Also clean any remaining codehilite in non-template pages
    print("\n=== Cleaning remaining codehilite ===")
    for f in sorted(DOCS_DIR.rglob('*.html')):
        if f.name in ('index.html', 'clio.html'):
            continue
        if f.name == 'index.html':
            continue
        success, msg = fix_codeblocks(f)
        if success:
            print(f"  OK  {f.relative_to(SITE_ROOT)} ({msg})")

if __name__ == '__main__':
    main()
