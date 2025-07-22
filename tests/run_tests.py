#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test runner for the BIOSIMULATE project.

This script discovers and runs all tests in the tests directory.
"""

import unittest
import os
import sys
import logging
from pathlib import Path

# Add the parent directory to the path so we can import the biosimulate package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def run_tests():
    """Discover and run all tests in the tests directory."""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # Get the directory containing this script
    tests_dir = Path(__file__).parent
    
    # Discover and run tests
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=tests_dir, pattern="test_*.py")
    
    # Create a test runner
    runner = unittest.TextTestRunner(verbosity=2)
    
    # Run the tests
    result = runner.run(suite)
    
    # Return the result
    return result


if __name__ == "__main__":
    # Run the tests
    result = run_tests()
    
    # Exit with appropriate status code
    sys.exit(not result.wasSuccessful())