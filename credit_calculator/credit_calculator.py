import sys
import math


def parse_arguments():
    args = sys.argv[1:]
    params = {}

    for arg in args:
        if "=" not in arg:
            print("Incorrect parameters")
            exit()

        key, value = arg.split("=")
        params[key] = value

    return params


def check_parameters(params):
    if "--type" not in params or "--interest" not in params:
        print("Incorrect parameters")
        exit()

    if params["--type"] not in ["annuity", "diff"]:
        print("Incorrect parameters")
        exit()


def calculate_diff(principal, periods, i):
    total = 0

    for m in range(1, periods + 1):
        payment = principal / periods + i * (principal - principal * (m - 1) / periods)
        payment = math.ceil(payment)

        total += payment
        print(f"Month {m}: payment is {payment}")

    overpayment = total - principal
    overpayment = round(overpayment)

    print(f"Overpayment = {overpayment}")


def calculate_annuity_payment(principal, periods, i):
    payment = principal * (i * (1 + i) ** periods) / ((1 + i) ** periods - 1)
    payment = math.ceil(payment)

    overpayment = payment * periods - principal
    overpayment = round(overpayment)

    print(f"Your annuity payment = {payment}!")
    print(f"Overpayment = {overpayment}")


def calculate_principal(payment, periods, i):
    principal = payment / ((i * (1 + i) ** periods) / ((1 + i) ** periods - 1))

    principal = math.floor(principal)

    overpayment = payment * periods - principal
    overpayment = round(overpayment)

    print(f"Your loan principal = {principal}!")
    print(f"Overpayment = {overpayment}")


def calculate_periods(principal, payment, i):
    periods = math.log(payment / (payment - i * principal), 1 + i)
    periods = math.ceil(periods)

    years = periods // 12
    months = periods % 12

    if years > 0 and months > 0:
        print(f"It will take {years} years and {months} months to repay this loan!")
    elif years > 0:
        print(f"It will take {years} years to repay this loan!")
    else:
        print(f"It will take {months} months to repay this loan!")

    overpayment = payment * periods - principal
    overpayment = round(overpayment)

    print(f"Overpayment = {overpayment}")


def main():
    params = parse_arguments()
    check_parameters(params)

    loan_type = params.get("--type")

    principal = float(params["--principal"]) if "--principal" in params else None
    payment = float(params["--payment"]) if "--payment" in params else None
    periods = int(params["--periods"]) if "--periods" in params else None
    interest = float(params["--interest"])

    if interest <= 0:
        print("Incorrect parameters")
        exit()

    for value in [principal, payment, periods]:
        if value is not None and value < 0:
            print("Incorrect parameters")
            exit()

    i = interest / (12 * 100)

    if loan_type == "diff":

        if principal is None or periods is None or payment is not None:
            print("Incorrect parameters")
            exit()

        calculate_diff(principal, periods, i)

    elif loan_type == "annuity":

        if principal is not None and payment is not None and periods is None:
            calculate_periods(principal, payment, i)

        elif principal is not None and periods is not None and payment is None:
            calculate_annuity_payment(principal, periods, i)

        elif payment is not None and periods is not None and principal is None:
            calculate_principal(payment, periods, i)

        else:
            print("Incorrect parameters")


main()
