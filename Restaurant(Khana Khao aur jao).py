import math

class ATM:
    def __init__(self, balance=100000, pin="1234"):
        if not math.isfinite(balance) or balance < 0:
            raise ValueError("Starting balance must be zero or more.")
        if not pin or not pin.isdigit():
            raise ValueError("PIN must contain digits only.")

        self.balance = balance
        self.pin = pin

    def check_pin(self):
        attempts = 0
        while attempts < 3:
            entered_pin = input("Enter your ATM PIN: ")
            if entered_pin == self.pin:
                print("Access granted.")
                return True

            print("Incorrect PIN.")
            attempts += 1

        print("Access denied. Too many incorrect attempts.")
        return False

    def show_balance(self):
        if self.check_pin():
            print(f"Current balance: Rs. {self.balance:,.2f}")

    def get_amount(self, prompt):
        try:
            amount = float(input(prompt))
        except ValueError:
            print("Please enter a valid number.")
            return None

        if not math.isfinite(amount) or amount <= 0:
            print("Enter an amount greater than zero.")
            return None
        return amount

    def deposit(self, amount):
        if self.check_pin():
            self.balance += amount
            print(f"Deposited: Rs. {amount:,.2f}")
            print(f"Current balance: Rs. {self.balance:,.2f}")

    def withdraw(self, amount):
        if not self.check_pin():
            return
        if amount > self.balance:
            print("Insufficient funds.")
            return

        self.balance -= amount
        print(f"Withdrawn: Rs. {amount:,.2f}")
        print(f"Current balance: Rs. {self.balance:,.2f}")

    def pay(self, amount):
        if not self.check_pin():
            return False
        if amount > self.balance:
            print("Insufficient funds.")
            return False

        self.balance -= amount
        print(f"Payment successful: Rs. {amount:,.2f}")
        print(f"Remaining balance: Rs. {self.balance:,.2f}")
        return True


class Restaurant:
    def __init__(self):
        self.atm = ATM()
        self.products = [
            ("Starter", (
                ("Masala Papad", 150),
                ("Gobi Manchurian", 250),
                ("Paneer Chili", 300),
                ("Baby Corn", 120),
                ("Chicken Lollipop", 350),
                ("Chicken 65", 300),
                ("Veg Spring Roll", 200),
                ("Chicken Spring Roll", 250),
                ("Go back", 0),
            )),
            ("Main Course", (
                ("Butter Chicken", 450),
                ("Veg Biryani", 250),
                ("Chicken Biryani", 350),
                ("Paneer Tikka Masala", 400),
                ("Chicken Tikka", 350),
                ("Paneer Butter Masala", 400),
                ("Roti", 20),
                ("Butter Roti", 30),
                ("Butter Naan", 40),
                ("Naan", 30),
                ("Jeera Rice", 150),
                ("Veg Pulao", 200),
                ("Go back", 0),
            )),
            ("Dessert", (
                ("Gulab Jamun", 100),
                ("Rasgulla", 50),
                ("Ice Cream", 80),
                ("Chocolate Brownie", 150),
                ("Go back", 0),
            )),
            ("Soup", (
                ("Tomato Soup", 100),
                ("Mushroom Soup", 120),
                ("Vegetable Soup", 100),
                ("Manchow Soup", 150),
                ("Chicken Soup", 250),
                ("Go back", 0),
            )),
            ("Beverage", (
                ("Coca Cola", 50),
                ("Pepsi", 50),
                ("Fanta", 50),
                ("Sprite", 50),
                ("Tea", 30),
                ("Coffee", 40),
                ("Ice Tea", 60),
                ("Lemonade", 70),
                ("Cold Coffee", 100),
                ("Go back", 0),
            )),
        ]
    def get_number(self, prompt):
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a valid number.")
            return None

    def print_bill(self, cart):
        total = 0
        print("\n" + "=" * 50)
        print("          KHANA KHAO AUR JAO")
        print("                 CUSTOMER BILL")
        print("=" * 50)

        for category, product, quantity in cart:
            name, price = product
            item_total = price * quantity
            total += item_total
            print(f"{category}: {name}")
            print(f"Price: Rs. {price:,}  Quantity: {quantity}")
            print(f"Item total: Rs. {item_total:,}")
            print("-" * 50)

        print(f"TOTAL AMOUNT: Rs. {total:,}")
        print("=" * 50)
        return total

    def online_banking(self, bill_total=None):
        while True:
            print("\nOnline Banking")
            options = (
                ("1. Check Balance", 1),
                ("2. Deposit Money", 2),
                ("3. Pay Bill", 3),
            )
            if bill_total is None:
                options += (("4. Exit", 4),)

            for label, _ in options:
                print(label)

            maximum_choice = len(options)
            choice = self.get_number(
                f"Choose an option (1-{maximum_choice}): "
            )
            if choice == 1:
                self.atm.show_balance()
            elif choice == 2:
                amount = self.atm.get_amount("Enter deposit amount: ")
                if amount is not None:
                    self.atm.deposit(amount)
            elif choice == 3:
                if bill_total is None:
                    print("A bill has not been prepared yet.")
                elif self.atm.pay(bill_total):
                    return True
            elif choice == 4 and bill_total is None:
                return False
            else:
                print(f"Choose a number from 1 to {maximum_choice}.")

    def run(self):
        cart = []
        categories = []
        for category, products in self.products:
            categories.append(category)

        print("="*50)
        print("Welcome to KHANA KHAO AUR JAO!")
        print("="*50)

        while True:
            print("\nRestaurant Menu")
            for category_number, (category, products) in enumerate(self.products, 1):
                print(f"\n{category_number}. {category}")

            print("\n" + "-" * 50)
            print("BANKING OPTIONS")
            print("B. Online Banking")
            print("C. Go to billing")
            print("\n" + "-" * 50)

            choice = input(
                f"Choose a food category (1-{len(categories)}), B for banking, "
                "or C for billing: "
            ).strip().lower()
            if choice == "b":
                self.online_banking()
                continue
            if choice == "c":
                if not cart:
                    print("There are no food items in the cart.")
                    continue

                total = self.print_bill(cart)
                if self.online_banking(total):
                    print("Thank you for dining with us!")
                else:
                    print("Payment was not completed.")
                return

            try:
                choice = int(choice)
            except ValueError:
                print("Invalid Choice.")
                continue

            if choice < 1 or choice > len(self.products):
                print("Invalid Choice.")
                continue

            category, products = self.products[choice - 1]

            print(f"\n{category}")
            for number, product in enumerate(products, 1):
                print(f"{number}. {product[0]} - Rs. {product[1]:,}")

            product_choice = self.get_number("Choose a product: ")
            while product_choice is None or not 1 <= product_choice <= len(products):
                print("Invalid Choice.")
                product_choice = self.get_number("Choose a product: ")

            if products[product_choice - 1][0] == "Go back":
                continue

            quantity = self.get_number("Enter quantity: ")
            if quantity is None or quantity <= 0:
                print("Quantity must be greater than zero.")
                return

            cart.append((category, products[product_choice - 1], quantity))
            answer = input("Order more food? (yes/no): ").strip().lower()

            while answer not in ("yes", "y", "no", "n"):
                answer = input("Please answer yes or no: ").strip().lower()

if __name__ == "__main__":
    Restaurant().run()