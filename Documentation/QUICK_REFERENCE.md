# 📝 Quick Reference Card

## 🚀 Getting Started (5 Minutes)

```bash
# 1. Navigate to project
cd expense_tracker

# 2. Create virtual environment
python -m venv venv

# 3. Activate (Windows)
venv\Scripts\activate
# OR Activate (macOS/Linux)
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run app
streamlit run app.py
```

---

## 📁 Project Structure Quick View

```
expense_tracker/
├── app.py                  # 👈 RUN THIS
├── requirements.txt        # Dependencies
├── config/categories.py    # 👈 EDIT CATEGORIES HERE
├── src/                    # Core logic (don't edit unless extending)
│   ├── pdf_parser.py
│   ├── categorizer.py
│   ├── data_manager.py
│   └── visualizer.py
└── data/                   # 👈 YOUR DATA STORED HERE
    └── expenses_history.csv
```

---

## ⚡ Common Tasks

### Upload a Statement
1. Click "Browse files" in sidebar
2. Select Volksbank PDF
3. Click "Process PDF"
4. Wait for confirmation

### View Your Data
- **Overview Tab**: See total income, expenses, savings
- **Monthly Tab**: Compare months
- **Category Tab**: See where money goes
- **History Tab**: Browse all transactions

### Export Data
- Click "Export to Excel" in sidebar
- Download the generated file
- Open in Excel/LibreOffice

### Filter Transactions
1. Go to "Transaction History" tab
2. Use dropdowns to filter:
   - Category
   - Type (Credit/Debit)
   - Date range
3. Download filtered CSV if needed

---

## 🔧 Customization

### Add a Category
Edit `config/categories.py`:
```python
CATEGORY_KEYWORDS = {
    'Your New Category': [
        'keyword1', 'keyword2', 'store_name'
    ],
}
```

### Change Colors
Edit `src/visualizer.py`:
```python
self.color_scheme = {
    'income': '#2ecc71',    # Green
    'expense': '#e74c3c',   # Red
    'primary': '#3498db',   # Blue
    'secondary': '#9b59b6'  # Purple
}
```

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| Charts are empty | Upload a PDF first |
| PDF parsing fails | Ensure it's a Volksbank PDF |
| Streamlit won't start | Activate virtual environment |
| Changes not showing | Save file, then click "Rerun" in browser |

---

## 💾 Backup Your Data

```bash
# Backup CSV
cp data/expenses_history.csv backup_$(date +%Y%m%d).csv

# OR use Excel export in app
```

---

## 🔑 Keyboard Shortcuts (PyCharm)

| Action | Windows/Linux | macOS |
|--------|---------------|-------|
| Run App | `Shift+F10` | `Ctrl+R` |
| Stop App | `Ctrl+F2` | `Cmd+F2` |
| Terminal | `Alt+F12` | `Fn+Alt+F12` |
| Save All | `Ctrl+S` | `Cmd+S` |
| Find File | `Ctrl+Shift+N` | `Cmd+Shift+O` |

---

## 📊 Understanding Your Data

### Transaction Types
- **Credit (H)**: Money in (income, refunds) → Positive amount
- **Debit (S)**: Money out (expenses) → Negative amount

### Categories
- **Income**: Salary, payments received
- **Groceries**: Supermarkets (ALDI, LIDL, etc.)
- **Restaurants**: Dining out
- **Personal Care**: Pharmacy, drugstore
- **Other**: Uncategorized (review these!)

### Key Metrics
- **Net Savings** = Total Income - Total Expenses
- **Current Balance** = Sum of all transactions

---

## 🎯 Best Practices

1. **Upload monthly** - Keep data current
2. **Review "Other"** - Add missing categories
3. **Export regularly** - Backup as Excel monthly
4. **Check duplicates** - App prevents them automatically
5. **Monitor trends** - Use Monthly tab

---

## 📞 Need Help?

1. Check `README.md` for full documentation
2. See `PYCHARM_SETUP.md` for IDE setup
3. Review `ARCHITECTURE.md` for technical details
4. Check PyCharm console for error messages

---

## 🔄 Update Dependencies

```bash
# Update all packages
pip install -r requirements.txt --upgrade

# Update specific package
pip install streamlit --upgrade
```

---

## 📈 Sample Workflow

```
Daily: Upload new statements when received
↓
Weekly: Review uncategorized transactions
↓
Monthly: Export to Excel for records
↓
Quarterly: Analyze spending trends
↓
Yearly: Review annual summary
```

---

## 🎨 Color Coding (in UI)

- 🟢 **Green** → Income/Positive balance
- 🔴 **Red** → Expenses/Negative balance
- 🔵 **Blue** → Primary actions/charts
- 🟣 **Purple** → Secondary elements

---

## ⚙️ Configuration Files

| File | Purpose | Edit? |
|------|---------|-------|
| `config/categories.py` | Category keywords | ✅ Yes |
| `requirements.txt` | Dependencies | ⚠️ Rarely |
| `.gitignore` | Version control | ⚠️ If using Git |
| Other `.py` files | Core logic | ❌ Advanced only |

---

## 📥 Supported File Format

**Input**: Volksbank Mittelhessen PDF statements only

**Format recognized**:
```
DD.MM. DD.MM. Description PN:XXX Amount S/H
```

**Example**:
```
01.10. 01.10. ALDI SAGT DANKE PN:931 2,60 S
```

---

## 🚦 Status Indicators

When uploading:
- ⏳ "Processing PDF..." → Working
- ✅ "Processing complete!" → Success
- ❌ "Error processing file" → Check file format

---

## 💡 Pro Tips

1. Keep original PDFs in a folder
2. Name PDFs clearly: `2025-10-volksbank.pdf`
3. Upload newest statements first
4. Review "Other" category monthly
5. Use Excel export for tax purposes
6. Set up monthly reminder to upload

---

## 🔐 Data Privacy

✅ **Your data stays on your computer**
✅ **No internet required** (except for Streamlit UI)
✅ **No cloud sync**
✅ **CSV is human-readable**

⚠️ **Recommendation**: Backup `data/` folder regularly

---

**Version**: 1.0.0
**Last Updated**: 03 February 2026

---

**Quick Start**: `streamlit run app.py`
**Quick Stop**: Press `Ctrl+C` in terminal