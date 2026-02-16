"""
Transaction Categorizer Module
Categorizes transactions based on description keywords
"""

from typing import Dict, List
import sys
import os

# Add config to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config.categories import CATEGORY_KEYWORDS, DEFAULT_CATEGORY


class TransactionCategorizer:
    """Categorizes transactions based on keywords in descriptions"""

    def __init__(self, custom_keywords: Dict[str, List[str]] = None):
        """
        Initialize categorizer

        Args:
            custom_keywords: Optional custom category keywords to merge with defaults
        """
        self.category_keywords = CATEGORY_KEYWORDS.copy()

        if custom_keywords:
            for category, keywords in custom_keywords.items():
                if category in self.category_keywords:
                    self.category_keywords[category].extend(keywords)
                else:
                    self.category_keywords[category] = keywords

    def categorize(self, description: str) -> str:
        description_lower = description.lower()

        # Define priority: Specific vendors MUST be checked before generic terms
        priority_order = [
            'Groceries', 'Restaurants & Dining', 'Personal Care',
            'Telecommunications', 'Clothing', 'Transportation', 'Income'
        ]

        # First, check high-priority specific categories
        for category in priority_order:
            if category in self.category_keywords:
                for keyword in self.category_keywords[category]:
                    if keyword.lower() in description_lower:
                        return category

        # Secondly, check remaining categories (Transfers, Cash, etc.)
        for category, keywords in self.category_keywords.items():
            if category not in priority_order:
                for keyword in keywords:
                    if keyword.lower() in description_lower:
                        return category

        return DEFAULT_CATEGORY

    def categorize_batch(self, transactions: List[Dict]) -> List[Dict]:
        """
        Categorize multiple transactions

        Args:
            transactions: List of transaction dictionaries

        Returns:
            List of transactions with category field added
        """
        for transaction in transactions:
            transaction['category'] = self.categorize(transaction['description'])

        return transactions

    def get_categories(self) -> List[str]:
        """Get list of all available categories"""
        return list(self.category_keywords.keys())

    def add_keyword(self, category: str, keyword: str):
        """
        Add a keyword to a category

        Args:
            category: Category name
            keyword: Keyword to add
        """
        if category not in self.category_keywords:
            self.category_keywords[category] = []

        if keyword.lower() not in [k.lower() for k in self.category_keywords[category]]:
            self.category_keywords[category].append(keyword)