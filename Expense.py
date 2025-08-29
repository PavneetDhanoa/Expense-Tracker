# expense_tracker.py
# Personal Expense Tracker with Data Visualization

import csv
import datetime
import os
import matplotlib.pyplot as plt

CSV_FILE = "expenses.csv"


# 1. Initialize CSV if not exists
def initialize_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Category", "Amount"])


# 2. Add income/expense
def add_entry(date, category, amount):
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, category, amount])


# 3. Load data from CSV
def load_data():
    data = []
    with open(CSV_FILE, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append({
                'Date': datetime.datetime.strptime(row['Date'], "%Y-%m-%d"),
                'Category': row['Category'],
                'Amount': float(row['Amount'])
            })
    return data


# 4. Generate bar chart by month
def show_monthly_summary(data):
    monthly = {}
    for entry in data:
        month = entry['Date'].strftime("%Y-%m")
        monthly[month] = monthly.get(month, 0) + entry['Amount']

    months = list(monthly.keys())
    amounts = list(monthly.values())

    plt.figure(figsize=(10, 5))
    plt.bar(months, amounts)
    plt.title("Monthly Spending")
    plt.xlabel("Month")
    plt.ylabel("Amount ($)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


# 5. Generate pie chart by category
# 5. Generate pie chart by category
def show_category_pie(data):
    categories = {}
    for entry in data:
        amount = entry['Amount']
        if amount < 0:  # Only consider expenses
            categories[entry['Category']] = categories.get(entry['Category'], 0) + abs(amount)

    if not categories:
        print("No expense data to plot.")
        return

    labels = list(categories.keys())
    sizes = list(categories.values())

    plt.figure(figsize=(6,6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title("Spending by Category")
    plt.axis('equal')
    plt.show()


# CLI for demo purposes
def menu():
    print("\nExpense Tracker")
    print("1. Add Income/Expense")
    print("2. Show Monthly Summary")
    print("3. Show Category Pie Chart")
    print("4. Exit")

    choice = input("Enter choice: ")
    return choice


def main():
    initialize_csv()
    while True:
        choice = menu()
        if choice == '1':
            date = input("Enter date (YYYY-MM-DD): ")
            category = input("Enter category (e.g., Rent, Food, Salary): ")
            amount = float(input("Enter amount (use negative for expenses): "))
            add_entry(date, category, amount)
        elif choice == '2':
            data = load_data()
            show_monthly_summary(data)
        elif choice == '3':
            data = load_data()
            show_category_pie(data)
        elif choice == '4':
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
