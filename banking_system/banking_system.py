import sqlite3
import random

DB_NAME = "card.s3db"


def safe_int(prompt, allow_zero=True):
    while True:
        value = input(prompt).strip()

        if not value.isdigit():
            print("Error: enter digits only!")
            continue

        number = int(value)

        if not allow_zero and number <= 0:
            print("Error: value must be greater than 0!")
            continue

        return number


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS card (
            id INTEGER PRIMARY KEY,
            number TEXT,
            pin TEXT,
            balance INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    return conn


def luhn_checksum(number_without_checksum: str) -> int:
    digits = [int(x) for x in number_without_checksum]

    for i in range(len(digits)):
        if i % 2 == 0:
            digits[i] *= 2
            if digits[i] > 9:
                digits[i] -= 9

    return sum(digits)


def validate_luhn(card_number: str) -> bool:
    if len(card_number) != 16 or not card_number.isdigit():
        return False

    checksum = luhn_checksum(card_number[:-1])
    return (checksum + int(card_number[-1])) % 10 == 0


def generate_card_number():
    iin = "400000"
    account_id = str(random.randint(0, 999999999)).zfill(9)
    partial = iin + account_id

    checksum = luhn_checksum(partial)
    last_digit = (10 - (checksum % 10)) % 10

    return partial + str(last_digit)


def generate_pin():
    return str(random.randint(0, 9999)).zfill(4)


def create_account(conn):
    cur = conn.cursor()

    while True:
        number = generate_card_number()
        cur.execute("SELECT number FROM card WHERE number = ?", (number,))
        if not cur.fetchone():
            break

    pin = generate_pin()

    cur.execute(
        "INSERT INTO card (number, pin, balance) VALUES (?, ?, 0)",
        (number, pin)
    )
    conn.commit()

    print("\nYour card has been created")
    print("Your card number:")
    print(number)
    print("Your card PIN:")
    print(pin)


def log_in(conn):
    cur = conn.cursor()

    card_number = input("Enter your card number:\n> ").strip()
    pin = input("Enter your PIN:\n> ").strip()

    if not card_number.isdigit() or not pin.isdigit():
        print("Wrong card number or PIN!")
        return

    cur.execute(
        "SELECT * FROM card WHERE number = ? AND pin = ?",
        (card_number, pin)
    )

    user = cur.fetchone()

    if not user:
        print("Wrong card number or PIN!")
        return

    print("\nYou have successfully logged in!")
    logged_menu(conn, card_number)


def get_balance(conn, number):
    cur = conn.cursor()
    cur.execute("SELECT balance FROM card WHERE number = ?", (number,))
    return cur.fetchone()[0]


def add_income(conn, number):
    amount = safe_int("Enter income:\n> ", allow_zero=False)

    cur = conn.cursor()
    cur.execute(
        "UPDATE card SET balance = balance + ? WHERE number = ?",
        (amount, number)
    )
    conn.commit()

    print("Income was added!")


def do_transfer(conn, sender):
    cur = conn.cursor()

    receiver = input("Enter card number:\n> ").strip()

    if not receiver.isdigit():
        print("Probably you made a mistake in the card number. Please try again!")
        return

    if receiver == sender:
        print("You can't transfer money to the same account!")
        return

    if not validate_luhn(receiver):
        print("Probably you made a mistake in the card number. Please try again!")
        return

    cur.execute("SELECT balance FROM card WHERE number = ?", (receiver,))
    row = cur.fetchone()

    if not row:
        print("Such a card does not exist.")
        return

    amount = safe_int("Enter how much money you want to transfer:\n> ", allow_zero=False)

    cur.execute("SELECT balance FROM card WHERE number = ?", (sender,))
    sender_balance = cur.fetchone()[0]

    if amount > sender_balance:
        print("Not enough money!")
        return

    cur.execute("UPDATE card SET balance = balance - ? WHERE number = ?", (amount, sender))
    cur.execute("UPDATE card SET balance = balance + ? WHERE number = ?", (amount, receiver))

    conn.commit()
    print("Success!")


def close_account(conn, number):
    cur = conn.cursor()
    cur.execute("DELETE FROM card WHERE number = ?", (number,))
    conn.commit()
    print("The account has been closed!")


def logged_menu(conn, number):
    while True:
        print("""
1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit
""")

        choice = input("> ").strip()

        if choice == "1":
            print(f"Balance: {get_balance(conn, number)}")

        elif choice == "2":
            add_income(conn, number)

        elif choice == "3":
            do_transfer(conn, number)

        elif choice == "4":
            close_account(conn, number)
            break

        elif choice == "5":
            print("You have successfully logged out!")
            break

        elif choice == "0":
            print("Bye!")
            exit()

        else:
            print("Error: invalid option!")


def main():
    conn = init_db()

    while True:
        print("""
1. Create an account
2. Log into account
0. Exit
""")

        choice = input("> ").strip()

        if choice == "1":
            create_account(conn)

        elif choice == "2":
            log_in(conn)

        elif choice == "0":
            print("Bye!")
            break

        else:
            print("Error: invalid option!")


if __name__ == "__main__":
    main()