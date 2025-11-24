import random

# кількість олівців
while True:
    pencils = input("How many pencils would you like to use:\n> ")

    if not pencils.isdigit():
        print("The number of pencils should be numeric")
        continue

    pencils = int(pencils)
    if pencils <= 0:
        print("The number of pencils should be positive")
        continue

    break

# Імена
name1 = "John"
name2 = "Jack"  # Jack — це бот

# Хто перший
while True:
    first = input(f"Who will be the first ({name1}, {name2}):\n> ")
    if first not in (name1, name2):
        print(f"Choose between '{name1}' and '{name2}'")
        continue
    break

current = first

print("|" * pencils)
print(f"{current}'s turn!")

while pencils > 0:

    # Хід бота перший
    if current == name2:

        # стратегія
        if pencils % 4 == 0:
            bot_take = 3
        elif pencils % 4 == 3:
            bot_take = 2
        elif pencils % 4 == 2:
            bot_take = 1
        else:
            bot_take = random.randint(1, 3)

        if bot_take > pencils:
            bot_take = pencils

        print(bot_take)
        pencils -= bot_take

    # Хід ігрока
    else:
        while True:
            take = input("> ")
            if take not in ("1", "2", "3"):
                print("Possible values: '1', '2' or '3'")
                continue

            take = int(take)
            if take > pencils:
                print("Too many pencils were taken")
                continue

            pencils -= take
            break

    if pencils == 0:
        winner = name2 if current == name1 else name1
        print(f"{winner} won!")
        break

    print("|" * pencils)

    current = name1 if current == name2 else name2
    print(f"{current}'s turn!")
