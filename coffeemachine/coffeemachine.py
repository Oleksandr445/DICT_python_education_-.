class CoffeeMachine:
    def __init__(self):
        self.water = 400
        self.milk = 540
        self.beans = 120
        self.cups = 9
        self.money = 550

        self.state = "main_menu"
        self.fill_step = 0

    def print_state(self):
        print("The coffee machine has:")
        print(f"{self.water} of water")
        print(f"{self.milk} of milk")
        print(f"{self.beans} of coffee beans")
        print(f"{self.cups} of disposable cups")
        print(f"{self.money} of money")

    def check_resources(self, need_water, need_milk, need_beans):
        if self.water < need_water:
            print("Sorry, not enough water!")
            return False
        if self.milk < need_milk:
            print("Sorry, not enough milk!")
            return False
        if self.beans < need_beans:
            print("Sorry, not enough coffee beans!")
            return False
        if self.cups < 1:
            print("Sorry, not enough disposable cups!")
            return False
        return True

    def make_coffee(self, need_water, need_milk, need_beans, cost):
        self.water -= need_water
        self.milk -= need_milk
        self.beans -= need_beans
        self.cups -= 1
        self.money += cost
        print("I have enough resources, making you a coffee!")

    def process(self, user_input):
        # MAIN MENU
        if self.state == "main_menu":
            if user_input == "buy":
                print("What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back – to main menu:")
                self.state = "buy"
            elif user_input == "fill":
                self.fill_step = 1
                print("Write how many ml of water do you want to add:")
                self.state = "fill"
            elif user_input == "take":
                print(f"I gave you {self.money}")
                self.money = 0
            elif user_input == "remaining":
                self.print_state()
            elif user_input == "exit":
                self.state = "exit"

        # BUY STATE
        elif self.state == "buy":
            if user_input == "back":
                self.state = "main_menu"
                return

            if user_input == "1":  # espresso
                if self.check_resources(250, 0, 16):
                    self.make_coffee(250, 0, 16, 4)

            elif user_input == "2":  # latte
                if self.check_resources(350, 75, 20):
                    self.make_coffee(350, 75, 20, 7)

            elif user_input == "3":  # cappuccino
                if self.check_resources(200, 100, 12):
                    self.make_coffee(200, 100, 12, 6)

            self.state = "main_menu"

        # FILL STATE
        elif self.state == "fill":
            if self.fill_step == 1:
                self.water += int(user_input)
                print("Write how many ml of milk do you want to add:")
                self.fill_step = 2
            elif self.fill_step == 2:
                self.milk += int(user_input)
                print("Write how many grams of coffee beans do you want to add:")
                self.fill_step = 3
            elif self.fill_step == 3:
                self.beans += int(user_input)
                print("Write how many disposable cups of coffee do you want to add:")
                self.fill_step = 4
            elif self.fill_step == 4:
                self.cups += int(user_input)
                self.state = "main_menu"

    def is_running(self):
        return self.state != "exit"


# ------------ RUN PROGRAM ------------

machine = CoffeeMachine()

while machine.is_running():
    if machine.state == "main_menu":
        print("Write action (buy, fill, take, remaining, exit):")

    user_input = input("> ")
    machine.process(user_input)
