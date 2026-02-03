# 🚀 Quick Start Guide for PyCharm

This guide will help you get the AusgabeAnalyst running in PyCharm in 5 minutes.

## Step-by-Step Setup

### 1. Open Project in PyCharm

1. Launch PyCharm
2. Click **"Open"** on the welcome screen (or `File → Open`)
3. Navigate to the `expense_tracker` folder (newly created in your system)
4. Click **"OK"**

### 2. Configure Python Interpreter

PyCharm should automatically detect that you need to set up an interpreter.

**Method 1: Automatic Setup**
- Look for a yellow banner at the top saying "No Python interpreter configured"
- Click **"Configure Python Interpreter"**
- Select **"Add New Interpreter"** → **"Add Local Interpreter"**
- Choose **"Virtualenv"**
- Click **"OK"**

**Method 2: Manual Setup**
1. Press `Ctrl+Alt+S` (Windows/Linux) or `Cmd+,` (macOS) to open Settings
2. Navigate to: **Project: expense_tracker** → **Python Interpreter**
3. Click the ⚙️ gear icon → **"Add"**
4. Select **"Virtualenv Environment"**
5. Choose **"New environment"**
6. Location: Leave default (`venv` in project folder)
7. Base interpreter: Select your Python 3.8+ installation
8. Check ✅ **"Make available to all projects"** (optional)
9. Click **"OK"**

### 3. Install Dependencies

**Method 1: Automatic (Recommended)**
1. Open `requirements.txt` in PyCharm
2. Look for the yellow banner: "Package requirements are not satisfied"
3. Click **"Install requirements"**
4. Wait for installation to complete

**Method 2: Terminal**
1. Open PyCharm's terminal: `Alt+F12` (Windows/Linux) or `Fn+Alt+F12` (macOS)
2. Verify virtual environment is activated (you should see `(venv)` in the prompt)
3. Run:
   ```bash
   pip install -r requirements.txt
   ```

### 4. Create Run Configuration

**Option A: Quick Run**
1. Right-click on `app.py` in the Project Explorer
2. Select **"Run 'app'"**
3. This will create a temporary configuration

**Option B: Permanent Configuration**
1. Click **"Run"** → **"Edit Configurations..."**
2. Click the **+** button → **"Python"**
3. Configure:
   - **Name**: `AusgabeAnalyst`
   - **Module name** (not Script path!): `streamlit`
   - **Parameters**: `run app.py`
   - **Python interpreter**: Select the venv you created
   - **Working directory**: Leave as project root
4. Click **"OK"**
5. Now you can run the app by clicking the green ▶️ play button

### 5. Run the Application

1. Click the **green play button** ▶️ in the top-right corner
2. Or press `Shift+F10` (Windows/Linux) or `Ctrl+R` (macOS)
3. The terminal will show:
   ```
   You can now view your Streamlit app in your browser.
   
   Local URL: http://localhost:8501
   Network URL: http://192.168.x.x:8501
   ```
4. PyCharm will automatically open the browser, or manually navigate to `http://localhost:8501`

## Project Structure in PyCharm

```
expense_tracker/
├── 📄 app.py                    # Main application - Run this!
├── 📄 requirements.txt          # Dependencies
├── 📄 README.md                 # Full documentation
├── 📄 PYCHARM_SETUP.md         # This file
├── 📁 config/
│   └── 📄 categories.py        # Edit to customize categories
├── 📁 src/                      # Core modules
│   ├── 📄 pdf_parser.py        # PDF extraction logic
│   ├── 📄 categorizer.py       # Transaction categorization
│   ├── 📄 data_manager.py      # Data storage & retrieval
│   └── 📄 visualizer.py        # Chart creation
├── 📁 data/                     # Created automatically
│   └── 📄 expenses_history.csv # Your transaction database
└── 📁 tests/                    # For unit tests (optional)
```

## PyCharm Tips & Tricks

### Terminal Shortcuts
- **Open Terminal**: `Alt+F12` (Windows/Linux) or `Fn+Alt+F12` (macOS)
- **New Terminal Tab**: Click **+** in terminal panel
- **Close Terminal**: `Ctrl+F4` (Windows/Linux) or `Cmd+W` (macOS)

### Running the App
- **Run**: `Shift+F10` (Windows/Linux) or `Ctrl+R` (macOS)
- **Stop**: `Ctrl+F2` (Windows/Linux) or `Cmd+F2` (macOS)
- **Rerun**: Click the green ▶️ again (Streamlit will auto-reload on file changes)

### Code Navigation
- **Find File**: `Ctrl+Shift+N` (Windows/Linux) or `Cmd+Shift+O` (macOS)
- **Find in Files**: `Ctrl+Shift+F` (Windows/Linux) or `Cmd+Shift+F` (macOS)
- **Go to Definition**: `Ctrl+B` (Windows/Linux) or `Cmd+B` (macOS)

### Useful PyCharm Features

1. **Code Completion**: Press `Ctrl+Space` for suggestions
2. **Quick Documentation**: Hover over any function/class with `Ctrl` pressed
3. **Rename**: `Shift+F6` to rename variables/functions everywhere
4. **Reformat Code**: `Ctrl+Alt+L` (Windows/Linux) or `Cmd+Alt+L` (macOS)

## First-Time Usage

### 1. Test the App
After starting the app:
1. You should see the AusgabeAnalyst interface
2. Sidebar shows "Quick Stats" (will be 0 initially)
3. Main area has 4 tabs: Overview, Monthly Analysis, Category Analysis, Transaction History

### 2. Upload Your First Statement
1. Click **"Browse files"** in the sidebar
2. Select a Volksbank PDF statement
3. Click **"Process PDF"**
4. Watch as transactions appear in the visualizations!

### 3. Explore the Data
- Check the **Overview** tab for balance timeline
- View **Monthly Analysis** for income vs expenses
- Examine **Category Analysis** to see spending breakdown
- Browse **Transaction History** to see all transactions

## Troubleshooting

### Problem: "No module named 'streamlit'"
**Solution**: Dependencies not installed
```bash
# In PyCharm terminal
pip install -r requirements.txt
```

### Problem: Virtual environment not activating
**Solution**: Manually activate
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### Problem: "streamlit: command not found"
**Solution**: Ensure you're using the project's virtual environment
1. Check PyCharm's Python interpreter settings
2. Verify the terminal shows `(venv)` in the prompt
3. Reinstall: `pip install streamlit`

### Problem: App opens but shows errors
**Solution**: Check the PyCharm console/terminal for specific error messages
- Most common: Missing dependencies → reinstall requirements
- PDF parsing error → ensure PDF is valid Volksbank format

### Problem: Changes not reflecting in app
**Solution**: Streamlit auto-reloads on file save
- Save file: `Ctrl+S` (Windows/Linux) or `Cmd+S` (macOS)
- If auto-reload doesn't work, click "Rerun" in the browser
- Or stop and restart the app in PyCharm

## Development Workflow

### Making Changes

1. **Edit Code**: Modify any `.py` file
2. **Save**: `Ctrl+S` or `Cmd+S`
3. **Auto-Reload**: Streamlit detects changes and shows "Rerun" button
4. **Test**: Click "Rerun" or let it auto-reload

### Adding New Categories

1. Open `config/categories.py`
2. Add your keywords:
   ```python
   'Entertainment': [
       'netflix', 'spotify', 'cinema', 'theater'
   ],
   ```
3. Save the file
4. Restart the app

### Debugging

1. **Print Statements**: Add `print()` or `st.write()` to see values
2. **PyCharm Debugger**: 
   - Set breakpoints: Click in the left margin of the code
   - Run in Debug mode: `Shift+F9` (Windows/Linux) or `Ctrl+D` (macOS)
3. **Streamlit Debugging**: Use `st.write()` to display variables in the UI

## Best Practices

### Version Control (Optional)
If using Git:
1. Create `.gitignore`:
   ```
   venv/
   data/
   *.pyc
   __pycache__/
   .idea/
   *.xlsx
   temp_*.pdf
   ```
2. Initialize Git: `git init`
3. Commit: `git add .` → `git commit -m "Initial commit"`

### Data Backup
- Regularly backup `data/expenses_history.csv`
- Use the "Export to Excel" feature for monthly archives

### Performance
- For large datasets (1000+ transactions), consider adding pagination
- Clear browser cache if charts seem slow

## Next Steps

1. ✅ Upload your first bank statement
2. ✅ Customize categories for your needs
3. ✅ Set up monthly upload routine
4. ✅ Explore the visualizations
5. ✅ Export reports for record-keeping

## Quick Reference Card

| Task | Shortcut |
|------|----------|
| Run App | `Shift+F10` / `Ctrl+R` |
| Stop App | `Ctrl+F2` / `Cmd+F2` |
| Open Terminal | `Alt+F12` / `Fn+Alt+F12` |
| Save All | `Ctrl+S` / `Cmd+S` |
| Find File | `Ctrl+Shift+N` / `Cmd+Shift+O` |
| Settings | `Ctrl+Alt+S` / `Cmd+,` |

---

**You're all set! 🎉 Start tracking your expenses!**

For more details, see the main [README.md](../README.md)