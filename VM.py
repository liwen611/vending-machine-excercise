import os
from item import Item


class VendingMachine:
    def __init__(self):
        """
        run get_inventory method to populate all the item objects for sales_logs
        sales_logs attribute is a dictionary for easy look up wether an item is still available
        selection is used a placeholder before client makes payment for the purchase
        """
        self.sales_logs = {}
        self.selection = None
        self.control_flow_map = {
            "homepage": {
                "prompt": """
                    Here is a menu of our services :
                    ================================
                    Enter 1 to display all inventory
                    Enter 2 to display available item
                    Enter 3 to select an item"
                    Enter 4 to make a payment"
                    Enter 5 to exit
                    ================================
                    Enter * to return to this homepage
                        """,
                "suggestion ": "Would you like to make a selection? Enter 3"
                        },
            "1": {
                "ops": self.display_inventory(),
                "suggestion ": "Would you like to make a selection? Enter 3"
            },
            "2": {
                "ops": self.display_available_items(),
                "suggestion ": "Would you like to make a selection? Enter 3"
            },
            }


    def get_inventory(self, data_input):
        """
        method take a local file path or a list of items as inventory for the vending machine
        turn all the inventory into Item class object for easier parsing later
        """
        if os.path.isfile(data_input):
            with open(data_input, "r") as infile:
                data = infile.readlines()

        for idx, item in enumerate(data):
            if idx == 0:
                continue
            item = item.strip("\n")
            name, price = item.split(",")
            it = Item(name, float(price))
            # add item to sales logs
            self.sales_logs[idx] = it

        print("Vending maching is well stocked again!")

    def display_inventory(self):
        """
        method display inventory within the vending machine
        """
        if self.sales_logs:
            print("Currently we offer the following :")
            for idx, item in self.sales_logs.items():
                print(idx, item.name, item.price, "==>", item.status)
        else:
            print("Vending Machine is empty today!")

    def display_available_items(self):
        """
        method display inventory within the vending machine
        """
        print("We still have these available :")
        for idx in self.sales_logs:
            item = self.sales_logs[idx]
            if item.status == "Available":
                print(idx, item.name, item.price, "==>", item.status)

    def select_item(self, idx):
        if idx not in self.sales_logs:
            print(f"{idx} not offered by the Vending Machine")
            print("This are the items that we currently offer ...")
            self.display_inventory()

        elif self.sales_logs[idx].status != "Available":
            print("This item is sold out!")
            self.display_available_items()
        else:
            self.selection = self.sales_logs[idx]
            print(
                f"You have selected {self.selection.name}, price : {self.selection.price}")

    def process_payment(self, balance):
        while not self.selection:
            idx = input("Select an item first!")
            self.select_item(idx)

        print(f"processing your payment of : {balance} dollars ...")
        if balance < self.selection.price:
            print(
                f"Sorry,  your current balance is less than {self.selection.price}")
        else:
            changes = balance - self.selection.price
            self.selection.status = "Sold out"
            self.selection = None

            if changes > 0:
                print(f"Your change is {changes}")

    def homepage(self):
        print(self.control_flow_map["homepage"]["prompt"])

    def control_flow(self, command, retries=5):

        while True:
            if command == "*":
                self.homepage()
                command = input()

            if command == "1":
                self.display_inventory()
                print("""
                ================================
                Enter 3 to select an item
                Enter * to return to homepage
                Enter 5 to exit """)
                command = input()

            if command == "2":
                self.display_available_items()
                print("""
                ================================
                Enter 3 to select an item
                Enter * to return to homepage
                Enter 5 to exit """
                )
                command = input()

            if command == "3":
                self.display_available_items()
                print("--------------------------")
                print("Enter the item number you would like to purchase.")
                idx = int(input())
                self.select_item(idx)
                command = "4"
                

            if command == "4":
                if not self.selection:
                    command = "3"
                    continue 
    
                print("Enter the dollars amount in your balance.")
                balance = input()
                self.process_payment(int(balance))
                print("""
                ================================
                Enter 3 to select an item
                Enter * to return to homepage
                Enter 5 to exit """)
                command = input()

            if command == "5":
                print("Thank you for using our service, come again!")
                break

            else:
                self.homepage()
                command = input()
                if retries <= 0:
                    break
                retries -= 1



if __name__ == "__main__":
    vm = VendingMachine()
    vm.get_inventory("inventory.csv")
    vm.homepage()
    # vm.select_item(1)
    # vm.process_payment(5)

    command = input()
    while command not in ["*", "1", "2", "3", "4", "5"]:
        print("Enter a number from the menu ^_^")
        command = input()

    vm.control_flow(command)




# vm = VendingMachine()
# vm.get_inventory("inventory.csv")
# #vm.display_inventory()
# # #vm.select_item("meow")
# vm.select_item("Coca-Cola")
# vm.process_payment(10)
# vm.display_inventory()
# #vm.display_available_items()
