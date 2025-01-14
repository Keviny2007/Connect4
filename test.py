from collections import namedtuple
import numpy as np

GameState = namedtuple('GameState', ['cur_state', 'board', 'cur_player'])
initial_board = np.full((5, 5), '_', dtype=str)

awei = GameState(cur_state='Ongoing', cur_player='X', board=initial_board)
print(awei.cur_state)
