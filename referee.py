from connect4 import Connect4  
from aiplayer import AIPlayer

def main():
    # Initialize the Connect4 game (board height=5, width=7) and the AI player.
    connect4 = Connect4(5, 7)
    aiplayer = AIPlayer(5, 5, 7)  # depth, height, and width

    while True:
        print(connect4.string_of_state(connect4.state))

        if connect4.state.cur_state in ('Win', 'Draw'):
            break

        current_player = connect4.state.cur_player

        if current_player == 'X':
            # Human player's turn
            user_move = input("Please enter a move (column number): ")
            
            if user_move == 'exit':
                break
            # Validate user input
            try:
                user_move = int(user_move)
            except ValueError:
                print("Invalid input! Please enter a valid integer.\n")
                continue
            
            possible_moves = connect4.legal_moves(connect4.state.board)
            if user_move not in possible_moves:
                print("Not a valid or available move!\n")
                continue

            connect4.state = connect4.next_state(connect4.state, user_move)

        else:
            # AI player's turn
            print("AI is thinking...\n")
            ai_move = aiplayer.next_move(connect4.state)
            print(f"AI chooses column: {ai_move}")
            connect4.state = connect4.next_state(connect4.state, ai_move)

if __name__ == '__main__':
    main()
