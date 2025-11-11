import random

def play_game():
    words = ['python', 'java', 'javascript', 'php']
    word = random.choice(words)
    display = "-" * len(word)
    lives = 8
    guessed_letters = set()
    while lives > 0 and "-" in display:
        print(display)
        letter = input("Input a letter: > ")
        # Перевірки введення
        if len(letter) != 1:
            print("You should input a single letter")
            continue
        if not letter.isalpha() or not letter.islower():
            print("Please enter a lowercase English letter")
            continue
        if letter in guessed_letters:
            print("You've already guessed this letter")
            continue
        guessed_letters.add(letter)

        if letter in word:
            new_display = ""
            for i in range(len(word)):
                if word[i] == letter:
                    new_display += letter
                else:
                    new_display += display[i]
            display = new_display
        else:
            print("That letter doesn't appear in the word")
            lives -= 1
    # Результат гри
    if "-" not in display:
        print(f"You guessed the word {word}!")
        print("You survived!")
    else:
        print("You lost!")
# Головне меню
print("HANGMAN")
while True:
    action = input('Type "play" to play the game, "exit" to quit: > ')
    if action == "play":
        play_game()
    elif action == "exit":
        break
    else:
        continue
