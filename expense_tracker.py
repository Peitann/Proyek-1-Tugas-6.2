from expense import Expense
import calendar
import datetime
import json
from recap import summarize_expenses_daily, summarize_expenses_monthly, summarize_expenses_weekly

# Variabel global untuk menyimpan budget
global_budget = 0.0


def main():
    print("WELCOME TO MONEY TRACKER APP")

    # Load budget from file
    budget = load_budget()

    # Initialize expenses list
    expenses = []
    
    # Latest Budget
    print_latest_budget(budget)

    while True:
        print("Select an option:")
        print("1. Add Expense")
        print("2. Summarize Expenses")
        print("3. Set Budget")
        print("4. Quit")
        option = input("Enter your choice: ")

        if option == "1":
            expense = add_expense(budget, expenses)
            expenses.append(expense)
            if expense is not None:
                expenses.append(expense)  # Add expense to the list
            
        elif option == "2":
            print("Select a summary period:")
            print("1. Daily")
            print("2. Weekly")
            print("3. Monthly")
            summary_option = input("Enter your choice: ")
            if summary_option == "1":
                summarize_expenses_daily(expenses, budget)
            elif summary_option == "2":
                summarize_expenses_weekly(expenses, budget)
            elif summary_option == "3":
                summarize_expenses_monthly(expenses, budget)
            else:
                print("Invalid summary period. Please try again.")
        elif option == "3":
            budget = set_budget()  # Perbarui budget setelah menambahkan budget baru
        elif option == "4":
            print("Exiting Money Tracker App. Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")
            
def print_latest_budget(budget):
    print()
    print(f"💸 Current Budget: Rp. {budget:.2f} 💸")
    
            
def add_expense(budget, expenses):
    global global_budget  # Menandai variabel global_budget untuk diakses dan diperbarui
    print(f"🎯 Running Expense Tracker!")
    expense_file_path = "expenses.csv"

    while True:
        # Get user input for expense.
        expense = get_user_expense(budget)

        if expense is not None:
            # Write their expense to a file.
            save_expense_to_file(expense, expense_file_path)

            print("Expense added successfully!")
            expenses.append(expense)  # Add expense to the list
            budget -= expense.amount
            global_budget = budget  # Memperbarui variabel global_budget
            break

    ask_for_another_operation(budget)
    return expense  # Return the expense object



def ask_for_another_operation(budget):
    while True:
        choice = input("Do you want to perform another operation? (yes/no): ").lower()
        if choice == "yes":
            print_latest_budget(budget)
            break
        elif choice == "no":
            print("Exiting Money Tracker App. Goodbye!")
            exit()  # Exiting directly without summarizing expenses
        else:
            print("Invalid choice. Please enter 'yes' or 'no'.")

def is_valid_date(date_str):
    try:
        year, month, day = map(int, date_str.split("-"))
        if year < 1000 or year > 9999 or month < 1 or month > 12 or day < 1 or day > 31:
            return False
        return True
    except ValueError:
        return False

def get_user_expense(budget):
    print(f"🎯 Getting User Expense")
    print()
    expense_name = input("Enter expense name: ")
    expense_amount = float(input("Enter expense amount: "))

    if expense_amount > budget:
        print(f"⚠️ Warning: The spending '{expense_amount}' exceeds the budget '{budget}'. Please re-enter.")
        return None

    expense_categories = [
        "🍔 Food",
        "🏠 Home",
        "💼 Work",
        "🎉 Fun",
        "✨ Misc",
    ]

    while True:
        print()
        print("Select a category: ")
        for i, category_name in enumerate(expense_categories):
            print(f"  {i + 1}. {category_name}")

        value_range = f"[1 - {len(expense_categories)}]"
        selected_index = int(input(f"Enter a category number {value_range}: ")) - 1

        if selected_index in range(len(expense_categories)):
            selected_category = expense_categories[selected_index]

            # Ambil input tanggal
            expense_date = input("Enter the date of the expense (YYYY-MM-DD): ")

            if not is_valid_date(expense_date):
                print("⚠️ Warning: The date is in an invalid format, please re-enter the date!")
                continue

            new_expense = Expense(
                name=expense_name, category=selected_category, amount=expense_amount, date=expense_date
            )
            return new_expense
        else:
            print("Invalid category. Please try again!")
            return new_expense

def set_budget():
    new_budget = float(input("Enter additional budget: Rp."))
    budget = load_budget()  # Load budget dari file
    budget += new_budget  # Tambahkan budget baru
    save_budget(budget)
    
    print(f"💸 Current Budget: Rp. {budget:.2f} 💸")
    return budget


def load_budget():
    try:
        with open("budget.txt", "r") as file:
            budget_str = file.read().strip()
            if not budget_str:  # Jika file kosong, kembalikan total pengeluaran
                print("No budget found. Setting initial budget.")
                total_expenses = 0.0
                with open("expenses.csv", "r", encoding='utf-8') as expenses_file:
                    for line in expenses_file:
                        parts = line.strip().split(",")
                        if len(parts) >= 2:
                            total_expenses += float(parts[1])
                return total_expenses
            budget_from_file = float(budget_str)
            print("Budget loaded successfully!")
            return budget_from_file
    except FileNotFoundError:
        print("No budget found. Setting initial budget.")
        total_expenses = 0.0
        with open("expenses.csv", "r", encoding='utf-8') as expenses_file:
            for line in expenses_file:
                parts = line.strip().split(",")
                if len(parts) >= 2:
                    total_expenses += float(parts[1])
        return total_expenses


def save_budget(budget):
    try:
        with open("budget.txt", "w", encoding="utf-8") as file:
            json.dump(budget, file, indent=4)
            print("Budget saved successfully!")
    except Exception as e:
        print(f"Error saving budget: {e}")

def save_expense_to_file(expense: Expense, expense_file_path):
    print()
    print(f"🎯 Saving User Expense: {expense}")
    with open(expense_file_path, "a", encoding='utf-8') as f:
        f.write(f"{expense.name},{expense.amount},{expense.category},{expense.date}\n")

    # Update budget in budget.txt
    budget = load_budget()  # Load budget dari file
    budget -= expense.amount  # Kurangkan expense baru dari budget
    save_budget(budget)

def summarize_expenses(expense_file_path, budget):
    print(f"🎯 Summarizing User Expense")
    expenses = []
    with open(expense_file_path, "r", encoding="utf-8") as f:  
        lines = f.readlines()
        for line in lines:
            expense_name, expense_amount, expense_category, expense_date = line.strip().split(",")
            line_expense = Expense(
                name=expense_name,
                amount=float(expense_amount),
                category=expense_category,
                date=expense_date
            )
            expenses.append(line_expense)

    amount_by_category = {}
    for expense in expenses:
        key = expense.category
        if key in amount_by_category:
            amount_by_category[key] += expense.amount
        else:
            amount_by_category[key] = expense.amount

    print("Expenses By Category 📈:")
    for key, amount in amount_by_category.items():
        print(f"  {key}: Rp.{amount:.2f}")

    total_spent = sum([x.amount for x in expenses])
    print(f"💵 Total Spent: Rp.{total_spent:.2f}")

    remaining_budget = budget - total_spent
    print(f"✅ Budget Remaining: Rp.{remaining_budget:.2f}")

    now = datetime.datetime.now()
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    remaining_days = days_in_month - now.day
    
if __name__ == "__main__":
    main()