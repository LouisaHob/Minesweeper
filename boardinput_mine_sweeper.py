"""
This program alters my previous code to make it more interactive.
Previously, the board was generated and printed on a set number of rows and columns.
Now, the user can input the number of rows and columns they want.
The program will then generate a board of that size and print it.
The program will have a limit to the number of rows and columns
the user can input.
The program will spit out 'That's too big! Are you crazy?!' if the user inputs a number larger than 20.
The program will also run an error is the user tries to input a board less than 5 rows or columns.
Finally the program will ask the player to choose a difficulty level.
The difficulty level will determine the number of mines on the board.
The number of mines needs to be proportional to the size of the board.
Easy = 12% of the board
Medium = 15% of the board
Hard = 20% of the board
Probably need to cast float to int to get the number of mines.
"""

# ========= Import Libraries =========
import random

# ========= Define Functions =========

def board_size():
    # Request the user to input the size of the board they would like
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
    # Print the board in a readable format
    for row in board:
        print(' '.join(row))
    print()

# Logic copied from the original code
def is_valid(board, row, col):
    # Check if the row and col are inside the board
    return 0 <= row < len(board) and 0 <= col < len(board[0])

def add_mine(board, row, col):
    # All 8 directions around a cell
    directions = [(-1, -1), (-1, 0), (-1, 1),
                  ( 0, -1),         ( 0, 1),
                  ( 1, -1), ( 1, 0), ( 1, 1)]
    
    for dr, dc in directions:
        new_row = row + dr  # dr = direction row
        new_col = col + dc  # dc = direction column
        # Check if the new cell is valid and not a mine
         # Check if the cell is within bounds
        if is_valid(board, new_row, new_col) and board[new_row][new_col] != '#':
            if board[new_row][new_col] == '-':
                board[new_row][new_col] = '1'
            else:
                board[new_row][new_col] = str(int(board[new_row][new_col]) + 1)

def count_mines(board):
    # Go through the board and add numbers around each mine
    for row_index, row in enumerate(board):
        for col_index, cell in enumerate(row):
            if cell == '#':
                add_mine(board, row_index, col_index)

def fill_empty_cells(board):
    # Replace all remaining '-' with '0'
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == '-':
                board[row][col] = '0'

# ========== Main Program =========

try:
    row_length, board_size = board_size()  # Get the board dimensions
    no_mines = get_difficulty(board_size)  # Get the number of mines based on difficulty
    board = make_board(row_length, board_size, no_mines)  # Create the board

    print("Original Board:")
    print_board(board)  # Print the original board
except Exception as e:
    print(f"An error occurred: {e}")

# The program will now generate a board of the specified size and difficulty level.
# The board will be printed with mines represented by '#' and empty spaces by '-'.
# The next steps would be to implement the mine counting and game logic.
# The program could be further improved by adding a function to count the mines around each cell

count_mines(board)

# Replace all remaining '-' with '0'
fill_empty_cells(board)

print("Board with Mine Counts:")
print_board(board)
# The board will now show the number of mines around each cell.

"""
Next stage of my minesweeper program is to make it playable. 
In order to do this, I need to add a function that allows the player to reveal cells.
The player will input the row and column of the cell they want to reveal.
The row and column need to be within the bounds of the board.
The row and colomn need to be converted to a number between 0 and the length of the board.
The program will then check if the cell is a mine or not.
If the cell is a mine, the game is over.
If the cell is not a mine, the program will reveal the cell and check if it is empty.
If the cell is empty, the program will reveal all adjacent cells that are also empty.
If the cell is not empty, the program will reveal the cell and show the number of mines around it.
The program will also need a function to check if the player has won or lost.
The player wins if all the cells that are not mines are revealed.
The player loses if they reveal a mine.
"""