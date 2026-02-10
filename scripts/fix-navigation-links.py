#!/usr/bin/env python3
"""
Final comprehensive link fixer - handles all remaining broken links.
"""

import re
from pathlib import Path

class FinalLinkFixer:
    """Fix ALL broken links."""
    
    def __init__(self, root_dir: str = '.'):
        self.root_dir = Path(root_dir).resolve()
        self.fixes = 0
        
    def fix_file(self, html_file: Path) -> bool:
        """Fix all links in one file."""
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original = content
            rel_path = html_file.relative_to(self.root_dir)
            parts = rel_path.parts
            
            # Skip template file
            if html_file.name == '.doc-template.html':
                return False
            
            # Determine product and depth
            if 'docs' not in parts:
                return False
            
            docs_idx = parts.index('docs')
            product = parts[docs_idx + 1] if docs_idx + 1 < len(parts) else None
            
            if not product:
                return False
            
            # Calculate depth to product index
            # File at docs/ALICE/file.html: parts=3, docs_idx=0, depth should be 0 (same dir)
            # File at docs/SAM/developer/file.html: parts=4, docs_idx=0, depth should be 1 (one ../index.html
            # Formula: (num_parts - 1) - (docs_idx + 2) = depth from product dir
            file_depth_from_product = (len(parts) - 1) - (docs_idx + 2)
            
            if file_depth_from_product == 0:
                product_index = 'index.html'
            else:
                product_index = '../' * file_depth_from_product + 'index.html'
            
            # Fix navbar "Docs" link - looks for ../index.html followed by >Docs</a>
            content = re.sub(
                r'href="../index\.html">Docs</a>',
                f'href="{product_index}">Docs</a>',
                content
            )
            
            # Fix footer "Documentation" link - looks for <li><a href="../index.html">Documentation</a></li>
            content = re.sub(
                r'<li><a href="../index\.html">Documentation</a></li>',
                f'<li><a href="{product_index}">Documentation</a></li>',
                content
            )
            
            # Fix deeper navigation links (../../index.html, ../../../index.html)
            content = re.sub(
                r'href="../../index\.html">Docs</a>',
                f'href="{product_index}">Docs</a>',
                content
            )
            
            content = re.sub(
                r'<li><a href="../../index\.html">Documentation</a></li>',
                f'<li><a href="{product_index}">Documentation</a></li>',
                content
            )
            
            content = re.sub(
                r'href="../../../index\.html">Docs</a>',
                f'href="{product_index}">Docs</a>',
                content
            )
            
            content = re.sub(
                r'<li><a href="../../../index\.html">Documentation</a></li>',
                f'<li><a href="{product_index}">Documentation</a></li>',
                content
            )
            
            # Fix breadcrumb links (any depth)
            for depth_num in range(1, 6):
                depth_str = '../' * depth_num
                content = re.sub(
                    rf'<a href="{re.escape(depth_str)}index\.html">Documentation</a>',
                    f'<a href="{product_index}">Documentation</a>',
                    content
                )
                content = re.sub(
                    rf'<a href="{re.escape(depth_str)}index\.html">Docs</a>',
                    f'<a href="{product_index}">Docs</a>',
                    content
                )
            
            if content != original:
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f' Fixed: {rel_path}')
                self.fixes += 1
                return True
            
            return False
            
        except Exception as e:
            print(f' Error: {html_file.relative_to(self.root_dir)}: {e}')
            return False
    
    def run(self):
        """Fix all files."""
        print('=' * 70)
        print('Final Link Repair - Navigation Links')
        print('=' * 70)
        print()
        
        html_files = []
        for file_path in self.root_dir.rglob('*.html'):
            if ('node_modules' not in file_path.parts and
                not any(p.startswith('.') for p in file_path.parts[:-1])):
                html_files.append(file_path)
        
        html_files = sorted(html_files)
        
        for html_file in html_files:
            self.fix_file(html_file)
        
        print()
        print('=' * 70)
        print(f'Complete! Fixed {self.fixes} files')
        print('=' * 70)


def main():
    fixer = FinalLinkFixer()
    fixer.run()


if __name__ == '__main__':
    main()
