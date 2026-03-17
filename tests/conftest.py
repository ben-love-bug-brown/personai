"""
Pytest configuration for PersonAI.
"""

import os
import sys

# Fix termcap issues in headless environments
os.environ.setdefault('TERM', 'dumb')
os.environ.setdefault('NO_COLOR', '1')

# Ensure src is in path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
