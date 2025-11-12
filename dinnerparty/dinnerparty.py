import random

# 1
num_friends = int(input("Enter the number of friends joining (including you):\n"))

if num_friends <= 0:
    print("No one is joining for the party")
else:
    print("Enter the name of every friend (including you), each on a new line:")
    friends = {}
    for _ in range(num_friends):
        name = input()
        friends[name] = 0

    # 2
    total_amount = int(input("Enter the total amount:\n"))
    share = round(total_amount / num_friends, 2)
    for friend in friends:
        friends[friend] = share

    # 3
    answer = input('Do you want to use the "Who is lucky?" feature? Write Yes/No:\n')

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
    else:
        print("No one is going to be lucky")

    print(friends)
