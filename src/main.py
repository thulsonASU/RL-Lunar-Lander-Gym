import board as bd

if __name__ == '__main__':
    
    # Start board instance
    board = bd.CheckersBoard()
    
    # Starting player
    current_player = board.starting_player
    
    # Main Loop
    while True:

        # Get user move and update board
        board.get_user_move(current_player)
            
        # Swap players
        current_player = board.swap_players(current_player)

        # Get Winner
        winner, winner_bool = board.get_winner()

        if winner_bool:
            print("Game Over!")
            print("Moves Made: " + str(board.move_list))
            print("Final Board: ")
            board.print_board(current_player)
            print(f"Thanks for playing! {winner} won!")
            break