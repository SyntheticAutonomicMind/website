#!/usr/bin/env python3
"""
Fix remaining content-level broken links.
These are links to files that exist but are in different locations than expected.
"""

import re
from pathlib import Path

root = Path('.')
fixes = []

# Map of wrong paths -> correct paths (context-aware)
fixes_map = {
    'docs/ALICE/index.html': [
        ('memory-and-rag.html', '../SAM/end-user/memory-and-rag.html'),
        ('shared-topics.html', '../SAM/end-user/shared-topics.html'),
        ('../power-user/configuration.html', '../SAM/power-user/configuration.html'),
        ('../power-user/tools-reference.html', '../SAM/power-user/tools-reference.html'),
        ('../power-user/advanced-workflows.html', '../SAM/power-user/advanced-workflows.html'),
        ('../power-user/troubleshooting.html', '../SAM/power-user/troubleshooting.html'),
    ],
    'docs/ALICE/getting-started.html': [
        ('href="../index.html">Docs</a>', 'href="index.html">Docs</a>'),  # Navbar fix
    ],
    'docs/ALICE/installation.html': [
        ('href="../index.html">Docs</a>', 'href="index.html">Docs</a>'),
    ],
    'docs/CLIO/api-providers.html': [
        ('href="../index.html">Docs</a>', 'href="index.html">Docs</a>'),
    ],
    'docs/CLIO/getting-started.html': [
        ('href="../index.html">Docs</a>', 'href="index.html">Docs</a>'),
    ],
    'docs/CLIO/index.html': [
        ('href="../index.html">Docs</a>', 'href="index.html">Docs</a>'),
    ],
    'docs/CLIO/installation.html': [
        ('href="../index.html">Docs</a>', 'href="index.html">Docs</a>'),
    ],
    'docs/CLIO/tools-reference.html': [
        ('href="../index.html">Docs</a>', 'href="index.html">Docs</a>'),
    ],
    'docs/CLIO/clio-quick-start.html': [
        ('../SAM/developer/clio.html', '../CLIO/clio.html'),
        ('../SAM/developer/the-unbroken-method.html', '../shared/the-unbroken-method.html'),
    ],
    'docs/CLIO/clio.html': [
        ('../shared/developers-guide.html', '../SAM/developer/developers-guide.html'),
    ],
    'docs/SAM/index.html': [
        ('developer/clio.html', '../CLIO/clio.html'),
        ('developer/the-unbroken-method.html', '../shared/the-unbroken-method.html'),
    ],
    'docs/SAM/end-user/getting-started.html': [
        ('../developer/contributing.html', '../../shared/contributing.html'),
    ],
    'docs/shared/contributing.html': [
        ('clio.html', '../CLIO/clio.html'),
    ],
}

print('Content-Level Link Fixes')
print('=' * 70)

for file_path, replacements in fixes_map.items():
    file = root / file_path
    if not file.exists():
        print(f' SKIP: {file_path} (not found)')
        continue
    
    with open(file) as f:
        content = f.read()
    
    original = content
    for old_str, new_str in replacements:
        if old_str in content:
            content = content.replace(old_str, new_str)
            fixes.append(f'{file_path}: {old_str} -> {new_str}')
    
    if content != original:
        with open(file, 'w') as f:
            f.write(content)
        print(f' Fixed: {file_path} ({len([r for r in replacements if r[0] in original])} replacements)')

print()
print('=' * 70)
print(f'Applied {len(fixes)} fixes across {len(fixes_map)} files')
