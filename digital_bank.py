import datetime
import yfinance as yf

class BankAccount:
    def __init__(self, account_number, name, balance=0, limit=0, password=''):
        self.account_number = account_number
        self.name = name
        self.balance = balance
        self.limit = limit
        self.password = password

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("The deposit amount must be greater than zero.")
        self.balance += amount

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("The withdrawal amount must be greater than zero.")
        if self.balance - amount < -self.limit:
            raise ValueError("Invalid operation: Insufficient balance.")
        self.balance -= amount

    def check_balance(self):
        return self.balance

    def check_limit(self):
        return self.limit

    def verify_password(self, password):
        return self.password == password

    def invest(self):
        print("\nStocks available for investment:")

        # List of predefined stocks
        stocks = {
            "Microsoft Corporation": "MSFT",
            "Apple Inc.": "AAPL",
            "Amazon.com Inc.": "AMZN",
            "Alphabet Inc.": "GOOGL",
            "Facebook Inc.": "FB",
            "Tesla Inc.": "TSLA",
            "Netflix Inc.": "NFLX",
            "NVIDIA Corporation": "NVDA",
            "JPMorgan Chase & Co.": "JPM",
            "Visa Inc.": "V"
        }

        for company, stock_code in stocks.items():
            print(f"- Company: {company} - Code: {stock_code}")
            

        print("To discover new stocks, visit: https://finance.yahoo.com/most-active")

        ticker = input("Type in the stock code: ")
        amount_stocks = int(input("Enter the number of stocks to be purchased: "))

        try:
            stock = yf.Ticker(ticker)
            stock_price = stock.info["ask"]

            amount_value = stock_price * amount_stocks

            if amount_value <= self.balance:
                self.balance -= amount_value
                print(f"Investment made successfully! You bought {amount_stocks} stocks of {ticker}.")
            else:
                print("Insufficient balance to carry out the investment.")

        except ValueError as e:
            print("Error:", str(e))


class Bank:
    def __init__(self):
        self.accounts = {}

    def create_account(self, account_number, name, initial_balance, limit, password):
        if account_number in self.accounts:
            raise ValueError("Existing account number.")
        if initial_balance < 0:
            raise ValueError("The opening balance cannot be negative.")
        if limit < 0:
            raise ValueError("The limit cannot be negative.")
        if len(password) != 6 or not password.isdigit():
            raise ValueError("The password must consist of 6 numbers.")
        if initial_balance > limit:
            raise ValueError("The limit cannot be less than the starting balance.")
        self.accounts[account_number] = BankAccount(account_number, name, initial_balance, limit, password)
        print("Account successfully created.")

    def delete_account(self, account_number):
        if account_number in self.accounts:
            del self.accounts[account_number]
            print("Account deleted successfully.")
        else:
            print("Account not found.")

    def get_account(self, account_number):
        if account_number in self.accounts:
            return self.accounts[account_number]
        else:
            raise ValueError("Account not found.")


def print_menu():
    print("Menu:")
    print("1. Create account")
    print("2. Access account")
    print("3. Delete account")
    print("4. Exit")

def print_account_menu(name):
    now = datetime.datetime.now()
    hour = now.hour

    if 6 <= hour < 12:
        greeting = "Good Morning"
    elif 12 <= hour < 18:
        greeting = "Good Afternoon"
    else:
        greeting = "Good Evening"

    print(f"\n{greeting}, {name}!")
    print("\nAccount Menu:")
    print("1. Make deposit")
    print("2. Withdraw")
    print("3. Check balance")
    print("4. Check limit")
    print("5. Invest")
    print("6. Back to main menu")


def main():
    bank = Bank()
    print("Welcome to Digital Bank!")

    while True:
        #print()
        print_menu()
        choice = input("Choose an option (1-4): ")

        if choice == "1":
            account_number = int(input("Enter account number: "))
            name = input("Enter the owner's name: ")
            initial_balance = float(input("Enter the opening balance: "))
            limit = float(input("Enter the limit: "))
            password = input("Type the password (6 numbers): ")
            try:
                bank.create_account(account_number, name, initial_balance, limit, password)
            except ValueError as e:
                print("Error:", str(e))

        elif choice == "2":
            account_number = int(input("Enter account number: "))
            try:
                account = bank.get_account(account_number)
                if account:
                    password = (input("Type the password: "))
                    if account.verify_password(password):
                        print_account_menu(account.name)  # Displays the welcome message
                        while True:
                            print()
                            print_account_menu(account.name)
                            account_choice = input("Choose an option (1-6): ")
                            if account_choice == "1":
                                amount = float(input("Enter the deposit amount: "))
                                try:
                                    destination_account = int(input("Enter the target account number: "))
                                    if destination_account in bank.accounts:
                                        dest_account = bank.get_account(destination_account)
                                        account.withdraw(amount)
                                        dest_account.deposit(amount)
                                        print("Deposit successfully made to the target account.")
                                    else:
                                        print("Target account not found.")
                                except ValueError as e:
                                    print("Error:", str(e))
                            elif account_choice == "2":
                                amount = float(input("Enter the withdrawal amount: "))
                                try:
                                    account.withdraw(amount)
                                    print("Withdrawal completed successfully.")
                                except ValueError as e:
                                    print("Error:", str(e))
                            elif account_choice == "3":
                                balance = account.check_balance()
                                print("Balance:", balance)
                            elif account_choice == "4":
                                limit = account.check_limit()
                                print("LImit:", limit)
                            elif account_choice == "5":
                                account.invest()
                            elif account_choice == "6":
                                break
                            else:
                                print("Invalid option. Try again.")
                    else:
                        print("Incorrect password.")
            except ValueError as e:
                print("Error:", str(e))

        elif choice == "3":
            account_number = int(input("Enter account number: "))
            bank.delete_account(account_number)

        elif choice == "4":
            print("Closing the program...")
            break

        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()
