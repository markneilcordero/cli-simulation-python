import json
import heapq
import os

DATA_FILE = "atm_data.json"

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({"users": {}, "transactions": []}, f)

def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

class ATM:
    def __init__(self):
        self.data = load_data()
        self.current_user = None
        self.transaction_queue = []

    def register(self, username, pin, initial_balance=0):
        if username in self.data["users"]:
            print("User already exists!")
            return False

        self.data["users"][username] = {
            "pin": pin,
            "balance": initial_balance,
            "transactions": []
        }
        save_data(self.data)
        print(f"User {username} registered successfull!")
        return True
    def login(self, username, pin):
        if username in self.data["users"] and self.data["users"][username]["pin"] == pin:
            self.current_user = username
            print(f"Welcome, {username}!")
            return True
        print("Invalid username or PIN.")
        return False

    def deposit(self, amount):
        if self.current_user:
            self.data["users"][self.current_user]["balance"] += amount
            self.data["users"][self.current_user]["transactions"].append(f"Deposited: ${amount}")
            save_data(self.data)
            print(f"Deposited ${amount} successfully!")
            return True
        print("Login required!")
        return False

    def withdraw(self, amount):
        if self.current_user:
            balance = self.data["users"][self.current_user]["balance"]
            if amount > balance:
                print("Insufficient funds!")
                return False

            heapq.heappush(self.transaction_queue, (-amount, self.current_user))
            print(f"Withdrawal request of ${amount} added to queue.")
            return True
        print("Login required!")
        return False

    def process_transactions(self):
        if not self.transaction_queue:
            print("No transactions to process.")
            return

        print("\nProcessing Transactions...")
        while self.transaction_queue:
            amount, user = heapq.heappop(self.transaction_queue)
            amount = -amount

            if self.data["users"][user]["balance"] >= amount:
                self.data["users"][user]["balance"] -= amount
                self.data["users"][user]["transactions"].append(f"Withdrew: ${amount}")
                print(f"Processed withdrawal of ${amount} for {user}.")
            else:
                print(f"Insufficient funds for {user}'s transaction of ${amount}. Skipping.")

        save_data(self.data)

    def check_balance(self):
        if self.current_user:
            balance = self.data["users"][self.current_user]["balance"]
            print(f"Your current balance: ${balance}")
            return balance
        print("Login required!")
        return None

    def view_transactions(self):
        if self.current_user:
            transactions = self.data["users"][self.current_user]["transactions"]
            print("\nTransaction History:")
            for t in transactions:
                print(f"- {t}")
            return transactions
        print("Login required!")
        return []

def main():
    atm = ATM()

    while True:
        print("\n=== ATM Simulation ===")
        print("1. Register")
        print("2. Login")
        print("3. Deposit")
        print("4. Withdraw")
        print("5. Check Balance")
        print("6. View Transactions")
        print("7. Process Transactions (Admin)")
        print("8. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            username = input("Enter username: ")
            pin = input("Enter PIN: ")
            atm.register(username, pin)
        elif choice == "2":
            username = input("Enter username: ")
            pin = input("Enter PIN: ")
            atm.login(username, pin)
        elif choice == "3":
            amount = float(input("Enter deposit amount: "))
            atm.deposit(amount)
        elif choice == "4":
            amount = float(input("Enter withdrawal amount: "))
            atm.withdraw(amount)
        elif choice == "5":
            atm.check_balance()
        elif choice == "6":
            atm.view_transactions()
        elif choice == "7":
            atm.process_transactions()
        elif choice == "8":
            print("Exiting ATM Simulation. Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()