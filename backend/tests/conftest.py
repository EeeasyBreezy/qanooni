import sys
from pathlib import Path

# Ensure "backend" is on sys.path for IDE discovery and pytest runs
BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

