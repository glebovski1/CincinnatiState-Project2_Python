import sys
import os
from datetime import datetime
from classes import Customer, Store, Rental


class RentalUILogic:
    """
    Manages operations of the ski and snowboard rental system, including inventory checks,
    rental creation, return processing, and revenue tracking.
    """

    def __init__(self):
        """
        Initializes the RentalUILogic.

        Attributes:
            shop (Store): The Store instance representing inventory of skis and snowboards.
            customer_rentals (dict): Active rentals keyed by customer ID.
            daily_ski_rentals (int): Count of skis rented today.
            daily_snowboard_rentals (int): Count of snowboards rented today.
            revenu (float): Total revenue collected from completed rentals.
        """
        self.shop: Store
        self.customer_rentals = {}
        self.daily_ski_rentals = 0
        self.daily_snowboard_rentals = 0
        self.revenu: float = 0.0

    def get_rental_type_str_from_int(self, rental_type: int) -> str:
        """
        Converts an integer rental type to its string label.

        Args:
            rental_type (int): Type of rental (1 = Hourly, 2 = Daily, 3 = Weekly).

        Returns:
            str: 'Hourly', 'Daily', or 'Weekly'.
        """
        if rental_type == 1:
            return "Hourly"
        if rental_type == 2:
            return "Daily"
        if rental_type == 3:
            return "Weekly"
        return ""

    def get_period_str(self, period: int, rental_type: int) -> str:
        """
        Returns a descriptive string for the rental period.

        Args:
            period (int): Length of the rental period.
            rental_type (int): Type of rental (1 = Hours, 2 = Days, 3 = Weeks).

        Returns:
            str: e.g. '5 Hours', '3 Days', '2 Weeks'.
        """
        if rental_type == 1:
            unit = "Hours"
        elif rental_type == 2:
            unit = "Days"
        elif rental_type == 3:
            unit = "Weeks"
        else:
            unit = ""
        return f"{period} {unit}"

    def get_current_skis(self) -> int:
        """
        Returns the number of skis currently available.
        """
        return self.shop.CurrentSki

    def get_current_snowboards(self) -> int:
        """
        Returns the number of snowboards currently available.
        """
        return self.shop.CurrentSnow

    def set_shop(self, skis: int, snowboards: int):
        """
        Initializes the store inventory and displays it.

        Args:
            skis (int): Total number of skis in stock.
            snowboards (int): Total number of snowboards in stock.
        """
        self.shop = Store(skis, snowboards)
        self.shop.Display_Inv()

    def estimate(self, skis: int, snowboards: int, rental_type: int,
                 rental_period: int, discount_code: str) -> str:
        """
        Provides an estimate for a potential rental.

        Args:
            skis (int): Number of skis requested.
            snowboards (int): Number of snowboards requested.
            rental_type (int): Type of rental (1 = Hourly, 2 = Daily, 3 = Weekly).
            rental_period (int): Duration of the rental.
            discount_code (str): Discount code, if any.

        Returns:
            str: Formatted estimate details.
        """
        rental = Rental("Estimate", self.shop, skis, snowboards)
        rental.estimateRental(rental_type, rental_period)

        lines = [
            "--- Order Estimate ---",
            f"Skis: {skis}",
            f"Snowboards: {snowboards}",
            f"Rental Type: {self.get_rental_type_str_from_int(rental_type)}",
            f"Period: {self.get_period_str(rental_period, rental_type)}",
            f"Discount Code: {discount_code}",
            f"Estimated Cost: ${rental.rentalEstimate:.2f}"
        ]
        return "\n".join(lines)

    def is_inventory_sufficient(self, skis: int, snowboards: int) -> bool:
        """
        Checks if requested equipment is available.

        Args:
            skis (int): Skis requested.
            snowboards (int): Snowboards requested.

        Returns:
            bool: True if available, False otherwise.
        """
        return self.shop.CurrentSki >= skis and self.shop.CurrentSnow >= snowboards

    def is_customer_id_valid(self, customer_id: str) -> bool:
        """
        Validates that the customer ID is not already used.

        Args:
            customer_id (str): Proposed customer ID.

        Returns:
            bool: True if not in use, False otherwise.
        """
        return customer_id not in self.customer_rentals

    def new_rental(
        self,
        customer_id: str,
        customer_name: str,
        skis_amount: int,
        snowboards_amount: int,
        rental_type: int,
        rent_time: datetime,
        discount_code: str = ""
    ) -> str:
        """
        Processes a new rental if validation passes.

        Args:
            customer_id (str): Unique customer ID.
            customer_name (str): Customer's name.
            skis_amount (int): Number of skis.
            snowboards_amount (int): Number of snowboards.
            rental_type (int): Rental type.
            rent_time (datetime): Start time of rental.
            discount_code (str, optional): Discount code.

        Returns:
            str: Rental summary or failure message.
        """
        try:
            customer = Customer(customer_name, customer_id)
            if (self.is_inventory_sufficient(skis_amount, snowboards_amount)
                    and self.is_customer_id_valid(customer_id)):
                result = customer.RequestEquipment(skis_amount, snowboards_amount, self.shop)
                if result != -1:
                    rental = Rental(customer, self.shop, skis_amount, snowboards_amount)
                    if skis_amount > 0:
                        rental.rentSkis(rental_type)
                        self.daily_ski_rentals += skis_amount
                    if snowboards_amount > 0:
                        rental.rentSnowboards(rental_type)
                        self.daily_snowboard_rentals += snowboards_amount
                    rental.rentalTime = rent_time

                    self.customer_rentals[customer_id] = {
                        'customer': customer,
                        'rental': rental,
                        'rental_type': rental_type,
                        'skis': skis_amount,
                        'snowboards': snowboards_amount,
                        'discountCode': discount_code
                    }

                    summary = [
                        "Order Summary",
                        f"Skis: {skis_amount}",
                        f"Snowboards: {snowboards_amount}",
                        f"Rental Type: {self.get_rental_type_str_from_int(rental_type)}",
                        f"Started: {rent_time}",
                        f"Discount Code: {discount_code}"
                    ]
                    return "\n".join(summary)
                return "Rental failed"
            return "Inventory is not sufficient. Rental failed"
        except Exception as e:
            return str(e)

    def return_rental(self, customer_id: str, return_time: datetime) -> str:
        """
        Processes a rental return and generates an invoice.

        Args:
            customer_id (str): ID of the customer returning equipment.
            return_time (datetime): Return time.

        Returns:
            str: Return invoice or error message.
        """
        if customer_id not in self.customer_rentals:
            return "Such ID does not exist"

        info = self.customer_rentals.pop(customer_id)
        rental = info['rental']
        customer = info['customer']
        rental_type = info['rental_type']
        discount_code = info['discountCode']

        rental.calculateRentalCost(rental_type, return_time)
        subtotal = rental.SubTotal
        rental.familyDiscount()
        rental.discountCode(discount_code)
        final_cost = rental.finalCost()

        rental.returnInv()
        self.revenu += final_cost

        duration = return_time - rental.rentalTime
        days = duration.days
        secs = duration.seconds
        hours, rem = divmod(secs, 3600)
        minutes, seconds = divmod(rem, 60)

        invoice = [
            "RENTAL RETURN INVOICE",
            f"Customer Name: {customer.name}",
            "Equipment Rented:",
            f"  Skis: {info['skis']}",
            f"  Snowboards: {info['snowboards']}",
            f"Duration: {days} days, {hours} hours, {minutes} minutes, {seconds} seconds",
            f"Subtotal: ${subtotal:.2f}",
            f"Final Total: ${final_cost:.2f}"
        ]
        return "\n".join(invoice)


class RentalUI:
    """
    Manages the user interface for the ski and snowboard rental system.
    """

    def __init__(self, debug: bool = False):
        """
        Initializes the RentalUI and sets up inventory.

        Args:
            debug (bool): If True, allows manual time entry.
        """
        self.debug = debug
        self.logic = RentalUILogic()
        self.build_store()

    def build_store(self) -> None:
        """
        Prompts for initial inventory and initializes the store.
        """
        print("-------------------------")
        print(" Set up shop inventory ")
        skis = int(self.validate_int_input("Enter number of skis: "))
        snowboards = int(self.validate_int_input("Enter number of snowboards: "))
        if skis < 0 or snowboards < 0:
            print("Inventory should be non-negative.")
            return self.build_store()
        self.logic.set_shop(skis, snowboards)

    def wait(self):
        """
        Pauses until the user presses a key.
        """
        input("Press any key to continue...")

    def yes_no(self, question: str) -> bool:
        """
        Prompts a yes/no question.

        Args:
            question (str): The question to ask.

        Returns:
            bool: True for 'y', False for 'n'.
        """
        while True:
            ans = input(question + " (y/n): ")
            if ans.lower() == 'y':
                return True
            if ans.lower() == 'n':
                return False
            print("Invalid input, please enter 'y' or 'n'.")

    def clear_console(self) -> None:
        """
        Clears the console screen.
        """
        os.system('cls')

    def validate_int_input(self, prompt: str, allow_zero: bool = False) -> int:
        """
        Validates integer input, optionally allowing zero.

        Args:
            prompt (str): Prompt message.
            allow_zero (bool): If True, zero is permitted.

        Returns:
            int: The validated integer.
        """
        while True:
            try:
                value = int(input(prompt))
                if value < 0 or (not allow_zero and value == 0):
                    print("Please enter a positive number.")
                    continue
                return value
            except ValueError:
                print("That's not a valid number. Please try again.")

    def validate_rental_type(self) -> int:
        """
        Prompts for and validates rental type.

        Returns:
            int: 1 for Hourly, 2 for Daily, 3 for Weekly.
        """
        while True:
            try:
                val = int(input("Enter rental type (1=Hourly, 2=Daily, 3=Weekly): "))
                if val in (1, 2, 3):
                    return val
                print("Please enter 1, 2, or 3.")
            except ValueError:
                print("That's not a valid number. Please try again.")

    def get_time_input(self) -> datetime:
        """
        Returns current time or prompts manually if debug is on.

        Returns:
            datetime: The selected datetime.
        """
        if self.debug:
            while True:
                try:
                    month, day, year, hour, minute = map(int, input(
                        "Enter date and time (M:D:Y:HH:MM): ").split(':'))
                    return datetime(year, month, day, hour, minute)
                except ValueError:
                    print("Invalid format. Use M:D:Y:HH:MM.")
        return datetime.now()

    def main_menu(self):
        """
        Displays the main menu and handles user choice.
        """
        self.clear_console()
        print("=== Ski & Snowboard Rental System ===")
        print("1. New Customer Rental")
        print("2. Rental Return")
        print("3. Show Inventory")
        print("4. End of Day")
        choice = input("Enter your choice: ")

        if choice == "1":
            self.new_customer_rental()
        elif choice == "2":
            self.rental_return()
        elif choice == "3":
            self.show_inventory()
        elif choice == "4":
            self.end_of_day()
        else:
            print("Invalid choice. Please try again.")
            self.wait()
            self.main_menu()

    def new_customer_rental(self):
        """
        Handles a new customer rental workflow.
        """
        name = input("Enter customer name: ")
        cust_id = self.validate_int_input("Enter customer ID: ")
        skis = self.validate_int_input("Enter skis to rent: ", True)
        boards = self.validate_int_input("Enter snowboards to rent: ", True)

        if not self.logic.is_inventory_sufficient(skis, boards):
            print("Inventory is not sufficient.")
            self.wait()
            return self.main_menu()

        rtype = self.validate_rental_type()
        period = self.validate_int_input(
            f"Enter rental duration (hours/days/weeks): ", True)
        code = input("Enter discount code (or press Enter): ")

        if self.yes_no("Show estimate?"):
            print(self.logic.estimate(skis, boards, rtype, period, code))

        if self.yes_no("Complete rental?"):
            current_time = self.get_time_input()
            self.clear_console()
            print(self.logic.new_rental(
                str(cust_id), name, skis, boards, rtype, current_time, code
            ))
            self.wait()
        self.main_menu()

    def rental_return(self):
        """
        Handles returning equipment and showing the invoice.
        """
        cust_id = self.validate_int_input("Enter customer ID: ")
        return_time = self.get_time_input()
        self.clear_console()
        print(self.logic.return_rental(str(cust_id), return_time))
        self.wait()
        self.main_menu()

    def show_inventory(self):
        """
        Displays the current inventory.
        """
        skis = self.logic.get_current_skis()
        boards = self.logic.get_current_snowboards()
        print("------ Inventory ------")
        print(f"Skis: {skis}")
        print(f"Snowboards: {boards}")
        self.wait()
        self.main_menu()

    def end_of_day(self):
        """
        Shows end-of-day report and exits the program.
        """
        self.clear_console()
        print("END OF DAY REPORT")
        print("=" * 30)
        print(f"Total Skis Rented Today: {self.logic.daily_ski_rentals}")
        print(f"Total Snowboards Rented Today: {self.logic.daily_snowboard_rentals}")
        print(f"Total Revenue Collected: ${self.logic.revenu:.2f}")
        print("=" * 30)
        print("Thank you for using the rental system! Goodbye!")
        sys.exit()


if __name__ == "__main__":
    ui = RentalUI(debug=True)
    ui.main_menu()
