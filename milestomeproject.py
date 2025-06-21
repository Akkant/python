def print_guide():
    print("Position guide:")
    print(" 1 | 2 | 3 ")
    print("---+---+---")
    print(" 4 | 5 | 6 ")
    print("---+---+---")
    print(" 7 | 8 | 9 ")
    print()

def print_board(board):
    print()
    print(f" {board[0]} | {board[1]} | {board[2]} ")
    print("---+---+---")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("---+---+---")
    print(f" {board[6]} | {board[7]} | {board[8]} ")
    print()

def check_win(board, mark):
    wins = [
        [0,1,2], [3,4,5], [6,7,8],
        [0,3,6], [1,4,7], [2,5,8],
        [0,4,8], [2,4,6]
    ]
    return any(all(board[i] == mark for i in combo) for combo in wins)

def play_game():
    board = [' '] * 9
    current = 'X'

    print_guide()

    for _ in range(9):
        print_board(board)
        try:
            move = int(input(f"Player {current}, choose a position (1-9): ")) - 1
            if move < 0 or move > 8 or board[move] != ' ':
                print("Invalid move. Try again.")
                continue
        except:
            print("Please enter a valid number.")
            continue

        board[move] = current

        if check_win(board, current):
            print_board(board)
            print(f"Player {current} wins! 🎉")
            return

        current = 'O' if current == 'X' else 'X'

    print_board(board)
    print("It's a tie!")

play_game()