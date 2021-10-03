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
            "*": {
                "command_name": "Return to Home Page",
                "prompt": "Here is a menu of our services :\n================================\nEnter 1 to display all inventory\nEnter 2 to display available item\nEnter 3 to select an item\nEnter 4 to make a payment\nEnter 5 to exit\n",
                "follow_ups": ["1", "2", "3", "4", "5"],
            },
            "1": {
                "ops": self.display_inventory,
                "command_name": "Display Items",
                "prompt": "These are the items we offer:\n================================",
                "follow_ups": ["2", "3", "5", "*"],
            },
            "2": {
                "ops": self.display_available_items,
                "command_name": "Display Available Items",
                "prompt": "These items are still avaiable :\n================================",
                "follow_ups": ["3", "5", "*"],
            },
            "3": {
                "ops": self.select_item,
                "command_name": "Select an Item",
                "prompt": "Enter item number to make a selection:\n================================",
                "follow_ups": ["4", "5", "*"],
            },
            "4": {
                "ops": self.process_payment,
                "command_name": "Make a Payment",
                "prompt": "Enter your balance :\n================================",
                "follow_ups": ["1", "2", "3", "4", "5"],
            },
            "5": {
                "ops": quit,
                "command_name": "Exit",
                "prompt": "Goodbye and come again!\n================================",
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

    def select_item(self):
        # get prompt
        idx = int(input("Enter the number of the item you would like to select :"))

        if idx not in self.sales_logs:
            print(f"{idx} not offered by the Vending Machine")
            self.display_inventory()
        elif self.sales_logs[idx].status != "Available":
            print("This item is sold out!")
            self.display_available_items()
        else:
            self.selection = self.sales_logs[idx]
            print(
                f"You have selected {self.selection.name}, price : {self.selection.price}"
            )

    def _mark_sold(self):
        self.selection.status = "Sold out"
        self.selection = None

    def _check_selection(self):
        if bool(self.selection):
            return self.selection.status == "Available"
        return False

    def process_payment(self):
        balance = int(input("Enter the balance you have in your wallet :"))

        while not self.selection:
            self.select_item()

        print(f"processing your payment of : {balance} dollars ...")
        if balance < self.selection.price:
            print(f"Sorry,  your current balance is less than {self.selection.price}")
        else:
            changes = balance - self.selection.price
            self.selection.status = "Sold out"
            self.selection = None

            if changes > 0:
                print(f"Your change is {changes}")

    def show_prompt(self, operation):
        """
        operation is a nested dictionary object within control_flow_map
        """
        prompt = operation.get("prompt")
        print(prompt)

    def handle_command(self, command_input):
        """
        This method handles the user command input and call the method that handle the request
        """
        operation = self.control_flow_map[command_input]
        self.show_prompt(operation)

        ops = operation.get("ops")
        if ops:
            ops()

        for follow_up in operation.get("follow_ups", []):
            follow_up_operation = self.control_flow_map[follow_up]
            print(
                "Enter", follow_up, "to ", follow_up_operation["command_name"]
            )
            command_input = input()
            if command_input:
                self.handle_command(command_input)

 