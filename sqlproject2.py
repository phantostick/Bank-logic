import mysql.connector
import random

con = mysql.connector.connect(user="root", password="", database="atm")
cur = con.cursor()
minimum = 500  
while True:
    print("\n1. Add\n2. Deposit Money\n3. Withdraw Money\n4. View Balance\n5. Transfer Money\n6. Delete\n7. Exit")
    ch = int(input('Enter Your Choice '))
    
# Creation of account 
    if ch == 1:
        accno = int(input('Enter your Pin Number: '))
        accholder = input('Enter the Account Holder\'s Name: ')
        balance = int(input('Enter Balance: '))
        rd = random.randint(1000, 9999)
        print("OTP is %d" % rd)
        otp = int(input("Enter your OTP: "))
        if otp == rd:
            if balance >= minimum:
                print("The info will be verified and added in 24h")
                sql = "INSERT INTO reg VALUES (%d, '%s', %d)" % (accno, accholder, balance)
                cur.execute(sql)
                con.commit()
            else:
                print("Minimum Balance Must Be 500")
        else:
            print("Wrong OTP")

# Deposit Money
    elif ch == 2:
        accno = int(input('Enter your Acc Number: '))
        upd = int(input('Enter the amount you want to deposit: '))

        sql = "SELECT balance FROM reg WHERE accno=%d" % (accno)
        cur.execute(sql)
        result = cur.fetchone()
        if result:
            rd = random.randint(1000, 9999)
            print("OTP is %d" % rd)
            otp = int(input("Enter your OTP: "))
            if otp == rd:
                current_balance = result[0]
                new_balance = current_balance + upd

                sql = "UPDATE reg SET balance=%d WHERE accno=%d" % (new_balance, accno)
                cur.execute(sql)
                con.commit()
                print("Deposit successful! New balance is:", new_balance)
            else:
                print("Wrong OTP")
        else:
            print("Account number not found.")

# Withdraw Money
    elif ch == 3:
        accno = int(input('Enter your Acc Number: '))
        upd = int(input('Enter the amount you want to withdraw: '))

        sql = "SELECT balance FROM reg WHERE accno=%d" % (accno)
        cur.execute(sql)
        result = cur.fetchone()
        if result:
            rd = random.randint(1000, 9999)
            print("OTP is %d" % rd)
            otp = int(input("Enter your OTP: "))
            if otp == rd:
                current_balance = result[0]
                new_balance = current_balance - upd
                if new_balance >= minimum:
                    sql = "UPDATE reg SET balance=%d WHERE accno=%d" % (new_balance, accno)
                    cur.execute(sql)
                    con.commit()
                    print("Withdrawal successful! New balance is:", new_balance)
                else:
                    print("Balance must not go below 500")
            else:
                print("Wrong OTP")
        else:
            print("Account number not found.")

# Viewing bal
    elif ch == 4:
        accno = int(input('Enter your account number: '))
        cur.execute("SELECT accno, accholder, balance FROM reg WHERE accno=%d" % (accno))
        abc = cur.fetchone()
        if abc:
            rd = random.randint(1000, 9999)
            print("OTP is %d" % rd)
            otp = int(input("Enter your OTP: "))
            if otp == rd:
                print(f"Pin number: {abc[0]}")
                print(f"Name: {abc[1]}")
                print(f"Balance: {abc[2]}")
            else:
                print("Wrong OTP")
        else:
            print("Account number not found.")

# Transfer
    elif ch == 5:
        accno = int(input("Enter Sender's Account Number: "))
        accno1 = int(input("Enter the Receiver's Account Number: "))
        mon = int(input("Enter the amount you want to transfer: "))
        if accno == accno1:
            print("Sender and receiver account numbers cannot be the same.")
            continue
        if mon <= 0:
            print("Transfer amount must be greater than zero.")
            continue
        if mon < minimum:
            print("Transfer amount must be at least 500.")
            continue
        if mon > 1000000:
            print("Transfer amount must not exceed 1,000,000.")
            continue
        cur.execute("SELECT balance FROM reg WHERE accno=%d" % (accno))
        sender_balance = cur.fetchone()
        cur.execute("SELECT balance FROM reg WHERE accno=%d" % (accno1))
        receiver_balance = cur.fetchone()

        if sender_balance and receiver_balance:
            rd = random.randint(1000, 9999)
            print("OTP is %d" % rd)
            otp = int(input("Enter your OTP: "))

            if otp == rd:
                if sender_balance[0] - mon >= minimum:
                    cur.execute("UPDATE reg SET balance=%d WHERE accno=%d" % (sender_balance[0] - mon, accno))
                    cur.execute("UPDATE reg SET balance=%d WHERE accno=%d" % (receiver_balance[0] + mon, accno1))
                    con.commit()
                    print("Transfer successful! New sender balance is:", sender_balance[0] - mon)
                else:
                    print("Sender's balance must not go below 500")
            else:
                print("Wrong OTP")
        else:
            print("Invalid account numbers.")

# Deletion
    elif ch == 6:
        accno = int(input('Enter the Account Number: '))
        sql = "DELETE FROM reg WHERE accno=%d" % (accno)
        cur.execute(sql)
        con.commit()
        print("Account deleted successfully.")

# break
    elif ch == 7:
        break

    else:
        print("Invalid Choice")
