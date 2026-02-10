#!/usr/bin/env python3
"""
Fix content-level link errors (wrong file locations in content).
This handles links that point to files that don't exist or are in wrong places.
"""

import re
from pathlib import Path

class ContentLinkFixer:
    """Fix content-level link errors."""
    
    def __init__(self, root_dir: str = '.'):
        self.root_dir = Path(root_dir).resolve()
        self.fixes = 0
        
        # Map of wrong paths -> correct paths (relative to docs/)
        self.path_mappings = {
            # Developer docs are in SAM
            '../developer/': '../SAM/developer/',
            '../../developer/': '../SAM/developer/',
            '../../../developer/': '../../SAM/developer/',
            
            # Shared docs location
            '../shared/': '../shared/',  # Already correct from most places
            
            # CLIO docs
            'clio.html': '../CLIO/clio.html',  # From SAM developer
            'clio-quick-start.html': '../CLIO/clio-quick-start.html',  # From SAM end-user  
            
            # The Unbroken Method is in shared
            'the-unbroken-method.html': '../shared/the-unbroken-method.html',  # From SAM/developer
            '../the-unbroken-method.html': '../../shared/the-unbroken-method.html',  # From SAM/developer/templates
            
            # Contributing is in shared
            'contributing.html': '../shared/contributing.html',  # From SAM/developer
            '../contributing.html': '../../shared/contributing.html',  # From SAM/developer/templates
            
            # Developers guide is in SAM/developer
            'developers-guide.html': '../SAM/developer/developers-guide.html',  # From CLIO or shared
            
            # Templates are in SAM/developer/templates
            'templates/': './templates/',  # From SAM/developer
        }
    
    def fix_alice_links(self, content: str) -> str:
        """Fix links in ALICE docs."""
        # ALICE links to SAM developer docs
        content = re.sub(
            r'href="\.\./developer/',
            'href="../SAM/developer/',
            content
        )
        
        # ALICE links to shared docs
        content = re.sub(
            r'href="\.\./shared/',
            'href="../shared/',
            content
        )
        
        # ALICE links to contributing (in shared)
        content = re.sub(
            r'href="\.\./(contributing\.html)"',
            r'href="../shared/\1"',
            content
        )
        
        return content
    
    def fix_clio_links(self, content: str) -> str:
        """Fix links in CLIO docs."""
        # CLIO links to SAM developer docs
        content = re.sub(
            r'href="\.\./developer/',
            'href="../SAM/developer/',
            content
        )
        
        # CLIO links to shared docs
        content = re.sub(
            r'href="(the-unbroken-method|developers-guide|contributing)\.html"',
            r'href="../shared/\1.html"',
            content
        )
        
        return content
    
    def fix_sam_developer_links(self, content: str) -> str:
        """Fix links in SAM/developer docs."""
        # Links to shared docs from developer/
        content = re.sub(
            r'href="(the-unbroken-method|contributing)\.html"',
            r'href="../../shared/\1.html"',
            content
        )
        
        # Links to CLIO docs
        content = re.sub(
            r'href="clio(-[^"]*)?\.html"',
            r'href="../../CLIO/clio\1.html"',
            content
        )
        
        return content
    
    def fix_sam_developer_templates_links(self, content: str) -> str:
        """Fix links in SAM/developer/templates docs."""
        # Links to shared docs from developer/templates/
        content = re.sub(
            r'href="\.\./the-unbroken-method\.html"',
            'href="../../../shared/the-unbroken-method.html"',
            content
        )
        
        content = re.sub(
            r'href="\.\./contributing\.html"',
            'href="../../../shared/contributing.html"',
            content
        )
        
        content = re.sub(
            r'href="\.\./developers-guide\.html"',
            'href="../developers-guide.html"',
            content
        )
        
        return content
    
    def fix_sam_enduser_links(self, content: str) -> str:
        """Fix links in SAM/end-user docs."""
        # Links to CLIO quick start
        content = re.sub(
            r'href="clio-quick-start\.html"',
            'href="../../CLIO/clio-quick-start.html"',
            content
        )
        
        return content
    
    def fix_shared_links(self, content: str) -> str:
        """Fix links in shared docs."""
        # Links to SAM developer docs from shared/
        content = re.sub(
            r'href="developers-guide\.html"',
            'href="../SAM/developer/developers-guide.html"',
            content
        )
        
        content = re.sub(
            r'href="templates/',
            'href="../SAM/developer/templates/',
            content
        )
        
        content = re.sub(
            r'href="the-unbroken-method\.html"',
            'href="./the-unbroken-method.html"',
            content
        )
        
        return content
    
    def fix_sam_index_links(self, content: str) -> str:
        """Fix links in SAM/index.html."""
        # Links to CLIO from SAM index
        content = re.sub(
            r'href="end-user/clio-quick-start\.html"',
            'href="../CLIO/clio-quick-start.html"',
            content
        )
        
        return content
    
    def fix_file(self, html_file: Path) -> bool:
        """Fix links in one file."""
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original = content
            rel_path = html_file.relative_to(self.root_dir)
            parts = rel_path.parts
            
            # Apply appropriate fixes based on file location
            if 'ALICE' in parts:
                content = self.fix_alice_links(content)
            
            if 'CLIO' in parts:
                content = self.fix_clio_links(content)
            
            if 'SAM' in parts:
                if 'developer' in parts:
                    if 'templates' in parts:
                        content = self.fix_sam_developer_templates_links(content)
                    else:
                        content = self.fix_sam_developer_links(content)
                elif 'end-user' in parts:
                    content = self.fix_sam_enduser_links(content)
                elif parts[-1] == 'index.html':
                    content = self.fix_sam_index_links(content)
            
            if 'shared' in parts:
                content = self.fix_shared_links(content)
            
            if content != original:
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f'✓ Fixed: {rel_path}')
                self.fixes += 1
                return True
            
            return False
            
        except Exception as e:
            print(f'✗ Error fixing {html_file.relative_to(self.root_dir)}: {e}')
            return False
    
    def run(self):
        """Fix all HTML files."""
        print('=' * 70)
        print('Content Link Repair')
        print('=' * 70)
        print()
        
        html_files = []
        for file_path in self.root_dir.rglob('*.html'):
            if ('node_modules' not in file_path.parts and
                not any(p.startswith('.') for p in file_path.parts[:-1]) and
                file_path.name != '.doc-template.html'):
                html_files.append(file_path)
        
        html_files = sorted(html_files)
        print(f'Checking {len(html_files)} HTML files\n')
        
        for html_file in html_files:
            self.fix_file(html_file)
        
        print()
        print('=' * 70)
        print(f'Complete! Fixed {self.fixes} files')
        print('=' * 70)


def main():
    fixer = ContentLinkFixer()
    fixer.run()


if __name__ == '__main__':
    main()
