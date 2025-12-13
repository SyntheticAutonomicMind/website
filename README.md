# SAM Website

Official documentation website for SAM (Synthetic Autonomic Mind) - a conversational AI with memory, RAG, and autonomous workflow capabilities.

**Live Site**: https://syntheticautonomicmind.org

---

## Overview

This website provides comprehensive documentation for SAM, organized by user expertise level:

- **End Users**: Getting started guides, features overview, and basic usage
- **Power Users**: Advanced configuration, tools reference, and complex workflows
- **Developers**: Architecture documentation, API reference, and contribution guidelines

---

## Local Development

### Prerequisites

- Python 3.x (for local web server)
- Modern web browser
- Text editor

### Running Locally

```bash
# Clone the repository
git clone git@github.com:SyntheticAutonomicMind/website.git
cd website

# Start local web server
python3 -m http.server 8000

# Open in browser
open http://localhost:8000
```

The website will be available at `http://localhost:8000`.

---

## Project Structure

```
syntheticautonomicmind.org/
├── index.html              # Landing page
├── viewer.html             # Markdown documentation viewer
├── LICENSE                 # CC BY-NC 4.0 license
├── .github/
│   └── copilot-instructions.md  # AI assistant guidelines
├── css/
│   ├── styles.css         # Global styles
│   └── markdown.css       # Markdown rendering styles
├── scripts/
│   └── user_collaboration.sh   # Collaboration checkpoint tool
└── docs/
    ├── README.md          # Documentation index
    ├── end-user/          # User guides
    ├── power-user/        # Advanced guides
    ├── developer/         # Technical documentation
    └── architecture/      # Deep-dive technical docs
```

---

## Documentation Standards

### Content Principles

1. **Clarity First**: Every sentence must be natural, readable, and helpful
2. **User-Focused**: Organized by what users want to accomplish, not technical structure
3. **Technically Accurate**: Facts verified against SAM source code
4. **Consistent**: Uniform tone, style, and formatting across all pages

### File Naming

All documentation files use `lowercase-with-hyphens.md`:

```
✅ getting-started.md
✅ memory-and-rag.md
✅ tools-reference.md
```

### Writing Style

- **Tone**: Professional but friendly, direct and concise
- **Voice**: Active voice preferred
- **Technical Terms**: Introduce simply, then use proper terminology
- **Examples**: Concrete and actionable

See `.github/copilot-instructions.md` for comprehensive guidelines.

---

## Contributing

### Making Changes

1. **Test locally** before committing
2. **Check links** - all internal links must work
3. **Maintain consistency** - follow existing style
4. **Verify accuracy** - ensure technical facts are correct

### Commit Message Format

```bash
docs: <action> <file/component> for <reason>

# Examples:
docs: Polish memory-and-rag.md for readability
docs: Fix broken links in developer section
docs: Add missing configuration examples
```

### Pre-Commit Checklist

- [ ] Tested website locally (`python3 -m http.server 8000`)
- [ ] Clicked through main pages and verified links work
- [ ] No broken links in modified files
- [ ] Consistent formatting with existing content
- [ ] Technical facts verified (if changed)
- [ ] Commit message follows format

---

## Key Features

### Markdown Viewer

The `viewer.html` page provides beautiful rendering of markdown documentation with:

- Syntax highlighting for code blocks
- Mermaid diagram support
- Automatic link rewriting for internal navigation
- Mobile-responsive design
- Dark theme optimized for readability

### Navigation

- **Homepage** (`index.html`): Feature showcase and quick start
- **Documentation Viewer** (`viewer.html?file=<path>`): Render any markdown file
- **Internal Links**: Automatically rewritten for seamless navigation

---

## Technical Details

### Built With

- **HTML5/CSS3**: Modern, semantic markup
- **JavaScript**: Client-side markdown rendering
- **Marked.js**: Markdown parser
- **Mermaid.js**: Diagram rendering
- **DOMPurify**: Security sanitization

### Browser Support

- Chrome/Edge: Latest 2 versions
- Firefox: Latest 2 versions
- Safari: Latest 2 versions

### Performance

- Static site (no build process required)
- Client-side rendering
- Fast initial load
- No external dependencies except CDN libraries

---

## License

This **website documentation** is licensed under the **Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0)**.

**Note**: The SAM application itself is licensed under **GNU General Public License v3.0 (GPLv3)**. This CC BY-NC license applies only to the website documentation content.

**You are free to**:
- Share and redistribute the website content
- Adapt and build upon the website content

**Under these terms**:
- **Attribution**: Give appropriate credit
- **NonCommercial**: Not for commercial use
- **No additional restrictions**: Don't apply legal/tech restrictions

See [LICENSE](LICENSE) for full details.  
Full legal text: https://creativecommons.org/licenses/by-nc/4.0/legalcode

**SAM Application License**: https://github.com/SyntheticAutonomicMind/SAM/blob/main/LICENSE

---

## Deployment

The website is automatically deployed to **syntheticautonomicmind.org** when changes are pushed to the `main` branch.

### Deployment Process

1. Commit changes to `main`
2. CI/CD pipeline triggered
3. Site deployed within 2-3 minutes
4. Changes live at https://syntheticautonomicmind.org

---

## Support

- **SAM Project**: https://github.com/SyntheticAutonomicMind/SAM
- **Website Issues**: https://github.com/SyntheticAutonomicMind/website/issues
- **Documentation**: Available at https://syntheticautonomicmind.org

---

## Maintenance

### Regular Tasks

- Review and update documentation for new SAM features
- Fix broken links
- Improve clarity based on user feedback
- Keep technical specifications current

### Quality Assurance

All changes go through review for:
- Readability and clarity
- Technical accuracy
- Link integrity
- Consistent formatting
