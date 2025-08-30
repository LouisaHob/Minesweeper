"""
This program creates a Minesweeper board with 5 mines and 20 empty cells.
The mines and mine-free cells are randomly placed on the board.
The program then counts the number of mines surrounding each cell and
displays the board with the mine counts.
The boards are represented as a 2D list, where:
- '#' represents a mine
- '-' represents an empty cell
- '0' represents a cell with no surrounding mines
- 'n' represents a cell with 'n' surrounding mines, where n is a number

The program includes functions to create the board, print the board,
count the mines, and fill empty cells with '0'.
"""

import random

def make_board():
    # Create a 1D list of 25 random mines and mine-free cells
    mine_list = ['#'] * 5 + ['-'] * 20
    random.shuffle(mine_list)
    # Create a 2D board from the 1D list
    board = [mine_list[i:i + 5] for i in range(0, 25, 5)]
    return board

def print_board(board):
    # Print the board in a readable format
    for row in board:
        print(' '.join(row))
    print()

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

board = make_board()
print("Original Board:")
print_board(board)

count_mines(board)

# Replace all remaining '-' with '0'
fill_empty_cells(board)

print("Board with Mine Counts:")
print_board(board)

# This program could be improved by recieving input from the user 
# to specify the number of mines (difficulty level) and the size of the board.
# This would make the game more interactive and customisable.
# In order to be playable, the program needs a function to reveal cells
# and check for game over conditions (dead/still alive).
# The current implementation is a basic version of the game. 
# I spent ages on this, so I hope you like it!
# The code is not complete and lacks the game logic to make it playable;
# I plan on working on a playable version of the game, 
# including exception handling and user input!
