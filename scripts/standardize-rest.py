#!/usr/bin/env python3
"""
Standardize non-content pages: doc index pages, product pages, homepage,
redirect stubs, and root pages.
Also injects Mermaid.js on pages that use it.

Usage:  python3 scripts/standardize-rest.py
"""

import re
import html as html_module
from pathlib import Path

SITE_ROOT = Path(__file__).resolve().parent.parent
BASE_URL = 'https://www.syntheticautonomicmind.org'

PRODUCTS = {
    'SAM':   {'label': 'SAM',   'img': '/images/sam.png',   'color': 'sam',   'desc': 'Native macOS AI assistant with voice control, document RAG, autonomous agents, and multi-provider support.'},
    'CLIO':  {'label': 'CLIO',  'img': '/images/clio.png',  'color': 'clio',  'desc': 'Terminal-native AI development agent with multi-agent coordination, remote execution, and persistent sessions.'},
    'ALICE': {'label': 'ALICE', 'img': '/images/alice.png', 'color': 'alice', 'desc': 'Local Stable Diffusion and audio generation server with web UI, OpenAI-compatible API, and multi-GPU support.'},
}

def make_head(title, description, canonical, og_image=None, extra=''):
    """Generate a standardized <head> block."""
    head = f'''<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{description}">
    <link rel="canonical" href="{canonical}">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{canonical}">'''
    if og_image:
        head += f'\n    <meta property="og:image" content="https://www.syntheticautonomicmind.org{og_image}">'
    head += '\n    <meta name="twitter:card" content="summary">'
    head += f'\n    <meta name="twitter:title" content="{title}">'
    head += f'\n    <meta name="twitter:description" content="{description}">'
    head += f'\n    <link rel="stylesheet" href="{extra if extra else ""}">'
    head += '\n</head>'
    return head

def get_h1(content):
    m = re.search(r'<h1[^>]*>\s*(.*?)\s*</h1>', content, re.DOTALL)
    if m:
        return html_module.unescape(re.sub(r'<[^>]+>', '', m.group(1)).strip())
    return None

def get_description(content):
    m = re.search(r'<p class="lead">\s*(.*?)\s*</p>', content, re.DOTALL)
    if m:
        d = html_module.unescape(re.sub(r'<[^>]+>', '', m.group(1)).strip())
        if len(d) > 10:
            return d[:160]
    # Try first paragraph after first h2
    m = re.search(r'<h2[^>]*>.*?<p>\s*(.*?)\s*</p>', content, re.DOTALL)
    if m:
        d = html_module.unescape(re.sub(r'<[^>]+>', '', m.group(1)).strip())
        if len(d) > 10:
            return d[:160]
    return ''

def inject_mermaid(filepath):
    """Add Mermaid.js CDN script to a page that uses .mermaid divs."""
    content = filepath.read_text(encoding='utf-8', errors='replace')
    if 'class="mermaid"' not in content:
        return False
    # Check if mermaid script is already loaded
    if 'mermaid' in content and ('mermaid.min.js' in content or 'mermaid.js' in content):
        return False

    # Add mermaid init script before the closing </body> or after include.js
    # Find the include.js script tag and add mermaid after it
    mermaid_script = '''    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        if (typeof mermaid !== 'undefined') {
            mermaid.initialize({
                startOnLoad: true,
                theme: 'default',
                themeVariables: {
                    fontSize: '14px',
                    fontFamily: "'SF Mono', 'Monaco', 'Cascadia Code', 'Courier New', monospace'",
                    lineColor: '#d2d2d7',
                    primaryColor: '#0071e3',
                    secondaryColor: '#e8f0fe',
                    tertiaryColor: '#f5f5f7',
                    borderRadius: '8px'
                }
            });
        }
    });
    </script>'''

    # Insert before </body>
    content = content.replace('</body>', mermaid_script + '\n</body>')
    filepath.write_text(content, encoding='utf-8')
    return True

def standardize_doc_index(filepath):
    """Standardize a doc index page (docs/X/index.html)."""
    content = filepath.read_text(encoding='utf-8', errors='replace')
    rel_path = filepath.relative_to(SITE_ROOT)
    parts = rel_path.parts

    # Get product info
    product_key = None
    if 'docs' in parts:
        di = parts.index('docs')
        if di + 1 < len(parts):
            product_key = parts[di + 1]

    if product_key not in PRODUCTS:
        return False

    product = PRODUCTS[product_key]
    depth = len(parts) - 1
    prefix = '../' * depth
    rel_str = str(rel_path).replace('\\', '/')

    # Get H1 title
    h1 = get_h1(content)
    if not h1:
        h1 = f'{product["label"]} Documentation'
    title = f'{h1} | {product["label"]}'

    # Get description
    desc = get_description(content)
    if not desc:
        desc = product['desc']

    canonical = f'{BASE_URL}/{rel_str}'

    # Build new head
    head = make_head(
        title, desc, canonical,
        og_image=product['img'],
        extra=f'{prefix}css/styles.css?v=13'
    )
    content = re.sub(r'<head>.*?</head>', head, content, count=1, flags=re.DOTALL)

    # Update breadcrumb
    # Current: <a href="../index.html">Documentation</a> / <span class="product-badge X">LABEL</span>
    # New: standardized format with proper links
    docs_prefix = '../' * (len(parts) - 2 - parts.index('docs'))
    new_bc = f'<nav class="doc-breadcrumb" aria-label="Breadcrumb"><a href="{docs_prefix}index.html">Documentation</a><span class="breadcrumb-separator">/</span><span class="product-badge {product["color"]} large">{product["label"]}</span></nav>'
    
    # Replace old breadcrumb (may be on same line as doc-container)
    content = re.sub(
        r'<div class="doc-breadcrumb">.*?</div>',
        new_bc,
        content,
        count=1,
        flags=re.DOTALL
    )
    content = re.sub(
        r'<nav class="doc-breadcrumb".*?</nav>',
        new_bc,
        content,
        count=1,
        flags=re.DOTALL
    )

    # Wrap in main/article
    if '<main>' not in content:
        # Find doc-container opening
        content = re.sub(
            r'(<div id="nav-placeholder"></div>\s*\n\s*)<!--.*-->\s*\n\s*<div class="doc-container">',
            r'\1<main>\n        <article class="doc-page" data-product="' + product_key + '" data-doc-path="' + rel_str + '">\n    <div class="doc-container">',
            content,
            count=1,
            flags=re.DOTALL
        )
        # Add closing before footer-placeholder
        content = re.sub(
            r'\s*</div>\s*\n\s*<div id="footer-placeholder">',
            '</div>\n    </article>\n</main>\n\n    <div id="footer-placeholder">',
            content,
            count=1,
            flags=re.DOTALL
        )

    # Bump version
    content = content.replace('js/main.js?v=12', 'js/main.js?v=13')

    filepath.write_text(content, encoding='utf-8')
    return True

def standardize_homepage():
    """Standardize the homepage."""
    filepath = SITE_ROOT / 'index.html'
    content = filepath.read_text(encoding='utf-8', errors='replace')

    head = make_head(
        'Synthetic Autonomic Mind - AI Tools for macOS & Linux',
        'SAM, CLIO, and ALICE - Open-source AI tools for macOS and Linux. Native apps, terminal agents, and local image & audio generation. Private by default.',
        f'{BASE_URL}/',
        og_image='/images/sam.png',
        extra='css/styles.css?v=13'
    )
    # Add Google Analytics
    head = head.replace('</head>', """    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-BGNMWS5QRM"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'G-BGNMWS5QRM');
    </script>
</head>""")

    content = re.sub(r'<head>.*?</head>', head, content, count=1, flags=re.DOTALL)
    content = content.replace('js/main.js?v=12', 'js/main.js?v=13')

    # Wrap in main
    if '<main>' not in content:
        content = content.replace(
            '<div id="nav-placeholder"></div>',
            '<div id="nav-placeholder"></div>\n\n    <main>',
            1
        )
        # Add closing main before footer-placeholder
        content = re.sub(
            r'(\s*)<!--\s*Footer\s*-->\s*\n\s*<div id="footer-placeholder">',
            r'\n</main>\n\n    <div id="footer-placeholder">',
            content,
            count=1,
            flags=re.DOTALL
        )
        # Actually, just add </main> before the footer-placeholder
        content = re.sub(
            r'\n(    <div id="footer-placeholder">)',
            r'\n</main>\n\n\1',
            content,
            count=1
        )

    filepath.write_text(content, encoding='utf-8')
    return True

def standardize_product_page(filepath):
    """Standardize a product page."""
    content = filepath.read_text(encoding='utf-8', errors='replace')
    product_key = filepath.stem.upper()

    if product_key not in PRODUCTS:
        return False

    product = PRODUCTS[product_key]
    depth = len(filepath.relative_to(SITE_ROOT).parts) - 1
    prefix = '../' * depth
    rel_str = str(filepath.relative_to(SITE_ROOT)).replace('\\', '/')

    h1 = get_h1(content)
    if not h1:
        h1 = product['label']
    title = f'{h1} | {product["label"]}'

    desc = get_description(content)
    if not desc:
        desc = product['desc']

    canonical = f'{BASE_URL}/{rel_str}'

    head = make_head(
        title, desc, canonical,
        og_image=product['img'],
        extra=f'{prefix}css/styles.css?v=13'
    )
    head = head.replace('</head>', """    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-BGNMWS5QRM"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'G-BGNMWS5QRM');
    </script>
</head>""")

    content = re.sub(r'<head>.*?</head>', head, content, count=1, flags=re.DOTALL)
    content = content.replace('js/main.js?v=12', 'js/main.js?v=13')

    # Wrap in main
    if '<main>' not in content:
        content = content.replace(
            '<div id="nav-placeholder"></div>',
            '<div id="nav-placeholder"></div>\n\n    <main>',
            1
        )
        content = re.sub(
            r'\n(    <div id="footer-placeholder">)',
            r'\n</main>\n\n\1',
            content,
            count=1
        )

    filepath.write_text(content, encoding='utf-8')
    return True

def standardize_redirect_stub(filepath):
    """Standardize a redirect stub page with proper metadata."""
    content = filepath.read_text(encoding='utf-8', errors='replace')

    # Extract redirect target
    target_match = re.search(r'url=([^"\s]+)', content)
    if not target_match:
        return False
    target = target_match.group(1).replace('&amp;', '&')

    # Determine product from filename
    name = filepath.stem
    product_name = name.replace('-', ' ').title()
    title = f'Redirecting to {product_name}...'

    description = 'Redirect page.'

    head = make_head(
        title, description,
        f'{BASE_URL}/{filepath.name}',
        extra='css/styles.css?v=13'
    )

    content = re.sub(r'<head>.*?</head>', head, content, count=1, flags=re.DOTALL)

    filepath.write_text(content, encoding='utf-8')
    return True

def standardize_docs_hub():
    """Standardize the docs index hub page."""
    filepath = DOCS_DIR = SITE_ROOT / 'docs' / 'index.html'
    content = filepath.read_text(encoding='utf-8', errors='replace')

    head = make_head(
        'Documentation | Synthetic Autonomic Mind',
        'Documentation for SAM, CLIO, and ALICE. Choose a product to browse guides, API references, and tutorials.',
        f'{BASE_URL}/docs/',
        og_image='/images/sam.png',
        extra='../css/styles.css?v=13'
    )

    content = re.sub(r'<head>.*?</head>', head, content, count=1, flags=re.DOTALL)
    content = content.replace('js/main.js?v=12', 'js/main.js?v=13')

    # Add main wrapper
    if '<main>' not in content:
        content = content.replace(
            '<div id="nav-placeholder"></div>',
            '<div id="nav-placeholder"></div>\n\n    <main>',
            1
        )
        content = re.sub(
            r'\n(    <div id="footer-placeholder">)',
            r'\n</main>\n\n\1',
            content,
            count=1
        )

    filepath.write_text(content, encoding='utf-8')
    return True

def main():
    SITE_ROOT = Path(__file__).resolve().parent.parent
    DOCS_DIR = SITE_ROOT / 'docs'

    changes = []

    # 1. Doc index pages
    print("=== Doc index pages ===")
    for idx in ['docs/SAM/index.html', 'docs/CLIO/index.html', 'docs/ALICE/index.html']:
        fp = SITE_ROOT / idx
        if fp.exists():
            ok = standardize_doc_index(fp)
            print(f"  {'OK' if ok else 'SKIP'} {idx}")

    # 2. Docs hub
    print("\n=== Docs hub ===")
    ok = standardize_docs_hub()
    print(f"  {'OK' if ok else 'SKIP'} docs/index.html")

    # 3. Homepage
    print("\n=== Homepage ===")
    ok = standardize_homepage()
    print(f"  {'OK' if ok else 'SKIP'} index.html")

    # 4. Product pages
    print("\n=== Product pages ===")
    for p in ['sam', 'clio', 'alice']:
        fp = SITE_ROOT / 'products' / f'{p}.html'
        if fp.exists():
            ok = standardize_product_page(fp)
            print(f"  {'OK' if ok else 'SKIP'} products/{p}.html")

    # 5. Redirect stubs
    print("\n=== Redirect stubs ===")
    for stub in ['ai-coding-assistant-macos.html', 'clio-terminal-ai.html',
                 'local-ai-assistant-macos.html', 'stable-diffusion-macos.html']:
        fp = SITE_ROOT / stub
        if fp.exists():
            ok = standardize_redirect_stub(fp)
            print(f"  {'OK' if ok else 'SKIP'} {stub}")

    # 6. Inject Mermaid.js
    print("\n=== Injecting Mermaid.js ===")
    mermaid_pages = [
        'docs/shared/the-unbroken-method.html',
        'docs/shared/the-reflexive-ecosystem.html',
        'docs/SAM/end-user/use-cases.html',
    ]
    for p in mermaid_pages:
        fp = SITE_ROOT / p
        if fp.exists():
            ok = inject_mermaid(fp)
            print(f"  {'OK' if ok else 'SKIP'} {p}")

if __name__ == '__main__':
    main()
