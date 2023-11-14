import board as bd

def play_game():
    # Initialize the board
    board = bd.Board()
    # Initialize the players
    player_1 = bd.Player('X')
    player_2 = bd.Player('O')
    current_player = player_1
    # Play the game
    while not board.is_game_over():
        # Print the board
        print(board)
        # Ask the current player to make a move
        move = input(f"{current_player}'s turn. Enter your move (e.g. 'a3 b4'): ")
        # Parse the move
        from_pos, to_pos = move.split()
        from_pos = bd.Position(from_pos[0], int(from_pos[1]))
        to_pos = bd.Position(to_pos[0], int(to_pos[1]))
        # Make the move
        if board.is_valid_move(from_pos, to_pos, current_player):
            board.make_move(from_pos, to_pos, current_player)
            # Switch to the other player
            current_player = player_2 if current_player == player_1 else player_1
        else:
            print("Invalid move. Try again.")
    # Print the final board and the winner
    print(board)
    print(f"{board.get_winner()} wins!")
    
if __name__ == '__main__':
    play_game()
