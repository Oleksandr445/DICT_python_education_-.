import random

def create_domino_set():
    return [[i, j] for i in range(7) for j in range(i, 7)]

def deal_pieces():
    while True:
        full_set = create_domino_set()
        random.shuffle(full_set)

        player = full_set[:7]
        computer = full_set[7:14]
        stock = full_set[14:]


        player_doubles = [p for p in player if p[0] == p[1]]
        computer_doubles = [c for c in computer if c[0] == c[1]]

        if not player_doubles and not computer_doubles:
            continue

        max_player = max(player_doubles) if player_doubles else [-1, -1]
        max_computer = max(computer_doubles) if computer_doubles else [-1, -1]

        if max_player > max_computer:
            snake = [max_player]
            player.remove(max_player)
            status = "computer"
        else:
            snake = [max_computer]
            computer.remove(max_computer)
            status = "player"

        return stock, computer, player, snake, status



def print_state(stock, computer, player, snake, status):
    print("=" * 70)
    print(f"Stock size: {len(stock)}")
    print(f"Computer pieces: {len(computer)}")


    if len(snake) > 6:
        print("".join(map(str, snake[:3])) + "..." + "".join(map(str, snake[-3:])))
    else:
        print("".join(map(str, snake)))

    print("\nYour pieces:")
    for i, p in enumerate(player, 1):
        print(f"{i}:{p}")

    if status == "player":
        print("\nStatus: It's your turn to make a move. Enter your command.")
    else:
        print("\nStatus: Computer is about to make a move. Press Enter to continue...")



def is_valid_move(piece, snake, side):
    if side == "left":
        return piece[0] == snake[0][0] or piece[1] == snake[0][0]
    else:
        return piece[0] == snake[-1][1] or piece[1] == snake[-1][1]


def place_piece(piece, snake, side):
    if side == "left":
        if piece[1] == snake[0][0]:
            snake.insert(0, piece)
        else:
            snake.insert(0, piece[::-1])
    else:
        if piece[0] == snake[-1][1]:
            snake.append(piece)
        else:
            snake.append(piece[::-1])



def player_move(player, stock, snake):
    while True:
        move = input("> ")


        if not move.lstrip("-").isdigit():
            print("Invalid input. Please try again.")
            continue

        move = int(move)

        if abs(move) > len(player):
            print("Invalid input. Please try again.")
            continue

        if move == 0:
            if stock:
                player.append(stock.pop())
            return

        piece = player[abs(move) - 1]
        side = "right" if move > 0 else "left"

        if not is_valid_move(piece, snake, side):
            print("Illegal move. Please try again.")
            continue

        player.pop(abs(move) - 1)
        place_piece(piece, snake, side)
        return



def computer_move(computer, stock, snake):
    input()


    count = {i: 0 for i in range(7)}
    for piece in computer + snake:
        count[piece[0]] += 1
        count[piece[1]] += 1


    scored = []
    for piece in computer:
        score = count[piece[0]] + count[piece[1]]
        scored.append((score, piece))

    scored.sort(reverse=True)

    for _, piece in scored:
        if is_valid_move(piece, snake, "right"):
            computer.remove(piece)
            place_piece(piece, snake, "right")
            return
        if is_valid_move(piece, snake, "left"):
            computer.remove(piece)
            place_piece(piece, snake, "left")
            return

    if stock:
        computer.append(stock.pop())



def check_game_over(player, computer, snake):
    if not player:
        print("Status: The game is over. You won!")
        return True

    if not computer:
        print("Status: The game is over. The computer won!")
        return True

    left = snake[0][0]
    right = snake[-1][1]

    if left == right:
        count = sum(piece.count(left) for piece in snake)
        if count == 8:
            print("Status: The game is over. It's a draw!")
            return True

    return False



def main():
    stock, computer, player, snake, status = deal_pieces()

    while True:
        print_state(stock, computer, player, snake, status)

        if check_game_over(player, computer, snake):
            break

        if status == "player":
            player_move(player, stock, snake)
            status = "computer"
        else:
            computer_move(computer, stock, snake)
            status = "player"


main()