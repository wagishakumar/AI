import random
import time

def print_board(board):
    """Prints the current state of the 3x3 board."""
    print("\n")
    print(f" {board[0]} | {board[1]} | {board[2]} ")
    print("---|---|---")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("---|---|---")
    print(f" {board[6]} | {board[7]} | {board[8]} ")
    print("\n")

def check_winner(board, player):
    """Checks if the specified player has won the game."""
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]              # Diagonals
    ]
    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] == player:
            return True
    return False

def check_draw(board):
    """Checks if the board is completely full (a tie game)."""
    return all(space in ["X", "O"] for space in board)

def get_computer_move(board):
    """Finds all empty spaces and picks one at random."""
    empty_spaces = [i for i, space in enumerate(board) if space not in ["X", "O"]]
    return random.choice(empty_spaces)

def play_game():
    """Main game loop managing human and computer turns."""
    board = [str(i) for i in range(1, 10)]
    current_player = "X"  # Player X is the Human, Player O is the Computer
    
    print("Welcome to Tic-Tac-Toe vs. Computer!")
    print("You are Player X. The Computer is Player O.")

    while True:
        print_board(board)
        
        if current_player == "X":
            # Human Player Turn
            try:
                choice = int(input("Your turn (X). Choose a spot (1-9): "))
                position = choice - 1
                
                if position < 0 or position > 8:
                    print("Invalid input! Please pick a number between 1 and 9.")
                    continue
                    
                if board[position] in ["X", "O"]:
                    print("That spot is already taken! Try another one.")
                    continue
                    
            except ValueError:
                print("Invalid input! Please type a valid integer.")
                continue
        else:
            # Computer Turn
            print("Computer (O) is thinking...")
            time.sleep(1) # Adds a small, natural-feeling delay
            position = get_computer_move(board)
            print(f"Computer chose spot {position + 1}")

        # Place the marker
        board[position] = current_player

        # Check for a win
        if check_winner(board, current_player):
            print_board(board)
            if current_player == "X":
                print("🎉 Congratulations! You beat the computer!")
            else:
                print("🤖 Game over! The computer wins.")
            break

        # Check for a tie
        if check_draw(board):
            print_board(board)
            print("🤝 It's a draw!")
            break

        # Switch turns
        current_player = "O" if current_player == "X" else "X"

if __name__ == "__main__":
    play_game()
