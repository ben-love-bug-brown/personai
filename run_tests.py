#!/usr/bin/env python
"""
Test runner that suppresses termcap warnings.
"""

import os
import subprocess
import sys

# Set proper TERM to avoid warnings
os.environ.setdefault('TERM', 'xterm')

# Run pytest
result = subprocess.run(
    [sys.executable, '-m', 'pytest', 'src/', '-v', '-x', '--tb=short'] + sys.argv[1:],
    capture_output=True,
    text=True
)

# Filter termcap warning from output
for line in result.stdout.splitlines():
    if 'termcap' not in line.lower() and 'dumb terminal' not in line.lower():
        print(line)

for line in result.stderr.splitlines():
    if 'termcap' not in line.lower() and 'dumb terminal' not in line.lower():
        print(line, file=sys.stderr)

sys.exit(result.returncode)
