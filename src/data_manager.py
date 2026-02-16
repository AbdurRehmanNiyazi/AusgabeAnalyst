"""
Data Manager Module
Handles CSV storage, duplicate detection, and data persistence
"""

import pandas as pd
import os
from typing import List, Dict
from datetime import datetime
import hashlib

import self


class DataManager:
    """Manages expense data storage and retrieval"""

    def __init__(self, data_dir: str = 'data'):
        """
        Initialize data manager

        Args:
            data_dir: Directory to store data files
        """
        self.data_dir = data_dir
        self.csv_path = os.path.join(data_dir, 'expenses_history.csv')

        # Create data directory if it doesn't exist
        os.makedirs(data_dir, exist_ok=True)

        # Initialize CSV if it doesn't exist
        if not os.path.exists(self.csv_path):
            self._initialize_csv()

    def _initialize_csv(self):
        """Create empty CSV with proper columns"""
        columns = [
            'transaction_id', 'value_date', 'booking_date', 'description',
            'amount', 'type', 'category', 'raw_description', 'upload_date'
        ]
        df = pd.DataFrame(columns=columns)
        df.to_csv(self.csv_path, index=False)

    def clear_all_data(self):
        """Deletes all transactions and resets the CSV"""
        if os.path.exists(self.csv_path):
            os.remove(self.csv_path)
        self._initialize_csv()  # This recreates the empty file

    def _generate_transaction_id(self, transaction: Dict) -> str:
        """
        Generate unique ID for a transaction

        Args:
            transaction: Transaction dictionary

        Returns:
            Unique transaction ID
        """
        # Create hash from date, amount, and description
        unique_string = f"{transaction['value_date']}_{transaction['amount']}_{transaction['description']}"
        return hashlib.md5(unique_string.encode()).hexdigest()[:16]

    def add_transactions(self, transactions: List[Dict]) -> Dict[str, int]:
        """
        Add new transactions to the CSV, avoiding duplicates

        Args:
            transactions: List of transaction dictionaries

        Returns:
            Dictionary with counts of added and skipped transactions
        """
        # Load existing data
        existing_df = pd.read_csv(self.csv_path)

        # Generate IDs for new transactions
        for transaction in transactions:
            transaction['transaction_id'] = self._generate_transaction_id(transaction)
            transaction['upload_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Create DataFrame from new transactions
        new_df = pd.DataFrame(transactions)

        # Find duplicates
        existing_ids = set(existing_df['transaction_id'].values) if not existing_df.empty else set()
        new_df['is_duplicate'] = new_df['transaction_id'].isin(existing_ids)

        duplicates_count = new_df['is_duplicate'].sum()
        new_transactions = new_df[~new_df['is_duplicate']].drop('is_duplicate', axis=1)

        # Append new transactions
        if not new_transactions.empty:
            combined_df = pd.concat([existing_df, new_transactions], ignore_index=True)
            combined_df.to_csv(self.csv_path, index=False)

        return {
            'added': len(new_transactions),
            'skipped': duplicates_count,
            'total': len(transactions)
        }

    def load_all_transactions(self) -> pd.DataFrame:
        """
        Load all transactions from CSV

        Returns:
            DataFrame with all transactions
        """
        df = pd.read_csv(self.csv_path)

        if not df.empty:
            # Convert date columns to datetime
            df['value_date'] = pd.to_datetime(df['value_date'])
            df['booking_date'] = pd.to_datetime(df['booking_date'])
            df['upload_date'] = pd.to_datetime(df['upload_date'])

            # Sort by value_date
            df = df.sort_values('value_date', ascending=False)

        return df

    def get_transactions_by_date_range(self, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Get transactions within a date range

        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)

        Returns:
            Filtered DataFrame
        """
        df = self.load_all_transactions()

        if not df.empty:
            mask = (df['value_date'] >= start_date) & (df['value_date'] <= end_date)
            return df[mask]

        return df

    def get_transactions_by_category(self, category: str) -> pd.DataFrame:
        """
        Get all transactions for a specific category

        Args:
            category: Category name

        Returns:
            Filtered DataFrame
        """
        df = self.load_all_transactions()

        if not df.empty:
            return df[df['category'] == category]

        return df

    def get_summary_statistics(self) -> Dict:
        """
        Calculate summary statistics

        Returns:
            Dictionary with summary stats
        """
        df = self.load_all_transactions()

        if df.empty:
            return {
                'total_transactions': 0,
                'total_income': 0.0,
                'total_expenses': 0.0,
                'net_savings': 0.0,
                'current_balance': 0.0
            }

        income = df[df['amount'] > 0]['amount'].sum()
        expenses = abs(df[df['amount'] < 0]['amount'].sum())

        return {
            'total_transactions': len(df),
            'total_income': income,
            'total_expenses': expenses,
            'net_savings': income - expenses,
            'current_balance': df['amount'].sum(),
            'date_range': f"{df['value_date'].min().strftime('%Y-%m-%d')} to {df['value_date'].max().strftime('%Y-%m-%d')}"
        }

    def get_monthly_summary(self) -> pd.DataFrame:
        """
        Get spending summary by month

        Returns:
            DataFrame with monthly totals
        """
        df = self.load_all_transactions()

        if df.empty:
            return pd.DataFrame()

        # Add month column
        df['month'] = df['value_date'].dt.to_period('M')

        # Group by month
        monthly = df.groupby('month').agg({
            'amount': 'sum'
        }).reset_index()

        monthly['month'] = monthly['month'].astype(str)

        # Separate income and expenses
        monthly_detail = df.groupby(['month', 'type']).agg({
            'amount': 'sum'
        }).reset_index()

        monthly_detail['month'] = monthly_detail['month'].astype(str)
        monthly_detail['amount'] = monthly_detail['amount'].abs()

        return monthly_detail

    def get_category_summary(self) -> pd.DataFrame:
        """
        Get spending summary by category

        Returns:
            DataFrame with category totals
        """
        df = self.load_all_transactions()

        if df.empty:
            return pd.DataFrame()

        # Filter only expenses (negative amounts)
        expenses = df[df['amount'] < 0].copy()
        expenses['amount'] = expenses['amount'].abs()

        # Group by category
        category_summary = expenses.groupby('category').agg({
            'amount': 'sum',
            'transaction_id': 'count'
        }).reset_index()

        category_summary.columns = ['category', 'total_amount', 'transaction_count']
        category_summary = category_summary.sort_values('total_amount', ascending=False)

        return category_summary

    def export_to_excel(self, output_path: str):
        """
        Export all data to Excel

        Args:
            output_path: Path for the Excel file
        """
        df = self.load_all_transactions()

        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='All Transactions', index=False)

            summary = self.get_summary_statistics()
            summary_df = pd.DataFrame([summary])
            summary_df.to_excel(writer, sheet_name='Summary', index=False)

            monthly = self.get_monthly_summary()
            if not monthly.empty:
                monthly.to_excel(writer, sheet_name='Monthly', index=False)

            category = self.get_category_summary()
            if not category.empty:
                category.to_excel(writer, sheet_name='Categories', index=False)
