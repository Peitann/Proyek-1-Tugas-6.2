
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

    while True:
        print("Select an option:")
        print("1. Add Expense")
        print("2. Summarize Expenses")
        print("3. Set Budget")
        print("4. Quit")
        option = input("Enter your choice: ")

        if option == "1":
            add_expense(budget)
        elif option == "2":
            print("Select a summary period:")
            print("1. Daily")
            print("2. Weekly")
            print("3. Monthly")
            summary_option = input("Enter your choice: ")
            if summary_option == "1":
                summarize_expenses_daily(budget)
            elif summary_option == "2":
                summarize_expenses_weekly(budget)
            elif summary_option == "3":
                summarize_expenses_monthly(budget)
            else:
                print("Invalid summary period. Please try again.")
        elif option == "3":
            budget = set_budget()
            save_budget(budget)
        elif option == "4":
            print("Exiting Money Tracker App. Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

def add_expense(budget):
    print(f"🎯 Running Expense Tracker!")
    expense_file_path = "expenses.csv"

    # Get user input for expense.
    expense = get_user_expense()

    # Write their expense to a file.
    save_expense_to_file(expense, expense_file_path)

    print("Expense added successfully!")
    ask_for_another_operation(budget)

def ask_for_another_operation(budget):
    while True:
        choice = input("Do you want to perform another operation? (yes/no): ").lower()
        if choice == "yes":
            break
        elif choice == "no":
            print("Exiting Money Tracker App. Goodbye!")
            # Summarize expenses
            expense_file_path = "expenses.csv"
            summarize_expenses(expense_file_path, budget)
            exit()
        else:
            print("Invalid choice. Please enter 'yes' or 'no'.")

def get_user_expense():
    print(f"🎯 Getting User Expense")
    expense_name = input("Enter expense name: ")
    expense_amount = float(input("Enter expense amount: "))
    expense_date = input("Enter expense date (YYYY-MM-DD): ")
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
            new_expense = Expense(
                name=expense_name, category=selected_category, amount=expense_amount, date=expense_date
            )
            return new_expense
        else:
            print("Invalid category. Please try again!")

def set_budget():
    new_budget = float(input("Enter your new budget: $"))
    return new_budget

def load_budget():
    try:
        with open("budget.txt", "r") as file:
            budget = float(file.read())
            print("Budget loaded successfully!")
            return budget
    except FileNotFoundError:
        print("No budget found. Setting initial budget.")
        return set_budget()

def save_budget(budget):
    with open("budget.txt", "w") as file:
        file.write(str(budget))
        print("Budget saved successfully!")

def save_expense_to_file(expense: Expense, expense_file_path):
    print(f"🎯 Saving User Expense: {expense} to {expense_file_path}")
    with open(expense_file_path, "a", encoding='utf-8') as f:
        f.write(f"{expense.name},{expense.amount},{expense.category},{expense.date}\n")
        
def summarize_expenses(expense_file_path, budget):
    print(f"🎯 Summarizing User Expense")
    expenses: list[Expense] = []
    with open(expense_file_path, "r", encoding="utf-8") as f:  # Menentukan pengkodean karakter utf-8
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
        print(f"  {key}: ${amount:.2f}")

    total_spent = sum([x.amount for x in expenses])
    print(f"💵 Total Spent: ${total_spent:.2f}")

    remaining_budget = budget - total_spent
    print(f"✅ Budget Remaining: ${remaining_budget:.2f}")

    now = datetime.datetime.now()
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    remaining_days = days_in_month - now.day

    daily_budget = remaining_budget / remaining_days
    print(f"👉 Budget Per Day: ${daily_budget:.2f}")


if __name__ == "__main__":
    main()
