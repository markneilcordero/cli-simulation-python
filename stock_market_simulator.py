import json
import heapq
import os

DATA_FILE = "stock_market.json"

class StockMarketSimulator:
    def __init__(self):
        self.load_data()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as file:
                data = json.load(file)
                self.user_balance = data.get("balance", 10000)
                self.user_portfolio = data.get("portfolio", {})
                self.buy_orders = data.get("buy_orders", [])
                self.sell_orders = data.get("sell_orders", [])
        else:
            self.user_balance = 10000
            self.user_portfolio = {}
            self.buy_orders = []
            self.sell_orders = []

    def save_data(self):
        data = {
            "balance": self.user_balance,
            "portfolio": self.user_portfolio,
            "buy_orders": self.buy_orders,
            "sell_orders": self.sell_orders
        }
        with open(DATA_FILE, "w") as file:
            json.dump(data, file, indent=4)

    def display_portfolio(self):
        print("\nYour Portfolio:")
        for stock, quantity in self.user_portfolio.items():
            print(f"- {stock}: {quantity} shares")
        print(f"Available Balance: ${self.user_balance}\n")

    def place_buy_order(self):
        stock = input("Enter stock symbol: ").upper()
        quantity = int(input("Enter quantity: "))
        price = float(input("Enter price per share: "))
        total_cost = quantity * price

        if total_cost > self.user_balance:
            print("Insufficient balance!")
            return

        heapq.heappush(self.buy_orders, (price, stock, quantity))
        self.user_balance -= total_cost
        print(f"Buy order placed: {quantity} shares of {stock} at ${price}/share")
        self.match_orders()
        self.save_data()

    def place_sell_order(self):
        stock = input("Enter stock symbol: ").upper()
        quantity = int(input("Enter quantity: "))
        price = float(input("Enter price per share: "))

        if stock not in self.user_portfolio or self.user_portfolio[stock] < quantity:
            print("Insufficient shares!")
            return

        heapq.heappush(self.sell_orders, (-price, stock, quantity))
        self.user_portfolio[stock] -= quantity
        if self.user_portfolio[stock] == 0:
            del self.user_portfolio[stock]

        print(f"Sell order placed: {quantity} shares of {stock} at ${price}/share")
        self.match_orders()
        self.save_data()

    def match_orders(self):
        while self.buy_orders and self.sell_orders:
            buy_price, buy_stock, buy_quantity = heapq.heappop(self.buy_orders)
            sell_price, sell_stock, sell_quantity = heapq.heappop(self.sell_orders)

            sell_price = -sell_price

            if buy_stock == sell_stock and buy_price >= sell_price:
                executed_price = (buy_price + sell_price) / 2
                executed_quantity = min(buy_quantity, sell_quantity)

                print(f"\nOrder Matched! {executed_quantity} shares of {buy_stock} at ${executed_price:.2f}/share\n")

                self.user_portfolio[buy_stock] = self.user_portfolio.get(buy_stock, 0) + executed_quantity

                if buy_quantity > executed_quantity:
                    heapq.heapreplace(self.buy_orders, (buy_price, buy_stock, buy_quantity - executed_quantity))

                if sell_quantity > executed_quantity:
                    heapq.heappush(self.sell_orders, (-sell_price, sell_stock, sell_quantity - executed_quantity))

                self.save_data()
            else:
                heapq.heappush(self.sell_orders, (-sell_price, sell_stock, sell_quantity))
                break
    def menu(self):
        while True:
            print("\nStock Market Simulator")
            print("1. View Portfolio")
            print("2. Buy Stock")
            print("3. Sell Stock")
            print("4. Exit")
            choice = input("Enter choice: ")

            if choice == "1":
                self.display_portfolio()
            elif choice == "2":
                self.place_buy_order()
            elif choice == "3":
                self.place_sell_order()
            elif choice == "4":
                print("Exiting Stock Market Simulator...")
                self.save_data()
                break
            else:
                print("Invalid choice! Please try again.")

if __name__ == "__main__":
    simulator = StockMarketSimulator()
    simulator.menu()