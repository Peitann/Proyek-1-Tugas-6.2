import datetime
import calendar

def get_remaining_days_in_month():
    now = datetime.datetime.now()
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    remaining_days = days_in_month - now.day
    return remaining_days

def get_remaining_days_in_week():
    now = datetime.datetime.now()
    remaining_days = 6 - now.weekday()  # Assuming Monday is the first day of the week
    return remaining_days

def summarize_expenses_daily(expenses, budget):
    print("Daily Expense Summary 📅:")
    total_spent = sum(expense.amount for expense in expenses)
    remaining_budget = budget - total_spent
    print(f"💵 Total Spent Today: ${total_spent:.2f}")
    print(f"✅ Budget Remaining Today: ${remaining_budget:.2f}")

def summarize_expenses_weekly(expenses, budget):
    print("Weekly Expense Summary 📆:")
    total_spent = sum(expense.amount for expense in expenses)
    remaining_budget = budget - total_spent
    remaining_days = get_remaining_days_in_week()
    weekly_budget = remaining_budget / (remaining_days + 1)  # Adding today as well
    print(f"💵 Total Spent This Week: ${total_spent:.2f}")
    print(f"✅ Budget Remaining This Week: ${remaining_budget:.2f}")
    print(f"📅 Remaining Days This Week: {remaining_days}")
    print(f"👉 Budget Per Day This Week: ${weekly_budget:.2f}")

def summarize_expenses_monthly(expenses, budget):
    print("Monthly Expense Summary 🗓️:")
    total_spent = sum(expense.amount for expense in expenses)
    remaining_budget = budget - total_spent
    remaining_days = get_remaining_days_in_month()
    monthly_budget = remaining_budget / (remaining_days + 1)  # Adding today as well
    print(f"💵 Total Spent This Month: ${total_spent:.2f}")
    print(f"✅ Budget Remaining This Month: ${remaining_budget:.2f}")
    print(f"📅 Remaining Days This Month: {remaining_days}")
    print(f"👉 Budget Per Day This Month: ${monthly_budget:.2f}")