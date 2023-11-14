"""
TODO:
    - Add logic for when a piece is able to be captured
        - Always check if a piece can be captured and if so player must move again
    - Add logic for when a piece is able to be kinged
        - Kinged pieces can move backwards
"""

import random

class CheckersBoard:
    def __init__(self):
        self.board = [
            ['_', 'b', '_', 'b', '_', 'b', '_', 'b'],
            ['b', '_', 'b', '_', 'b', '_', 'b', '_'],
            ['_', 'b', '_', 'b', '_', 'b', '_', 'b'],
            ['_', '_', '_', '_', '_', '_', '_', '_'],
            ['_', '_', '_', '_', '_', '_', '_', '_'],
            ['w', '_', 'w', '_', 'w', '_', 'w', '_'],
            ['_', 'w', '_', 'w', '_', 'w', '_', 'w'],
            ['w', '_', 'w', '_', 'w', '_', 'w', '_']
        ]

        # Initalize attributes
        self.winner = None
        self.white_pieces = None
        self.black_pieces = None
        self.starting_player = random.choice(['w','b'])

    def print_board(self,player):
        print("  " + " ".join(str(i) for i in range(len(self.board[0]))))  # print column numbers
        if player == 'w':
            for i, row in enumerate(self.board):
                print(str(i) + " " + ' '.join(row))  # print row number and row
        else:
            for i, row in reversed(list(enumerate(self.board))):
                print(str(i) + " " + ' '.join(row))  # print row number and row

    def get_possible_moves(self, player):
        possible_moves = []
        for row_index in range(len(self.board)):
            for col_index in range(len(self.board[row_index])):
                if self.board[row_index][col_index] == player:
                    possible_moves += self.get_possible_moves_for_piece(row_index, col_index, player)
        return possible_moves
    
    def get_possible_moves_for_piece(self,row,col,player):
        possible_moves = []
        if player == 'w':
            if row > 0:
                if col > 0:
                    if self.board[row-1][col-1] == '_':
                        possible_moves.append((row,col,row-1,col-1))
                if col < 7:
                    if self.board[row-1][col+1] == '_':
                        possible_moves.append((row,col,row-1,col+1))
            if row > 1:
                if col > 1:
                    if self.board[row-1][col-1] == 'b' and self.board[row-2][col-2] == '_':
                        possible_moves.append((row,col,row-2,col-2))
                if col < 6:
                    if self.board[row-1][col+1] == 'b' and self.board[row-2][col+2] == '_':
                        possible_moves.append((row,col,row-2,col+2))
        elif player == 'b':
            if row < 7:
                if col > 0:
                    if self.board[row+1][col-1] == '_':
                        possible_moves.append((row,col,row+1,col-1))
                if col < 7:
                    if self.board[row+1][col+1] == '_':
                        possible_moves.append((row,col,row+1,col+1))
            if row < 6:
                if col > 1:
                    if self.board[row+1][col-1] == 'w' and self.board[row+2][col-2] == '_':
                        possible_moves.append((row,col,row+2,col-2))
                if col < 6:
                    if self.board[row+1][col+1] == 'w' and self.board[row+2][col+2] == '_':
                        possible_moves.append((row,col,row+2,col+2))
        return possible_moves

    def make_move(self, move, player):
        row, col = move[0]
        direction = move[1]
        dx, dy = 0, 0
        if player == 'w':
            if direction == 'fr':
                dx, dy = -1, 1
            elif direction == 'fl':
                dx, dy = -1, -1
            elif direction == 'br':
                dx, dy = 1, 1
            elif direction == 'bl':
                dx, dy = 1, -1
        else:
            if direction == 'fr':
                dx, dy = 1, -1
            elif direction == 'fl':
                dx, dy = 1, 1
            elif direction == 'br':
                dx, dy = -1, -1
            elif direction == 'bl':
                dx, dy = -1, 1

        new_move = (row + dx, col + dy)

        # If the destination square is occupied, move one more square in the same direction
        if str(self.board[new_move[0]][new_move[1]]) != '_':
            print("there")
            new_move = (row, col, new_move[0] + dx, new_move[1] + dy)
        else:
            print("here")
            new_move = (row, col, new_move[0], new_move[1])
        
        possible_moves = self.get_possible_moves(player)
        
        print(possible_moves)
        print(new_move)
        
        if new_move not in possible_moves:
            raise ValueError("Invalid move")
        # Updte piece on board
        
        if new_move[0] == new_move[2] - 2 or new_move[0] == new_move[2] + 2:
            self.board[(new_move[0] + new_move[2]) // 2][(new_move[1] + new_move[3]) // 2] = '_'
        self.board[new_move[2]][new_move[3]] = self.board[new_move[0]][new_move[1]]
        self.board[new_move[0]][new_move[1]] = '_'
    
    def get_winner(self):
            self.white_pieces = 0
            self.black_pieces = 0
            for row in self.board:
                for piece in row:
                    if piece == 'w':
                        self.white_pieces += 1
                    elif piece == 'b':
                        self.black_pieces += 1
            if self.white_pieces == 0:
                self.winner == 'b'
            elif self.black_pieces == 0:
                self.winner = 'w'
            else:
                return
                
if __name__ == '__main__':
    
    # Start board instance
    board = CheckersBoard()
    
    # Starting player
    current_player = board.starting_player
    
    # Main Loop
    while True:

        # Update Board
        board.print_board(current_player)
        move_list = []
        
        while True:
            # ask user to make a move
            move = input(f"{current_player}'s turn. Enter your move (e.g. '50 fr'): ")

            try:
                # Parse the move
                from_pos, direction = move.split()
                from_pos = (int(from_pos[0]), int(from_pos[1]))

                # Check if direction is valid
                if direction not in ['fr', 'fl', 'bl', 'br']:
                    raise ValueError("Invalid direction, please enter 'fr', 'fl', 'bl', or 'br'.")

                # Make the move    
                move = board.make_move(((from_pos[0], from_pos[1]), direction), current_player)
                move_list.append(((from_pos[0], from_pos[1]), direction))

                break  # if the move is valid, break the loop and swap players
            except ValueError as e:
                print(e)
                print("Invalid move, please try again.")

                # reprint board request
                boardPrint = ''
                while boardPrint != 'y' and boardPrint != 'n':
                    boardPrint = input("Would you like to print the board? (y/n): ")
                    if boardPrint == 'y':
                        board.print_board()
                    continue
        
        # Get winner
        board.get_winner()
        if board.winner == 'w':
            print("White Wins!")
            break
        elif board.winner == 'b':
            print("Black Wins!")
            break
        else:
            print(f" Number of white pieces remaining: {board.white_pieces}")
            print(f" Number of black pieces remaining: {board.black_pieces}")
            print("Moves Made so Far: " + str(move_list))
            
        # Swap Players (Add if a piece is taken then don't swap logic)
        if current_player == 'w':
            current_player = 'b'
        else:
            current_player = 'w'