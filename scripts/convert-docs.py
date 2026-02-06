#!/usr/bin/env python3
import os, re, markdown

def convert_file(md_path, template):
    print(f"Converting {md_path}...")
    with open(md_path, 'r') as f:
        md_content = f.read()
    title_match = re.search(r'^# (.+)$', md_content, re.MULTILINE)
    title = title_match.group(1) if title_match else 'Documentation'
    md = markdown.Markdown(extensions=['extra', 'codehilite', 'toc'])
    html_content = md.convert(md_content)
    
    # Fix depth calculation - count slashes to get levels deep
    depth = md_path.count('/')  # docs/file.md = 1, docs/cat/file.md = 2
    home_path = '../' * depth if depth > 0 else ''
    
    parts = md_path.replace('.md', '').split('/')
    breadcrumb = f'<a href="{home_path}docs/README.html">Documentation</a> / {parts[-1].replace("-", " ").title()}'
    html = template.replace('{{TITLE}}', title)
    html = html.replace('{{DESCRIPTION}}', f'SAM Documentation: {title}')
    html = html.replace('{{CSS_PATH}}', home_path)
    html = html.replace('{{HOME_PATH}}', home_path)
    html = html.replace('{{BREADCRUMB}}', breadcrumb)
    html = html.replace('{{CONTENT}}', html_content)
    html = re.sub(r'href="([^"]+)\.md"', r'href="\1.html"', html)
    html = re.sub(r'href="viewer\.html\?file=([^"]+)"', r'href="\1"', html)
    html_path = md_path.replace('.md', '.html')
    with open(html_path, 'w') as f:
        f.write(html)
    print(f"  -> {html_path}")

def main():
    with open('.doc-template.html', 'r') as f:
        template = f.read()
    md_files = []
    for root, dirs, files in os.walk('docs'):
        for file in files:
            if file.endswith('.md'):
                md_files.append(os.path.join(root, file))
    print(f"Found {len(md_files)} markdown files\n")
    for md_file in md_files:
        convert_file(md_file, template)
    print(f"\nDone! Converted {len(md_files)} files.")

if __name__ == '__main__':
    main()
