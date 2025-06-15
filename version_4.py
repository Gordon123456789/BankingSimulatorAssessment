import matplotlib.pyplot as plt
from easygui import *

"""
Version 4
The following program is an advanced banking simulator
Users must be 13 years old or over to use the simulator
Users can create an account, withdraw, and deposit, while not being able to overdraw
Users can also log into previously created accounts or create new accounts using account names and passwords
Users are able to view their balance over time visually (on a graph)
This program is written with EasyGui
"""

#Menu text
options=[
    "Create/Login Account",
    "Check Balance",
    "Deposit",
    "Withdraw",
    "Show Transaction History",
    "Show Transaction Graph",
    "Exit"]

#Stores all account info
accounts = {}

#Tracks the account users currently logged into
current_account = None

#Constants
MIN_AGE = 13
MIN_TRANSACTION_AMOUNT = 0
MIN_STARTING_BALANCE = 0

#Check users age eligibility
def check_age():
    """
    Checks to see if user is at least 13 years old
    Exits the program if they are under 13, otherwise continues
    """
    age = int()
    while True:
        age = integerbox("Enter your age (years):", "Age Check") #asks for user to input age 
        if age is None: #checks if age input is blank
            msgbox("You must enter your age", "Error")
            continue
        if age < MIN_AGE: #checks if user is below 13 years old
            msgbox(f"You need to be {MIN_AGE} years or older. Exiting...", "Below Age Requirement")
            exit() #exits program
        else:
            msgbox("You are old enough to use the simulator", "Welcome")
            break

#login or create a new account function
def create_or_login_account(current_account):
    """
    Lets user login to an existing account or create a new one
    Lets user set password to account name
    """
    while True:
        #Asks for account name first to check if it exists
        account_name = enterbox("Enter account name:", "Account Login/Create")
        if not account_name: #checks if user does not enter an account name (blank)
            msgbox("You must enter an account name", "Error")
        else: #breaks loop if account name is valid
            break

    if account_name in accounts: #checks to see if account name is same as one already made
        while True:
            #lets user try to login with password
            password = passwordbox("Enter your password:", "Login") #asks user to input password set for that account name
            if password == accounts[account_name]["password"]: #checks if password is same as one set for that account name
                current_account = account_name #sets current account as the account logged in
                msgbox(f"Logged in as '{account_name}'.", "Login Success")
                break
            else: #password is incorrect
                msgbox("Wrong password.", "Login Failed")
    else:
        while True:
            while True:
                #Ask for account name and password in one box
                msg = "Create a new account"
                title = "New Account Setup"
                fields = ["Account Name", "Password"]
                values = [account_name, ""] 
                input_values = multenterbox(msg, title, fields, values) #formats the multenterbox
                if input_values is None: #if user presses cancel on form
                    msgbox("Account creation cancelled.", "Cancelled")
                    return current_account
                entered_name, password = input_values
                if not entered_name or not password: #checks if both fields are filled
                    msgbox("You must fill in both fields.", "Error")
                    continue
                if entered_name in accounts: #checks if account name already exists from dictionary
                    msgbox("This account name already exists. Try a different one.", "Error")
                    continue
                break
            while True:
                try: #asks user for starting balance of that account
                    balance_input = enterbox("Enter starting balance:", "New Account")
                    if balance_input is None: #checks if user enters blank input for starting balance
                        msgbox("Account creation cancelled.", "Cancelled")
                        return current_account
                    balance = float(balance_input)
                    if balance < MIN_STARTING_BALANCE: #checks if user enters a negative balance
                        msgbox("Balance must not be negative.", "Error")
                        continue
                    #saves account info 
                    accounts[entered_name] = {
                        "password": password,
                        "balance": balance,
                        "transactions": [],
                        "transactions_numbers": []
                    }
                    current_account = entered_name
                    msgbox(f"Account '{entered_name}' created with ${balance}", "Success")
                    return current_account
                except ValueError: #catches invalid input (user enters non-number)
                    msgbox("Please enter numbers only.", "Invalid Input")
    return current_account

#function to check current balance
def check_balance(current_account):
    """
    Allows user to check the current balance of the account logged into
    """
    if current_account is None: #checks if user has logged into an account
        msgbox("You must login first.", "Error")
        return
    balance = accounts[current_account]["balance"] #reads balance from dictionary
    msgbox(f"Balance for {current_account}: ${balance}", "Balance")

#function to deposit
def deposit(current_account):
    """
    Lets user deposit money into the account currently logged into
    Updates transaction history of changes to account balance
    """
    if current_account is None: #checks if user has logged into an account
        msgbox("You must login first.", "Error")
        return
    while True:
        try:
            amount_input = enterbox("Enter deposit amount:", "Deposit") #asks user to input amount they want to deposit
            if amount_input is None: #checks if user enters blank for deposit amount and if it is cancel deposit
                msgbox("Deposit cancelled.", "Cancelled")
                return
            amount = float(amount_input)
            if amount > MIN_TRANSACTION_AMOUNT: #checks if deposit amount input is valid, adds to current balance and records in history
                accounts[current_account]["balance"] += amount
                accounts[current_account]["transactions"].append(f"Deposited: ${amount}")
                accounts[current_account]["transactions_numbers"].append(amount)
                msgbox(f"${amount} deposited.", "Success")
                break
            else: #checks if users input is 0 or negative
                msgbox("Deposit amount must be a positive number", "Error")
        except ValueError: 
            msgbox("Please enter numbers only.", "Error")

#function to withdraw
def withdraw(current_account):
    """
    Lets user deposit money into the account currently logged into
    Updates transaction history of changes to account balance
    Prevents user from overdrawing
    """
    if current_account is None: #checks if user has logged into an account
        msgbox("You must login first.", "Error")
        return
    while True:
        try:
            amount_input = enterbox("Enter amount to withdraw:", "Withdraw")
            if amount_input is None: #checks to see if withdrawal amount is blank and if it is cancel withdrawal
                msgbox("Withdrawal cancelled.", "Cancelled")
                return
            amount = float(amount_input)
            balance = accounts[current_account]["balance"]
            if amount <= MIN_TRANSACTION_AMOUNT: #checks if withdrawal amount is 0 or below and prints error
                msgbox("Withdraw amount must be a positive number", "Error")
            elif amount > balance: #checks to see if withdrawal amount is above balance (overdraw) and prints error
                msgbox(f"Not enough funds. Balance: ${balance}", "Insufficient Funds")
                accounts[current_account]["transactions"].append(f"Failed withdrawal: ${amount}")
                break
            else: #subtracts withdrawal amount from balance and records in history
                accounts[current_account]["balance"] -= amount
                accounts[current_account]["transactions"].append(f"Withdrew: ${amount}")
                accounts[current_account]["transactions_numbers"].append(-amount)
                msgbox(f"${amount} withdrawn.", "Success")
                break
        except ValueError: #checks if user enters non-number
            msgbox("Please enter numbers only.", "Error")

#Show actions user has made function
def show_history(current_account):
    """
    Shows the transaction history and current balance to user
    """
    if current_account is None: #checks if user has logged into an account
        msgbox("You must login first.", "Error")
        return
    history = "\n".join(accounts[current_account]["transactions"]) #joins all transaction strings into a list
    textbox(f"History for {current_account}", #title
            "Transaction History", #header
            f"{history}\n\nCurrent balance: ${accounts[current_account]['balance']}") 

#transaction graph function
def plot_transactions(current_account):
    """
    Visually shows a graph of users transactions over time to user using matplotlib
    """
    if current_account is None: #checks if user has logged into an account
        msgbox("You must login first.", "Error")
        return
    transaction_amounts = accounts[current_account]["transactions_numbers"] #gets list of transaction amounts
    starting_balance = accounts[current_account]["balance"] - sum(transaction_amounts) #calculates original balance
    running_balance = [starting_balance]

    for amount in transaction_amounts: #calculates every change made from starting balance
        running_balance.append(running_balance[-1] + amount)

    #sets graph features in matplotlib
    plt.figure(figsize=(10, 5))
    plt.plot(running_balance, marker='o')
    plt.xticks(range(len(running_balance))) #makes the transaction number axis only show integers
    plt.grid(True)
    #graph formatting
    plt.title(f"Transaction History for {current_account}")
    plt.xlabel("Transaction Number")
    plt.ylabel("Balance ($)")
    plt.tight_layout()
    plt.show() #calls graph window

#option menu function


#calling function
main()