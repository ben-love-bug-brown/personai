"""
Site customization - suppress termcap warning in headless environments.
"""

import sys
import os
import io

# Suppress curses termcap warning in headless/headless environments
# This must be done before curses is imported
if os.environ.get('TERM', '') == 'dumb':
    try:
        # Capture stderr during curses import
        old_stderr = sys.stderr
        sys.stderr = io.StringIO()
        import curses
        # Discard the warning, restore stderr
        sys.stderr = old_stderr
    except Exception:
        # If anything fails, restore stderr
        sys.stderr = old_stderr
