import requests


def get_currency_code():
    while True:
        code = input("Enter your currency code: ").strip().lower()
        if code.isalpha() and len(code) == 3:
            return code
        print("Invalid currency code. Try again.")


def get_amount():
    while True:
        try:
            amount = float(input("Enter amount of money: "))
            if amount >= 0:
                return amount
            print("Amount must be positive.")
        except ValueError:
            print("Invalid number. Try again.")


def get_rates(base_currency):
    try:
        url = f"https://www.floatrates.com/daily/{base_currency}.json"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        print("Error while getting data from server.")
        return {}


def convert_currency():
    base_currency = get_currency_code()
    rates = get_rates(base_currency)

    if not rates:
        return

    cache = {}

    # кешуємо USD і EUR
    if "usd" in rates:
        cache["usd"] = rates["usd"]["rate"]
    if "eur" in rates:
        cache["eur"] = rates["eur"]["rate"]

    while True:
        target = input("\nEnter currency you want (empty to exit): ").strip().lower()

        if target == "":
            break

        if not target.isalpha() or len(target) != 3:
            print("Invalid currency code.")
            continue

        amount = get_amount()

        print("Checking the cache...")

        if target in cache:
            print("It is in the cache!")
            rate = cache[target]
        else:
            print("Sorry, but it is not in the cache!")
            if target in rates:
                rate = rates[target]["rate"]
                cache[target] = rate
            else:
                print("Currency not found.")
                continue

        result = round(amount * rate, 2)
        print(f"You received {result} {target.upper()}.")


convert_currency()