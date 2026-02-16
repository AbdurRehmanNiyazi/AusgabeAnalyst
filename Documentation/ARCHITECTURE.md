# 🏗️ AusgabeAnalyst - Technical Architecture & Design

## 📋 Table of Contents
1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Component Details](#component-details)
4. [Data Flow](#data-flow)
5. [File Formats](#file-formats)
6. [Extending the Application](#extending-the-application)

---

## Overview

### Purpose
A personal finance tracking application that:
- Parses Volksbank PDF bank statements
- Categorizes transactions automatically
- Provides interactive visualizations
- Maintains historical data with duplicate prevention
- Exports analysis to Excel

### Technology Stack
- **Frontend**: Streamlit (Python web framework)
- **Data Processing**: Pandas (DataFrames and CSV operations)
- **PDF Parsing**: pdfplumber (Text extraction)
- **Visualization**: Plotly (Interactive charts)
- **Storage**: CSV files (Human-readable, portable)
- **Language**: Python 3.8+

### Design Philosophy
- **MVC-Inspired**: Separation of concerns (Model, View, Controller)
- **Modularity**: Each component has a single responsibility
- **Extensibility**: Easy to add new features
- **Maintainability**: Clean code with documentation
- **User-Friendly**: Intuitive interface for non-technical users

---

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                       │
│                         (Streamlit App)                      │
│                           app.py                             │
└────────────────┬────────────────────────────────────────────┘
                 │
                 │ Controls & Events
                 │
┌────────────────▼────────────────────────────────────────────┐
│                        CONTROLLER                            │
│                    ExpenseTrackerApp                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ File Upload  │  │ Data Export  │  │ Tab Routing  │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└────────────────┬────────────────────────────────────────────┘
                 │
                 │ Uses
                 │
┌────────────────▼────────────────────────────────────────────┐
│                          MODEL LAYER                         │
│  ┌────────────────┐  ┌────────────────┐  ┌──────────────┐  │
│  │  PDF Parser    │  │  Categorizer   │  │ DataManager  │  │
│  │ (pdf_parser)   │  │ (categorizer)  │  │(data_manager)│  │
│  └────────────────┘  └────────────────┘  └──────────────┘  │
└────────────────┬────────────────────────────────────────────┘
                 │
                 │ Reads/Writes
                 │
┌────────────────▼────────────────────────────────────────────┐
│                      DATA PERSISTENCE                        │
│              expenses_history.csv (Database)                 │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│                          VIEW LAYER                          │
│                      (Visualization)                         │
│  ┌────────────────┐  ┌────────────────┐  ┌──────────────┐  │
│  │ Timeline Chart │  │  Monthly Bars  │  │Category Pie  │  │
│  └────────────────┘  └────────────────┘  └──────────────┘  │
│                      (visualizer.py)                         │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│                      CONFIGURATION                           │
│                    categories.py                             │
│              (Category Keywords Mapping)                     │
└──────────────────────────────────────────────────────────────┘
```

### Directory Structure

```
expense_tracker/
│
├── app.py                          # Main application (Controller)
│   └── ExpenseTrackerApp class
│       ├── _render_sidebar()       # Upload & controls
│       ├── _render_overview_tab()  # Financial summary
│       ├── _render_monthly_tab()   # Monthly analysis
│       ├── _render_category_tab()  # Category breakdown
│       └── _render_history_tab()   # Transaction list
│
├── config/                         # Configuration
│   ├── __init__.py
│   └── categories.py               # Category keyword mappings
│       └── CATEGORY_KEYWORDS       # Dictionary of categories
│
├── src/                            # Model components
│   ├── __init__.py
│   │
│   ├── pdf_parser.py               # PDF extraction
│   │   └── VolksbankPDFParser
│   │       ├── parse_pdf()         # Main parsing method
│   │       ├── _extract_metadata()  # Account info
│   │       ├── _extract_transactions()
│   │       ├── _parse_date()       # Date conversion
│   │       ├── _parse_amount()     # Amount conversion
│   │       └── _clean_description()
│   │
│   ├── categorizer.py              # Transaction categorization
│   │   └── TransactionCategorizer
│   │       ├── categorize()        # Single transaction
│   │       ├── categorize_batch()  # Multiple transactions
│   │       └── add_keyword()       # Add custom keywords
│   │
│   ├── data_manager.py             # Data persistence
│   │   └── DataManager
│   │       ├── add_transactions()  # Add with deduplication
│   │       ├── load_all_transactions()
│   │       ├── get_summary_statistics()
│   │       ├── get_monthly_summary()
│   │       ├── get_category_summary()
│   │       └── export_to_excel()
│   │
│   └── visualizer.py               # Chart creation
│       └── ExpenseVisualizer
│           ├── create_monthly_bar_chart()
│           ├── create_category_pie_chart()
│           ├── create_timeline_chart()
│           └── create_income_expense_comparison()
│
├── data/                           # Data storage (auto-created)
│   └── expenses_history.csv        # Transaction database
│
├── tests/                          # Unit tests
│   └── test_expense_tracker.py
│
├── requirements.txt                # Python dependencies
├── README.md                       # User documentation
├── PYCHARM_SETUP.md               # PyCharm setup guide
└── .gitignore                      # Version control exclusions
```

---

## Component Details

### 1. PDF Parser (`pdf_parser.py`)

**Purpose**: Extract transaction data from Volksbank PDF statements

**Key Features**:
- Regex-based pattern matching for transaction lines
- German date format conversion (DD.MM. → YYYY-MM-DD)
- German number format parsing (1.234,56 → 1234.56)
- Debit/Credit type handling (S/H indicators)
- Multi-line description cleaning
- Metadata extraction (IBAN, balances, statement number)

**Input Format**:
```
DD.MM. DD.MM. Description PN:XXX Amount S/H
```

**Output Format**:
```python
{
    'transactions': [
        {
            'value_date': '2025-10-01',
            'booking_date': '2025-10-01',
            'description': 'ALDI SE + Co. KG',
            'amount': -2.60,  # Negative for expenses
            'type': 'Debit',
            'raw_description': 'Full original text...'
        }
    ],
    'metadata': {
        'iban': 'DE94XXXXXXXXXXXXXXXXXX',
        'statement_number': '6',
        'year': '2025',
        'old_balance': 26.71,
        'new_balance': 91.12
    }
}
```

### 2. Categorizer (`categorizer.py`)

**Purpose**: Automatically categorize transactions based on keywords

**Algorithm**:
1. Convert description to lowercase
2. Check against each category's keywords
3. Return first matching category
4. Default to "Other" if no match

**Category Matching**:
```python
# Example: "ALDI SAGT DANKE" → "Groceries"
'aldi' in 'aldi sagt danke'.lower() → True → Return "Groceries"
```

**Extensibility**:
- Add keywords via `add_keyword()` method
- Modify `config/categories.py` for permanent changes
- Custom keyword dictionaries can be passed to constructor

### 3. Data Manager (`data_manager.py`)

**Purpose**: Handle all data persistence and retrieval operations

**Duplicate Detection**:
```python
# Generate unique ID from key fields
unique_string = f"{date}_{amount}_{description}"
transaction_id = md5(unique_string).hexdigest()[:16]
```

**Storage Schema** (CSV):
| Column | Type | Description |
|--------|------|-------------|
| transaction_id | string | MD5 hash (16 chars) |
| value_date | datetime | Transaction value date |
| booking_date | datetime | Bank booking date |
| description | string | Cleaned description |
| amount | float | Amount (negative for expenses) |
| type | string | Credit or Debit |
| category | string | Assigned category |
| raw_description | string | Original PDF text |
| upload_date | datetime | When transaction was added |

**Query Methods**:
- Filter by date range
- Filter by category
- Aggregate by month
- Aggregate by category
- Calculate summary statistics

### 4. Visualizer (`visualizer.py`)

**Purpose**: Create interactive charts using Plotly

**Chart Types**:

1. **Monthly Bar Chart**: Grouped bars for income vs expenses
2. **Category Pie Chart**: Donut chart showing expense distribution
3. **Timeline Chart**: Line chart with cumulative balance
4. **Category Bar Chart**: Horizontal bars for top categories
5. **Trend Comparison**: Line chart comparing income/expense trends

**Color Scheme**:
- Income: Green (#2ecc71)
- Expense: Red (#e74c3c)
- Primary: Blue (#3498db)
- Secondary: Purple (#9b59b6)

---

## Data Flow

### Upload & Processing Flow

```
┌─────────────┐
│ User Uploads│
│     PDF     │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│  Save to Temp   │
│    Location     │
└──────┬──────────┘
       │
       ▼
┌──────────────────────┐
│   PDF Parser         │
│  - Extract text      │
│  - Parse transactions│
│  - Extract metadata  │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│   Categorizer        │
│  - Match keywords    │
│  - Assign categories │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│   Data Manager       │
│  - Generate IDs      │
│  - Check duplicates  │
│  - Append to CSV     │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│   Clean up temp file │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│  Notify user         │
│  Refresh UI          │
└──────────────────────┘
```

### Visualization Flow

```
┌─────────────┐
│ User selects│
│     Tab     │
└──────┬──────┘
       │
       ▼
┌──────────────────────┐
│   Data Manager       │
│  - Load from CSV     │
│  - Filter/Aggregate  │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│   Visualizer         │
│  - Create charts     │
│  - Apply styling     │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│   Streamlit          │
│  - Render charts     │
│  - Display tables    │
└──────────────────────┘
```

---

## File Formats

### Input: Volksbank PDF Statement

**Structure**:
```
Kontoauszug (Account Statement)
Header: Account info, IBAN, Statement number
Body: Transaction lines
Footer: Balance information
```

**Transaction Line Format**:
```
01.10. 01.10. ALDI SE + Co. KG PN:931 2,60 S
│      │      │                 │     │    │
│      │      │                 │     │    └─ Type (S=Debit, H=Credit)
│      │      │                 │     └────── Amount
│      │      │                 └──────────── Bank code
│      │      └────────────────────────────── Description
│      └───────────────────────────────────── Booking date
└──────────────────────────────────────────── Value date
```

### Output: CSV Database

**File**: `data/expenses_history.csv`

**Format**: Standard CSV with headers
```csv
transaction_id,value_date,booking_date,description,amount,type,category,raw_description,upload_date
a1b2c3d4e5f6g7h8,2025-10-01,2025-10-01,ALDI SE + Co. KG,-2.60,Debit,Groceries,"Full text...",2025-02-03 14:30:00
```

### Export: Excel Report

**File**: `expense_report_YYYYMMDD_HHMMSS.xlsx`

**Sheets**:
1. **All Transactions**: Complete transaction list
2. **Summary**: Key statistics
3. **Monthly**: Monthly breakdown
4. **Categories**: Category totals

---

## Extending the Application

### Adding New Categories

**Method 1**: Edit configuration file
```python
# config/categories.py
CATEGORY_KEYWORDS = {
    'Entertainment': [
        'netflix', 'spotify', 'cinema', 'steam'
    ],
    # ... existing categories
}
```

**Method 2**: Programmatically
```python
categorizer = TransactionCategorizer()
categorizer.add_keyword('Entertainment', 'netflix')
```

### Adding New Visualizations

**Step 1**: Create method in `visualizer.py`
```python
def create_custom_chart(self, data: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    # ... create chart
    return fig
```

**Step 2**: Use in app.py
```python
def _render_custom_tab(self):
    st.header("Custom Analysis")
    data = self.data_manager.load_all_transactions()
    fig = self.visualizer.create_custom_chart(data)
    st.plotly_chart(fig)
```

### Adding Database Support

**Replace CSV with SQLite**:

```python
# data_manager.py
import sqlite3

class DataManager:
    def __init__(self, db_path='expenses.db'):
        self.conn = sqlite3.connect(db_path)
        self._create_tables()
    
    def _create_tables(self):
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                transaction_id TEXT PRIMARY KEY,
                value_date DATE,
                amount REAL,
                category TEXT
            )
        ''')
```

### Adding Budget Tracking

**Step 1**: Define budgets in config
```python
# config/budgets.py
MONTHLY_BUDGETS = {
    'Groceries': 300.00,
    'Restaurants & Dining': 150.00,
    'Transportation': 100.00
}
```

**Step 2**: Add budget comparison view
```python
def compare_to_budget(self):
    actual = self.data_manager.get_category_summary()
    # Compare with budgets
    # Show over/under
```

### Supporting Multiple Bank Formats

**Create parser interface**:
```python
# src/parsers/base_parser.py
class BankStatementParser:
    def parse_pdf(self, pdf_path: str) -> Dict:
        raise NotImplementedError

# src/parsers/volksbank_parser.py
class VolksbankParser(BankStatementParser):
    # ... implementation

# src/parsers/sparkasse_parser.py
class SparkasseParser(BankStatementParser):
    # ... implementation
```

---

## Performance Considerations

### For Large Datasets (>10,000 transactions)

1. **Add Indexing**:
   ```python
   df.set_index('transaction_id', inplace=True)
   ```

2. **Use Date Filtering**:
   ```python
   # Only load recent data
   df = df[df['value_date'] >= '2024-01-01']
   ```

3. **Implement Pagination**:
   ```python
   # Show 100 transactions per page
   page_size = 100
   page = st.number_input('Page', 1, total_pages)
   ```

4. **Cache Computations**:
   ```python
   @st.cache_data
   def get_monthly_summary():
       # Expensive computation
   ```

---

## Security & Privacy

### Current Implementation
- ✅ Local storage only (no cloud)
- ✅ No authentication (single user)
- ✅ Plain CSV (human readable)
- ⚠️ No encryption

### Recommendations for Production
1. **Encrypt sensitive data**
2. **Add user authentication**
3. **Implement audit logging**
4. **Regular backups**
5. **Input validation**

---

## Future Enhancement Ideas

1. **Machine Learning**:
   - Predict future spending
   - Anomaly detection
   - Smart categorization

2. **Mobile App**:
   - React Native frontend
   - FastAPI backend
   - Cloud sync

3. **Integrations**:
   - Direct bank API connections
   - Google Sheets export
   - Telegram/Slack notifications

4. **Advanced Features**:
   - Multi-currency support
   - Investment tracking
   - Tax reporting
   - Split transactions
   - Recurring transaction detection

---

**Project created**: 03 February 2026
**Version**: 1.0.0
**Maintainer**: Abdur Rehman Niyazi