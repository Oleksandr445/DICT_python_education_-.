import random

LEVEL_DESCRIPTIONS = {
    1: "simple operations with numbers 2-9",
    2: "integral squares of 11-29"
}

def get_level():
    while True:
        print("\nWhich level do you want? Enter a number:")
        print("1 - simple operations with numbers 2-9")
        print("2 - integral squares of 11-29")

        level_input = input("> ")

        if level_input not in ("1", "2"):
            print("\nIncorrect format.")
            continue

        return int(level_input)


def generate_task(level):
    if level == 1:
        num1 = random.randint(2, 9)
        num2 = random.randint(2, 9)
        operation = random.choice(["+", "-", "*"])
        question = f"{num1} {operation} {num2}"

        if operation == "+":
            answer = num1 + num2
        elif operation == "-":
            answer = num1 - num2
        else:
            answer = num1 * num2

        return question, answer

    else:
        num = random.randint(11, 29)
        question = f"{num}"
        answer = num ** 2
        return question, answer


def get_user_answer():
    while True:
        user_input = input("> ")

        try:
            return int(user_input)
        except ValueError:
            print("\nIncorrect format.")


def ask_to_save(score, level):
    print(f"\nYour mark is {score}/5.")
    print("Would you like to save your result to the file? Enter yes or no.")

    save_answer = input("> ")

    if save_answer.lower() in ("yes", "y"):
        print("\nWhat is your name?")
        name = input("> ")

        try:
            with open("results.txt", "a", encoding="utf-8") as file:
                file.write(
                    f"{name}: {score}/5 in level {level} "
                    f"({LEVEL_DESCRIPTIONS[level]})\n"
                )
            print('\nThe results are saved in "results.txt".')
        except OSError:
            print("\nError while saving the file.")


def main():
    level = get_level()
    score = 0

    for _ in range(5):
        question, correct_answer = generate_task(level)
        print(f"\n{question}")

        user_answer = get_user_answer()

        if user_answer == correct_answer:
            print("\nRight!")
            score += 1
        else:
            print("\nWrong!")

    ask_to_save(score, level)

if __name__ == "__main__":
    main()