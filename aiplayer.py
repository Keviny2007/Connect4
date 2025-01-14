from connect4 import Connect4

class AIPlayer:
    def __init__(self, depth, h, w):
        self.depth = depth
        self.connect4 = Connect4(h, w)

    def minimax(self, state, depth, isMaxie) -> tuple[float, int]:
        moves = self.connect4.legal_moves(state[1])

        # depth reached or no more legal moves
        if depth == 0 or not moves:
            return self.connect4.estimate_value(state), -1
        
        if self.connect4.state.cur_state != 'Ongoing':
            return float('-inf') if isMaxie else float('inf'), -1 # if isMaxie, that means Minnie has won and vice versa

        if isMaxie:
            # maximize score
            best_val = float('-inf')
            best_move = -1
            for move in moves:
                child_state = self.connect4.next_state(state, move)
                child_val, _ = self.minimax(child_state, depth - 1, isMaxie=0)
                if child_val > best_val:
                    best_val = child_val
                    best_move = move
            return (best_val, best_move)
        else:
            # minimize score
            best_val = float('inf')
            best_move = -1
            for move in moves:
                child_state = self.connect4.next_state(state, move)
                child_val, _ = self.minimax(child_state, depth - 1, isMaxie=1)
                if child_val < best_val:
                    best_val = child_val
                    best_move = move
            return (best_val, best_move)

    def alphabeta(self, board, depth, maxie):
        return

    def next_move(self, state):
        player = 0 if state[2] == 'O' else 1
        return self.minimax(state, self.depth, player)[1]