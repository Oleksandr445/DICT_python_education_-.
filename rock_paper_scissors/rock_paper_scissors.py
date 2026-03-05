import random


def get_user_name():
    print("Enter your name:")
    name = input("> ")
    print(f"Hello, {name}")
    return name


def get_user_score(name):
    score = 0
    try:
        with open("rating.txt", "r") as file:
            for line in file:
                user, points = line.split()
                if user == name:
                    score = int(points)
                    break
    except FileNotFoundError:
        pass
    return score


def get_game_options():
    print("Please enter the set of game options separated by commas:")
    options_input = input("> ").strip()

    if options_input == "":
        return ["rock", "paper", "scissors"]

    options = [opt.strip() for opt in options_input.split(",") if opt.strip() != ""]
    return options


def get_result(user_choice, computer_choice, options):
    if user_choice == computer_choice:
        return "draw"

    index = options.index(user_choice)
    rotated = options[index + 1:] + options[:index]

    half = len(rotated) // 2
    lose_list = rotated[:half]

    if computer_choice in lose_list:
        return "lose"
    else:
        return "win"


def play_game(options, score):

    print("Okay, let's start")

    while True:

        user_choice = input("> ").strip()

        if user_choice == "!exit":
            print("Bye!")
            break

        if user_choice == "!rating":
            print(f"Your rating: {score}")
            continue

        if user_choice not in options:
            print("Invalid input")
            continue

        computer_choice = random.choice(options)

        result = get_result(user_choice, computer_choice, options)

        if result == "draw":
            print(f"There is a draw ({computer_choice})")
            score += 50

        elif result == "win":
            print(f"Well done. The computer chose {computer_choice} and failed")
            score += 100

        else:
            print(f"Sorry, but the computer chose {computer_choice}")


def main():
    name = get_user_name()
    score = get_user_score(name)
    options = get_game_options()
    play_game(options, score)


main()
