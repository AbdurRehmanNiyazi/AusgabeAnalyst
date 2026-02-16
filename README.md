# 💰 AusgabeAnalyst

A comprehensive expense tracking application built with Streamlit and Pandas for analyzing Volksbank bank statements.

## 📋 Features

- **PDF Parsing**: Automatically extract transactions from Volksbank PDF statements
- **Smart Categorization**: Automatic transaction categorization based on keywords
- **Duplicate Detection**: Prevents duplicate entries when uploading multiple statements
- **Interactive Visualizations**: 
  - Monthly income vs expenses charts
  - Category distribution pie charts
  - Balance timeline
  - Trend analysis
- **Data Persistence**: All transactions stored in CSV with history
- **Export Capabilities**: Export to Excel with summary sheets
- **Filtering**: Filter transactions by date, category, and type

## 🏗️ Architecture

This project follows an MVC-inspired architecture:

```
expense_tracker/
├── app.py                      # Main Streamlit application (Controller)
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── config/
│   └── categories.py          # Category mapping configuration
├── src/                        # Model components
│   ├── pdf_parser.py          # PDF parsing logic
│   ├── categorizer.py         # Transaction categorization
│   ├── data_manager.py        # Data persistence and retrieval
│   └── visualizer.py          # Visualization creation (View helper)
├── data/                       # Data storage
│   └── expenses_history.csv   # Transaction database (auto-created)
└── tests/                      # Unit tests (optional)
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- PyCharm IDE (recommended) or any Python IDE
- Pip package manager

### Installation Steps

#### 1. Clone or Download the Project

If you have the project folder, skip to step 2. Otherwise:

```bash
# Create project directory
mkdir expense_tracker
cd expense_tracker
```

#### 2. Set Up PyCharm Project

1. Open PyCharm
2. Click `File` → `Open` → Select the `expense_tracker` folder
3. PyCharm will detect the project structure

#### 3. Create Virtual Environment

In PyCharm:
1. Go to `File` → `Settings` (Windows/Linux) or `PyCharm` → `Preferences` (macOS)
2. Navigate to `Project: expense_tracker` → `Python Interpreter`
3. Click the gear icon ⚙️ → `Add`
4. Select `Virtualenv Environment` → `New environment`
5. Choose base interpreter (Python 3.8+)
6. Click `OK`

Or via terminal in PyCharm:
```bash
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

#### 4. Install Dependencies

In PyCharm terminal:
```bash
pip install -r requirements.txt
```

Or use PyCharm's built-in installer:
1. Open `requirements.txt`
2. Click the yellow banner at the top: "Install requirements"

#### 5. Run the Application

In PyCharm terminal:
```bash
streamlit run app.py
```
Note: When you run streamlit run main.py,
it defaults to localhost. To allow your Android phone to connect,
you must bind it to your local network interface using the --server.address flag.

```bash
streamlit run main.py --server.address 0.0.0.0
```
Or create a Run Configuration:
1. Click `Run` → `Edit Configurations`
2. Click `+` → `Python`
3. Name: `AusgabeAnalyst`
4. Module name: `streamlit`
5. Parameters: `run app.py`
6. Click `OK`
7. Click the green play button ▶️

The app will open in your default browser at `http://localhost:8501`

## 📖 Usage Guide

### Uploading Bank Statements

1. Click **"Browse files"** in the sidebar
2. Select your Volksbank PDF statement
3. Click **"Process PDF"**
4. The app will:
   - Extract all transactions
   - Categorize them automatically
   - Add them to your history (skipping duplicates)
   - Update all visualizations

### Navigating Tabs

#### Overview Tab 📊
- View total income, expenses, and net savings
- See your balance timeline chart
- Get a quick financial snapshot

#### Monthly Analysis Tab 📅
- Compare income vs expenses by month
- View trend lines
- Analyze monthly summary table

#### Category Analysis Tab 📂
- See expense distribution pie chart
- View top spending categories
- Examine detailed category breakdown

#### Transaction History Tab 📋
- Browse all transactions
- Filter by category, type, or date range
- Download filtered data as CSV

### Customizing Categories

Edit `config/categories.py` to add or modify categories:

```python
CATEGORY_KEYWORDS = {
    'Your Category': [
        'keyword1', 'keyword2', 'store_name'
    ],
    # Add more categories...
}
```

### Exporting Data

Click **"Export to Excel"** in the sidebar to get:
- All transactions sheet
- Summary statistics
- Monthly breakdown
- Category analysis

## 🔧 Configuration

### Data Storage

Transactions are stored in `data/expenses_history.csv` with the following columns:
- `transaction_id`: Unique identifier (MD5 hash)
- `value_date`: Transaction value date
- `booking_date`: Bank booking date
- `description`: Cleaned description
- `amount`: Transaction amount (negative for expenses, positive for income)
- `type`: Credit or Debit
- `category`: Assigned category
- `raw_description`: Original description from PDF
- `upload_date`: When the transaction was added

### Duplicate Detection

Duplicates are identified by combining:
- Value date
- Amount
- Description

This generates a unique MD5 hash. Transactions with the same hash are skipped.

## 🧪 Testing

Create test files in the `tests/` directory:

```bash
# Run tests (if you create them)
pytest tests/
```

Example test structure:
```python
# tests/test_parser.py
import unittest
from src.pdf_parser import VolksbankPDFParser

class TestPDFParser(unittest.TestCase):
    def test_date_parsing(self):
        parser = VolksbankPDFParser()
        result = parser._parse_date("01.10.", "2025")
        self.assertEqual(result, "2025-10-01")
```

## 📊 Supported Transaction Format

The parser expects Volksbank Mittelhessen PDF statements with this format:

```
DD.MM. DD.MM. Description PN:XXX Amount S/H
```

Example:
```
01.10. 01.10. ALDI SE + Co. KG PN:931 2,60 S
```

Where:
- First date: Value date
- Second date: Booking date
- Description: Transaction description (may be multi-line)
- PN:XXX: Internal bank code
- Amount: German number format (e.g., 1.234,56)
- S/H: S for debit (Soll), H for credit (Haben)

## 🐛 Troubleshooting

### PDF Parsing Errors

**Problem**: "Error parsing PDF"
**Solution**: 
- Ensure the PDF is from Volksbank Mittelhessen
- Check that the PDF is not password-protected
- Verify the PDF contains transaction data

### Module Import Errors

**Problem**: `ModuleNotFoundError`
**Solution**:
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Streamlit Not Starting

**Problem**: Streamlit command not found
**Solution**:
```bash
# Ensure virtual environment is activated
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Verify installation
pip list | grep streamlit
```

### Data Not Showing

**Problem**: Charts are empty
**Solution**:
- Upload at least one PDF statement
- Check that `data/expenses_history.csv` exists and contains data
- Restart the Streamlit app

## 🔐 Privacy & Security

- **Local Storage**: All data is stored locally on your machine
- **No Cloud**: No data is sent to external servers
- **CSV Format**: Data is in plain CSV for transparency
- **Manual Backups**: Recommended to backup `data/expenses_history.csv` regularly

## 🚀 Future Enhancements

Potential features to add:
- [ ] Budget tracking and alerts
- [ ] Recurring transaction detection
- [ ] Multi-currency support
- [ ] Custom category rules editor in UI
- [ ] Predictive spending analysis
- [ ] Mobile-responsive design improvements
- [ ] Database support (SQLite/PostgreSQL)
- [ ] Multi-user support with authentication

## 🤝 Contributing

To extend the application:

1. Add new categories in `config/categories.py`
2. Create new visualizations in `src/visualizer.py`
3. Add new analysis methods in `src/data_manager.py`
4. Extend the UI in `app.py`

## 📝 License

This project is for personal use. Feel free to modify and extend as needed.

## 💡 Tips

- **Regular Uploads**: Upload statements monthly to keep data current
- **Category Review**: Periodically review uncategorized transactions (category: "Other")
- **Export Backups**: Export to Excel monthly for backup
- **Custom Categories**: Tailor categories to your spending habits

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review PyCharm console for error messages
3. Verify all dependencies are installed correctly

---

**Happy Tracking! 💰📊**


## Version History

### **v1.0.1 (Current Version, Dated: 16 February 2026)

    + [Logic] Prioritized vendor keywords (Aldi, Lidl, etc.) over generic banking labels.
    + [Parser] Implemented multi-line block detection for PDF vendor names.
    + [UI] Fixed st.rerun() bug that caused "RerunData" error messages.
    + [Data] Added "Delete All Data" feature to reset the local database.
    + [Fix] Resolved AttributeError by fixing method indentation in data_manager.py.

