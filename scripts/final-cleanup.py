#!/usr/bin/env python3
"""
Final cleanup - fix remaining broken links.
"""

import re
from pathlib import Path

root = Path('.')

fixes = {}

# Fix ALICE index.html image paths
alice_index = root / 'docs/ALICE/index.html'
if alice_index.exists():
    with open(alice_index) as f:
        content = f.read()
    
    # Fix image paths (should be ../../images/ not ../../../images/)
    original = content
    content = re.sub(r'src="../../../images/', 'src="../../images/', content)
    content = re.sub(r'href="features-overview\.html"', 'href="getting-started.html"', content)
    
    if content != original:
        with open(alice_index, 'w') as f:
            f.write(content)
        fixes['docs/ALICE/index.html'] = 'Fixed image paths and removed non-existent features-overview link'

# Fix SAM index.html - developer/contributing doesn't exist, it's in shared
sam_index = root / 'docs/SAM/index.html'
if sam_index.exists():
    with open(sam_index) as f:
        content = f.read()
    
    original = content
    content = re.sub(r'href="developer/contributing\.html"', 'href="../shared/contributing.html"', content)
    
    if content != original:
        with open(sam_index, 'w') as f:
            f.write(content)
        fixes['docs/SAM/index.html'] = 'Fixed contributing link'

# Fix shared docs - they should link to SAM index, not their own index
for shared_file in (root / 'docs/shared').glob('*.html'):
    with open(shared_file) as f:
        content = f.read()
    
    original = content
    # Replace "Documentation" links that point to index.html with SAM index
    content = re.sub(r'<a href="index\.html">Documentation</a>', '<a href="../SAM/index.html">Documentation</a>', content)
    content = re.sub(r'href="index\.html">Docs</a>', 'href="../SAM/index.html">Docs</a>', content)
    content = re.sub(r'<li><a href="index\.html">Documentation</a></li>', '<li><a href="../SAM/index.html">Documentation</a></li>', content)
    
    # Fix content links to architecture (in SAM/developer)
    content = re.sub(r'href="architecture\.html"', 'href="../SAM/developer/architecture.html"', content)
    
    if content != original:
        with open(shared_file, 'w') as f:
            f.write(content)
        fixes[str(shared_file.relative_to(root))] = 'Fixed navigation to SAM index and architecture link'

# Fix CLIO/clio.html - architecture link
clio_file = root / 'docs/CLIO/clio.html'
if clio_file.exists():
    with open(clio_file) as f:
        content = f.read()
    
    original = content
    content = re.sub(r'href="architecture\.html"', 'href="../SAM/developer/architecture.html"', content)
    
    if content != original:
        with open(clio_file, 'w') as f:
            f.write(content)
        fixes['docs/CLIO/clio.html'] = 'Fixed architecture link'

# Fix SAM/developer/templates getting-started links
for template_file in (root / 'docs/SAM/developer/templates').glob('*.html'):
    with open(template_file) as f:
        content = f.read()
    
    original = content
    # These incorrectly link to ../../../end-user/getting-started.html
    # Should be ../../../end-user/getting-started.html (which is correct!) - wait, let me check
    # From docs/SAM/developer/templates/file.html to docs/SAM/end-user/getting-started.html
    # = ../../../end-user/getting-started.html ... wait that's outside SAM
    # Should be: ../../end-user/getting-started.html
    content = re.sub(r'href="../../../end-user/getting-started\.html"', 'href="../../end-user/getting-started.html"', content)
    
    if content != original:
        with open(template_file, 'w') as f:
            f.write(content)
        fixes[str(template_file.relative_to(root))] = 'Fixed getting-started link depth'

print('Final Cleanup - Remaining Link Fixes')
print('=' * 70)
for file, desc in fixes.items():
    print(f' {file}: {desc}')
print()
print(f'Fixed {len(fixes)} files')
