class MoneyTracker:
    def __init__(self):
        self.daily_transactions = {}
        self.weekly_transactions = {}
        self.monthly_transactions = {}

    def record_transaction(self, transaction_type, amount):
        if transaction_type == 'income':
            self._record_income(amount)
        elif transaction_type == 'expense':
            self._record_expense(amount)
        else:
            print("Invalid transaction type.")

    def _record_income(self, amount):
        today = datetime.date.today()
        self.daily_transactions.setdefault(today, {'income': 0, 'expense': 0})
        self.daily_transactions[today]['income'] += amount

        week_number = today.isocalendar()[1]
        self.weekly_transactions.setdefault(week_number, {'income': 0, 'expense': 0})
        self.weekly_transactions[week_number]['income'] += amount

        month = today.month
        self.monthly_transactions.setdefault(month, {'income': 0, 'expense': 0})
        self.monthly_transactions[month]['income'] += amount

    def _record_expense(self, amount):
        today = datetime.date.today()
        self.daily_transactions.setdefault(today, {'income': 0, 'expense': 0})
        self.daily_transactions[today]['expense'] += amount

        week_number = today.isocalendar()[1]
        self.weekly_transactions.setdefault(week_number, {'income': 0, 'expense': 0})
        self.weekly_transactions[week_number]['expense'] += amount

        month = today.month
        self.monthly_transactions.setdefault(month, {'income': 0, 'expense': 0})
        self.monthly_transactions[month]['expense'] += amount

    def print_daily_summary(self):
        today = datetime.date.today()
        print(f"Daily Summary for {today}:")
        print("Income:", self.daily_transactions.get(today, {'income': 0})['income'])
        print("Expense:", self.daily_transactions.get(today, {'expense': 0})['expense'])
        self._back_to_main_menu()

    def print_weekly_summary(self):
        week_number = datetime.date.today().isocalendar()[1]
        print(f"Weekly Summary for Week {week_number}:")
        print("Income:", self.weekly_transactions.get(week_number, {'income': 0})['income'])
        print("Expense:", self.weekly_transactions.get(week_number, {'expense': 0})['expense'])
        self._back_to_main_menu()

    def print_monthly_summary(self):
        month = datetime.date.today().month
        print(f"Monthly Summary for Month {month}:")
        print("Income:", self.monthly_transactions.get(month, {'income': 0})['income'])
        print("Expense:", self.monthly_transactions.get(month, {'expense': 0})['expense'])
        self._back_to_main_menu()

    def _back_to_main_menu(self):
        input("Press Enter to return to the main menu.")

import datetime

def main():
    tracker = MoneyTracker()
    while True:
        print("=============================")
        print("WELCOME TO MONEY TRACKER APP")
        print("=============================\n")
        print("Select an Option :")
        print("1. Record Income")
        print("2. Record Expense")
        print("3. View Daily Summary")
        print("4. View Weekly Summary")
        print("5. View Monthly Summary")
        print("6. Exit")

        choice = int(input("Enter your choice: "))

        if choice == 1:
            amount = float(input("Enter income amount: "))
            tracker.record_transaction('income', amount)
            print("Income recorded successfully.")

        elif choice == 2:
            amount = float(input("Enter expense amount: "))
            tracker.record_transaction('expense', amount)
            print("Expense recorded successfully.")

        elif choice == 3:
            tracker.print_daily_summary()

        elif choice == 4:
            tracker.print_weekly_summary()

        elif choice == 5:
            tracker.print_monthly_summary()

        elif choice == 6:
            print("Exiting the program.")
            break

        else:
            print("Invalid choice. Please choose a valid option.")


if __name__ == "__main__":
    main()
