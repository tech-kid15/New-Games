# Creates a list with 9 empty spaces
board = [" " for _ in range(9)]

def print_board():
    print()
    print(f"{board[0]} | {board[1]} | {board[2]} |  ")
    print("---  ---  ---")
    print(f"{board[3]} | {board[4]} | {board[5]}  | ")
    print("---  ---  ---")
    print(f"{board[6]} | {board[7]} | {board[8]}  | ")
    print()

def make_move(player):
    while True:
        try:
            move = int(input(f"Player {player}, choose a position (0-8): "))
            if 0<= move <9 and board[move] == " ":
                board[move]=player
                break
            else:
                print("Invalid move. Try again.")
            
        except ValueError:
            print("Please enter a number from 0 to 8")

def check_winner(player):
    win_combos = [ [0,1,2], [3,4,5], [6,7,8], 
                  [0,3,6], [1,4,7], [2,5,8],
                  [0,4,8], [2,4,6]
    ]

    for combo in win_combos:
        if all(board[i] == player for i in combo):
            return True
    return False




def is_tie():
    return " " not in board


def play_game():
    current_player = "X"
    print_board()

    while True:
        make_move(current_player)
        print_board()

        if check_winner(current_player):
            print(f"🎉 Player {current_player} wins!")
            break
            play_game()
        elif is_tie():
            print("It is a tie!")
            break
            play_game()
        current_player = "O" if current_player == "X" else "X"
play_game()
