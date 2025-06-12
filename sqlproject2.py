import mysql.connector
import random

# Constants
MINIMUM_BALANCE = 500
OTP_RANGE = (1000, 9999)

# DB Connection
con = mysql.connector.connect(user="root", password="", database="atm")
cur = con.cursor()

def get_otp():
    otp = random.randint(*OTP_RANGE)
    print(f"OTP is {otp}")
    return otp

def verify_otp():
    return int(input("Enter your OTP: ")) == get_otp()

def get_balance(accno):
    cur.execute(f"SELECT balance FROM reg WHERE accno={accno}")
    return cur.fetchone()

def update_balance(accno, amount):
    cur.execute(f"UPDATE reg SET balance={amount} WHERE accno={accno}")
    con.commit()

def account_exists(accno):
    cur.execute(f"SELECT * FROM reg WHERE accno={accno}")
    return cur.fetchone()

def display_account_info(accno):
    cur.execute(f"SELECT accno, accholder, balance FROM reg WHERE accno={accno}")
    info = cur.fetchone()
    if info and verify_otp():
        print(f"Pin number: {info[0]}\nName: {info[1]}\nBalance: {info[2]}")
    else:
        print("Account not found or wrong OTP")

def add_account():
    accno = int(input('Enter your Pin Number: '))
    name = input("Enter the Account Holder's Name: ")
    balance = int(input("Enter Balance: "))
    if balance < MINIMUM_BALANCE:
        print("Minimum Balance Must Be 500")
        return
    if verify_otp():
        cur.execute(f"INSERT INTO reg VALUES ({accno}, '{name}', {balance})")
        con.commit()
        print("The info will be verified and added in 24h")
    else:
        print("Wrong OTP")

def deposit():
    accno = int(input("Enter your Acc Number: "))
    amount = int(input("Enter the amount you want to deposit: "))
    current = get_balance(accno)
    if current and verify_otp():
        new_balance = current[0] + amount
        update_balance(accno, new_balance)
        print("Deposit successful! New balance is:", new_balance)
    else:
        print("Account number not found or wrong OTP")

def withdraw():
    accno = int(input("Enter your Acc Number: "))
    amount = int(input("Enter the amount you want to withdraw: "))
    current = get_balance(accno)
    if current and verify_otp():
        new_balance = current[0] - amount
        if new_balance >= MINIMUM_BALANCE:
            update_balance(accno, new_balance)
            print("Withdrawal successful! New balance is:", new_balance)
        else:
            print("Balance must not go below 500")
    else:
        print("Account number not found or wrong OTP")

def transfer():
    sender = int(input("Enter Sender's Account Number: "))
    receiver = int(input("Enter the Receiver's Account Number: "))
    amount = int(input("Enter the amount you want to transfer: "))

    if sender == receiver:
        print("Sender and receiver account numbers cannot be the same.")
        return
    if not (MINIMUM_BALANCE <= amount <= 1000000):
        print("Transfer amount must be between 500 and 1,000,000.")
        return

    sender_bal = get_balance(sender)
    receiver_bal = get_balance(receiver)

    if sender_bal and receiver_bal and verify_otp():
        if sender_bal[0] - amount >= MINIMUM_BALANCE:
            update_balance(sender, sender_bal[0] - amount)
            update_balance(receiver, receiver_bal[0] + amount)
            print("Transfer successful! New sender balance is:", sender_bal[0] - amount)
        else:
            print("Sender's balance must not go below 500")
    else:
        print("Invalid account numbers or wrong OTP")

def delete_account():
    accno = int(input("Enter the Account Number: "))
    if not account_exists(accno):
        print("Account number not found.")
        return
    if verify_otp():
        cur.execute(f"DELETE FROM reg WHERE accno={accno}")
        con.commit()
        print("Account deleted successfully.")
    else:
        print("Wrong OTP")

# Main loop
while True:
    print("""
1. Add Account
2. Deposit Money
3. Withdraw Money
4. View Balance
5. Transfer Money
6. Delete Account
7. Exit""")
    choice = int(input("Enter Your Choice: "))
    if choice == 1:
        add_account()
    elif choice == 2:
        deposit()
    elif choice == 3:
        withdraw()
    elif choice == 4:
        accno = int(input("Enter your account number: "))
        display_account_info(accno)
    elif choice == 5:
        transfer()
    elif choice == 6:
        delete_account()
    elif choice == 7:
        break
    else:
        print("Invalid Choice")
