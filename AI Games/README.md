Three Games with Minimax AI


A collection of three classic games implemented in Python with AI opponents using the minimax algorithm.

🎮 Games Included
Tic Tac Toe - Classic 3x3 game with perfect AI

Chess - Simplified chess with AI opponent

Connect Four - Vertical connect-four game with AI

📋 Prerequisites
Required Software/Libraries
Python 3.7 or higher

Pygame library

Installation Steps
Install Python:

Download from python.org

Verify installation: python --version

Install Pygame:

bash
pip install pygame
Verify Pygame installation:

python
python -c "import pygame; print('Pygame installed successfully')"
🚀 How to Run
Option 1: Run Individual Games
Download the game files:

tic_tac_toe.py

chess.py

connect_four.py

Run each game separately:

bash
python tic_tac_toe.py
python chess.py
python connect_four.py


🎯 How to Play Each Game
1. Tic Tac Toe


Game Rules:

3x3 grid game

Players alternate placing X and O

First to get 3 in a row (horizontal, vertical, or diagonal) wins

How to Play:

You play as X

AI plays as O

Click on any empty square to place your X

The AI will automatically respond with its move

Click "Reset" to start a new game

AI Features:

Uses minimax algorithm for perfect play

Cannot be beaten (best outcome is a tie)

2. Chess


Game Rules:

Standard chess rules (simplified)

Win by capturing the opponent's king

How to Play:

You play as White

AI plays as Black

Click on a piece to select it (green highlight)

Valid moves will show as green circles

Click on a valid move square to move

Click "Reset" to start a new game

Piece Movement:

Pawn: Move forward, capture diagonally

Rook: Horizontal and vertical movement

Knight: L-shaped movement

Bishop: Diagonal movement

Queen: Any direction

King: One square in any direction

AI Features:

Uses minimax with alpha-beta pruning

Depth-limited search for performance

Evaluates board position based on piece values

3. Connect Four


Game Rules:

7-column, 6-row vertical board

Players alternate dropping discs

First to connect 4 in a row (horizontal, vertical, or diagonal) wins

How to Play:

You play as Red

AI plays as Yellow

Click on any column to drop your disc

Discs fall to the lowest available position

Click "Reset" to start a new game

AI Features:

Uses minimax with alpha-beta pruning

Heuristic evaluation function

Prefers center columns for better positioning

Looks for winning moves and blocks opponent wins

🏆 Game Features
Common Features Across All Games:
Reset functionality - Start fresh anytime

Game status display - Current player and win messages

Visual feedback - Highlights and animations

AI opponents - All use minimax algorithm

AI Implementation Details:
Game	Algorithm	Search Depth	Evaluation Function
Tic Tac Toe	Minimax	Full game tree	Win/Lose/Tie
Chess	Minimax with Alpha-Beta	Depth 2	Piece values + positioning
Connect Four	Minimax with Alpha-Beta	Depth 4	Heuristic scoring
🐛 Troubleshooting
Common Issues:
"Pygame not found" error:

bash
pip install --upgrade pygame
Game runs slowly:

Close other applications

Reduce minimax depth in code if needed

Window not responding:

AI is thinking (especially in Chess)

Wait a few seconds for move calculation

Game crashes:

Ensure all game files are in the same directory

Verify Python and Pygame versions
