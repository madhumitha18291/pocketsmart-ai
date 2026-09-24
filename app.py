import os
import json
from datetime import datetime

class PocketSmartAI:
    def __init__(self, budget: float = 0.0):
        self.budget = budget
        self.expenses = []

    def add_expense(self, category: str, amount: float, description: str = ""):
        """Adds a new expense item."""
        record = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "category": category,
            "amount": amount,
            "description": description
        }
        self.expenses.append(record)
        print(f"Added expense: ${amount:.2f} for '{category}'")

    def total_spent(self) -> float:
        """Calculates total money spent."""
        return sum(item["amount"] for item in self.expenses)

    def remaining_budget(self) -> float:
        """Returns the remaining budget."""
        return self.budget - self.total_spent()

    def generate_insights(self) -> str:
        """Generates simple AI-like financial insights based on spending habits."""
        total = self.total_spent()
        remaining = self.remaining_budget()
        
        if total == 0:
            return "No expenses recorded yet. You're fully on track!"
        
        if remaining < 0:
            return f"⚠️ Warning: You have overspent by ${abs(remaining):.2f}!"
        elif remaining < (0.2 * self.budget):
            return f"⚠️ Caution: You have less than 20% of your budget left (${remaining:.2f})."
        else:
            return f"✅ Great job! You have ${remaining:.2f} remaining out of ${self.budget:.2f}."


if __name__ == "__main__":
    # Example usage
    tracker = PocketSmartAI(budget=1000.0)
    
    tracker.add_expense("Groceries", 150.50, "Weekly grocery run")
    tracker.add_expense("Utilities", 85.00, "Electricity bill")
    tracker.add_expense("Entertainment", 45.00, "Movie tickets")
    
    print("\n--- Summary ---")
    print(f"Total Spent: ${tracker.total_spent():.2f}")
    print(tracker.generate_insights())
