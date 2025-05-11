import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 3
CELL_SIZE = WIDTH // GRID_SIZE
WHITE = (255, 255, 255)
LINE_COLOR = (0, 0, 0)
CIRCLE_COLOR = (0, 0, 255)
CROSS_COLOR = (255, 0, 0)
AI_PLAYER = 'O'
HUMAN_PLAYER = 'X'

# Initialize the game window
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")

# Functions
def draw_grid():
    for row in range(1, GRID_SIZE):
        pygame.draw.line(win, LINE_COLOR, (0, row * CELL_SIZE), (WIDTH, row * CELL_SIZE), 5)
        pygame.draw.line(win, LINE_COLOR, (row * CELL_SIZE, 0), (row * CELL_SIZE, HEIGHT), 5)

def draw_markers(board):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            marker = board[row][col]
            if marker == 'X':
                draw_cross(row, col)
            elif marker == 'O':
                draw_circle(row, col)

def draw_cross(row, col):
    x = col * CELL_SIZE + CELL_SIZE // 2
    y = row * CELL_SIZE + CELL_SIZE // 2
    pygame.draw.line(win, CROSS_COLOR, (x - CELL_SIZE // 2, y - CELL_SIZE // 2), (x + CELL_SIZE // 2, y + CELL_SIZE // 2), 5)
    pygame.draw.line(win, CROSS_COLOR, (x + CELL_SIZE // 2, y - CELL_SIZE // 2), (x - CELL_SIZE // 2, y + CELL_SIZE // 2), 5)

def draw_circle(row, col):
    x = col * CELL_SIZE + CELL_SIZE // 2
    y = row * CELL_SIZE + CELL_SIZE // 2
    pygame.draw.circle(win, CIRCLE_COLOR, (x, y), CELL_SIZE // 2 - 5)

def check_winner(board, player):
    for row in board:
        if all(cell == player for cell in row):
            return True

    for col in range(GRID_SIZE):
        if all(board[row][col] == player for row in range(GRID_SIZE)):
            return True

    if all(board[i][i] == player for i in range(GRID_SIZE)) or all(board[i][GRID_SIZE - 1 - i] == player for i in range(GRID_SIZE)):
        return True

    return False

def is_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def make_move(board, player, row, col):
    if board[row][col] == ' ':
        board[row][col] = player

def minimax(board, depth, is_maximizing):
    if check_winner(board, AI_PLAYER):
        return 1
    if check_winner(board, HUMAN_PLAYER):
        return -1
    if is_draw(board):
        return 0

    if is_maximizing:
        best_score = -float("inf")
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = AI_PLAYER
                    score = minimax(board, depth + 1, False)
                    board[i][j] = ' '
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = HUMAN_PLAYER
                    score = minimax(board, depth + 1, True)
                    board[i][j] = ' '
                    best_score = min(score, best_score)
        return best_score

def best_move(board):
    best_score = -float("inf")
    best_move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = AI_PLAYER
                score = minimax(board, 0, False)
                board[i][j] = ' '
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
    return best_move

def draw_ending_message(message):
    font = pygame.font.Font(None, 36)
    text = font.render(message, True, CROSS_COLOR)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    win.blit(text, text_rect)

def main(board):
    current_player = HUMAN_PLAYER
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if current_player == HUMAN_PLAYER:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    row = y // CELL_SIZE
                    col = x // CELL_SIZE
                    if board[row][col] == ' ':
                        make_move(board, HUMAN_PLAYER, row, col)
                        current_player = AI_PLAYER

            elif current_player == AI_PLAYER:
                ai_move = best_move(board)
                if ai_move:
                    make_move(board, AI_PLAYER, ai_move[0], ai_move[1])
                    current_player = HUMAN_PLAYER

            if check_winner(board, HUMAN_PLAYER):
                game_over = True
                draw_ending_message("Human player wins!")

            if check_winner(board, AI_PLAYER):
                game_over = True
                draw_ending_message("AI player wins!")

            if is_draw(board):
                game_over = True
                draw_ending_message("It's a draw!")

        win.fill(WHITE)
        draw_grid()
        draw_markers(board)
        pygame.display.update()

    # Final end screen loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # Reset the game board
                    board = [[' ' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
                    main(board)
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        draw_ending_message("Press 'R' to restart or 'Q' to quit")
        pygame.display.update()

if __name__ == "__main__":
    board = [[' ' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    main(board)
