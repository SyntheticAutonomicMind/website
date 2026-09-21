# SAM Website

Official documentation website for the Synthetic Autonomic Mind (SAM) ecosystem — SAM, CLIO, and ALICE. Open source AI tools for macOS and Linux: a native AI assistant, a terminal-native development agent, and local image & audio generation.

**Live Site**: https://www.syntheticautonomicmind.org

---

## Overview

This is a static HTML documentation site — no build step required. Pages are committed as `.html` files and deployed as-is when changes are pushed to `main`.

```
website/
├── index.html              # Landing page
├── products/
│   ├── sam.html            # SAM product page
│   ├── clio.html           # CLIO product page
│   └── alice.html          # ALICE product page
├── docs/
│   ├── index.html          # Documentation hub with product selector
│   ├── SAM/                # SAM documentation (end-user, power-user, developer)
│   ├── CLIO/               # CLIO documentation (flat structure)
│   ├── ALICE/              # ALICE documentation (flat structure)
│   └── shared/             # Cross-product docs (methodology, contributing)
├── css/styles.css          # Global stylesheet
├── js/main.js              # Client-side logic (navigation, tabs)
├── images/                 # All image assets (PNG, SVG)
├── scripts/                # Python utilities for link validation and fixes
├── robots.txt              # Search engine crawl rules
├── sitemap.xml             # Sitemap for SEO
├── CNAME                   # Domain configuration (syntheticautonomicmind.org)
└── LICENSE                 # CC BY-NC 4.0 (website content)
```

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

---

## Documentation Structure

Documentation is organized by product, with SAM further organized by audience:

| Directory | Audience | Content |
|-----------|----------|---------|
| `docs/SAM/end-user/` | End users | Getting started, features, memory & RAG |
| `docs/SAM/power-user/` | Power users | Configuration, tools reference, advanced workflows |
| `docs/SAM/developer/` | Developers | Architecture, API reference, building, developers guide |
| `docs/CLIO/` | All CLIO users | Installation, getting started, commands, tools, remote execution |
| `docs/ALICE/` | All ALICE users | Installation, web interface, model management, API, deployment |
| `docs/shared/` | Everyone | The Unbroken Method, The Reflexive Ecosystem, contributing |

---

## Development Workflow

### Making Changes

1. **Edit HTML directly** — documentation pages are committed as `.html` files
2. **Test locally** before committing (`python3 -m http.server 8000`)
3. **Check links** — run `python3 scripts/validate-links.py`
4. **Follow style** — see `AGENTS.md` for technical reference

### Commit Message Format

```bash
docs: <action> <file/component> for <reason>
```

Examples:
```
docs: Fix broken links in developer section
docs: Add missing configuration examples
docs: Polish memory-and-rag.md for readability
```

### Pre-Commit Checklist

- [ ] Tested website locally (`python3 -m http.server 8000`)
- [ ] Clicked through changed pages, verified no console errors
- [ ] Link validation passes (`python3 scripts/validate-links.py`)
- [ ] No broken internal links
- [ ] Consistent formatting with existing content

---

## Design Standards

- **Semantic HTML**: `<header>`, `<nav>`, `<main>`, `<article>`, `<section>`, `<footer>`
- **No inline styles** — all styling via `css/styles.css`
- **Accessibility**: `lang="en"`, descriptive titles, alt text on images
- **External links**: always `rel="noopener noreferrer"` and `target="_blank"`
- **Internal links**: relative paths (`./foo.html` or `../CLIO/foo.html`)
- **Meta tags**: every page has `<title>` and `<meta name="description">`

### Product Color System

Each product has a distinct color palette defined as CSS variables:

| Product | CSS class | Color |
|---------|-----------|-------|
| SAM | `--sam-primary` | Blue (`#0071e3`) |
| CLIO | `--clio-primary` | Purple (`#6b46c1`) |
| ALICE | `--alice-primary` | Orange (`#e67e22`) |
| Shared | `--shared-primary` | Emerald (`#059669`) |

---

## License

This **website and documentation** is licensed under the **Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0)**.

**SAM, CLIO, and ALICE applications** are licensed under **GNU General Public License v3.0 (GPLv3)**.

See [LICENSE](LICENSE) for full details.

---

## Deployment

Push to `main` — the site deploys automatically to **www.syntheticautonomicmind.org** within 2-3 minutes. No manual deploy step.

---

## Support

- **Issues**: https://github.com/SyntheticAutonomicMind/website/issues
- **SAM**: https://github.com/SyntheticAutonomicMind/SAM
- **CLIO**: https://github.com/SyntheticAutonomicMind/CLIO
- **ALICE**: https://github.com/SyntheticAutonomicMind/ALICE
