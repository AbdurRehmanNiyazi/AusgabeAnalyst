"""
PDF Parser Module
Extracts transaction data from Volksbank bank statements
"""

import re
from datetime import datetime
from typing import List, Dict, Optional
import pdfplumber


class VolksbankPDFParser:
    """Parser for Volksbank Mittelhessen bank statements"""

    def __init__(self):
        # Pattern to match transaction lines
        # Format: DD.MM. DD.MM. Description PN:XXX Amount S/H
        self.transaction_pattern = re.compile(
            r'(\d{2}\.\d{2}\.)\s+(\d{2}\.\d{2}\.)\s+(.*?)\s+PN:\d+\s+([\d,\.]+)\s+([SH])'
        )

        # Pattern to extract account balance
        self.balance_pattern = re.compile(
            r'neuer Kontostand vom (\d{2}\.\d{2}\.\d{4})\s+([\d,\.]+)\s+([SH])'
        )

        # Pattern to extract old balance
        self.old_balance_pattern = re.compile(
            r'alter Kontostand vom (\d{2}\.\d{2}\.\d{4})\s+([\d,\.]+)\s+([SH])'
        )

    def parse_pdf(self, pdf_path: str) -> Dict:
        """
        Parse a Volksbank PDF statement

        Args:
            pdf_path: Path to the PDF file

        Returns:
            Dictionary containing transactions and metadata
        """
        transactions = []
        metadata = {}

        try:
            with pdfplumber.open(pdf_path) as pdf:
                full_text = ""
                for page in pdf.pages:
                    full_text += page.extract_text() + "\n"

                # Extract metadata
                metadata = self._extract_metadata(full_text)

                # Extract transactions
                transactions = self._extract_transactions(full_text, metadata.get('year'))

        except Exception as e:
            raise Exception(f"Error parsing PDF: {str(e)}")

        return {
            'transactions': transactions,
            'metadata': metadata
        }

    def _extract_metadata(self, text: str) -> Dict:
        """Extract account information and balances from statement"""
        metadata = {}

        # Extract IBAN
        iban_match = re.search(r'IBAN:\s*(DE\d{2}\s*\d{4}\s*\d{4}\s*\d{4}\s*\d{4}\s*\d{2})', text)
        if iban_match:
            metadata['iban'] = iban_match.group(1).replace(' ', '')

        # Extract statement number and year
        statement_match = re.search(r'(\d+)/(\d{4})', text)
        if statement_match:
            metadata['statement_number'] = statement_match.group(1)
            metadata['year'] = statement_match.group(2)

        # Extract old balance
        old_balance_match = self.old_balance_pattern.search(text)
        if old_balance_match:
            date_str, amount_str, type_indicator = old_balance_match.groups()
            metadata['old_balance_date'] = date_str
            metadata['old_balance'] = self._parse_amount(amount_str, type_indicator)

        # Extract new balance
        new_balance_match = self.balance_pattern.search(text)
        if new_balance_match:
            date_str, amount_str, type_indicator = new_balance_match.groups()
            metadata['new_balance_date'] = date_str
            metadata['new_balance'] = self._parse_amount(amount_str, type_indicator)

        return metadata

    def _extract_transactions(self, text: str, year: Optional[str] = None) -> List[Dict]:
        """Extract individual transactions from the statement text with multi-line support"""
        transactions = []
        if not year:
            year = str(datetime.now().year)

        # This pattern identifies the start of a transaction row (Date Date)
        row_start_pattern = re.compile(r'^(\d{2}\.\d{2}\.)\s+(\d{2}\.\d{2}\.)', re.MULTILINE)

        # We also need to identify the ending (Amount S/H)
        amount_pattern = re.compile(r'([\d,\.]+)\s+([SH])$')

        lines = text.split('\n')
        current_transaction = None

        for line in lines:
            line = line.strip()
            row_match = row_start_pattern.match(line)

            if row_match:
                # If we were already building a transaction, save it
                if current_transaction:
                    transactions.append(current_transaction)

                # Start a new transaction
                val_date, book_date = row_match.groups()
                # Find the amount at the end of this same line
                amt_match = amount_pattern.search(line)

                if amt_match:
                    amt_str, type_ind = amt_match.groups()
                    # Everything between the dates and the amount is the first line of description
                    desc_part = line[row_match.end():amt_match.start()].strip()

                    current_transaction = {
                        'value_date': self._parse_date(val_date, year),
                        'booking_date': self._parse_date(book_date, year),
                        'description_lines': [desc_part],
                        'amount': self._parse_amount(amt_str, type_ind),
                        'type': 'Credit' if type_ind == 'H' else 'Debit',
                        'raw_description': line
                    }
            elif current_transaction and line and not re.match(r'^\d', line):
                # This line belongs to the previous transaction's description
                # We skip lines starting with digits to avoid capturing page footers or metadata
                current_transaction['description_lines'].append(line)
                current_transaction['raw_description'] += " " + line

        # Add the final transaction
        if current_transaction:
            transactions.append(current_transaction)

        # Finalize the description by joining all captured lines
        for t in transactions:
            t['description'] = " ".join(t.pop('description_lines'))

        return transactions

    def _parse_date(self, date_str: str, year: str) -> str:
        """
        Convert DD.MM. format to YYYY-MM-DD

        Args:
            date_str: Date in DD.MM. format
            year: Year as string

        Returns:
            Date in YYYY-MM-DD format
        """
        day, month = date_str.strip('.').split('.')
        return f"{year}-{month.zfill(2)}-{day.zfill(2)}"

    def _parse_amount(self, amount_str: str, type_indicator: str) -> float:
        """
        Convert German number format to float
        Handle S (Soll/Debit) as negative, H (Haben/Credit) as positive

        Args:
            amount_str: Amount in German format (e.g., "1.234,56")
            type_indicator: 'S' for debit, 'H' for credit

        Returns:
            Amount as float (negative for debits, positive for credits)
        """
        # Remove thousand separators and replace comma with dot
        amount_str = amount_str.replace('.', '').replace(',', '.')
        amount = float(amount_str)

        # Make debits negative
        if type_indicator == 'S':
            amount = -amount

        return amount

    def _clean_description(self, description: str) -> str:
        lines = [line.strip() for line in description.split('\n') if line.strip()]
        if not lines:
            return "Unknown"

        # Keywords to ignore if they are the only thing on the first line
        ignore_headers = ['KARTENZAHLUNG GIROCARD', 'BASISLASTSCHRIFT', 'ÜBERWEISUNG', 'GUTSCHRIFT']

        main_desc = lines[0]

        # If the first line is just a generic header, try to find the vendor on line 2 or 3
        if any(header in main_desc.upper() for header in ignore_headers) and len(lines) > 1:
            # Check the next two lines for a more descriptive name
            for potential_vendor in lines[1:3]:
                # Skip lines that look like transaction IDs (mostly numbers/special chars)
                if not any(char.isdigit() for char in potential_vendor[:5]):
                    return potential_vendor

        return main_desc