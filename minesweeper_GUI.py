import tkinter as tk
import random

class Minesweeper:
    def __init__(self, master, rows=8, cols=8, mines=10):
        self.master = master
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.board = [['' for _ in range(cols)] for _ in range(rows)]
        self.revealed = [[False for _ in range(cols)] for _ in range(rows)]
        self.buttons = {}
        self.game_over = False

        self.place_mines()
        self.calculate_numbers()
        self.create_buttons()

    def place_mines(self):
        positions = random.sample(range(self.rows * self.cols), self.mines)
        for pos in positions:
            r, c = divmod(pos, self.cols)
            self.board[r][c] = 'M'

    def calculate_numbers(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] == 'M':
                    continue
                count = 0
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < self.rows and 0 <= nc < self.cols:
                            if self.board[nr][nc] == 'M':
                                count += 1
                self.board[r][c] = str(count) if count > 0 else ''

    def create_buttons(self):
        for r in range(self.rows):
            for c in range(self.cols):
                btn = tk.Button(self.master, width=2, height=1, command=lambda r=r, c=c: self.reveal(r, c))
                btn.grid(row=r, column=c)
                self.buttons[(r, c)] = btn

    def reveal(self, r, c):
        if self.revealed[r][c] or self.game_over:
            return

        self.revealed[r][c] = True
        btn = self.buttons[(r, c)]
        value = self.board[r][c]

        if value == 'M':
            btn.config(text='💣', bg='red')
            self.end_game()
        else:
            btn.config(text=value, relief=tk.SUNKEN, state='disabled')
            if value == '':
                # Reveal surrounding tiles
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < self.rows and 0 <= nc < self.cols:
                            self.reveal(nr, nc)

    def end_game(self):
        self.game_over = True
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] == 'M':
                    self.buttons[(r, c)].config(text='💣', bg='red')
        print("Game over!")

# Run it
root = tk.Tk()
root.title("Minesweeper")
game = Minesweeper(root)
root.mainloop()
