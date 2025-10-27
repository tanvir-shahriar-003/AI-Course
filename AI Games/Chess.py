import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 800
BOARD_SIZE = 8
SQUARE_SIZE = 80
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

GREEN = (0, 128, 0)
BROWN = (165, 42, 42)
LIGHT_BROWN = (210, 180, 140)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess with Minimax")
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 36)

class Chess:
    def __init__(self):
        self.board = self.initialize_board()
        self.current_player = 'white'
        self.selected_piece = None
        self.valid_moves = []
        self.game_over = False
        self.winner = None
        self.depth = 2  # Minimax depth

    def initialize_board(self):
        # Create an 8x8 board
        board = [['' for _ in range(8)] for _ in range(8)]
        
        # Set up pawns
        for col in range(8):
            board[1][col] = 'black_pawn'
            board[6][col] = 'white_pawn'
        
        # Set up other pieces
        pieces = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']
        for col, piece in enumerate(pieces):
            board[0][col] = f'black_{piece}'
            board[7][col] = f'white_{piece}'
        
        return board

    def get_piece_moves(self, row, col):
        piece = self.board[row][col]
        if not piece:
            return []
        
        color, piece_type = piece.split('_')
        moves = []
        
        if piece_type == 'pawn':
            direction = 1 if color == 'black' else -1
            # Move forward
            if 0 <= row + direction < 8 and not self.board[row + direction][col]:
                moves.append((row + direction, col))
                # Double move from starting position
                if (row == 1 and color == 'black') or (row == 6 and color == 'white'):
                    if not self.board[row + 2 * direction][col]:
                        moves.append((row + 2 * direction, col))
            
            # Capture diagonally
            for dc in [-1, 1]:
                if 0 <= row + direction < 8 and 0 <= col + dc < 8:
                    target = self.board[row + direction][col + dc]
                    if target and target.split('_')[0] != color:
                        moves.append((row + direction, col + dc))
        
        elif piece_type == 'rook':
            # Horizontal and vertical moves
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                for i in range(1, 8):
                    r, c = row + i * dr, col + i * dc
                    if not (0 <= r < 8 and 0 <= c < 8):
                        break
                    if not self.board[r][c]:
                        moves.append((r, c))
                    else:
                        if self.board[r][c].split('_')[0] != color:
                            moves.append((r, c))
                        break
        
        elif piece_type == 'knight':
            # L-shaped moves
            for dr, dc in [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]:
                r, c = row + dr, col + dc
                if 0 <= r < 8 and 0 <= c < 8:
                    if not self.board[r][c] or self.board[r][c].split('_')[0] != color:
                        moves.append((r, c))
        
        elif piece_type == 'bishop':
            # Diagonal moves
            for dr, dc in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                for i in range(1, 8):
                    r, c = row + i * dr, col + i * dc
                    if not (0 <= r < 8 and 0 <= c < 8):
                        break
                    if not self.board[r][c]:
                        moves.append((r, c))
                    else:
                        if self.board[r][c].split('_')[0] != color:
                            moves.append((r, c))
                        break
        
        elif piece_type == 'queen':
            # Combine rook and bishop moves
            rook_moves = self.get_piece_moves_rook(row, col, color)
            bishop_moves = self.get_piece_moves_bishop(row, col, color)
            moves = rook_moves + bishop_moves
        
        elif piece_type == 'king':
            # One square in any direction
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    r, c = row + dr, col + dc
                    if 0 <= r < 8 and 0 <= c < 8:
                        if not self.board[r][c] or self.board[r][c].split('_')[0] != color:
                            moves.append((r, c))
        
        return moves

    def get_piece_moves_rook(self, row, col, color):
        moves = []
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            for i in range(1, 8):
                r, c = row + i * dr, col + i * dc
                if not (0 <= r < 8 and 0 <= c < 8):
                    break
                if not self.board[r][c]:
                    moves.append((r, c))
                else:
                    if self.board[r][c].split('_')[0] != color:
                        moves.append((r, c))
                    break
        return moves

    def get_piece_moves_bishop(self, row, col, color):
        moves = []
        for dr, dc in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            for i in range(1, 8):
                r, c = row + i * dr, col + i * dc
                if not (0 <= r < 8 and 0 <= c < 8):
                    break
                if not self.board[r][c]:
                    moves.append((r, c))
                else:
                    if self.board[r][c].split('_')[0] != color:
                        moves.append((r, c))
                    break
        return moves

    def select_piece(self, row, col):
        if self.game_over:
            return
        
        piece = self.board[row][col]
        if piece and piece.split('_')[0] == self.current_player:
            self.selected_piece = (row, col)
            self.valid_moves = self.get_piece_moves(row, col)
        elif self.selected_piece and (row, col) in self.valid_moves:
            # Move the piece
            self.move_piece(self.selected_piece[0], self.selected_piece[1], row, col)
            self.selected_piece = None
            self.valid_moves = []
            
            # Switch player and let AI move
            self.current_player = 'black'
            if not self.game_over:
                self.ai_move()

    def move_piece(self, from_row, from_col, to_row, to_col):
        self.board[to_row][to_col] = self.board[from_row][from_col]
        self.board[from_row][from_col] = ''
        
        # Check for game over (simplified - just check if king is captured)
        if 'king' in self.board[to_row][to_col]:
            opponent_color = 'black' if self.current_player == 'white' else 'white'
            if f'{opponent_color}_king' not in [piece for row in self.board for piece in row]:
                self.game_over = True
                self.winner = self.current_player

    def evaluate_board(self):
        # Simple evaluation function
        piece_values = {
            'pawn': 1,
            'knight': 3,
            'bishop': 3,
            'rook': 5,
            'queen': 9,
            'king': 100
        }
        
        score = 0
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece:
                    color, piece_type = piece.split('_')
                    value = piece_values.get(piece_type, 0)
                    if color == 'white':
                        score += value
                    else:
                        score -= value
        return score

    def minimax(self, depth, alpha, beta, is_maximizing):
        if depth == 0 or self.game_over:
            return self.evaluate_board(), None
        
        if is_maximizing:
            max_eval = -float('inf')
            best_move = None
            
            # Get all possible moves for white
            for row in range(8):
                for col in range(8):
                    piece = self.board[row][col]
                    if piece and piece.split('_')[0] == 'white':
                        moves = self.get_piece_moves(row, col)
                        for move in moves:
                            # Make the move
                            original_piece = self.board[move[0]][move[1]]
                            self.board[move[0]][move[1]] = self.board[row][col]
                            self.board[row][col] = ''
                            
                            # Evaluate
                            eval_score, _ = self.minimax(depth - 1, alpha, beta, False)
                            
                            # Undo the move
                            self.board[row][col] = self.board[move[0]][move[1]]
                            self.board[move[0]][move[1]] = original_piece
                            
                            if eval_score > max_eval:
                                max_eval = eval_score
                                best_move = ((row, col), move)
                            
                            alpha = max(alpha, eval_score)
                            if beta <= alpha:
                                break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            best_move = None
            
            # Get all possible moves for black
            for row in range(8):
                for col in range(8):
                    piece = self.board[row][col]
                    if piece and piece.split('_')[0] == 'black':
                        moves = self.get_piece_moves(row, col)
                        for move in moves:
                            # Make the move
                            original_piece = self.board[move[0]][move[1]]
                            self.board[move[0]][move[1]] = self.board[row][col]
                            self.board[row][col] = ''
                            
                            # Evaluate
                            eval_score, _ = self.minimax(depth - 1, alpha, beta, True)
                            
                            # Undo the move
                            self.board[row][col] = self.board[move[0]][move[1]]
                            self.board[move[0]][move[1]] = original_piece
                            
                            if eval_score < min_eval:
                                min_eval = eval_score
                                best_move = ((row, col), move)
                            
                            beta = min(beta, eval_score)
                            if beta <= alpha:
                                break
            return min_eval, best_move

    def ai_move(self):
        if self.current_player == 'black' and not self.game_over:
            _, best_move = self.minimax(self.depth, -float('inf'), float('inf'), False)
            if best_move:
                from_pos, to_pos = best_move
                self.move_piece(from_pos[0], from_pos[1], to_pos[0], to_pos[1])
                self.current_player = 'white'

    def reset_game(self):
        self.__init__()

    def draw_piece(self, screen, piece, x, y):
        if 'pawn' in piece:
            color = WHITE if 'white' in piece else BLACK
            pygame.draw.circle(screen, color, (x, y), 20)
            pygame.draw.circle(screen, RED if 'white' in piece else BLUE, (x, y), 20, 2)
        elif 'rook' in piece:
            color = WHITE if 'white' in piece else BLACK
            pygame.draw.rect(screen, color, (x-20, y-20, 40, 40))
            pygame.draw.rect(screen, RED if 'white' in piece else BLUE, (x-20, y-20, 40, 40), 2)
        elif 'knight' in piece:
            color = WHITE if 'white' in piece else BLACK
            pygame.draw.polygon(screen, color, [(x, y-25), (x-20, y+25), (x+20, y+25)])
            pygame.draw.polygon(screen, RED if 'white' in piece else BLUE, 
                              [(x, y-25), (x-20, y+25), (x+20, y+25)], 2)
        elif 'bishop' in piece:
            color = WHITE if 'white' in piece else BLACK
            pygame.draw.circle(screen, color, (x, y), 25)
            pygame.draw.circle(screen, RED if 'white' in piece else BLUE, (x, y), 25, 2)
            pygame.draw.circle(screen, color, (x, y-10), 15)
        elif 'queen' in piece:
            color = WHITE if 'white' in piece else BLACK
            pygame.draw.circle(screen, color, (x, y), 25)
            pygame.draw.circle(screen, RED if 'white' in piece else BLUE, (x, y), 25, 2)
            # Crown
            points = [(x-15, y-5), (x-10, y-15), (x, y-20), (x+10, y-15), (x+15, y-5)]
            pygame.draw.polygon(screen, RED if 'white' in piece else BLUE, points)
        elif 'king' in piece:
            color = WHITE if 'white' in piece else BLACK
            pygame.draw.circle(screen, color, (x, y), 30)
            pygame.draw.circle(screen, RED if 'white' in piece else BLUE, (x, y), 30, 2)
            # Crown
            points = [(x-20, y-10), (x-15, y-20), (x, y-25), (x+15, y-20), (x+20, y-10)]
            pygame.draw.polygon(screen, RED if 'white' in piece else BLUE, points)

    def draw(self, screen):
        screen.fill(WHITE)
        
        # Draw title
        title_text = font.render("Chess", True, BLACK)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 20))
        
        # Draw board
        board_x = (WIDTH - 8 * SQUARE_SIZE) // 2
        board_y = 100
        
        for row in range(8):
            for col in range(8):
                color = LIGHT_BROWN if (row + col) % 2 == 0 else BROWN
                pygame.draw.rect(screen, color, 
                               (board_x + col * SQUARE_SIZE, 
                                board_y + row * SQUARE_SIZE, 
                                SQUARE_SIZE, SQUARE_SIZE))
                
                # Draw selected piece highlight
                if self.selected_piece and self.selected_piece == (row, col):
                    pygame.draw.rect(screen, GREEN, 
                                   (board_x + col * SQUARE_SIZE, 
                                    board_y + row * SQUARE_SIZE, 
                                    SQUARE_SIZE, SQUARE_SIZE), 3)
                
                # Draw valid moves
                if self.selected_piece and (row, col) in self.valid_moves:
                    pygame.draw.circle(screen, GREEN, 
                                     (board_x + col * SQUARE_SIZE + SQUARE_SIZE // 2, 
                                      board_y + row * SQUARE_SIZE + SQUARE_SIZE // 2), 
                                     10)
                
                # Draw pieces
                piece = self.board[row][col]
                if piece:
                    x = board_x + col * SQUARE_SIZE + SQUARE_SIZE // 2
                    y = board_y + row * SQUARE_SIZE + SQUARE_SIZE // 2
                    self.draw_piece(screen, piece, x, y)
        
        # Draw game status
        if self.game_over:
            status_text = f"Game Over: {self.winner} wins!"
            status_color = GREEN
        else:
            status_text = f"Current Player: {self.current_player}"
            status_color = BLACK
        
        text = font.render(status_text, True, status_color)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 750))
        
        # Draw reset button
        pygame.draw.rect(screen, GRAY, (WIDTH // 2 - 75, 50, 150, 40))
        reset_text = font.render("Reset", True, BLACK)
        screen.blit(reset_text, (WIDTH // 2 - reset_text.get_width() // 2, 55))

def main():
    game = Chess()
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
                board_x = (WIDTH - 8 * SQUARE_SIZE) // 2
                board_y = 100
                
                if board_x <= x <= board_x + 8 * SQUARE_SIZE and board_y <= y <= board_y + 8 * SQUARE_SIZE:
                    col = (x - board_x) // SQUARE_SIZE
                    row = (y - board_y) // SQUARE_SIZE
                    
                    if 0 <= row < 8 and 0 <= col < 8:
                        if game.current_player == 'white':  # Human player
                            game.select_piece(row, col)
        
        game.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
