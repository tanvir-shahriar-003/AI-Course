import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 700
BOARD_SIZE = 3
SQUARE_SIZE = 150
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 128, 0)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe with Minimax")
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 36)
small_font = pygame.font.SysFont('Arial', 24)

class TicTacToe:
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.game_over = False
        self.winner = None

    def make_move(self, row, col):
        if self.board[row][col] == ' ' and not self.game_over:
            self.board[row][col] = self.current_player
            if self.check_winner(self.current_player):
                self.game_over = True
                self.winner = self.current_player
            elif self.is_board_full():
                self.game_over = True
                self.winner = 'Tie'
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'

    def is_board_full(self):
        for row in self.board:
            if ' ' in row:
                return False
        return True

    def check_winner(self, player):
        # Check rows
        for row in self.board:
            if all(cell == player for cell in row):
                return True

        # Check columns
        for col in range(3):
            if all(self.board[row][col] == player for row in range(3)):
                return True

        # Check diagonals
        if all(self.board[i][i] == player for i in range(3)):
            return True
        if all(self.board[i][2-i] == player for i in range(3)):
            return True

        return False

    def get_empty_cells(self):
        empty_cells = []
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == ' ':
                    empty_cells.append((row, col))
        return empty_cells

    def minimax(self, depth, is_maximizing):
        if self.check_winner('X'):
            return -10 + depth, None
        if self.check_winner('O'):
            return 10 - depth, None
        if self.is_board_full():
            return 0, None

        if is_maximizing:
            best_score = -float('inf')
            best_move = None
            for row, col in self.get_empty_cells():
                self.board[row][col] = 'O'
                score, _ = self.minimax(depth + 1, False)
                self.board[row][col] = ' '
                if score > best_score:
                    best_score = score
                    best_move = (row, col)
            return best_score, best_move
        else:
            best_score = float('inf')
            best_move = None
            for row, col in self.get_empty_cells():
                self.board[row][col] = 'X'
                score, _ = self.minimax(depth + 1, True)
                self.board[row][col] = ' '
                if score < best_score:
                    best_score = score
                    best_move = (row, col)
            return best_score, best_move

    def ai_move(self):
        if self.current_player == 'O' and not self.game_over:
            _, move = self.minimax(0, True)
            if move:
                self.make_move(move[0], move[1])

    def reset_game(self):
        self.__init__()

    def draw(self, screen):
        screen.fill(WHITE)
        
        # Draw title
        title_text = font.render("Tic Tac Toe", True, BLACK)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 20))
        
        # Draw board
        board_x = (WIDTH - 3 * SQUARE_SIZE) // 2
        board_y = 100
        
        for i in range(1, 3):
            pygame.draw.line(screen, BLACK, 
                           (board_x, board_y + i * SQUARE_SIZE), 
                           (board_x + 3 * SQUARE_SIZE, board_y + i * SQUARE_SIZE), 3)
            pygame.draw.line(screen, BLACK, 
                           (board_x + i * SQUARE_SIZE, board_y), 
                           (board_x + i * SQUARE_SIZE, board_y + 3 * SQUARE_SIZE), 3)
        
        # Draw X's and O's
        for row in range(3):
            for col in range(3):
                x_pos = board_x + col * SQUARE_SIZE + SQUARE_SIZE // 2
                y_pos = board_y + row * SQUARE_SIZE + SQUARE_SIZE // 2
                if self.board[row][col] == 'X':
                    pygame.draw.line(screen, RED, 
                                   (x_pos - 40, y_pos - 40), 
                                   (x_pos + 40, y_pos + 40), 5)
                    pygame.draw.line(screen, RED, 
                                   (x_pos + 40, y_pos - 40), 
                                   (x_pos - 40, y_pos + 40), 5)
                elif self.board[row][col] == 'O':
                    pygame.draw.circle(screen, BLUE, (x_pos, y_pos), 40, 5)
        
        # Draw game status
        if self.game_over:
            if self.winner == 'Tie':
                status_text = "Game Over: It's a Tie!"
            else:
                status_text = f"Game Over: {self.winner} wins!"
            status_color = GREEN
        else:
            status_text = f"Current Player: {self.current_player}"
            status_color = BLACK if self.current_player == 'X' else BLUE
        
        text = font.render(status_text, True, status_color)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 550))
        
        # Draw reset button
        pygame.draw.rect(screen, GRAY, (WIDTH // 2 - 75, 600, 150, 50))
        reset_text = font.render("Reset", True, BLACK)
        screen.blit(reset_text, (WIDTH // 2 - reset_text.get_width() // 2, 610))

def main():
    game = TicTacToe()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                
                # Check reset button
                if WIDTH // 2 - 75 <= x <= WIDTH // 2 + 75 and 600 <= y <= 650:
                    game.reset_game()
                    continue
                
                # Check board click
                board_x = (WIDTH - 3 * SQUARE_SIZE) // 2
                board_y = 100
                
                if board_x <= x <= board_x + 3 * SQUARE_SIZE and board_y <= y <= board_y + 3 * SQUARE_SIZE:
                    col = (x - board_x) // SQUARE_SIZE
                    row = (y - board_y) // SQUARE_SIZE
                    
                    if 0 <= row < 3 and 0 <= col < 3:
                        if game.current_player == 'X':  # Human player
                            game.make_move(row, col)
                            
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
