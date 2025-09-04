"""
Main entry point for EduSeedbank application.
"""

import os
import sys

# Add src to path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from eduseedbank.cli.main import main

if __name__ == "__main__":
    main()