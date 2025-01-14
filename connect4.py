import numpy as np

from collections import namedtuple

GameState = namedtuple('GameState', ['cur_state', 'board', 'cur_player'])

class Connect4:
    def __init__(self, h, w):
        initial_board = np.full((w, h), '_', dtype=str)
        self.initial_state = GameState(cur_state="Ongoing", board=initial_board, cur_player='X')
        self.state = self.initial_state  # Current state of the game

    def string_of_player(self, player):
        return 'Player 1' if player == 'X' else 'Player 2'

    def string_of_board(self, board) -> str:
        res = ''
        cords = ''
        for column in range(board.shape[1] - 1, -1, -1):
            for row in range(board.shape[0]):
                res += board[row][column] + ' '
            res += '\n'
        for i in range(board.shape[0]):
            cords += str(i + 1) + ' '
        return res + cords

    def string_of_state(self, state) -> str:
        res = ''
        if state.cur_state == "Win":
            res += self.string_of_player(self.get_other_player(state.cur_player)) + ' wins!\nBoard: \n' + self.string_of_board(state.board)
        elif state.cur_state == "Ongoing":
            res += "It is " + self.string_of_player(state.cur_player) + "'s turn. \nBoard: \n" + self.string_of_board(state.board)
        else:
            res += "The game ends in a draw! \nBoard: \n" + self.string_of_board(state.board)
        return res

    def get_other_player(self, player):
        return 'X' if player == 'O' else 'O'

    def legal_moves(self, board) -> list:
        res = []
        for row in range(board.shape[0]):
            for col in range(board.shape[1]):
                if board[row][col] == '_':
                    res.append(row + 1)
                    break
        return res

    def in_a_row(self, row, n):
        row = np.array(row)
        for i in range(len(row) - n + 1):
            window = row[i:i + n]
            if np.all(window == window[0]) and window[0] != '_':
                return True
        return False

    def vert_win(self, board):
        for row in board:
            win = self.in_a_row(row, 4)
            if win:
                return True

    def diag_win(self, board):
        for offset in range(-board.shape[0] + 1, board.shape[1]):
            diag = np.diagonal(board, offset=offset)
            if self.in_a_row(diag, 4):
                return True

        flipped = np.fliplr(board)
        for offset in range(-flipped.shape[0] + 1, flipped.shape[1]):
            diag = np.diagonal(flipped, offset=offset)
            if self.in_a_row(diag, 4):
                return True
        return False

    def game_status(self, board):
        if self.vert_win(board) or self.vert_win(np.transpose(board)) or self.diag_win(board):
            return "Win"
        elif len(self.legal_moves(board)) == 0:
            return "Draw"
        else:
            return "Ongoing"

    def next_state(self, state, move):
        new_board = state.board.copy()
        for spot in range(new_board.shape[1]):
            if new_board[move - 1][spot] == '_':
                new_board[move - 1][spot] = state.cur_player
                break
        next_player = self.get_other_player(state.cur_player)
        next_state = self.game_status(new_board)
        return GameState(cur_state=next_state, board=new_board, cur_player=next_player)

    def score(self):
        return

    def _score_player_streak(self, count: int) -> float:
        """Helper: scoring for the player's own streak."""
        if count == 4:
            return float('inf')
        elif count == 3:
            return 100_000.
        elif count == 2:
            return 100.
        else:
            return 0.

    def _score_opponent_streak(self, count: int) -> float:
        """Helper: scoring for the opponent's streak."""
        if count == 3:
            return 9_999_999_999.
        elif count == 2:
            return 50.
        else:
            return 0.

    def streak_estimate(state, player, opponent):
        row_score = 0.0
        for row in state.board:
            row_score += self.score(row, player) - self.score(row, opponent)

        col_score = 0.0
        transposed = np.transpose(state.board)
        for col in transposed:
            col_score += self.score(col, player) - self.score(col, opponent)

        diag_score = 0.0
        right_diags = []
        left_diags = []
        for offset in range(-state.board.shape[0] + 1, state.board.shape[1]):
            diag = np.diagonal(state.board, offset=offset)
            right_diags.append(diag)

        flipped = np.fliplr(state.board)
        for offset in range(-flipped.shape[0] + 1, flipped.shape[1]):
            diag = np.diagonal(flipped, offset=offset)
            left_diags.append(diag)

        for diag in right_diags:
            diag_score += self.score(diag, player) - self.score(diag, opponent)
        for diag in left_diags:
            diag_score += self.score(diag, player) - self.score(diag, opponent)

        return row_score + col_score + diag_score

    def estimate_value(self, state):
        """
        1) Large positive value for X win and large negative value for O win
        2) 0 for draw
        3) Heuristic for ongoing game
        """
        if state.cur_player == "Win":
            # last move was made by the other player 
            last_player = self.get_other_player(state.cur_player)
            # big positive number if X just won, negative if O just won
            return 999999.0 if last_player == 'X' else -999999.0
        
        if state.cur_player == "Draw":
            return 0.0

        # higher score for more pieces in a row
        board = state.board
        score = 0
        for row in range(board.shape[0]):
            for col in range(board.shape[1]):
                if board[row, col] == 'X':
                    score += 1
                elif board[row, col] == 'O':
                    score -= 1

        return float(score)

    def reset(self):
        self.state = self.initial_state

