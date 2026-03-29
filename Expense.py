# expense_tracker.py
# Personal Expense Tracker with Data Visualization
# Student Portfolio Project

import csv
import datetime
import os
import matplotlib.pyplot as plt

CSV_FILE = "expenses.csv"
FIELDNAMES = ["Date", "Category", "Type", "Amount", "Description"]


# ─────────────────────────────────────────────
#  CSV SETUP
# ─────────────────────────────────────────────

def initialize_csv():
    """Create the CSV file with headers if it does not exist."""
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writeheader()


# ─────────────────────────────────────────────
#  DATA LOADING
# ─────────────────────────────────────────────

def load_data():
    """
    Load all rows from the CSV into a list of dicts.
    Skips corrupted or incomplete rows with a warning.
    """
    data = []
    with open(CSV_FILE, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for i, row in enumerate(reader, start=1):
            try:
                # Validate required fields exist and are not blank
                if not row.get("Date") or not row.get("Category") or \
                   not row.get("Type") or not row.get("Amount"):
                    raise ValueError("Missing required field(s)")

                entry = {
                    "Date":        datetime.datetime.strptime(row["Date"].strip(), "%Y-%m-%d"),
                    "Category":    row["Category"].strip().title(),
                    "Type":        row["Type"].strip().capitalize(),
                    "Amount":      float(row["Amount"].strip()),
                    "Description": row.get("Description", "").strip()
                }

                if entry["Type"] not in ("Income", "Expense"):
                    raise ValueError(f"Invalid type: {row['Type']}")
                if entry["Amount"] < 0:
                    raise ValueError("Amount must be positive in the new format")

                data.append(entry)

            except (ValueError, KeyError) as e:
                print(f"  [Warning] Skipping row {i}: {e}")

    return data


# ─────────────────────────────────────────────
#  ADD ENTRY
# ─────────────────────────────────────────────

def add_entry():
    """Prompt the user for all fields and append a new row to the CSV."""
    print("\n--- Add New Entry ---")

    # Date
    while True:
        date_str = input("Date (YYYY-MM-DD): ").strip()
        try:
            datetime.datetime.strptime(date_str, "%Y-%m-%d")
            break
        except ValueError:
            print("  Invalid date. Please use the format YYYY-MM-DD (e.g. 2025-06-15).")

    # Category
    while True:
        category = input("Category (e.g. Food, Rent, Salary): ").strip().title()
        if category:
            break
        print("  Category cannot be blank.")

    # Type
    while True:
        entry_type = input("Type (Income / Expense): ").strip().capitalize()
        if entry_type in ("Income", "Expense"):
            break
        print("  Please enter either 'Income' or 'Expense'.")

    # Amount
    while True:
        amount_str = input("Amount (positive number): ").strip()
        try:
            amount = float(amount_str)
            if amount <= 0:
                raise ValueError
            break
        except ValueError:
            print("  Invalid amount. Please enter a positive number (e.g. 49.99).")

    # Description (optional)
    description = input("Description (optional, press Enter to skip): ").strip()

    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writerow({
            "Date":        date_str,
            "Category":    category,
            "Type":        entry_type,
            "Amount":      f"{amount:.2f}",
            "Description": description
        })

    print(f"  Entry added: {date_str} | {category} | {entry_type} | ${amount:.2f}")


# ─────────────────────────────────────────────
#  VIEW ALL ENTRIES
# ─────────────────────────────────────────────

def view_entries():
    """Print all transactions in a numbered table."""
    data = load_data()
    if not data:
        print("\n  No entries found.")
        return

    print("\n--- All Transactions ---")
    print(f"{'#':<4} {'Date':<12} {'Category':<16} {'Type':<10} {'Amount':>10}  {'Description'}")
    print("-" * 70)

    for i, entry in enumerate(data, start=1):
        date_str = entry["Date"].strftime("%Y-%m-%d")
        sign = "+" if entry["Type"] == "Income" else "-"
        print(
            f"{i:<4} {date_str:<12} {entry['Category']:<16} {entry['Type']:<10} "
            f"{sign}${entry['Amount']:>8.2f}  {entry['Description']}"
        )

    print("-" * 70)
    print(f"  Total rows: {len(data)}")


# ─────────────────────────────────────────────
#  FINANCIAL SUMMARY
# ─────────────────────────────────────────────

def show_summary():
    """Print total income, total expenses, and net balance."""
    data = load_data()
    if not data:
        print("\n  No data available for summary.")
        return

    total_income   = sum(e["Amount"] for e in data if e["Type"] == "Income")
    total_expenses = sum(e["Amount"] for e in data if e["Type"] == "Expense")
    net_balance    = total_income - total_expenses

    print("\n--- Financial Summary ---")
    print(f"  Total Income:    ${total_income:>10.2f}")
    print(f"  Total Expenses:  ${total_expenses:>10.2f}")
    print(f"  {'─' * 28}")
    balance_label = "Net Balance:    "
    sign = "+" if net_balance >= 0 else ""
    print(f"  {balance_label} {sign}${net_balance:.2f}")


# ─────────────────────────────────────────────
#  MONTHLY NET CASH FLOW CHART
# ─────────────────────────────────────────────

def show_monthly_chart():
    """
    Bar chart showing net cash flow (income minus expenses) per month.
    Green bars = surplus, red bars = deficit.
    """
    data = load_data()
    if not data:
        print("\n  No data available to chart.")
        return

    # Aggregate income and expenses per month
    monthly_income   = {}
    monthly_expenses = {}

    for entry in data:
        month = entry["Date"].strftime("%Y-%m")
        if entry["Type"] == "Income":
            monthly_income[month]   = monthly_income.get(month, 0)   + entry["Amount"]
        else:
            monthly_expenses[month] = monthly_expenses.get(month, 0) + entry["Amount"]

    # Build a sorted list of all months that appear in the data
    all_months = sorted(set(list(monthly_income.keys()) + list(monthly_expenses.keys())))

    net_flow = [
        monthly_income.get(m, 0) - monthly_expenses.get(m, 0)
        for m in all_months
    ]

    # Color each bar based on surplus/deficit
    colors = ["steelblue" if v >= 0 else "tomato" for v in net_flow]

    plt.figure(figsize=(12, 5))
    bars = plt.bar(all_months, net_flow, color=colors, edgecolor="white")
    plt.axhline(0, color="black", linewidth=0.8, linestyle="--")
    plt.title("Monthly Net Cash Flow (Income − Expenses)", fontsize=14)
    plt.xlabel("Month")
    plt.ylabel("Amount ($)")
    plt.xticks(rotation=45, ha="right")

    # Label each bar with its value
    for bar, val in zip(bars, net_flow):
        y_pos = bar.get_height() + 10 if val >= 0 else bar.get_height() - 50
        plt.text(bar.get_x() + bar.get_width() / 2, y_pos,
                 f"${val:,.0f}", ha="center", va="bottom", fontsize=8)

    plt.tight_layout()
    plt.show()


# ─────────────────────────────────────────────
#  CATEGORY SPENDING PIE CHART
# ─────────────────────────────────────────────

def show_category_chart():
    """Pie chart showing expense breakdown by category."""
    data = load_data()
    expenses = [e for e in data if e["Type"] == "Expense"]

    if not expenses:
        print("\n  No expense data available to chart.")
        return

    # Sum expenses per category
    categories = {}
    for entry in expenses:
        categories[entry["Category"]] = categories.get(entry["Category"], 0) + entry["Amount"]

    labels = list(categories.keys())
    sizes  = list(categories.values())

    # Explode the largest slice slightly for emphasis
    max_index = sizes.index(max(sizes))
    explode   = [0.05 if i == max_index else 0 for i in range(len(sizes))]

    plt.figure(figsize=(8, 7))
    wedges, texts, autotexts = plt.pie(
        sizes,
        labels=labels,
        autopct="%1.1f%%",
        startangle=140,
        explode=explode,
        pctdistance=0.82
    )
    for text in autotexts:
        text.set_fontsize(9)

    plt.title("Expense Breakdown by Category", fontsize=14)
    plt.axis("equal")
    plt.tight_layout()
    plt.show()


# ─────────────────────────────────────────────
#  DELETE ENTRY
# ─────────────────────────────────────────────

def delete_entry():
    """Let the user delete a transaction by its index number."""
    data = load_data()
    if not data:
        print("\n  No entries to delete.")
        return

    view_entries()

    while True:
        choice = input("\nEnter the # of the entry to delete (or 0 to cancel): ").strip()
        try:
            index = int(choice)
        except ValueError:
            print("  Please enter a valid number.")
            continue

        if index == 0:
            print("  Deletion cancelled.")
            return

        if 1 <= index <= len(data):
            entry = data[index - 1]
            confirm = input(
                f"  Delete entry {index}: {entry['Date'].strftime('%Y-%m-%d')} | "
                f"{entry['Category']} | {entry['Type']} | ${entry['Amount']:.2f}? (yes/no): "
            ).strip().lower()
            if confirm == "yes":
                data.pop(index - 1)
                _rewrite_csv(data)
                print("  Entry deleted successfully.")
            else:
                print("  Deletion cancelled.")
            return
        else:
            print(f"  Please enter a number between 1 and {len(data)}, or 0 to cancel.")


def _rewrite_csv(data):
    """Overwrite the CSV file with the current data list (used after deletion)."""
    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        for entry in data:
            writer.writerow({
                "Date":        entry["Date"].strftime("%Y-%m-%d"),
                "Category":    entry["Category"],
                "Type":        entry["Type"],
                "Amount":      f"{entry['Amount']:.2f}",
                "Description": entry["Description"]
            })


# ─────────────────────────────────────────────
#  MENU & MAIN LOOP
# ─────────────────────────────────────────────

def print_menu():
    print("\n╔══════════════════════════════╗")
    print("║      EXPENSE TRACKER         ║")
    print("╠══════════════════════════════╣")
    print("║  1. Add Entry                ║")
    print("║  2. View All Entries         ║")
    print("║  3. Show Financial Summary   ║")
    print("║  4. Show Monthly Chart       ║")
    print("║  5. Show Category Chart      ║")
    print("║  6. Delete Entry             ║")
    print("║  7. Exit                     ║")
    print("╚══════════════════════════════╝")


def main():
    initialize_csv()

    # Migrate old-format CSV (3 columns) to new format (5 columns) if needed
    _migrate_if_needed()

    while True:
        print_menu()
        choice = input("Choose an option (1–7): ").strip()

        if choice == "1":
            add_entry()
        elif choice == "2":
            view_entries()
        elif choice == "3":
            show_summary()
        elif choice == "4":
            show_monthly_chart()
        elif choice == "5":
            show_category_chart()
        elif choice == "6":
            delete_entry()
        elif choice == "7":
            print("\n  Goodbye!\n")
            break
        else:
            print("  Invalid choice. Please enter a number from 1 to 7.")


# ─────────────────────────────────────────────
#  MIGRATION HELPER
# ─────────────────────────────────────────────

def _migrate_if_needed():
    """
    If the CSV was created with the old 3-column format (Date, Category, Amount),
    convert it to the new 5-column format automatically.
    Old format used negative amounts for expenses and positive for income.
    """
    if not os.path.exists(CSV_FILE):
        return

    with open(CSV_FILE, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        headers = reader.fieldnames or []

    # Already in new format
    if set(FIELDNAMES).issubset(set(headers)):
        return

    # Only migrate if it looks like the old format
    if headers == ["Date", "Category", "Amount"]:
        print("  [Info] Migrating CSV to new format (Date, Category, Type, Amount, Description)...")
        old_rows = []
        with open(CSV_FILE, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                old_rows.append(row)

        with open(CSV_FILE, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writeheader()
            for row in old_rows:
                try:
                    amount = float(row["Amount"])
                    entry_type = "Expense" if amount < 0 else "Income"
                    writer.writerow({
                        "Date":        row["Date"].strip(),
                        "Category":    row["Category"].strip().title(),
                        "Type":        entry_type,
                        "Amount":      f"{abs(amount):.2f}",
                        "Description": ""
                    })
                except (ValueError, KeyError):
                    pass  # Skip bad rows during migration

        print("  [Info] Migration complete.")


if __name__ == "__main__":
    main()
