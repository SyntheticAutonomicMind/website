#!/usr/bin/env python3
"""
Link Validation Script for SAM Website
Validates all internal and external links across the entire site.
"""

import os
import sys
import re
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse, urljoin
import urllib.request
import urllib.error
from typing import List, Dict, Set, Tuple
import json

class LinkExtractor(HTMLParser):
    """Extract all links from HTML content."""
    
    def __init__(self):
        super().__init__()
        self.links = []
        self.current_tag = None
        
    def handle_starttag(self, tag, attrs):
        self.current_tag = tag
        attrs_dict = dict(attrs)
        
        # Extract href from <a> and <link> tags
        if tag in ['a', 'link'] and 'href' in attrs_dict:
            href = attrs_dict['href']
            self.links.append({
                'type': 'href',
                'tag': tag,
                'url': href,
                'text': ''
            })
        
        # Extract src from <script>, <img>, <iframe> tags
        elif tag in ['script', 'img', 'iframe'] and 'src' in attrs_dict:
            src = attrs_dict['src']
            self.links.append({
                'type': 'src',
                'tag': tag,
                'url': src,
                'text': ''
            })
    
    def handle_data(self, data):
        # Add link text for anchor tags
        if self.links and self.current_tag == 'a' and self.links[-1]['tag'] == 'a':
            self.links[-1]['text'] = data.strip()


class LinkValidator:
    """Validate all links on the SAM website."""
    
    def __init__(self, root_dir: str = '.'):
        self.root_dir = Path(root_dir).resolve()
        self.errors = []
        self.warnings = []
        self.checked_urls = {}  # Cache for external URL checks
        self.all_files = set()
        
    def find_html_files(self) -> List[Path]:
        """Find all HTML files in the project."""
        html_files = []
        for file_path in self.root_dir.rglob('*.html'):
            # Skip node_modules and hidden directories
            if 'node_modules' in file_path.parts or any(part.startswith('.') for part in file_path.parts[:-1]):
                continue
            html_files.append(file_path)
            self.all_files.add(file_path.relative_to(self.root_dir))
        return sorted(html_files)
    
    def extract_links(self, html_file: Path) -> List[Dict]:
        """Extract all links from an HTML file."""
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            parser = LinkExtractor()
            parser.feed(content)
            return parser.links
        except Exception as e:
            self.errors.append({
                'file': str(html_file.relative_to(self.root_dir)),
                'error': f'Failed to parse HTML: {str(e)}'
            })
            return []
    
    def resolve_relative_path(self, base_file: Path, relative_url: str) -> Path:
        """Resolve a relative URL from the base file's directory."""
        base_dir = base_file.parent
        # Remove query strings and anchors
        clean_url = relative_url.split('?')[0].split('#')[0]
        resolved = (base_dir / clean_url).resolve()
        return resolved
    
    def check_internal_link(self, html_file: Path, link: Dict) -> bool:
        """Check if an internal link is valid."""
        url = link['url']
        
        # Skip anchors within same page
        if url.startswith('#'):
            return True
        
        # Skip mailto and tel links
        if url.startswith(('mailto:', 'tel:')):
            return True
        
        # Check if it's a relative path
        if not url.startswith(('http://', 'https://', '//')):
            # Remove query string and anchor for file checking
            file_url = url.split('?')[0].split('#')[0]
            
            if not file_url:  # Empty after removing query/anchor
                return True
            
            try:
                resolved_path = self.resolve_relative_path(html_file, file_url)
                
                # Check if file exists
                if not resolved_path.exists():
                    self.errors.append({
                        'file': str(html_file.relative_to(self.root_dir)),
                        'link': url,
                        'type': 'missing_file',
                        'tag': link['tag'],
                        'text': link.get('text', ''),
                        'resolved': str(resolved_path.relative_to(self.root_dir)) if self.root_dir in resolved_path.parents else str(resolved_path),
                        'error': 'File does not exist'
                    })
                    return False
                
                # Check if it's a file (not directory)
                if resolved_path.is_dir():
                    self.warnings.append({
                        'file': str(html_file.relative_to(self.root_dir)),
                        'link': url,
                        'type': 'directory_link',
                        'warning': 'Link points to directory, not file'
                    })
                    return False
                    
            except Exception as e:
                self.errors.append({
                    'file': str(html_file.relative_to(self.root_dir)),
                    'link': url,
                    'error': f'Path resolution error: {str(e)}'
                })
                return False
        
        return True
    
    def check_external_url(self, url: str) -> Tuple[bool, str]:
        """Check if an external URL is reachable."""
        # Use cache to avoid duplicate requests
        if url in self.checked_urls:
            return self.checked_urls[url]
        
        try:
            # Set a reasonable timeout and user agent
            req = urllib.request.Request(
                url,
                headers={'User-Agent': 'Mozilla/5.0 (SAM Website Link Validator)'}
            )
            
            with urllib.request.urlopen(req, timeout=10) as response:
                status = response.getcode()
                if status >= 200 and status < 400:
                    result = (True, f'HTTP {status}')
                else:
                    result = (False, f'HTTP {status}')
            
            self.checked_urls[url] = result
            return result
            
        except urllib.error.HTTPError as e:
            result = (False, f'HTTP {e.code}')
            self.checked_urls[url] = result
            return result
        except urllib.error.URLError as e:
            result = (False, f'URL Error: {str(e.reason)}')
            self.checked_urls[url] = result
            return result
        except Exception as e:
            result = (False, f'Error: {str(e)}')
            self.checked_urls[url] = result
            return result
    
    def validate_file(self, html_file: Path, check_external: bool = True) -> Dict:
        """Validate all links in a single HTML file."""
        rel_path = html_file.relative_to(self.root_dir)
        print(f'Checking: {rel_path}')
        
        links = self.extract_links(html_file)
        
        internal_links = []
        external_links = []
        
        for link in links:
            url = link['url']
            
            # Categorize link
            if url.startswith(('http://', 'https://', '//')):
                external_links.append(link)
                if check_external:
                    is_valid, status = self.check_external_url(url)
                    if not is_valid:
                        self.errors.append({
                            'file': str(rel_path),
                            'link': url,
                            'type': 'external_unreachable',
                            'tag': link['tag'],
                            'text': link.get('text', ''),
                            'error': status
                        })
            else:
                internal_links.append(link)
                self.check_internal_link(html_file, link)
        
        return {
            'file': str(rel_path),
            'total_links': len(links),
            'internal': len(internal_links),
            'external': len(external_links)
        }
    
    def validate_all(self, check_external: bool = True) -> Dict:
        """Validate all HTML files in the project."""
        print('=' * 70)
        print('SAM Website Link Validation')
        print('=' * 70)
        print()
        
        html_files = self.find_html_files()
        print(f'Found {len(html_files)} HTML files to check\n')
        
        stats = {
            'total_files': len(html_files),
            'total_links': 0,
            'internal_links': 0,
            'external_links': 0,
            'files_checked': []
        }
        
        for html_file in html_files:
            file_stats = self.validate_file(html_file, check_external)
            stats['files_checked'].append(file_stats)
            stats['total_links'] += file_stats['total_links']
            stats['internal_links'] += file_stats['internal']
            stats['external_links'] += file_stats['external']
        
        print()
        print('=' * 70)
        print('Validation Results')
        print('=' * 70)
        print()
        print(f'Files checked: {stats["total_files"]}')
        print(f'Total links: {stats["total_links"]}')
        print(f'Internal links: {stats["internal_links"]}')
        print(f'External links: {stats["external_links"]}')
        print(f'Errors found: {len(self.errors)}')
        print(f'Warnings: {len(self.warnings)}')
        print()
        
        if self.errors:
            print('=' * 70)
            print('ERRORS')
            print('=' * 70)
            print()
            for i, error in enumerate(self.errors, 1):
                print(f'{i}. File: {error["file"]}')
                print(f'   Link: {error["link"]}')
                if 'tag' in error:
                    print(f'   Tag: <{error["tag"]}>')
                if 'text' in error and error['text']:
                    print(f'   Text: {error["text"]}')
                if 'resolved' in error:
                    print(f'   Resolved to: {error["resolved"]}')
                print(f'   Error: {error["error"]}')
                print()
        
        if self.warnings:
            print('=' * 70)
            print('WARNINGS')
            print('=' * 70)
            print()
            for i, warning in enumerate(self.warnings, 1):
                print(f'{i}. File: {warning["file"]}')
                print(f'   Link: {warning["link"]}')
                print(f'   Warning: {warning["warning"]}')
                print()
        
        return stats
    
    def save_report(self, output_file: str = 'link-validation-report.json'):
        """Save validation results to JSON file."""
        report = {
            'errors': self.errors,
            'warnings': self.warnings,
            'checked_urls': self.checked_urls
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        
        print(f'Full report saved to: {output_file}')


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Validate all links on SAM website'
    )
    parser.add_argument(
        '--no-external',
        action='store_true',
        help='Skip external URL validation (faster)'
    )
    parser.add_argument(
        '--output',
        default='link-validation-report.json',
        help='Output file for detailed report'
    )
    
    args = parser.parse_args()
    
    validator = LinkValidator()
    validator.validate_all(check_external=not args.no_external)
    validator.save_report(args.output)
    
    # Exit with error code if issues found
    if validator.errors:
        print()
        print('❌ Validation FAILED - broken links found!')
        sys.exit(1)
    elif validator.warnings:
        print()
        print('⚠️  Validation completed with warnings')
        sys.exit(0)
    else:
        print()
        print('✅ Validation PASSED - all links are valid!')
        sys.exit(0)


if __name__ == '__main__':
    main()
