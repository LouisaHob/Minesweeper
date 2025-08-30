"""
This program begins to include some of the game logic for the minesweeper game.
Our previous code generated a board with mines and numbers indicating the number of adjacent mines.
This board can be any size and user can choose difficulty level.
This game logic will include the ability to reveal cells and check for game over conditions.
The board will first be printed for the player to view.
With '.' representing empty cells, the size of the board will be printed.
For readability, the board will also be printed with row and column numbers.
The player will be prompted to enter the row and column of the cell they want to reveal.
The program will check if the cell is a mine or not.
If the cell is a mine, the game is over.
If the cell is not a mine, the program will reveal the cell and check if it is empty.
If the cell is empty, the program will reveal all adjacent cells that are also empty.
If the cell is not empty, the program will reveal the cell and show the number of mines around it.
The program will continue to prompt the player for input until they either win or lose.
The program will also check if the player has won by revealing all non-mine cells.
The program will also check if the player has lost by revealing a mine.
"""

# ========= Import Libraries =========
import string  # for column letters

# Sample board (5x5) for testing
board = [
    [0, 0, 1, '#', '#'],
    [0, 1, 2, 2, 1],
    [0, 0, 1, '#', 1],
    [1, 1, 1, 1, 1],
    ['#', 1, 0, 0, 0]
]

row_length = 5

# ========== Create Visible Board ==========
def make_visible_board(row_length):
    # Create an empty visible board with '.' for hidden cells
    row_length_new = row_length + 1
    visible_board = [['.' for _ in range(row_length_new)] for _ in range(row_length_new)]

    # Fill top row with letters for columns (A, B, C, ...)
    for i in range(1, row_length_new):
        visible_board[0][i] = string.ascii_uppercase[i - 1]

    # Fill first column with numbers for rows (0, 1, 2, ...)
    for i in range(1, row_length_new):
        visible_board[i][0] = str(i - 1)

    # Set top-left corner empty
    visible_board[0][0] = ' '

    # Print the board for display
    for row in visible_board:
        print(' '.join(row))
    print()

    return visible_board

# ========== Get User Input for Cell Choice ==========
def get_cell_choice(row_length):
    while True:
        try:
            cell_choice = input("Enter the cell you want to reveal (e.g., A1): ").upper()
            if len(cell_choice) < 2 or len(cell_choice) > 3:
                raise ValueError("Invalid input length.")
            
            col = string.ascii_uppercase.index(cell_choice[0]) + 1
            row = int(cell_choice[1:]) + 1

            if col < 1 or col > row_length or row < 1 or row > row_length:
                raise ValueError("Cell out of bounds.")

            return row, col

        except (ValueError, IndexError):
            print("Invalid input. Please enter a valid cell (e.g., A1).")

# ========== Reveal Logic ==========
def reveal_cell(board, row, col):
    # Adjust for index (0-based for board, 1-based for user input)
    if board[row][col] == '#':
        print("Game Over! You hit a mine.")
        return False  # Game over
    else:
        print(f"You revealed cell {row}, {col}.")
        return True  # Continue game

# ========== Reveal Adjacent Cells Recursively ==========
def reveal_cells(row, col, board, visible_board, row_length, revealed=set()):
    # Prevent infinite loops by tracking revealed cells
    if (row, col) in revealed:
        return
    revealed.add((row, col))

    # Reveal this cell
    visible_board[row][col] = str(board[row - 1][col - 1])  # adjust for label row/col

    # If it's not zero, stop
    if board[row - 1][col - 1] != 0:
        return

    # Otherwise, explore all adjacent cells (8 directions)
    directions = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1),          (0, 1),
                  (1, -1),  (1, 0), (1, 1)]
    
    for dr, dc in directions:
        r, c = row + dr, col + dc
        if 1 <= r <= row_length and 1 <= c <= row_length:
            if visible_board[r][c] == '.':
                reveal_cells(r, c, board, visible_board, row_length, revealed)

# ========== Main Game Loop ==========
# Initialize visible board and print it
visible_board = make_visible_board(row_length)

# Game loop
game_over = False
while not game_over:
    # Get the user's choice for the cell they want to reveal
    player_row, player_col = get_cell_choice(row_length)

    # Check if it's a mine
    if not reveal_cell(board, player_row - 1, player_col - 1):  # adjust for 0-indexed board
        # Game over if it's a mine, reveal the entire board
        game_over = True
        print("Game Over! Here's the full board with the revealed mines:")
        # Reveal all mines (reveal all the '#' cells in the board)
        for r in range(row_length):
            for c in range(row_length):
                if board[r][c] == '#':
                    visible_board[r+1][c+1] = '#'  # Adjust for row/col numbering
        # Print the board showing the mines
        for row in visible_board:
            print(' '.join(row))
    else:
        # If safe, reveal all connected cells if they are empty (0)
        reveal_cells(player_row, player_col, board, visible_board, row_length)

        # Show the updated visible board
        for row in visible_board:
            print(' '.join(row))
    
    # You can check here if the player has won by revealing all non-mine cells.
    # This check can be added at the end of the game loop if desired.

    """
    Final thing I need to do is add win conditions
    The player wins if they reveal all the cells that are not mines.
    I need to add both codes together to make a playable game.
    I need to add exception handing to this code.
    In the final program I will add colour and an emoji to the board when a player hits a mine.
    The final step is turning the game into a GUI game. 
    """
