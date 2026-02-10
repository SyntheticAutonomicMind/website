#!/usr/bin/env python3
"""
Fix final 8 remaining errors.
"""

import re
from pathlib import Path

root = Path('.')

# Fix breadcrumb links in ALICE/CLIO pages
for product in ['ALICE', 'CLIO']:
    product_dir = root / 'docs' / product
    for html_file in product_dir.glob('*.html'):
        with open(html_file) as f:
            content = f.read()
        
        original = content
        
        # Fix breadcrumb: "ALICE Documentation" or "CLIO Documentation"
        content = re.sub(
            rf'<a href="\.\./index\.html">{product} Documentation</a>',
            f'<a href="index.html">{product} Documentation</a>',
            content
        )
        
        if content != original:
            with open(html_file, 'w') as f:
                f.write(content)
            print(f' Fixed breadcrumb: {html_file.relative_to(root)}')

# Fix ALICE/index.html contributing link
alice_index = root / 'docs/ALICE/index.html'
if alice_index.exists():
    with open(alice_index) as f:
        content = f.read()
    
    original = content
    content = content.replace(
        '../SAM/developer/contributing.html',
        '../shared/contributing.html'
    )
    
    if content != original:
        with open(alice_index, 'w') as f:
            f.write(content)
        print(f' Fixed contributing link: docs/ALICE/index.html')

print('\\nAll broken links fixed!')
