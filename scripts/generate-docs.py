#!/usr/bin/env python3
"""
Generate properly formatted documentation pages for CLIO and ALICE
using the .doc-template.html template.
"""

import os
import sys

# Read template
with open('.doc-template.html', 'r') as f:
    template = f.read()

def generate_page(output_path, title, description, breadcrumb, home_path, css_path, content):
    """Generate a documentation page from template"""
    page = template
    page = page.replace('{{TITLE}}', title)
    page = page.replace('{{DESCRIPTION}}', description)
    page = page.replace('{{BREADCRUMB}}', breadcrumb)
    page = page.replace('{{HOME_PATH}}', home_path)
    page = page.replace('{{CSS_PATH}}', css_path)
    page = page.replace('{{CONTENT}}', content)
    
    # Fix footer links that reference old paths
    page = page.replace('href="{{HOME_PATH}}docs/end-user/getting-started.html"', 
                       'href="{{HOME_PATH}}docs/SAM/end-user/getting-started.html"')
    page = page.replace('href="{{HOME_PATH}}docs/README.html"',
                       'href="{{HOME_PATH}}docs/SAM/index.html"')
    
    with open(output_path, 'w') as f:
        f.write(page)
    print(f"Generated: {output_path}")

# Define CLIO pages
clio_pages = {
    'index.html': {
        'title': 'CLIO Documentation',
        'desc': 'CLIO - Command Line Intelligence Orchestrator documentation',
        'breadcrumb': '<a href="../../">Home</a> / <a href="index.html">CLIO Documentation</a>',
        'content': '''<h1>CLIO Documentation</h1>
<p class="lead">Command Line Intelligence Orchestrator - Your AI pair programming partner for the terminal</p>

<h2>What is CLIO?</h2>
<p>CLIO is a terminal-based AI code assistant designed for developers who live in the command line...</p>'''
    }
}

# Generate CLIO pages
for filename, data in clio_pages.items():
    output_path = f'docs/CLIO/{filename}'
    generate_page(
        output_path=output_path,
        title=data['title'],
        description=data['desc'],
        breadcrumb=data['breadcrumb'],
        home_path='../../',
        css_path='../../',
        content=data['content']
    )

print("Documentation generation complete!")
