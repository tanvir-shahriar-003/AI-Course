import pygame
import sys
import math
import random


# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 700, 700
COLS, ROWS = 7, 6
SQUARE_SIZE = 80
RADIUS = SQUARE_SIZE // 2 - 5
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
GREEN = (0, 128, 0)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connect Four with Minimax")
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 36)

class ConnectFour:
    def __init__(self):
        self.board = [[' ' for _ in range(COLS)] for _ in range(ROWS)]
        self.current_player = 'R'
        self.game_over = False
        self.winner = None

    def make_move(self, col):
        if self.game_over:
            return False
            
        for row in range(ROWS-1, -1, -1):
            if self.board[row][col] == ' ':
                self.board[row][col] = self.current_player
                
                if self.check_winner(row, col):
                    self.game_over = True
                    self.winner = self.current_player
                elif self.is_board_full():
                    self.game_over = True
                    self.winner = 'Tie'
                else:
                    self.current_player = 'Y' if self.current_player == 'R' else 'R'
                return True
        return False

    def is_board_full(self):
        return all(self.board[0][col] != ' ' for col in range(COLS))

    def check_winner(self, row, col):
        player = self.board[row][col]
        
        # Check horizontal
        for c in range(max(0, col-3), min(COLS-3, col+1)):
            if all(self.board[row][c+i] == player for i in range(4)):
                return True

        # Check vertical
        for r in range(max(0, row-3), min(ROWS-3, row+1)):
            if all(self.board[r+i][col] == player for i in range(4)):
                return True

        # Check diagonal (top-left to bottom-right)
        for r in range(max(0, row-3), min(ROWS-3, row+1)):
            for c in range(max(0, col-3), min(COLS-3, col+1)):
                if all(self.board[r+i][c+i] == player for i in range(4)):
                    return True

        # Check diagonal (bottom-left to top-right)
        for r in range(min(ROWS-1, row+3), max(2, row-1), -1):
            for c in range(max(0, col-3), min(COLS-3, col+1)):
                if all(self.board[r-i][c+i] == player for i in range(4)):
                    return True

        return False

    def get_valid_moves(self):
        return [col for col in range(COLS) if self.board[0][col] == ' ']

    def minimax(self, depth, alpha, beta, is_maximizing):
        valid_moves = self.get_valid_moves()
        
        if depth == 0 or self.game_over or not valid_moves:
            if self.game_over:
                if self.winner == 'Y':
                    return 1000, None
                elif self.winner == 'R':
                    return -1000, None
                else:
                    return 0, None
            else:
                return self.evaluate_board(), None

        if is_maximizing:
            max_eval = -float('inf')
            best_col = random.choice(valid_moves)
            
            for col in valid_moves:
                row = self.get_next_open_row(col)
                self.board[row][col] = 'Y'
                
                eval_score, _ = self.minimax(depth - 1, alpha, beta, False)
                
                self.board[row][col] = ' '
                
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_col = col
                
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            
            return max_eval, best_col
        else:
            min_eval = float('inf')
            best_col = random.choice(valid_moves)
            
            for col in valid_moves:
                row = self.get_next_open_row(col)
                self.board[row][col] = 'R'
                
                eval_score, _ = self.minimax(depth - 1, alpha, beta, True)
                
                self.board[row][col] = ' '
                
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_col = col
                
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            
            return min_eval, best_col

    def get_next_open_row(self, col):
        for row in range(ROWS-1, -1, -1):
            if self.board[row][col] == ' ':
                return row
        return -1

    def evaluate_board(self):
        score = 0
        
        # Evaluate center column
        center_array = [self.board[row][COLS//2] for row in range(ROWS)]
        center_count = center_array.count('Y')
        score += center_count * 3
        
        # Evaluate horizontal
        for row in range(ROWS):
            row_array = self.board[row]
            for col in range(COLS-3):
                window = row_array[col:col+4]
                score += self.evaluate_window(window)
        
        # Evaluate vertical
        for col in range(COLS):
            col_array = [self.board[row][col] for row in range(ROWS)]
            for row in range(ROWS-3):
                window = col_array[row:row+4]
                score += self.evaluate_window(window)
        
        # Evaluate positive diagonal
        for row in range(ROWS-3):
            for col in range(COLS-3):
                window = [self.board[row+i][col+i] for i in range(4)]
                score += self.evaluate_window(window)
        
        # Evaluate negative diagonal
        for row in range(3, ROWS):
            for col in range(COLS-3):
                window = [self.board[row-i][col+i] for i in range(4)]
                score += self.evaluate_window(window)
        
        return score

    def evaluate_window(self, window):
        score = 0
        opponent = 'R'
        player = 'Y'
        
        if window.count(player) == 4:
            score += 100
        elif window.count(player) == 3 and window.count(' ') == 1:
            score += 5
        elif window.count(player) == 2 and window.count(' ') == 2:
            score += 2
        
        if window.count(opponent) == 3 and window.count(' ') == 1:
            score -= 4
        
        return score

    def ai_move(self):
        if self.current_player == 'Y' and not self.game_over:
            _, best_col = self.minimax(4, -float('inf'), float('inf'), True)
            if best_col is not None:
                self.make_move(best_col)

    def reset_game(self):
        self.__init__()

    def draw(self, screen):
        screen.fill(BLUE)
        
        # Draw title
        title_text = font.render("Connect Four", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 20))
        
        # Draw board
        board_x = (WIDTH - COLS * SQUARE_SIZE) // 2
        board_y = 100
        
        for row in range(ROWS):
            for col in range(COLS):
                pygame.draw.rect(screen, BLUE, 
                               (board_x + col * SQUARE_SIZE, 
                                board_y + row * SQUARE_SIZE, 
                                SQUARE_SIZE, SQUARE_SIZE))
                pygame.draw.circle(screen, WHITE, 
                                 (board_x + col * SQUARE_SIZE + SQUARE_SIZE // 2, 
                                  board_y + row * SQUARE_SIZE + SQUARE_SIZE // 2), 
                                 RADIUS)
                
                if self.board[row][col] == 'R':
                    pygame.draw.circle(screen, RED, 
                                     (board_x + col * SQUARE_SIZE + SQUARE_SIZE // 2, 
                                      board_y + row * SQUARE_SIZE + SQUARE_SIZE // 2), 
                                     RADIUS)
                elif self.board[row][col] == 'Y':
                    pygame.draw.circle(screen, YELLOW, 
                                     (board_x + col * SQUARE_SIZE + SQUARE_SIZE // 2, 
                                      board_y + row * SQUARE_SIZE + SQUARE_SIZE // 2), 
                                     RADIUS)
        
        # Draw game status
        if self.game_over:
            if self.winner == 'Tie':
                status_text = "Game Over: It's a Tie!"
            else:
                winner_name = "Red" if self.winner == 'R' else "Yellow"
                status_text = f"Game Over: {winner_name} wins!"
            status_color = GREEN
        else:
            player_name = "Red" if self.current_player == 'R' else "Yellow"
            status_text = f"Current Player: {player_name}"
            status_color = RED if self.current_player == 'R' else YELLOW
        
        text = font.render(status_text, True, status_color)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 650))
        
        # Draw reset button
        pygame.draw.rect(screen, GRAY, (WIDTH // 2 - 75, 50, 150, 40))
        reset_text = font.render("Reset", True, BLACK)
        screen.blit(reset_text, (WIDTH // 2 - reset_text.get_width() // 2, 55))

def main():
    game = ConnectFour()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                
                # Check reset button
                if WIDTH // 2 - 75 <= x <= WIDTH // 2 + 75 and 50 <= y <= 90:
                    game.reset_game()
                    continue
                
                # Check board click
                board_x = (WIDTH - COLS * SQUARE_SIZE) // 2
                board_y = 100
                
                if board_x <= x <= board_x + COLS * SQUARE_SIZE and board_y <= y <= board_y + ROWS * SQUARE_SIZE:
                    col = (x - board_x) // SQUARE_SIZE
                    
                    if 0 <= col < COLS:
                        if game.current_player == 'R':  # Human player
                            if game.make_move(col):
                                # AI move after human move
                                if not game.game_over:
                                    game.ai_move()
        
        game.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
