"""
Demo Script - Test PDF Parsing
This script demonstrates how to use the AusgabeAnalyst components programmatically
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.pdf_parser import VolksbankPDFParser
from src.categorizer import TransactionCategorizer
from src.data_manager import DataManager


def demo_parse_pdf(pdf_path):
    """
    Demonstrate PDF parsing and categorization

    Args:
        pdf_path: Path to PDF file
    """
    print("=" * 80)
    print("AusgabeAnalyst - PDF PARSING DEMO")
    print("=" * 80)

    # Initialize components
    parser = VolksbankPDFParser()
    categorizer = TransactionCategorizer()

    print(f"\n1. Parsing PDF: {pdf_path}")
    print("-" * 80)

    try:
        # Parse PDF
        result = parser.parse_pdf(pdf_path)

        # Display metadata
        print("\nMetadata:")
        for key, value in result['metadata'].items():
            print(f"  {key}: {value}")

        # Display transactions
        print(f"\nTransactions found: {len(result['transactions'])}")
        print("-" * 80)

        # Categorize transactions
        transactions = categorizer.categorize_batch(result['transactions'])

        # Show first 10 transactions
        print("\nFirst 10 Transactions:")
        print("-" * 80)
        for i, txn in enumerate(transactions[:10], 1):
            print(f"\n{i}. {txn['value_date']}")
            print(f"   Description: {txn['description']}")
            print(f"   Amount: €{txn['amount']:.2f}")
            print(f"   Type: {txn['type']}")
            print(f"   Category: {txn['category']}")

        # Category summary
        print("\n" + "=" * 80)
        print("CATEGORY SUMMARY")
        print("=" * 80)

        category_totals = {}
        for txn in transactions:
            if txn['amount'] < 0:  # Only expenses
                category = txn['category']
                if category not in category_totals:
                    category_totals[category] = 0
                category_totals[category] += abs(txn['amount'])

        for category, total in sorted(category_totals.items(), key=lambda x: x[1], reverse=True):
            print(f"{category:.<40} €{total:>10.2f}")

        # Financial summary
        print("\n" + "=" * 80)
        print("FINANCIAL SUMMARY")
        print("=" * 80)

        total_income = sum(txn['amount'] for txn in transactions if txn['amount'] > 0)
        total_expenses = abs(sum(txn['amount'] for txn in transactions if txn['amount'] < 0))
        net_savings = total_income - total_expenses

        print(f"Total Income:     €{total_income:>10.2f}")
        print(f"Total Expenses:   €{total_expenses:>10.2f}")
        print(f"Net Savings:      €{net_savings:>10.2f}")

        return True

    except Exception as e:
        print(f"\nError: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def demo_with_data_manager(pdf_path):
    """
    Demonstrate using the data manager to store transactions

    Args:
        pdf_path: Path to PDF file
    """
    print("\n" + "=" * 80)
    print("DATA MANAGER DEMO")
    print("=" * 80)

    # Initialize components
    parser = VolksbankPDFParser()
    categorizer = TransactionCategorizer()
    data_manager = DataManager(data_dir='demo_data')

    print("\n1. Parsing and categorizing transactions...")
    result = parser.parse_pdf(pdf_path)
    transactions = categorizer.categorize_batch(result['transactions'])

    print(f"   Found {len(transactions)} transactions")

    print("\n2. Adding transactions to database...")
    add_result = data_manager.add_transactions(transactions)

    print(f"   Added: {add_result['added']}")
    print(f"   Skipped (duplicates): {add_result['skipped']}")

    print("\n3. Retrieving summary statistics...")
    stats = data_manager.get_summary_statistics()

    for key, value in stats.items():
        print(f"   {key}: {value}")

    print("\n4. Getting monthly summary...")
    monthly = data_manager.get_monthly_summary()
    print(monthly)

    print("\n5. Getting category summary...")
    categories = data_manager.get_category_summary()
    print(categories)

    print("\n✅ Demo complete! Check 'demo_data/expenses_history.csv' for the stored data.")


if __name__ == "__main__":
    # Example usage
    # Replace with your PDF path
    pdf_file = "path/to/your/volksbank_statement.pdf"

    if len(sys.argv) > 1:
        pdf_file = sys.argv[1]

    if os.path.exists(pdf_file):
        demo_parse_pdf(pdf_file)
        print("\n")
        demo_with_data_manager(pdf_file)
    else:
        print(f"Usage: python demo.py <path_to_pdf>")
        print(f"\nExample: python demo.py statement.pdf")
        print(f"\nNote: PDF file not found: {pdf_file}")