#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test script for the BIOSIMULATE utility functions.

This module contains tests for the utility functions and data generators
used throughout the simulation.
"""

import unittest
import os
import sys
import numpy as np
from typing import Dict, List, Any

# Add the parent directory to the path so we can import the biosimulate package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from biosimulate.utils.data_generator import (
    generate_normal_distribution,
    generate_uniform_distribution,
    generate_normal,
    generate_triangular,
    generate_beta
)
# These modules don't exist yet
# from biosimulate.utils.name_generator import generate_name
# from biosimulate.utils.id_generator import generate_id


class TestDataGenerator(unittest.TestCase):
    """Test cases for the data generator functions."""

    def test_generate_normal_distribution(self):
        """Test generating values from a normal distribution."""
        # Generate values
        mean = 100
        std = 15
        size = 1000
        values = generate_normal_distribution(mean, std, size)
        
        # Check that the correct number of values was generated
        self.assertEqual(len(values), size)
        
        # Check that the values have approximately the expected mean and std
        self.assertAlmostEqual(np.mean(values), mean, delta=2)
        self.assertAlmostEqual(np.std(values), std, delta=2)
        
        # Test with truncation
        min_val = 70
        max_val = 130
        truncated_values = generate_normal_distribution(mean, std, size, min_val, max_val)
        
        # Check that all values are within the truncation range
        self.assertGreaterEqual(min(truncated_values), min_val)
        self.assertLessEqual(max(truncated_values), max_val)

    def test_generate_uniform_distribution(self):
        """Test generating values from a uniform distribution."""
        # Generate values
        min_val = 10
        max_val = 50
        size = 1000
        values = generate_uniform_distribution(min_val, max_val, size)
        
        # Check that the correct number of values was generated
        self.assertEqual(len(values), size)
        
        # Check that all values are within the specified range
        self.assertGreaterEqual(min(values), min_val)
        self.assertLessEqual(max(values), max_val)
        
        # Check that the values have approximately a uniform distribution
        # by checking that the mean is close to the expected value
        expected_mean = (min_val + max_val) / 2
        self.assertAlmostEqual(np.mean(values), expected_mean, delta=2)

    def test_generate_normal(self):
        """Test generating a single value from a normal distribution."""
        # Generate values
        mean = 100
        std = 15
        
        # Generate multiple values to test the function
        values = [generate_normal(mean, std) for _ in range(1000)]
        
        # Check that the values have approximately the expected mean and std
        self.assertAlmostEqual(np.mean(values), mean, delta=2)
        self.assertAlmostEqual(np.std(values), std, delta=2)
        
        # Test with truncation
        min_val = 70
        max_val = 130
        truncated_values = generate_normal(mean, std, 1000, min_val, max_val)
        
        # Check that all values are within the truncation range
        self.assertTrue(np.all(truncated_values >= min_val))
        self.assertTrue(np.all(truncated_values <= max_val))

    def test_generate_triangular(self):
        """Test generating values from a triangular distribution."""
        # Generate values
        min_val = 10
        mode = 30
        max_val = 50
        
        # Generate multiple values to test the function
        values = [generate_triangular(min_val, mode, max_val) for _ in range(1000)]
        
        # Check that all values are within the specified range
        self.assertGreaterEqual(min(values), min_val)
        self.assertLessEqual(max(values), max_val)
        
        # Check that the values have approximately the expected mode
        # by checking the most frequent value (binned)
        hist, bin_edges = np.histogram(values, bins=20)
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
        most_frequent_bin = bin_centers[np.argmax(hist)]
        
        # The most frequent bin should be close to the mode
        self.assertAlmostEqual(most_frequent_bin, mode, delta=5)

    def test_generate_beta(self):
        """Test generating values from a beta distribution."""
        # Generate values
        alpha = 2
        beta = 5
        
        # Generate multiple values to test the function
        values = [generate_beta(alpha, beta) for _ in range(1000)]
        
        # Check that all values are within the [0, 1] range
        self.assertGreaterEqual(min(values), 0)
        self.assertLessEqual(max(values), 1)
        
        # Check that the values have approximately the expected mean
        expected_mean = alpha / (alpha + beta)
        self.assertAlmostEqual(np.mean(values), expected_mean, delta=0.05)
        
        # Test with scaling
        min_val = 10
        max_val = 50
        scaled_values = generate_beta(alpha, beta, 1000, min_val, max_val)
        
        # Check that all values are within the scaled range
        self.assertTrue(np.all(scaled_values >= min_val))
        self.assertTrue(np.all(scaled_values <= max_val))
        
        # Check that the values have approximately the expected scaled mean
        expected_scaled_mean = min_val + expected_mean * (max_val - min_val)
        self.assertAlmostEqual(np.mean(scaled_values), expected_scaled_mean, delta=2)


# class TestNameGenerator(unittest.TestCase):
#     """Test cases for the name generator functions."""

#     def test_generate_name(self):
#         """Test generating names for different entity types."""
#         # Test generating a research entity name
#         research_name = generate_name("research_entity")
#         self.assertIsInstance(research_name, str)
#         self.assertGreater(len(research_name), 0)
        
#         # Test generating a commercial player name
#         commercial_name = generate_name("commercial_player")
#         self.assertIsInstance(commercial_name, str)
#         self.assertGreater(len(commercial_name), 0)
        
#         # Test generating a regulatory body name
#         regulatory_name = generate_name("regulatory_body")
#         self.assertIsInstance(regulatory_name, str)
#         self.assertGreater(len(regulatory_name), 0)
        
#         # Test generating a market participant name
#         market_name = generate_name("market_participant")
#         self.assertIsInstance(market_name, str)
#         self.assertGreater(len(market_name), 0)
        
#         # Test generating a name with a specific region
#         region_name = generate_name("research_entity", region="europe")
#         self.assertIsInstance(region_name, str)
#         self.assertGreater(len(region_name), 0)
        
#         # Test generating a name with a specific subtype
#         subtype_name = generate_name("commercial_player", subtype="biotech_corporation")
#         self.assertIsInstance(subtype_name, str)
#         self.assertGreater(len(subtype_name), 0)
        
#         # Test that different calls generate different names
#         names = [generate_name("research_entity") for _ in range(10)]
#         unique_names = set(names)
#         self.assertGreater(len(unique_names), 1)  # At least some should be different


# class TestIdGenerator(unittest.TestCase):
#     """Test cases for the ID generator functions."""

#     def test_generate_id(self):
#         """Test generating IDs for different entity types."""
#         # Test generating a research entity ID
#         research_id = generate_id("research_entity")
#         self.assertIsInstance(research_id, str)
#         self.assertGreater(len(research_id), 0)
#         self.assertTrue(research_id.startswith("re_"))
        
#         # Test generating a commercial player ID
#         commercial_id = generate_id("commercial_player")
#         self.assertIsInstance(commercial_id, str)
#         self.assertGreater(len(commercial_id), 0)
#         self.assertTrue(commercial_id.startswith("cp_"))
        
#         # Test generating a regulatory body ID
#         regulatory_id = generate_id("regulatory_body")
#         self.assertIsInstance(regulatory_id, str)
#         self.assertGreater(len(regulatory_id), 0)
#         self.assertTrue(regulatory_id.startswith("rb_"))
        
#         # Test generating a market participant ID
#         market_id = generate_id("market_participant")
#         self.assertIsInstance(market_id, str)
#         self.assertGreater(len(market_id), 0)
#         self.assertTrue(market_id.startswith("mp_"))
        
#         # Test generating an ID with a specific region
#         region_id = generate_id("research_entity", region="europe")
#         self.assertIsInstance(region_id, str)
#         self.assertGreater(len(region_id), 0)
#         self.assertTrue(region_id.startswith("re_"))
#         self.assertTrue("europe" in region_id)
        
#         # Test generating an ID with a specific subtype
#         subtype_id = generate_id("commercial_player", subtype="biotech_corporation")
#         self.assertIsInstance(subtype_id, str)
#         self.assertGreater(len(subtype_id), 0)
#         self.assertTrue(subtype_id.startswith("cp_"))
#         self.assertTrue("biotech" in subtype_id)
        
#         # Test that different calls generate different IDs
#         ids = [generate_id("research_entity") for _ in range(10)]
#         unique_ids = set(ids)
#         self.assertEqual(len(unique_ids), 10)  # All should be different


if __name__ == "__main__":
    unittest.main()