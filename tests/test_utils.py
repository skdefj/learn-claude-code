"""
Tests for utility functions.
"""

import unittest
from utils import add, multiply
from hello import greet


class TestGreet(unittest.TestCase):
    """Test cases for the greet function."""

    def test_greet_with_name(self):
        """Test greeting with a name."""
        self.assertEqual(greet("Alice"), "Hello, Alice!")

    def test_greet_with_empty_string(self):
        """Test greeting with an empty string."""
        self.assertEqual(greet(""), "Hello, !")

    def test_greet_with_special_chars(self):
        """Test greeting with special characters."""
        self.assertEqual(greet("Bob!"), "Hello, Bob!!")


class TestAdd(unittest.TestCase):
    """Test cases for the add function."""

    def test_add_positive_numbers(self):
        """Test adding positive numbers."""
        self.assertEqual(add(2, 3), 5)

    def test_add_negative_numbers(self):
        """Test adding negative numbers."""
        self.assertEqual(add(-1, -1), -2)

    def test_add_mixed_numbers(self):
        """Test adding mixed positive and negative numbers."""
        self.assertEqual(add(-1, 1), 0)

    def test_add_zeros(self):
        """Test adding zeros."""
        self.assertEqual(add(0, 0), 0)


class TestMultiply(unittest.TestCase):
    """Test cases for the multiply function."""

    def test_multiply_positive_numbers(self):
        """Test multiplying positive numbers."""
        self.assertEqual(multiply(2, 3), 6)

    def test_multiply_negative_numbers(self):
        """Test multiplying negative numbers."""
        self.assertEqual(multiply(-2, -3), 6)

    def test_multiply_mixed_numbers(self):
        """Test multiplying mixed positive and negative numbers."""
        self.assertEqual(multiply(-2, 3), -6)

    def test_multiply_by_zero(self):
        """Test multiplying by zero."""
        self.assertEqual(multiply(5, 0), 0)


if __name__ == "__main__":
    unittest.main()
