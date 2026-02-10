# Link Validation System

## Overview

The SAM website now has automated link validation to prevent broken links from being published.

## Quick Start

### Before Committing

**ALWAYS** run link validation before committing HTML changes:

```bash
python3 scripts/test-links.py
```

This tests all internal links (fast, ~5 seconds).

### Testing External Links

To also test external URLs (slower, ~1-2 minutes):

```bash
python3 scripts/test-links.py --external
```

## Tools

### `scripts/validate-links.py`

**Primary validation tool** - Checks all links across the entire site.

```bash
# Test internal links only (fast)
python3 scripts/validate-links.py --no-external

# Test all links including external URLs
python3 scripts/validate-links.py

# Save detailed report
python3 scripts/validate-links.py --output my-report.json
```

**Output:**
- Console summary with error count
- Detailed JSON report (`link-validation-report.json`)
- Exit code 0 = success, 1 = errors found

### `scripts/test-links.py`

**Pre-commit test wrapper** - Simplified interface for quick testing.

```bash
# Fast internal-only check
python3 scripts/test-links.py

# Full check with external URLs
python3 scripts/test-links.py --external
```

## Link Fixing Scripts

### Automated Fixes

When validation finds errors, use these scripts to fix common issues:

```bash
# Fix path calculation errors (CSS, images, navigation)
python3 scripts/fix-all-links.py

# Fix content-level link errors (wrong file locations)
python3 scripts/fix-content-links.py

# Then re-validate
python3 scripts/test-links.py
```

### Manual Fixes

For complex link errors:

1. Run validation: `python3 scripts/validate-links.py --no-external`
2. Read the error report
3. Fix links manually
4. Re-validate

## What Gets Validated

### Internal Links

✓ All `href` and `src` attributes in HTML files  
✓ Relative paths (`../`, `./`, no prefix)  
✓ File existence checks  
✓ Path resolution

### External Links

✓ HTTP/HTTPS URLs  
✓ Reachability check (HTTP status code)  
✓ Timeout handling (10 seconds per URL)

### Excluded

- Template variables (e.g., `{{HOME_PATH}}`)
- Fragment identifiers within same page (`#section`)
- `mailto:` and `tel:` links
- JavaScript URLs

## Common Error Patterns

### Wrong Path Depth

**Error:** `../../../css/styles.css` resolves outside project

**Fix:** Recalculate depth from file to resource
- From `docs/ALICE/file.html` to `css/` = `../../css/`
- From `docs/SAM/developer/file.html` to `css/` = `../../../css/`

**Auto-fix:** `python3 scripts/fix-all-links.py`

### Missing Files

**Error:** Link points to non-existent file

**Common causes:**
- File deleted but links remain
- File moved to different location
- Typo in filename

**Fix:** Update link or create missing file

### Wrong Product Cross-Links

**Error:** ALICE doc links to `../developer/` expecting `docs/developer/`

**Actual:** Developer docs are in `docs/SAM/developer/`

**Correct link:** `../SAM/developer/`

**Auto-fix:** `python3 scripts/fix-content-links.py`

## Integration with Git

### Pre-Commit Hook (Recommended)

Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash
# Pre-commit hook: validate links before committing

echo "Validating internal links..."
python3 scripts/test-links.py

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Commit rejected: broken links found"
    echo "Fix the errors and try again"
    exit 1
fi

echo "✅ Link validation passed"
exit 0
```

Then make it executable:

```bash
chmod +x .git/hooks/pre-commit
```

### Manual Workflow

If not using pre-commit hooks:

```bash
# Make changes to HTML files
git add docs/

# VALIDATE BEFORE COMMITTING
python3 scripts/test-links.py

# If validation passes:
git commit -m "docs: update documentation"

# If validation fails, fix errors then retry
```

## CI/CD Integration

For automated testing in CI/CD pipelines:

```yaml
# GitHub Actions example
- name: Validate Links
  run: |
    python3 scripts/test-links.py --external
```

```bash
# GitLab CI example
test:links:
  script:
    - python3 scripts/test-links.py --external
```

## Troubleshooting

### False Positives

**Template file errors:** `.doc-template.html` will always show 11 errors for template variables. This is expected and safe to ignore.

**Directory warnings:** Links like `/` or `/#section` point to directories, not files. These are warnings, not errors, and are usually correct for navigation.

### External URL Failures

Some external URLs may fail for legitimate reasons:

- **403 Forbidden:** OpenAI API pages require authentication
- **Rate limiting:** Some sites block automated requests
- **Timeouts:** Slow sites may exceed 10-second timeout

For persistent external errors, consider:
1. Update the link to current URL
2. Remove if resource no longer exists
3. Add to allow-list if false positive

## Best Practices

### When Editing HTML

1. **Test locally first:** Use local web server to verify links work
   ```bash
   python3 -m http.server 8000
   # Open http://localhost:8000 and click through pages
   ```

2. **Validate before committing:**
   ```bash
   python3 scripts/test-links.py
   ```

3. **Fix errors immediately:** Don't commit broken links

### When Adding New Pages

1. Create the HTML file
2. Add links to the new page from existing pages
3. Validate to ensure bidirectional linking works
4. Test in browser

### When Moving Files

1. Move the file
2. Search for all references to old path
3. Update all links
4. Validate to catch missed references

## Validation Report Format

The JSON report contains:

```json
{
  "errors": [
    {
      "file": "docs/ALICE/index.html",
      "link": "../missing.html",
      "type": "missing_file",
      "tag": "a",
      "text": "Click here",
      "resolved": "docs/missing.html",
      "error": "File does not exist"
    }
  ],
  "warnings": [...],
  "checked_urls": {
    "https://example.com": [true, "HTTP 200"]
  }
}
```

**Error fields:**
- `file`: Source file containing the link
- `link`: The actual href/src value
- `type`: Error category
- `tag`: HTML tag (`<a>`, `<img>`, etc.)
- `text`: Link text (for `<a>` tags)
- `resolved`: Where the link points (filesystem path or URL)
- `error`: Human-readable error message

## Script Reference

| Script | Purpose | Speed |
|--------|---------|-------|
| `validate-links.py` | Full validation with detailed reporting | Medium |
| `test-links.py` | Pre-commit quick check | Fast |
| `fix-all-links.py` | Auto-fix path calculation errors | Instant |
| `fix-content-links.py` | Auto-fix content-level errors | Instant |
| `fix-navigation-links.py` | Auto-fix navbar/footer links | Instant |
| `final-cleanup.py` | Fix remaining edge cases | Instant |

## Support

For questions or issues with link validation:

1. Check this documentation
2. Review the JSON error report for details
3. Run fix scripts for common patterns
4. Manual review for complex cases
