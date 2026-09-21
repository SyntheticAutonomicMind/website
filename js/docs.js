// SAM Website - Documentation Enhancements
// Handles: Mermaid.js loading, TOC generation, code copy buttons,
// audience tab switching, and scroll-based active link highlighting.

(function() {
    'use strict';

    var isDocPage = document.querySelector('article.doc-page') !== null;
    if (!isDocPage) return;

    // ============================================================
    // MERMAID.JS (conditional loading)
    // ============================================================

    // Only load Mermaid.js if the page contains mermaid diagrams
    function initMermaid() {
        if (!document.querySelector('.mermaid')) return;

        var script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js';
        script.async = true;
        script.onload = function() {
            window.mermaid.initialize({
                startOnLoad: true,
                theme: 'default',
                themeVariables: {
                    fontSize: '14px',
                    fontFamily: "'SF Mono', 'Monaco', 'Cascadia Code', 'Courier New', monospace",
                    lineColor: '#d2d2d7',
                    primaryColor: '#0071e3',
                    secondaryColor: '#e8f0fe',
                    tertiaryColor: '#f5f5f7',
                    borderRadius: '8px',
                    fontSize: '13px'
                }
            });
        };
        document.head.appendChild(script);
    }

    // ============================================================
    // TABLE OF CONTENTS
    // ============================================================

    // Generate TOC from headings in .doc-content
    function generateTOC() {
        var tocContainer = document.getElementById('doc-toc');
        if (!tocContainer) return;

        var content = document.querySelector('.doc-content');
        if (!content) return;

        var headings = content.querySelectorAll('h2, h3, h4');
        if (headings.length < 2) return; // Don't show TOC for very short pages

        var tocHtml = '<ul>';
        var lastLevel = 2;

        headings.forEach(function(heading, index) {
            var level = parseInt(heading.tagName.charAt(1));
            var text = heading.textContent.trim();
            var slug = slugify(heading.textContent);

            // Add ID to heading for anchor links
            heading.id = slug;

            // Handle nesting
            if (level > lastLevel) {
                tocHtml += '<ul>';
            } else if (level < lastLevel) {
                tocHtml += '</ul>';
            }
            lastLevel = level;

            var anchorClass = 'level-' + level;
            if (index === 0) anchorClass += ' active';

            tocHtml += '<li><a href="#' + slug + '" class="' + anchorClass + '">' + text + '</a></li>';
        });

        tocHtml += '</ul>';
        tocContainer.innerHTML = tocHtml;
        tocContainer.classList.remove('hidden');
    }

    function slugify(text) {
        return text.toString().toLowerCase()
            .replace(/\s+/g, '-')
            .replace(/[^\w\-]+/g, '')
            .replace(/\-\-+/g, '-')
            .replace(/^-+/, '')
            .replace(/-+$/, '');
    }

    // ============================================================
    // TOC ACTIVE HIGHLIGHT ON SCROLL
    // ============================================================

    function initTOCHighlight() {
        var tocLinks = document.querySelectorAll('#doc-toc a');
        if (tocLinks.length === 0) return;

        var headings = [];
        tocLinks.forEach(function(link) {
            var heading = document.getElementById(link.getAttribute('href').substring(1));
            if (heading) {
                headings.push({ link: link, element: heading });
            }
        });

        if (headings.length === 0) return;

        var observer = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry) {
                var link = entry.target;
                var id = link.getAttribute('href').substring(1);

                if (entry.intersecting) {
                    link.classList.add('active');
                } else {
                    link.classList.remove('active');
                }
            });
        }, {
            root: null,
            rootMargin: '-30% 0px -50% 0px',
            threshold: 0
        });

        // Use ID-based observer
        headings.forEach(function(item) {
            observer.observe(item.element);
        });
    }

    // ============================================================
    // CODE COPY BUTTON
    // ============================================================

    function addCopyButtons() {
        var codeBlocks = document.querySelectorAll('.doc-content pre');

        codeBlocks.forEach(function(block) {
            // Skip already processed blocks
            if (block.parentNode.classList.contains('code-block-wrapper')) return;

            var wrapper = document.createElement('div');
            wrapper.className = 'code-block-wrapper';
            block.parentNode.insertBefore(wrapper, block);
            wrapper.appendChild(block);

            var button = document.createElement('button');
            button.className = 'copy-btn';
            button.setAttribute('aria-label', 'Copy code');
            button.innerHTML = 'Copy';
            wrapper.appendChild(button);

            button.addEventListener('click', function() {
                var text = block.textContent || block.innerText;
                navigator.clipboard.writeText(text).then(function() {
                    button.textContent = 'Copied!';
                    button.classList.add('copied');
                    setTimeout(function() {
                        button.textContent = 'Copy';
                        button.classList.remove('copied');
                    }, 2000);
                });
            });
        });
    }

    // ============================================================
    // AUDIENCE TABS (for doc index pages)
    // ============================================================

    function initAudienceTabs() {
        var tabs = document.querySelectorAll('.audience-tabs a');
        if (tabs.length === 0) return;

        tabs.forEach(function(tab) {
            tab.addEventListener('click', function(e) {
                e.preventDefault();
                var target = this.getAttribute('href').substring(1);

                // Update active state
                tabs.forEach(function(t) { t.classList.remove('active'); });
                this.classList.add('active');

                // Show corresponding section
                var sections = document.querySelectorAll('.audience-section');
                sections.forEach(function(s) {
                    s.style.display = 'none';
                });

                var targetSection = document.getElementById(target);
                if (targetSection) {
                    targetSection.style.display = '';
                }
            });
        });
    }

    // ============================================================
    // INIT
    // ============================================================

    function init() {
        initMermaid();
        generateTOC();
        initTOCHighlight();
        addCopyButtons();
        initAudienceTabs();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();
