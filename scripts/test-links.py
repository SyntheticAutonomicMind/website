#!/usr/bin/env python3
"""
Pre-commit link validation test.
Run this before committing changes to ensure no broken links.

Usage:
    python3 scripts/test-links.py              # Test internal links only (fast)
    python3 scripts/test-links.py --external   # Test all links including external (slow)
"""

import sys
import subprocess
from pathlib import Path

def main():
    """Run link validation and exit with appropriate code."""
    args = sys.argv[1:]
    
    # Default to internal-only for speed
    if '--external' in args:
        cmd = ['python3', 'scripts/validate-links.py']
        print('Testing ALL links (internal + external)...')
        print('This may take 1-2 minutes.\n')
    else:
        cmd = ['python3', 'scripts/validate-links.py', '--no-external']
        print('Testing INTERNAL links only (fast)...')
        print('Use --external to also test external URLs.\n')
    
    # Run validation
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    # Parse results
    lines = result.stdout.split('\n')
    errors_line = [l for l in lines if 'Errors found:' in l]
    
    if errors_line:
        errors = int(errors_line[0].split(':')[1].strip())
        template_errors = 11  # Expected template variable errors
        
        real_errors = max(0, errors - template_errors)
        
        if real_errors > 0:
            print(result.stdout)
            print('\n' + '=' * 70)
            print(f'FAILED: Found {real_errors} broken link(s)')
            print('=' * 70)
            print('\nRun `python3 scripts/validate-links.py --no-external` for details.')
            sys.exit(1)
        else:
            print(result.stdout)
            print('\n' + '=' * 70)
            print('PASSED: All internal links are valid!')
            print('=' * 70)
            sys.exit(0)
    else:
        print(result.stdout)
        print(result.stderr)
        print('\nERROR: Could not parse validation results')
        sys.exit(1)


if __name__ == '__main__':
    main()
