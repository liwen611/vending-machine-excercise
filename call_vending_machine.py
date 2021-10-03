from pprint import pprint
from vending_machine import VendingMachine

# sustaintiate a venching machine class object
vm = VendingMachine()
vm.get_inventory("inventory.csv")

if __name__ == "__main__":
    vm.handle_command("*")