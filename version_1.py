"""
Version 1
The following program is a simple banking simulator
Users can create an account, withdraw, and deposit, while not being able to overdraw
"""

#Option menu list
options = [
            "\n--- Bank Account Simulator ---",
            "1. Create Account",
            "2. Deposit",
            "3. Withdraw",
            "4. Show Transaction History",
            "5. Exit"]

#Defining variables
balance = 0
transactions = []
account_created = 1
account_name = ""

def create_account():
    global balance, transactions, account_created, account_name 
    print("\n----------------------------------------\n") #divider
    if account_created == 2: #checks if user has already created account
        print("You have already created an account") 
        return #returns user to option menu
    
    while True: 
        account_name = input("Enter account name: ") #asks user for account name input
        if account_name == "": #returns user if account name is blank
            print("You must enter a name.")
        else:
            break

    while True:
        try:
            balance = float(input("Enter starting balance: $")) #asks user for starting balance input
            if balance < 0: #if user enters negative number prompts user for input again
                print("Balance must be positive.") 
                continue
            transactions = []
            account_created = 2 #tells the code that user has created an account
            print(f"You have created an account called {account_name} with a balance of ${balance}")
            print("\n----------------------------------------") #divider
            break
        except ValueError: #user enters a non-number
            print("Invalid input. Please enter a number.")

def deposit():
    global balance
    print("\n----------------------------------------\n") #divider
    if account_created == 1: #checks if user has not created an account
        print("Please create an account first.")
        return #returns user to menu
    try:
        amount = float(input("Enter amount to deposit: $")) #asks user to input amount they want to deposit into account
        if amount > 0:
            balance += amount #adds deposit amount to user balance
            transactions.append(f"Deposited: ${amount}")
            print(f"${amount} has been deposited successfully.")
        else: #user enters negative or 0 for deposit amount
            print("Deposit must be positive.") 
    except ValueError: #user enters a non number
        print("Invalid input.")

def withdraw():
    global balance
    print("\n----------------------------------------\n") #divider
    if account_created == 1: #checks if user has not created an account
        print("Please create an account first.")
        return
    try:
        amount = float(input("Enter amount to withdraw: $")) #asks user to input withdraw amount
        if amount <= 0: #user enters 0 or negative number for amount
            print("Withdrawal amount must be positive.")
        elif amount > balance: #user is overdrawing funds
            print("Insufficient funds. Withdrawal canceled.")
            print("\n----------------------------------------\n") #divider
            transactions.append(f"Failed withdrawal attempt: ${amount} (Insufficient funds)")
        else:
            balance -= amount #subtracts user withdraw amount from balance
            transactions.append(f"Withdrew: ${amount}")
            print(f"${amount} withdrawn successfully.")
            print("\n----------------------------------------\n") #divider
    except ValueError:
        print("Invalid input.")

def show_history():
    print("\n----------------------------------------\n") #divider
    if account_created == 1: #checks if user has not created an account
        print("Please create an account first.")
        return
    print("\nTransaction History:")
    for transaction in transactions: #prints each transaction user has made from transactions list
        print(transaction)
    print(f"Your current balance is: ${balance}\n") #tells user balance after transaction list


def main():
    print("\n----------------------------------------") #divider
    while True:
        for option in options: #prints each line in options
            print(option) 
        choice = input("Select an option (1-5): ") #asks for users option choice input
        if choice == "1":
            create_account()
        elif choice == "2":
            deposit()
        elif choice == "3":
            withdraw()
        elif choice == "4":
            show_history()
        elif choice == "5":
            print("Exiting the simulator...")
            print("----------------------------------------") #divider
            quit() #exits program
        else:
            print("Invalid choice, Choose from 1-5. (integers only)") #user enters a non number or a boundary input
            print("\n----------------------------------------") #divider

#Calling function
main()
