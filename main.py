#!/usr/bin/env python3
"""
AWS DevOps Agent - Main Entry Point
Modern entry point following Python best practices
"""

import sys
from pathlib import Path

# Add src to Python path for development
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from aws_devops_agent.main import main

if __name__ == "__main__":
    sys.exit(main())
