import random
import sqlite3
conn = sqlite3.connect('banking/card.s3db')
cur = conn.cursor()
cur.execute('create table IF NOT EXISTS card('
            'id INTEGER PRIMARY KEY AUTOINCREMENT, '
            'number TEXT, '
            'pin TEXT, '
            'balance INTEGER DEFAULT 0'
            ');')
conn.commit()

class Account:

    def __init__(self):
        self.card_number = "400000" + ("%0.9d" % random.randint(0, 999999999))
        check1 = 0
        for index, x in enumerate(self.card_number):
            y = int(x)
            if index % 2 != 0:
                check1 += y
            else:
                z = y * 2
                if z > 9:
                    z -= 9
                check1 += z
        if check1 % 10 == 0:
            self.card_number += str(0)
        else:
            self.card_number += str(10 - (check1 % 10) % 10)
        self.card_pin = "%0.4d" % random.randint(0, 9999)

    def get_card_number(self):
        return self.card_number

    def get_card_pin(self):
        return self.card_pin


def in_account(number):
    while True:
        account_action = int(input("1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit\n"))
        if account_action == 1:
            balance_all = cur.execute(f"select balance from card where number = \"{number}\";")
            balance_row = balance_all.fetchone()
            print(f"Balance: {balance_row[0]}")
        elif account_action == 2:
            balance_all = cur.execute(f"select balance from card where number = \"{number}\";")
            balance_row = balance_all.fetchone()
            to_add = int(input("Enter income:\n"))
            cur.execute(f"update card set balance = {balance_row[0] + to_add} where number = \"{number}\";")
            conn.commit()
            print("Income was added!")
        elif account_action == 3:
            card_number_transfer = input("Transfer\nEnter card number:\n")
            last_digit = card_number_transfer[-1:]
            find_sum = card_number_transfer[:-1]
            check1 = 0
            for index, x in enumerate(find_sum):
                y = int(x)
                if index % 2 != 0:
                    check1 += y
                else:
                    z = y * 2
                    if z > 9:
                        z -= 9
                    check1 += z
            if check1 % 10 == 0:
                last_should = str(0)
            else:
                last_should = str(10 - (check1 % 10) % 10)
            if last_should != last_digit:
                print("Probably you made a mistake in the card number. Please try again!")
                continue
            elif cur.execute(f"select id from card where number = \"{card_number_transfer}\";").fetchone() is None:
                print("Such a card does not exist.")
            else:
                money_to_transfer = int(input("Enter how much money you want to transfer:"))
                balance_benefactor = cur.execute(f"select balance from card where number = \"{number}\";").fetchone()[0]
                if money_to_transfer > balance_benefactor:
                    print("Not enough money!")
                else:
                    cur.execute(f"update card set balance = {balance_benefactor - money_to_transfer} where number = \"{number}\";")
                    balance_beneficiary = cur.execute(f"select balance from card where number = \"{card_number_transfer}\";").fetchone()[0]
                    cur.execute(f"update card set balance = {balance_beneficiary + money_to_transfer} where number = \"{card_number_transfer}\";")
                    conn.commit()
                    print("Success!")
        elif account_action == 4:
            cur.execute(f"delete from card where number = \"{number}\";")
            conn.commit()
            print("The account has been closed!")
        elif account_action == 5:
            return 1
        elif account_action == 0:
            return


while True:
    action = int(input("1. Create an account\n2. Log into account\n0. Exit\n"))
    print("")
    if action == 1:
        new_account = Account()
        number = new_account.get_card_number()
        pin = new_account.get_card_pin()
        cur.execute(f'insert into card (number, pin) values ({number}, {pin});')
        print(f"Your card number:\n{number}\nYour card PIN:\n{pin}\n")
        conn.commit()
    elif action == 2:
        entered_card_number = input("Enter your card number:\n")
        entered_card_pin = input("Enter your PIN:\n")
        print("")
        index_number = cur.execute(f"select id from card where number = \"{entered_card_number}\";")
        number = index_number.fetchone()
        index_pin = cur.execute(f"select id from card where pin = \"{entered_card_pin}\";")
        pin = index_pin.fetchone()
        if number is not None and pin is not None:
            print("You have successfully logged in!")
            print("")
            returned_value = in_account(entered_card_number)
            if returned_value is not None:
                continue
            else:
                break
        else:
            print("Wrong card number or PIN!")
            print("")
    elif action == 0:
        print("Bye")
        break



