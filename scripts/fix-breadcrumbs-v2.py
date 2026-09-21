#!/usr/bin/env python3
"""
Regenerate breadcrumbs on all doc pages with a cleaner format.

New breadcrumb logic:
- Index pages: Documentation (breadcrumb is minimal, H1 shows product)
- Content pages with section: Documentation / Section / Page Title
- Content pages without section: Documentation / Page Title
- Shared pages: Documentation / Page Title

This avoids repeating the product name when it's already in the H1.
"""

from pathlib import Path
import re
import html as html_module

SITE_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = SITE_ROOT / 'docs'

PRODUCTS = {
    'SAM':   {'label': 'SAM', 'color': 'sam'},
    'CLIO':  {'label': 'CLIO', 'color': 'clio'},
    'ALICE': {'label': 'ALICE', 'color': 'alice'},
    'shared': {'label': 'Shared', 'color': 'shared'},
}

SECTIONS = {
    'end-user':   'End User',
    'power-user': 'Power User',
    'developer':  'Developer',
    'templates':  'Templates',
}

def get_path_parts(fp):
    parts = fp.relative_to(SITE_ROOT).parts
    if 'docs' in parts:
        di = parts.index('docs')
        product_key = parts[di + 1] if di + 1 < len(parts) else None
        section = parts[di + 2] if di + 2 < len(parts) - 1 else None
        is_index = fp.name == 'index.html'
        return parts, product_key, section, di, is_index
    return parts, None, None, -1, False

def get_docs_prefix(parts, di):
    return '../' * (len(parts) - 2 - di)

def build_breadcrumb(parts, product_key, section, di, is_index, page_title):
    docs_prefix = get_docs_prefix(parts, di)
    product = PRODUCTS.get(product_key, {})
    
    crumbs = [{'label': 'Documentation', 'href': f'{docs_prefix}index.html'}]
    
    if is_index:
        # On index pages, just show "Documentation" - the H1 has the product name
        pass
    elif section and section in SECTIONS:
        # Content pages in a section: Documentation / Section / Page Title
        crumbs.append({'label': SECTIONS[section], 'href': ''})
        crumbs.append({'label': page_title, 'href': ''})
    else:
        # Content pages at product root: Documentation / Page Title
        crumbs.append({'label': page_title, 'href': ''})
    
    # Build HTML
    html = ['<nav class="doc-breadcrumb" aria-label="Breadcrumb">']
    for i, c in enumerate(crumbs):
        if i > 0:
            html.append('<span class="breadcrumb-separator">/</span>')
        if c['href']:
            html.append(f'<a href="{c["href"]}">{c["label"]}</a>')
        else:
            html.append(f'<span>{c["label"]}</span>')
    html.append('</nav>')
    return ''.join(html)

def extract_h1(content):
    m = re.search(r'<h1[^>]*>\s*(.*?)\s*</h1>', content, re.DOTALL)
    if m:
        return html_module.unescape(re.sub(r'<[^>]+>', '', m.group(1)).strip())
    return None

def process_page(fp):
    content = fp.read_text(encoding='utf-8', errors='replace')
    parts, product_key, section, di, is_index = get_path_parts(fp)
    if not product_key:
        return False
    
    page_title = extract_h1(content)
    if not page_title:
        return False
    
    new_bc = build_breadcrumb(parts, product_key, section, di, is_index, page_title)
    
    # Replace existing breadcrumb (both nav and div variants)
    old_pattern = r'<nav class="doc-breadcrumb".*?</nav>|<div class="doc-breadcrumb">.*?</div>'
    new_content, count = re.subn(old_pattern, new_bc, content, count=1, flags=re.DOTALL)
    
    if count:
        fp.write_text(new_content, encoding='utf-8')
        return True
    return False

def main():
    # Skip template pages (they have different breadcrumb)
    doc_files = []
    for f in DOCS_DIR.rglob('*.html'):
        if 'templates' in f.parts:
            continue
        doc_files.append(f)
    doc_files.sort()
    
    print(f"Regenerating breadcrumbs on {len(doc_files)} pages...\n")
    
    for fp in doc_files:
        rel = fp.relative_to(SITE_ROOT)
        if process_page(fp):
            print(f"  OK  {rel}")
        else:
            print(f"  SKIP {rel}")
    
    print("\nDone!")

if __name__ == '__main__':
    main()
