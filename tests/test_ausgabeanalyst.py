"""
Sample Unit Tests for AusgabeAnalyst
Run with: pytest tests/
"""

import unittest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.pdf_parser import VolksbankPDFParser
from src.categorizer import TransactionCategorizer


class TestPDFParser(unittest.TestCase):
    """Test cases for PDF parser"""

    def setUp(self):
        """Set up test fixtures"""
        self.parser = VolksbankPDFParser()

    def test_parse_date(self):
        """Test date parsing from DD.MM. format"""
        result = self.parser._parse_date("01.10.", "2025")
        self.assertEqual(result, "2025-10-01")

        result = self.parser._parse_date("31.12.", "2024")
        self.assertEqual(result, "2024-12-31")

    def test_parse_amount_debit(self):
        """Test amount parsing for debits (expenses)"""
        result = self.parser._parse_amount("123,45", "S")
        self.assertEqual(result, -123.45)

        result = self.parser._parse_amount("1.234,56", "S")
        self.assertEqual(result, -1234.56)

    def test_parse_amount_credit(self):
        """Test amount parsing for credits (income)"""
        result = self.parser._parse_amount("123,45", "H")
        self.assertEqual(result, 123.45)

        result = self.parser._parse_amount("1.234,56", "H")
        self.assertEqual(result, 1234.56)

    def test_clean_description(self):
        """Test description cleaning"""
        # Single line description
        result = self.parser._clean_description("ALDI SE + Co. KG")
        self.assertEqual(result, "ALDI SE + Co. KG")

        # Multi-line description
        multi_line = "Kartenzahlung girocard\nALDI SE + Co. KG SCHLOSS HOLTE"
        result = self.parser._clean_description(multi_line)
        self.assertEqual(result, "ALDI SE + Co. KG SCHLOSS HOLTE")


class TestCategorizer(unittest.TestCase):
    """Test cases for transaction categorizer"""

    def setUp(self):
        """Set up test fixtures"""
        self.categorizer = TransactionCategorizer()

    def test_categorize_groceries(self):
        """Test grocery categorization"""
        result = self.categorizer.categorize("ALDI SAGT DANKE")
        self.assertEqual(result, "Groceries")

        result = self.categorizer.categorize("LIDL MARBURG")
        self.assertEqual(result, "Groceries")

    def test_categorize_income(self):
        """Test income categorization"""
        result = self.categorizer.categorize("ZenJob SE Lohn")
        self.assertEqual(result, "Income")

        result = self.categorizer.categorize("Gehalt Oktober")
        self.assertEqual(result, "Income")

    def test_categorize_personal_care(self):
        """Test personal care categorization"""
        result = self.categorizer.categorize("DM DROGERIEMARKT SAGT DANKE")
        self.assertEqual(result, "Personal Care")

    def test_categorize_restaurant(self):
        """Test restaurant categorization"""
        result = self.categorizer.categorize("CHICKEN HOUSE")
        self.assertEqual(result, "Restaurants & Dining")

        result = self.categorizer.categorize("Harun Murg Restaurant")
        self.assertEqual(result, "Restaurants & Dining")

    def test_categorize_unknown(self):
        """Test unknown transaction categorization"""
        result = self.categorizer.categorize("UNKNOWN MERCHANT XYZ")
        self.assertEqual(result, "Other")

    def test_add_keyword(self):
        """Test adding new keywords"""
        self.categorizer.add_keyword("Shopping", "amazon")
        result = self.categorizer.categorize("Amazon Prime")
        self.assertEqual(result, "Shopping")


if __name__ == '__main__':
    unittest.main()