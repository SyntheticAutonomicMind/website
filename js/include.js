// SAM Website - Universal Component Loader
// Loads shared nav, footer, and prev/next navigation. Breadcrumbs are in HTML.
// All paths calculated at runtime based on page URL depth.

(function() {
    'use strict';

    // ============================================================
    // PATH CALCULATION
    // ============================================================

    // Calculate path prefixes based on current page URL.
    // Returns:
    //   root:      prefix to reach site root from current page
    //   docs:      prefix to reach docs/ directory from current page
    //   includes:  prefix to reach includes/ directory from current page
    function calculatePaths() {
        var path = window.location.pathname;
        var parts = path.split('/');
        parts.pop(); // remove filename
        var dirParts = parts.filter(function(p) { return p !== ''; });
        var depth = dirParts.length;

        var rootPrefix = '';
        for (var i = 0; i < depth; i++) {
            rootPrefix += '../';
        }

        var includesPrefix = rootPrefix + 'includes/';

        if (dirParts[0] === 'docs') {
            // Inside docs/ — count levels to reach docs/
            var docsDepth = depth - 1; // subtract 'docs' itself
            var docsPrefix = '';
            for (var j = 0; j < docsDepth; j++) {
                docsPrefix += '../';
            }
            return { root: rootPrefix, docs: docsPrefix, includes: includesPrefix };
        } else {
            // Not in docs/ — docs path is root + 'docs/'
            return { root: rootPrefix, docs: rootPrefix + 'docs/', includes: includesPrefix };
        }
    }

    function replacePlaceholders(html, paths) {
        return html
            .replace(/\{\{HOME_PATH\}\}/g, paths.root)
            .replace(/\{\{DOCS_PATH\}\}/g, paths.docs);
    }

    // ============================================================
    // FRAGMENT LOADING
    // ============================================================

    function loadFragment(url, placeholderId, paths) {
        var placeholder = document.getElementById(placeholderId);
        if (!placeholder) return;

        fetch(url)
            .then(function(response) {
                if (!response.ok) {
                    throw new Error('HTTP ' + response.status);
                }
                return response.text();
            })
            .then(function(html) {
                placeholder.innerHTML = replacePlaceholders(html, paths);
            })
            .catch(function(err) {
                console.warn('Fragment load failed (' + placeholderId + '):', err.message);
            });
    }

    function loadComponents() {
        var paths = calculatePaths();

        loadFragment(paths.includes + 'nav.html', 'nav-placeholder', paths);
        loadFragment(paths.includes + 'footer.html', 'footer-placeholder', paths);
    }

    // ============================================================
    // PREV/NEXT DOC NAVIGATION
    // ============================================================

    // Generates prev/next navigation based on data-prev and data-next
    // attributes on the <article class="doc-page"> element.
    // Attribute format: data-prev="docs/product/page.html|Page Title"
    // (path is relative to site root; we prepend root prefix for correct href)
    function generatePrevNext(article) {
        var prev = article.getAttribute('data-prev');
        var next = article.getAttribute('data-next');
        if (!prev && !next) return;

        // Get the root prefix for relative links
        var paths = calculatePaths();
        var rootPrefix = paths.root;

        var container = document.createElement('nav');
        container.className = 'doc-prev-next';
        container.setAttribute('aria-label', 'Documentation navigation');

        var html = '<div class="nav-group">';
        if (prev) {
            var prevParts = prev.split('|');
            // Convert docs-relative path to site-root-relative, then prefix with root
            var prevHref = rootPrefix + prevParts[0];
            html += '<a href="' + prevHref + '" class="prev">';
            html += '<span class="nav-label">Previous</span>';
            html += '<span class="nav-title">' + (prevParts[1] || '') + '</span>';
            html += '</a>';
        } else {
            html += '<div class="prev"></div>';
        }
        html += '</div>';

        html += '<div class="nav-group">';
        if (next) {
            var nextParts = next.split('|');
            var nextHref = rootPrefix + nextParts[0];
            html += '<a href="' + nextHref + '" class="next">';
            html += '<span class="nav-label">Next</span>';
            html += '<span class="nav-title">' + (nextParts[1] || '') + '</span>';
            html += '</a>';
        } else {
            html += '<div class="next"></div>';
        }
        html += '</div>';

        container.innerHTML = html;

        // Insert after the doc-content div
        var docContent = article.querySelector('.doc-content');
        if (docContent) {
            docContent.parentNode.insertBefore(container, docContent.nextSibling);
        }
    }

    // ============================================================
    // CONDITIONAL DOC SCRIPTS
    // ============================================================

    function loadDocScripts() {
        // Load docs.js on documentation pages (has <article class="doc-page">)
        if (document.querySelector('article.doc-page')) {
            var paths = calculatePaths();
            var script = document.createElement('script');
            script.src = paths.root + 'js/docs.js?v=13';
            script.async = true;
            document.head.appendChild(script);
        }
    }

    // ============================================================
    // INIT
    // ============================================================

    function init() {
        loadComponents();
        loadDocScripts();

        // Generate prev/next nav for doc pages
        var article = document.querySelector('article.doc-page');
        if (article) {
            generatePrevNext(article);
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();
