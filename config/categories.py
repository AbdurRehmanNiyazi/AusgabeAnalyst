"""
Category mapping configuration for transaction classification
"""

CATEGORY_KEYWORDS = {
    # Specific Vendors First
    'Groceries': [
        'aldi', 'lidl', 'edeka', 'rewe', 'kaufland', 'netto', 'penny',
        'herkules', 'mix markt', 'city markt', 'ariana mini market',
        'schwaelmer brotladen', 'schaefers backstuben'
    ],
    'Restaurants & Dining': [
        'restaurant', 'pizza', 'burger', 'murg', 'phung', 'chicken house',
        'gastro', 'zam zam', 'halal food', 'somat doner', 'lezzeti mangal',
        'central grill', 'west imbiss', 'espresso house', 'malamania'
    ],
    'Income': [
        'lohn', 'gehalt', 'rente', 'zenjob', 'gutschrift', 'salary'
    ],
    'Personal Care': [
        'dm drogerie', 'dm drogeriemarkt', 'rossmann', 'müller', 'apotheke', 'pharmacy'
    ],
    'Telecommunications': [
        'drillisch', 'sim24', 'telekom', 'vodafone', 'o2'
    ],
    'Clothing': [
        'kik', 'h&m', 'zara', 'c&a', 'primark', 'takko holding', 'woolworth'
    ],
    'Transportation': [
        'tankstelle', 'shell', 'aral', 'esso', 'db ', 'bahn', 'rmv', 'flix'
    ],
    'Cash Withdrawal': [
        'auszahlung', 'geldautomat', 'withdrawal', 'atm'
    ],
    # Generic Transfers Last
    'Transfers': [
        'überweisung', 'transfer', 'sepa', 'wise'
    ],
    'Shopping': [
        'amazon', 'ebay', 'online', 'shop'
    ],
    'Other': []
}

# Default category for unmatched transactions
DEFAULT_CATEGORY = 'Other'

# Transaction type indicators in Volksbank statements
TRANSACTION_TYPES = {
    'S': 'Debit',   # Soll (withdrawal/expense)
    'H': 'Credit'   # Haben (deposit/income)
}