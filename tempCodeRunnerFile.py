from expense import Expense
import calendar
import datetime
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
            time_period = ""  # Inisialisasi variabel time_period
            if summary_option == "1":
                time_period = "daily"
            elif summary_option == "2":
                time_period = "weekly"
            elif summary_option == "3":
                time_period = "monthly"
            else:
                print("Invalid summary period. Please try again.")
                continue
            summarize_expenses(budget, expenses, time_period)
        elif option == "3":
            budget = set_budget()
            save_budget(budget)
        elif option == "4":
            print("Exiting Money Tracker App. Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")
            
def print_latest_budget(budget):
    print(f"💸 Current Budget: ${budget:.2f} 💸")
            
def add_expense(budget, expenses):
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
            break

    ask_for_another_operation(budget)
    return expense  # Return the expense object


def ask_for_another_operation(budget):
    while True:
        choice = input("Do you want to perform another operation? (yes/no): ").lower()
        if choice == "yes":
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
    expense_name = input("Enter expense name: ")
    expense_amount = float(input("Enter expense amount: "))

    if expense_amount > budget:
        print(f"⚠️ Warning: The expense amount '{expense_amount}' exceeds the budget '{budget}'. Please re-enter a lower amount.")
        return None

    expense_categories = [
        "🍔 Food",
        "🏠 Home",
        "💼 Work",
        "🎉 Fun",
        "✨ Misc",
    ]

    while True:
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
    new_budget = float(input("Enter additional budget: $"))
    budget = load_budget()
    budget += new_budget
    save_budget(budget)
    
    print(f"💸 Current Budget: $ {budget:.2f} 💸")
    return budget


def load_budget():
    try:
        with open("budget.txt", "r") as file:
            budget = float(file.read())
            print("Budget loaded successfully!")
    except FileNotFoundError:
        print("No budget found. Setting initial budget.")
        budget = 0.0

    # Calculate total expenses from expenses.csv
    total_expenses = 0.0
    with open("expenses.csv", "r", encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split(",")
            if len(parts) >= 2:
                total_expenses += float(parts[1])

    # Update budget by subtracting total expenses
    budget -= total_expenses
    return budget


def save_budget(budget):
    with open("budget.txt", "w") as file:
        file.write(str(budget))
        print("Budget saved successfully!")


def save_expense_to_file(expense: Expense, expense_file_path):
    print(f"🎯 Saving User Expense: {expense} to {expense_file_path}")
    with open(expense_file_path, "a", encoding='utf-8') as f:
        f.write(f"{expense.name},{expense.amount},{expense.category},{expense.date}\n")

    # Update budget in budget.txt
    budget = load_budget()
    budget -= expense.amount  # Mengurangkan expense dari budget
    save_budget(budget)

def summarize_expenses(expenses, budget, time_period):
    print(f"{time_period.capitalize()} Expense Summary:")
    total_spent = sum(expense.amount for expense in expenses)
    remaining_budget = budget - total_spent

    if time_period == "daily":
        print(f"💵 Total Spent: ${total_spent:.2f}")
        print(f"✅ Budget Remaining: ${remaining_budget:.2f}")

    elif time_period == "weekly":
        remaining_days = get_remaining_days_in_week()
        weekly_budget = remaining_budget / (remaining_days + 1)  # Adding today as well
        print(f"💵 Total Spent This Week: ${total_spent:.2f}")
        print(f"✅ Budget Remaining This Week: ${remaining_budget:.2f}")
        print(f"📅 Remaining Days This Week: {remaining_days}")
        print(f"👉 Budget Per Day This Week: ${weekly_budget:.2f}")

    elif time_period == "monthly":
        remaining_days = get_remaining_days_in_month()
        monthly_budget = remaining_budget / (remaining_days + 1)  # Adding today as well
        print(f"💵 Total Spent This Month: ${total_spent:.2f}")
        print(f"✅ Budget Remaining This Month: ${remaining_budget:.2f}")
        print(f"📅 Remaining Days This Month: {remaining_days}")
        print(f"👉 Budget Per Day This Month: ${monthly_budget:.2f}")


if __name__ == "__main__":
    main()
