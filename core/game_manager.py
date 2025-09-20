import random
from typing import List, Tuple


class TicTacToe:
    def __init__(self):
        self.board = [" "] * 9
        self.current_player = "X"

    def display_board(self):
        board_str = f"""
   |   |   
 {self.board[0]} | {self.board[1]} | {self.board[2]} 
___|___|___
   |   |   
 {self.board[3]} | {self.board[4]} | {self.board[5]} 
___|___|___
   |   |   
 {self.board[6]} | {self.board[7]} | {self.board[8]} 
   |   |   
"""
        return board_str

    def make_move(self, position: int) -> bool:
        if 0 <= position <= 8 and self.board[position] == " ":
            self.board[position] = self.current_player
            return True
        return False

    def switch_player(self):
        self.current_player = "O" if self.current_player == "X" else "X"

    def check_winner(self) -> str:
        winning_combinations = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],  # строки
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],  # столбцы
            [0, 4, 8],
            [2, 4, 6],  # диагонали
        ]

        for combo in winning_combinations:
            if (
                self.board[combo[0]]
                == self.board[combo[1]]
                == self.board[combo[2]]
                != " "
            ):
                return self.board[combo[0]]

        if " " not in self.board:
            return "Draw"

        return None


class TetrisPiece:
    def __init__(self, shape: List[List[int]], color: str):
        self.shape = shape
        self.color = color
        self.x = 0
        self.y = 0


class SimpleTetris:
    def __init__(self):
        self.board_width = 10
        self.board_height = 15
        self.board = [
            [" " for _ in range(self.board_width)] for _ in range(self.board_height)
        ]
        self.current_piece = None
        self.game_over = False
        self.score = 0

    def create_random_piece(self):
        pieces = [
            [[1, 1, 1, 1]],  # I
            [[1, 1], [1, 1]],  # O
            [[1, 1, 1], [0, 1, 0]],  # T
            [[1, 1, 1], [1, 0, 0]],  # L
            [[1, 1, 1], [0, 0, 1]],  # J
        ]
        colors = ["cyan", "yellow", "purple", "orange", "blue"]
        piece_data = random.choice(pieces)
        color = random.choice(colors)
        return TetrisPiece(piece_data, color)

    def display_board(self):
        # Упрощенное отображение для консоли
        display = "Тетрис (упрощенная версия):\n"
        display += "+" + "-" * self.board_width + "+\n"
        for row in self.board:
            display += (
                "|" + "".join(["█" if cell != " " else " " for cell in row]) + "|\n"
            )
        display += "+" + "-" * self.board_width + "+\n"
        display += f"Счет: {self.score}\n"
        return display
