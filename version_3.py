import matplotlib.pyplot as plt

"""
Version 3
The following program is an advanced banking simulator
Users must be 13 years old or over to use the simulator
Users can create an account, withdraw, and deposit, while not being able to overdraw
Users can also log into previously created accounts or create new accounts using account names and passwords
Users are able to view their balance over time visually (on a graph)
"""

#Menu text
options = [
    "\n--- Bank Account Simulator ---",
    "1. Create or Login to different Account",
    "2. Check Balance",
    "3. Deposit",
    "4. Withdraw",
    "5. Show Transaction History",
    "6. Show Transaction History Graph",
    "7. Exit"
]

#Stores all account info
accounts = {}

#Tracks the account users currently logged into
current_account = None

#check users age eligibility
def check_age():
    user_age = int()
    while True:
        try:
            user_age = int(input("Enter your age (years): "))
            if user_age <= 12: #checks if user is below 13 years old
                print("You need to be 13 years old or over\nExiting...")
                exit()
        except ValueError: #catches if user enters non-integer
            print("Please enter integers only")
        else:
          print("You are old enough to use the simulator")
          break
          
#login or create a new account function
def create_or_login_account():
    global current_account
    print("\n----------------------------------------\n") #divider
    while True:
        account_name = input("Enter account name: ").strip() #asks user for account name and clears all spaces on outsides

        if account_name == "": #returns user if account name is blank
            print("You must enter a name.")
            return
        else:
            break

    if account_name in accounts:
        #lets user try to login with password
        password = input("Enter your password: ")
        if password == accounts[account_name]["password"]: #checks if password matches the one stored
            current_account = account_name
            print(f"Logged in as '{account_name}'.")
        else:
            print("Wrong password.")
    else: #creates new account if account name does not already exit
        while True:
            password = input("Set a password: ").strip() #removes leading/trailing spaces from user password
            if password == "": #checks if user password is blank
                print("Password can't be empty.")
            else:
                break
        while True:
            try:
                balance = float(input("Enter starting balance: $"))
                if balance < 0: #checks if user balance is negative
                    print("Balance must be positive.")
                    continue
                #saves user account details in dictionary
                accounts[account_name] = {
                    "password": password,
                    "balance": balance,
                    "transactions": [],
                    "transactions_numbers": []
                }
                current_account = account_name #sets this account as currently logged in account
                print(f"Account '{account_name}' created with ${balance}")
                break
            except ValueError:
                print("Enter a valid number.")
    print("\n----------------------------------------\n") #divider

#Show current balance function
def check_balance():
    if current_account is None:
        print("Log in first.")
        return
    balance = accounts[current_account]["balance"] #accesses balance from dictionary
    print(f"\nBalance for {current_account}: ${balance}")

#function to deposit
def deposit():
    if current_account is None: #checks if user has not made account
        print("Log in first.")
        return
    try:
        amount = float(input("Enter deposit amount: $"))
        if amount > 0: #updates new balance and stores deposit amount in history
            accounts[current_account]["balance"] += amount
            accounts[current_account]["transactions"].append(f"Deposited: ${amount}")
            accounts[current_account]["transactions_numbers"].append(amount)
            print(f"${amount} deposited.")
        else: #checks if user has entered 0 or negative for deposit amount
            print("Deposit must be positive")
    except ValueError: #checks if user has entered non-number
        print("Enter numbers only.")

#function to withdraw
def withdraw():
    if current_account is None: #checks if user has not made account
        print("Log in first.")
        return
    try:
        amount = float(input("Enter amount to withdraw: $")) #asks user for withdrawal amount
        balance = accounts[current_account]["balance"]
        if amount <= 0: #checks if user has entered 0 or negative for withdraw amount
            print("Withdrawal must be positive")
        elif amount > balance: #checks if amount user wants to withdraw is above balance
            print(f"Not enough funds. Balance: ${balance}")
            accounts[current_account]["transactions"].append(f"Failed withdrawal: ${amount}")
        else: #subtracts withdraw amount from balance and updates history
            accounts[current_account]["balance"] -= amount
            accounts[current_account]["transactions"].append(f"Withdrew: ${amount}")
            accounts[current_account]["transactions_numbers"].append(-amount)
            print(f"${amount} withdrawn.")
    except ValueError: #checks if user has entered non-number
        print("Enter numbers only.")

#Show actions user has made function
def show_history():
    if current_account is None: #checks if user has not made account
        print("Log in first.")
        return
    print(f"\nHistory for {current_account}:")
    for transaction in accounts[current_account]["transactions"]:
        print(transaction) #prints each transaction from dictionary
    print(f"Current balance: ${accounts[current_account]['balance']}") #prints current balance for account logged into from dictionary


#Main menu function
def main(): 
    print("\n----------------------------------------")
    while True:
        for option in options:
            print(option)
        choice = input("Select an option (1-7): ")

        if choice == "1": #check age and create new account
            check_age()
            create_or_login_account()
        elif choice == "2": #check balance
            check_balance()
        elif choice == "3": #deposit
            deposit()
        elif choice == "4": #withdraw
            withdraw()
        elif choice == "5": #transaction history
            show_history()
        elif choice == "6": #transactions graph
            plot_transactions()
        elif choice == "7": #exit
            print("Exiting...")
            print("----------------------------------------")
            break
        else:
            print("Pick a number from 1 to 7.") #user enters invalid or boundary input
            print("\n----------------------------------------")

#Calling function
main()