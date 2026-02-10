#!/usr/bin/env python3
"""
Comprehensive link fixer for SAM website.
Fixes ALL broken internal links systematically.
"""

import os
import re
from pathlib import Path
from typing import Tuple

class ComprehensiveLinkFixer:
    """Fix all broken links across the website."""
    
    def __init__(self, root_dir: str = '.'):
        self.root_dir = Path(root_dir).resolve()
        self.total_fixes = 0
        
    def calculate_depth(self, html_file: Path) -> str:
        """Calculate correct path depth from file to root."""
        rel_path = html_file.relative_to(self.root_dir)
        depth = len(rel_path.parts) - 1
        return '../' * depth if depth > 0 else ''
    
    def fix_all_patterns(self, html_file: Path, content: str) -> str:
        """Apply all fix patterns to content."""
        rel_path = html_file.relative_to(self.root_dir)
        depth = self.calculate_depth(html_file)
        
        # Track changes
        original = content
        
        # 1. Fix escaped forward slashes in paths (from bad regex replacement)
        content = content.replace(r'\/', '/')
        
        # 2. Fix CSS paths
        content = re.sub(
            r'href="[^"]*css/styles\.css[^"]*"',
            f'href="{depth}css/styles.css?v=7"',
            content
        )
        
        # 3. Fix logo image paths
        content = re.sub(
            r'src="[^"]*images/sam4\.png"',
            f'src="{depth}images/sam4.png"',
            content
        )
        
        # 4. Fix home/index links in navbar
        content = re.sub(
            r'href="[^"]*index\.html"([^>]*class="nav-logo")',
            f'href="{depth}index.html"\\1',
            content
        )
        
        # 5. Fix navbar "SAM" link
        content = re.sub(
            r'<a href="[^"]*"([^>]*>\s*SAM\s*</a>)',
            f'<a href="{depth}index.html"\\1',
            content
        )
        
        # Get context about current file location
        parts = rel_path.parts
        
        if 'docs' in parts:
            docs_idx = parts.index('docs')
            product = parts[docs_idx + 1] if docs_idx + 1 < len(parts) else None
            
            # 6. Fix product documentation navigation links
            # These should point to the product's own index, not docs/index.html
            if product:
                product_depth = len(parts) - (docs_idx + 2)
                correct_product_index = '../' * product_depth + 'index.html' if product_depth > 0 else 'index.html'
                
                # Fix "Product Documentation" header links
                content = re.sub(
                    rf'href="[^"]*index\.html"([^>]*>\s*{product}\s+Documentation)',
                    f'href="{correct_product_index}"\\1',
                    content,
                    flags=re.IGNORECASE
                )
                
                # Fix all navbar/footer "Documentation" links that point to ../index.html
                # These should point to product index
                content = re.sub(
                    r'href="\.\.+/index\.html"([^>]*>\s*Documentation\s*</a>)',
                    f'href="{correct_product_index}"\\1',
                    content
                )
                
                # Fix breadcrumb documentation links
                content = re.sub(
                    r'href="\.\.+/index\.html"([^>]*>\s*(Docs?|Documentation))',
                    f'href="{correct_product_index}"\\1',
                    content,
                    flags=re.IGNORECASE
                )
            
            # 7. Fix "Getting Started" links
            if product == 'SAM':
                # Within SAM docs
                if 'end-user' in parts:
                    gs_path = 'getting-started.html'
                elif 'power-user' in parts or 'developer' in parts:
                    subdir_depth = len(parts) - (docs_idx + 3)  # Depth within SAM/category
                    if 'templates' in parts:  # Special case: developer/templates
                        gs_path = '../../../end-user/getting-started.html'
                    else:
                        gs_path = '../end-user/getting-started.html'
                else:
                    gs_path = 'end-user/getting-started.html'
            else:
                # From ALICE or CLIO docs
                gs_path = '../SAM/end-user/getting-started.html'
            
            content = re.sub(
                r'href="[^"]*end-user/getting-started\.html"',
                f'href="{gs_path}"',
                content
            )
            
            # 8. Fix top-level product page links (SAM, CLIO, ALICE pages)
            # From docs/*/*, links to ../../local-ai-assistant-macos.html should be ../../../
            file_depth = len(parts) - 1  # Total depth from root
            root_depth = '../' * file_depth
            
            for page in ['local-ai-assistant-macos.html', 'clio-terminal-ai.html', 'stable-diffusion-macos.html']:
                content = re.sub(
                    rf'href="[^"]*{page}"',
                    f'href="{root_depth}{page}"',
                    content
                )
            
            # 9. Fix docs/README.html links (doesn't exist, should point to product index or SAM index)
            if product:
                docs_link = correct_product_index
            else:
                docs_link = f'{depth}docs/SAM/index.html'
            
            content = re.sub(
                r'href="[^"]*docs/README\.html"',
                f'href="{docs_link}"',
                content
            )
        
        # Count fixes
        if content != original:
            # Count number of changes (rough estimate)
            fixes = len(content) - len(original)
            return content
        
        return content
    
    def fix_file(self, html_file: Path) -> bool:
        """Fix all links in one file. Returns True if changed."""
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original = content
            fixed = self.fix_all_patterns(html_file, content)
            
            if fixed != original:
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(fixed)
                print(f'✓ Fixed: {html_file.relative_to(self.root_dir)}')
                self.total_fixes += 1
                return True
            
            return False
            
        except Exception as e:
            print(f'✗ Error fixing {html_file.relative_to(self.root_dir)}: {e}')
            return False
    
    def run(self):
        """Fix all HTML files."""
        print('=' * 70)
        print('Comprehensive Link Repair')
        print('=' * 70)
        print()
        
        html_files = []
        for file_path in self.root_dir.rglob('*.html'):
            if ('node_modules' not in file_path.parts and
                not any(p.startswith('.') for p in file_path.parts[:-1]) and
                file_path.name != '.doc-template.html'):
                html_files.append(file_path)
        
        html_files = sorted(html_files)
        print(f'Found {len(html_files)} HTML files\n')
        
        for html_file in html_files:
            self.fix_file(html_file)
        
        print()
        print('=' * 70)
        print(f'Complete! Modified {self.total_fixes} files')
        print('=' * 70)


def main():
    fixer = ComprehensiveLinkFixer()
    fixer.run()


if __name__ == '__main__':
    main()
