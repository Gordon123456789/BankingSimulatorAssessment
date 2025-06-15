"""
Version 2
The following program is a banking simulator
Users must be 13 years old or over to use the simulator
Users can create an account, withdraw, and deposit, while not being able to overdraw
Users can also log into previously created accounts or create new accounts using account names and passwords
"""

#Option menu list
options = [
    "\n--- Bank Account Simulator ---",
    "1. Create or Login to different Account",
    "2. Check Balance",
    "3. Deposit",
    "4. Withdraw",
    "5. Show Transaction History",
    "6. Exit"
]

#Stores all account info
accounts = {}

#Tracks the account users currently logged into
current_account = None

#check users age eligibility
def check_age():
    while True:
        try:
            user_age = int(input("Enter your age (years): ")) #prompts user to input age
            if user_age <= 12:
                print("You need to be 13 years old or over\nExiting...")
                exit()
        except ValueError: #user enters non-integer
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
        else:
            break

    if account_name in accounts:
        #lets user try to login with password
        password = input("Enter your password: ")
        if password == accounts[account_name]["password"]:
            current_account = account_name
            print(f"Logged in as '{account_name}'.")
        else:
            print("Wrong password.")
    else:
        #make new account
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
    if current_account is None: #checks if user is logged into account
        print("Log in first.")
        return
    balance = accounts[current_account]["balance"] #gets balance of current logged in account
    print(f"\nBalance for {current_account}: ${balance}")
    print("\n----------------------------------------\n") #divider

#Add money function
def deposit():
    if current_account is None:
        print("Log in first.")
        return
    try:
        amount = float(input("Enter deposit amount: $")) #gets deposit amount from user
        if amount > 0: #adds deposit to current balance of current account logged in and records in history
            accounts[current_account]["balance"] += amount
            accounts[current_account]["transactions"].append(f"Deposited: ${amount}")
            accounts[current_account]["transactions_numbers"].append(amount)
            print(f"${amount} deposited.")
            print("\n----------------------------------------\n") #divider
        else: #user enters 0 or negative number
            print("Deposit must be positive")
    except ValueError: #user enters non number
        print("Enter numbers only.")

#Take out money function
def withdraw():
    if current_account is None:
        print("Log in first.")
        return
    try:
        amount = float(input("Enter amount to withdraw: $")) #gets withdrawal amount from user
        balance = accounts[current_account]["balance"]
        if amount <= 0:
            print("Withdraw must be positive")
        elif amount > balance: #checks if there is enough in balance to withdraw
            print(f"Not enough funds. Balance: ${balance}")
            accounts[current_account]["transactions"].append(f"Failed withdrawal: ${amount}")
        else: #withdraws from current account logged in and records in history
            accounts[current_account]["balance"] -= amount
            accounts[current_account]["transactions"].append(f"Withdrew: ${amount}")
            accounts[current_account]["transactions_numbers"].append(-amount)
            print(f"${amount} withdrawn.")
            print("\n----------------------------------------\n") #divider
    except ValueError:
        print("Invalid number.")

#Show actions user has made function
def show_history():
    if current_account is None: #checks if user has not logged into account
        print("Log in first.")
        return
    print(f"\nHistory for {current_account}:")
    for transaction in accounts[current_account]["transactions"]:
        print(transaction) #prints each transaction line in dictionary
    print(f"Current balance: ${accounts[current_account]['balance']}")
    print("\n----------------------------------------\n") #divider

#Main menu function
def main(): 
    print("\n----------------------------------------")
    while True:
        for option in options:
            print(option)
        choice = input("Select an option (1-6): ")
        if choice == "1": #login to account
            create_or_login_account()
        elif choice == "2": #check balance
            check_balance()
        elif choice == "3": #deposit
            deposit()
        elif choice == "4": #withdraw
            withdraw()
        elif choice == "5": #show history
            show_history()
        elif choice == "6": #exit
            print("Exiting...!")
            print("----------------------------------------")
            break
        else: #boundary or invalid input
            print("Pick a number from 1 to 6. (integers only)")
            print("\n----------------------------------------")

#Calling functions
check_age()
main()