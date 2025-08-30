"""This is a fully playable version of the classic Minesweeper game."""

import random
import string

# Define Functions
def board_size():
    while True:
        try:
            row_length = int(input("How big would you like the board to be? (between 5 and 20): "))
            if row_length < 5:
                print("Oof! Too small ... Please enter a value between 5 and 20.")
                continue
            if row_length > 20:
                print("That's too big! Are you crazy?! Please enter a value between 5 and 20.")
                continue
            board_size = row_length * row_length
            return row_length, board_size
        except ValueError:
            print("Invalid input! Please enter an integer number.")

def get_difficulty(board_size):
    display_options = ("What difficulty level would you like to play? "
                       "Please choose from the following options:\n"
                       "e = Easy\n"
                       "m = Medium\n"
                       "h = Hard\n")
    print(display_options)
    while True:
        difficulty = input("Please enter your choice: ").lower()
        if difficulty == 'e':
            print("You have chosen Easy difficulty.")
            no_mines = int(board_size * 0.12)
            return no_mines
        elif difficulty == 'm':
            print("You have chosen Medium difficulty.")
            no_mines = int(board_size * 0.15)
            return no_mines
        elif difficulty == 'h':
            print("You have chosen Hard difficulty.")
            no_mines = int(board_size * 0.20)
            return no_mines
        else:
            print("Invalid choice. Please enter 'e', 'm', or 'h'.")

def make_board(row_length, board_size, no_mines):
    mine_list = ['#'] * no_mines + ['-'] * (board_size - no_mines)
    random.shuffle(mine_list)
    board = [mine_list[i:i + row_length] for i in range(0, board_size, row_length)]
    return board

def print_board(board):
    for row in board:
        print(' '.join(row))
    print()

def is_valid(board, row, col):
    return 0 <= row < len(board) and 0 <= col < len(board[0])

def add_mine(board, row, col):
    directions = [(-1, -1), (-1, 0), (-1, 1),
                  ( 0, -1),         ( 0, 1),
                  ( 1, -1), ( 1, 0), ( 1, 1)]
    
    for dr, dc in directions:
        new_row = row + dr
        new_col = col + dc
        if is_valid(board, new_row, new_col) and board[new_row][new_col] != '#':
            if board[new_row][new_col] == '-':
                board[new_row][new_col] = '1'
            else:
                board[new_row][new_col] = str(int(board[new_row][new_col]) + 1)

def count_mines(board):
    for row_index, row in enumerate(board):
        for col_index, cell in enumerate(row):
            if cell == '#':
                add_mine(board, row_index, col_index)

def fill_empty_cells(board):
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == '-':
                board[row][col] = '0'

def make_visible_board(row_length):
    visible_board = [['.' for _ in range(row_length)] for _ in range(row_length)]

    # Add column labels
    visible_board.insert(0, [' '] + list(string.ascii_uppercase[:row_length]))

    # Add row numbers
    for i in range(1, row_length + 1):
        visible_board[i].insert(0, str(i))

    return visible_board

def get_cell_choice(row_length):
    while True:
        try:
            cell_choice = input("Enter the cell you want to reveal (e.g., A1): ").upper()
            if len(cell_choice) < 2 or len(cell_choice) > 3:
                raise ValueError("Invalid input length.")
            
            col = string.ascii_uppercase.index(cell_choice[0])  # Get column index
            row = int(cell_choice[1:]) - 1  # Convert to 0-indexed

            if col < 0 or col >= row_length or row < 0 or row >= row_length:
                raise ValueError("Cell out of bounds.")

            return row, col

        except (ValueError, IndexError):
            print("Invalid input. Please enter a valid cell (e.g., A1).")

def reveal_cell(board, row, col):
    if board[row][col] == '#':
        print("Game Over! You hit a mine.")
        return False
    else:
        print(f"You revealed cell {row+1},{col+1}.")
        return True

def reveal_cells(row, col, board, visible_board, row_length, revealed=set()):
    if (row, col) in revealed:
        return
    revealed.add((row, col))

    visible_board[row + 1][col + 1] = str(board[row][col])  # Update visible board

    if board[row][col] != '0':
        return

    directions = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1),          (0, 1),
                  (1, -1),  (1, 0), (1, 1)]
    
    for dr, dc in directions:
        r, c = row + dr, col + dc
        if 0 <= r < row_length and 0 <= c < row_length:
            if visible_board[r + 1][c + 1] == '.':
                reveal_cells(r, c, board, visible_board, row_length, revealed)

def check_win(board, visible_board):
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] != '#' and visible_board[row + 1][col + 1] == '.':
                return False
    return True

# Main Program
try:
    row_length, board_size = board_size()
    no_mines = get_difficulty(board_size)
    board = make_board(row_length, board_size, no_mines)

    count_mines(board)
    fill_empty_cells(board)

    visible_board = make_visible_board(row_length)

    game_over = False
    while not game_over:
        for row in visible_board:
            print(' '.join(row))
        print()

        player_row, player_col = get_cell_choice(row_length)

        if not reveal_cell(board, player_row, player_col):
            game_over = True
            print("Game Over! Here's the full board with the revealed mines:")
            # Show full board on game over
            for r in range(row_length):
                for c in range(row_length):
                    if board[r][c] == '#':
                        visible_board[r + 1][c + 1] = '#'
            for row in visible_board:
                print(' '.join(row))
        else:
            reveal_cells(player_row, player_col, board, visible_board, row_length)

            if check_win(board, visible_board):
                game_over = True
                print("Congratulations, you've won the game! Here's the full board:")
                # Show full board when player wins
                for r in range(row_length):
                    for c in range(row_length):
                        if board[r][c] == '#':
                            visible_board[r + 1][c + 1] = '#'
                for row in visible_board:
                    print(' '.join(row))

except Exception as e:
    print(f"An error occurred: {e}")