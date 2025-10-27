import csv
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import re

FILENAME = "exp.csv"

# ---------------------------
# Load existing expenses
# ---------------------------
def load_expenses():
    expenses = []
    try:
        with open(FILENAME, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                expenses.append(row)
    except FileNotFoundError:
        pass
    return expenses

# ---------------------------
# Save all expenses
# ---------------------------
def save_expenses(expenses):
    with open(FILENAME, mode="w", newline="", encoding="utf-8") as file:
        fieldnames = ["date", "category", "description", "amount"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(expenses)

# ---------------------------
# Add new expense
# ---------------------------
def add_expense():
    date = input("Enter date (YYYY-MM-DD) or leave blank for today: ").strip()
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")
    category = input("Enter category (e.g., Food, Travel, Bills): ").strip()
    description = input("Enter description: ").strip()
    try:
        amount = float(input("Enter amount (₹): "))
    except ValueError:
        print("Invalid amount! Please enter a number.")
        return

    expense = {"date": date, "category": category, "description": description, "amount": amount}
    expenses = load_expenses()
    expenses.append(expense)
    save_expenses(expenses)
    print("✅ Expense added successfully!")

# ---------------------------
# View all expenses
# ---------------------------
def view_expenses():
    expenses = load_expenses()
    if not expenses:
        print("No expenses found.")
        return
    df = pd.DataFrame(expenses)
    print("\n=== All Expenses ===")
    print(df.to_string(index=False))

# ---------------------------
# Dashboard View
# ---------------------------
def show_dashboard():
    try:
        df = pd.read_csv(FILENAME)
    except FileNotFoundError:
        print("No data available yet.")
        return

    if df.empty:
        print("No data to show.")
        return

    # Clean and convert amount
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)
    df = df[df["amount"] > 0]

    if df.empty:
        print("No valid data to display.")
        return

    print("\n=== EXPENSE DASHBOARD ===")
    print(f"Total Expenses: ₹{df['amount'].sum():.2f}")
    print(f"Total Entries: {len(df)}")

    if "category" not in df.columns or df["category"].dropna().empty:
        print("Most Spent Category: N/A")
    else:
        category_sums = df.groupby("category")["amount"].sum()
        top_category = category_sums.idxmax() if not category_sums.empty else "N/A"
        print(f"Most Spent Category: {top_category}")

    # ---------- Monthly Summary ----------
    df["month"] = df["date"].astype(str).str[:7]
    monthly = df.groupby("month")["amount"].sum()

    if not monthly.empty:
        plt.figure(figsize=(8, 4))
        monthly.plot(kind="bar", title="Monthly Spending", color="skyblue")
        plt.ylabel("Total (₹)")
        plt.xlabel("Month (YYYY-MM)")
        plt.tight_layout()
        plt.show()
    else:
        print("No monthly data to plot.")

    # ---------- Category Summary ----------
    category = df.groupby("category")["amount"].sum()
    if not category.empty:
        category.plot(kind="pie", autopct="%1.1f%%", title="Spending by Category", figsize=(5, 5))
        plt.ylabel("")
        plt.show()
    else:
        print("No category data to plot.")

# ---------------------------
# Clear all expenses
# ---------------------------
def clear_expenses():
    confirm = input("Are you sure you want to delete all data? (y/n): ").lower()
    if confirm == "y":
        save_expenses([])
        print("All expenses cleared!")
    else:
        print("Cancelled.")

# ---------------------------
# Search expenses by date or category
# ---------------------------
def search_expenses():
    expenses = load_expenses()
    if not expenses:
        print("No expenses to search.")
        return

    choice = input("Search by (1) Category or (2) Date: ").strip()
    results = []

    if choice == "1":
        cat = input("Enter category to search: ").strip().lower()
        results = [e for e in expenses if e["category"].lower() == cat]

    elif choice == "2":
        date_input = input("Enter date to search (YYYY-MM-DD, DD MM, or DD Mon): ").strip().lower()
        month_map = {"jan":"01","feb":"02","mar":"03","apr":"04","may":"05","jun":"06",
                     "jul":"07","aug":"08","sep":"09","oct":"10","nov":"11","dec":"12"}
        for name,num in month_map.items():
            if name in date_input:
                date_input = date_input.replace(name,num)
        parts = re.findall(r"\d+", date_input)
        parts = [p.zfill(2) for p in parts]

        for e in expenses:
            if all(p in e["date"] for p in parts):
                results.append(e)
    else:
        print("Invalid choice.")
        return

    if results:
        print("\n=== Search Results ===")
        for i, e in enumerate(results,1):
            print(f"{i}. {e['date']} | {e['category']} | {e['description']} | ₹{e['amount']}")
    else:
        print("No matching expenses found.")

# ---------------------------
# Top N spending categories
# ---------------------------
def top_categories(n=3):
    try:
        df = pd.read_csv(FILENAME)
    except FileNotFoundError:
        print("No data available.")
        return
    if df.empty:
        print("No data to analyze.")
        return

    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)
    df = df[df["amount"] > 0]

    if "category" not in df.columns or df["category"].dropna().empty:
        print("No category data available.")
        return

    top = df.groupby("category")["amount"].sum().sort_values(ascending=False).head(n)
    print(f"\n=== Top {n} Spending Categories ===")
    for i, (cat, amt) in enumerate(top.items(),1):
        print(f"{i}. {cat}: ₹{amt:.2f}")

# ---------------------------
# Main Menu
# ---------------------------
def main_menu():
    while True:
        print("\n========== EXPENSE TRACKER ==========")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Dashboard View")
        print("4. Clear All Data")
        print("5. Exit")
        print("6. Search Expenses")
        print("7. Top Spending Categories")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            show_dashboard()
        elif choice == "4":
            clear_expenses()
        elif choice == "5":
            print("Exiting... Goodbye!")
            break
        elif choice == "6":
            search_expenses()
        elif choice == "7":
            top_categories()
        else:
            print("Invalid choice. Please try again.")

# ---------------------------
# Run Program
# ---------------------------
if __name__ == "__main__":
    main_menu()
