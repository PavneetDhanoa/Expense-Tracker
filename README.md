# Expense Tracker (Python)

A command-line based expense tracking application built using Python. The program lets you record income and expenses, store everything in a CSV file, and visualize your spending with charts. This project shows practical use of Python for data handling, file I/O, input validation, and basic data visualization.

---

## Features

- Add income and expense entries with category, date, amount, and an optional description
- Input validation — catches bad dates, blank fields, invalid types, and negative amounts before saving
- View all transactions in a clean numbered table with +/- signs
- Financial summary showing total income, total expenses, and net balance
- Monthly net cash flow bar chart (green = surplus, red = deficit) with labeled bars
- Expense breakdown by category using a pie chart (highlights the biggest category)
- Delete any entry by its number, with a confirmation step before removing it
- Persistent data storage using CSV files
- Auto-migration support — if you have an older version of the CSV (3-column format), it automatically converts it to the new 5-column format on startup

---

## Technologies Used

- Python
- CSV file handling
- Matplotlib (data visualization)
- `datetime` module for date parsing and validation
- Basic data processing and control flow

---

## How to Run

1. Clone the repository:

```bash
git clone https://github.com/PavneetDhanoa/Expense-Tracker.git
cd Expense-Tracker
```

2. Install the required library:

```bash
pip install matplotlib
```

3. Run the program:

```bash
python Expense.py
```

---

## CSV Format

The data is stored in `expenses.csv` with the following columns:

| Column | Description |
|---|---|
| Date | Format: YYYY-MM-DD |
| Category | e.g. Food, Rent, Salary |
| Type | Either `Income` or `Expense` |
| Amount | Positive number |
| Description | Optional note |

> If you have a CSV from an older version of this project (with just Date, Category, Amount), the program will automatically migrate it to the new format when you run it.

---
