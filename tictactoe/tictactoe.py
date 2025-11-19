def print_board(cells):
    print("---------")
    for i in range(0, 9, 3):
        print(f"| {cells[i]} {cells[i+1]} {cells[i+2]} |")
    print("---------")

def check_winner(cells):
    lines = [
        cells[0:3],
        cells[3:6],
        cells[6:9],
        cells[0::3],
        cells[1::3],
        cells[2::3],
        cells[0:9:4],
        cells[2:7:2]
    ]

    if ["X", "X", "X"] in lines:
        return "X"
    if ["O", "O", "O"] in lines:
        return "O"
    return None

def game_state(cells):
    winner = check_winner(cells)
    if winner == "X":
        return "X wins"
    if winner == "O":
        return "O wins"
    if "_" not in cells:
        return "Draw"
    return "Game not finished"

def get_valid_coordinates(cells):
    while True:
        coords = input("Enter the coordinates: ").split()

        if len(coords) != 2:
            print("You should enter numbers!")
            continue

        if not (coords[0].isdigit() and coords[1].isdigit()):
            print("You should enter numbers!")
            continue

        x, y = int(coords[0]), int(coords[1])

        if x not in [1, 2, 3] or y not in [1, 2, 3]:
            print("Coordinates should be from 1 to 3!")
            continue

        index = (x - 1) + (3 - y) * 3

        if cells[index] != "_":
            print("This cell is occupied! Choose another one!")
            continue

        return index

def main():
    cells = ["_"] * 9

    print_board(cells)

    current_player = "X"

    while True:
        move_index = get_valid_coordinates(cells)
        cells[move_index] = current_player

        print_board(cells)

        state = game_state(cells)
        if state != "Game not finished":
            print(state)
            break

        current_player = "O" if current_player == "X" else "X"

if __name__ == "__main__":
    main()
