import heapq
import json
import os

DATA_FILE = "checkin_queue.json"

class AirportCheckIn:
    def __init__(self):
        self.queue = []
        self.load_queue()

    def save_queue(self):
        with open(DATA_FILE, "w") as f:
            json.dump(self.queue, f)

    def load_queue(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                try:
                    self.queue = json.load(f)
                    heapq.heapify(self.queue)
                except json.JSONDecodeError:
                    self.queue = []

    def get_priority(self, class_type, special_assistance):
        priority_map = {"First-Class": 1, "Business": 2, "Economy": 3}
        base_priority = priority_map.get(class_type, 3)
        return 0 if special_assistance else base_priority

    def check_in_passenger(self, name, class_type, special_assistance):
        priority = self.get_priority(class_type, special_assistance)
        heapq.heappush(self.queue, (priority, name, class_type, special_assistance))
        print(f"\n✅ {name} checked in successfully!")
        self.save_queue()

    def process_next_passenger(self):
        if not self.queue:
            print("\n⏳ No passengers in queue!")
            return

        priority, name, class_type, special_assistance = heapq.heappop(self.queue)
        print(f"\n Processing passenger: {name} ({class_type}, {'Special Assistance' if special_assistance else 'Standard' })")
        self.save_queue()

    def display_queue(self):
        if not self.queue:
            print("\n No passengers in queue.")
            return

        print("\nCheck-in Queue:")
        for i, (_, name, class_type, special_assistance) in enumerate(sorted(self.queue), 1):
            print(f"{i}. {name} - {class_type} {'(Special Assistance)' if special_assistance else ''}")

    def main_menu(self):
        while True:
            print("\n=== Airport Check-in System ===")
            print("1. check-in Passenger")
            print("2. Process Next Passenger")
            print("3. View Check-in Queue")
            print("4. Exit")

            choice = input("Enter choice: ").strip()
            if choice == "1":
                name = input("Enter passenger name: ").strip()
                class_type = input("Enter class (First-Class, Business, Economy): ").strip()
                special_assistance = input("Special assistance needed? (yes/no): ").strip().lower() == "yes"
                self.check_in_passenger(name, class_type, special_assistance)
            elif choice == "2":
                self.process_next_passenger()
            elif choice == "3":
                self.display_queue()
            elif choice == "4":
                print("Saving and exiting...")
                self.save_queue()
                break
            else:
                print("Invalid choice! Please try again.")

if __name__ == "__main__":
    system = AirportCheckIn()
    system.main_menu()