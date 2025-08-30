import pygame
import random
import sys

# Configs
CELL_SIZE = 40
GRID_SIZE = 10
NUM_MINES = 15
WIDTH = HEIGHT = GRID_SIZE * CELL_SIZE

# Colors
COLORS = {
    0: (200, 200, 200),
    1: (0, 0, 255),
    2: (0, 128, 0),
    3: (255, 165, 0),
    4: (128, 0, 128),
    5: (255, 0, 0),
    6: (64, 224, 208),
    7: (0, 0, 0),
    8: (128, 128, 128),
}

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper")

font = pygame.font.SysFont(None, 30)

# Generate Minesweeper Board
def create_board():
    board = [['0' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    mines = set()
    while len(mines) < NUM_MINES:
        r = random.randint(0, GRID_SIZE - 1)
        c = random.randint(0, GRID_SIZE - 1)
        if (r, c) not in mines:
            board[r][c] = 'M'
            mines.add((r, c))

    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if board[r][c] == 'M':
                continue
            count = 0
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE:
                        if board[nr][nc] == 'M':
                            count += 1
            board[r][c] = str(count)
    return board

def reveal_zeros(r, c, board, revealed):
    stack = [(r, c)]
    while stack:
        row, col = stack.pop()
        if revealed[row][col]:
            continue
        revealed[row][col] = True
        if board[row][col] == '0':
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nr, nc = row + dr, col + dc
                    if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE:
                        if not revealed[nr][nc]:
                            stack.append((nr, nc))

def draw_board(board, revealed, game_over):
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            rect = pygame.Rect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if revealed[r][c] or game_over:
                pygame.draw.rect(screen, (180, 180, 180), rect)
                pygame.draw.rect(screen, (100, 100, 100), rect, 1)
                val = board[r][c]
                if val == 'M':
                    pygame.draw.circle(screen, (255, 0, 0), rect.center, 10)
                elif val != '0':
                    txt = font.render(val, True, COLORS[int(val)])
                    screen.blit(txt, (rect.x + 12, rect.y + 8))
            else:
                pygame.draw.rect(screen, (120, 120, 120), rect)
                pygame.draw.rect(screen, (60, 60, 60), rect, 1)

# Main loop
def main():
    board = create_board()
    revealed = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    game_over = False
    win = False

    while True:
        screen.fill((0, 0, 0))
        draw_board(board, revealed, game_over)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                x, y = event.pos
                row, col = y // CELL_SIZE, x // CELL_SIZE
                if board[row][col] == 'M':
                    game_over = True
                else:
                    reveal_zeros(row, col, board, revealed)

        # Check win
        if not game_over:
            unrevealed = sum(not cell for row in revealed for cell in row)
            if unrevealed == NUM_MINES:
                win = True
                game_over = True

        if game_over and win:
            print("🎉 You win!")
        elif game_over and not win:
            print("💥 You hit a mine!")

if __name__ == "__main__":
    main()
