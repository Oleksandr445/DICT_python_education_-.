import random

# 1 + Захист
num_input = input("Enter the number of friends joining (including you):\n> ")
if not num_input.isdigit() or int(num_input) <= 0:
    print("No one is joining for the party")
else:
    num_friends = int(num_input)
    print("Enter the name of every friend (including you), each on a new line:")
    friends = {}
    for _ in range(num_friends):
        name = input("> ")
        friends[name] = 0

    # 2 + Захист
    total_input = input("Enter the total amount:\n> ")
    while not total_input.isdigit():
        total_input = input("Enter the total amount (numbers only):\n> ")
    total_amount = int(total_input)
    share = round(total_amount / num_friends, 2)
    for friend in friends:
        friends[friend] = share

    # 3
    answer = input('Do you want to use the "Who is lucky?" feature? Write Yes/No:\n> ')
    if answer == "Yes":
        lucky_one = random.choice(list(friends.keys()))
        print(f"{lucky_one} is the lucky one!")

        # 4
        new_share = round(total_amount / (num_friends - 1), 2)
        for friend in friends:
            if friend == lucky_one:
                friends[friend] = 0
            else:
                friends[friend] = new_share
        print(friends)
    else:
        print("No one is going to be lucky")
        print(friends)
