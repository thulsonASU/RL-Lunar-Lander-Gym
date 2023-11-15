"""
TODO:
    - Add logic for when a piece is able to be kinged ( Might not do this and just allow all directional movement for pieces )
        - Kinged pieces can move backwards
"""

import random

class CheckersBoard:
    def __init__(self):
        # self.board = [
        #     ['_', 'b', '_', 'b', '_', 'b', '_', 'b'],
        #     ['b', '_', 'b', '_', 'b', '_', 'b', '_'],
        #     ['_', 'b', '_', 'b', '_', 'b', '_', 'b'],
        #     ['_', '_', '_', '_', '_', '_', '_', '_'],
        #     ['_', '_', '_', '_', '_', '_', '_', '_'],
        #     ['w', '_', 'w', '_', 'w', '_', 'w', '_'],
        #     ['_', 'w', '_', 'w', '_', 'w', '_', 'w'],
        #     ['w', '_', 'w', '_', 'w', '_', 'w', '_']
        # ]

        # Board for jump testing
        # self.board = [
        #     ['_', 'b', '_', 'b', '_', 'b', '_', 'b'],
        #     ['b', '_', 'b', '_', 'b', '_', '_', '_'],
        #     ['_', 'b', '_', 'b', '_', 'b', '_', 'b'],
        #     ['_', '_', '_', '_', '_', '_', '_', '_'],
        #     ['_', '_', '_', 'b', '_', '_', '_', '_'],
        #     ['w', '_', 'w', '_', 'w', '_', 'w', '_'],
        #     ['_', 'w', '_', 'w', '_', 'w', '_', 'w'],
        #     ['w', '_', 'w', '_', 'w', '_', 'w', '_']
        # ]

        # Board for king jump testing
        self.board = [
            ['_', 'b', '_', 'b', '_', 'b', '_', 'b'],
            ['b', '_', 'b', '_', '_', '_', '_', '_'],
            ['_', 'b', '_', 'b', '_', 'bk', '_', 'b'],
            ['_', '_', '_', '_', '_', '_', '_', '_'],
            ['_', 'bk', '_', '_', '_', '_', '_', '_'],
            ['wk', '_', 'w', '_', 'wk', '_', 'w', '_'],
            ['_', 'w', '_', '_', '_', '_', '_', 'w'],
            ['w', '_', 'w', '_', 'w', '_', 'w', '_']
        ]

        # Initalize attributes
        self.winner = None
        self.opponent = None
        self.white_pieces = None
        self.black_pieces = None
        self.must_jump = None
        self.starting_player = random.choice(['w','b'])
        self.boardRetryCounter = 0
        self.winner_bool = False
        self.move_list = []

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
    
    def get_possible_moves_for_piece(self, row, col, player):
        possible_moves = []
        if player == 'w' or player == 'wk':
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
            if player == 'wk':
                if row < 7:
                    if col > 0:
                        if self.board[row+1][col-1] == '_':
                            possible_moves.append((row,col,row+1,col-1))
                    if col < 7:
                        if self.board[row+1][col+1] == '_':
                            possible_moves.append((row,col,row+1,col+1))
                if row < 6:
                    if col > 1:
                        if self.board[row+1][col-1] == 'b' and self.board[row+2][col-2] == '_':
                            possible_moves.append((row,col,row+2,col-2))
                    if col < 6:
                        if self.board[row+1][col+1] == 'b' and self.board[row+2][col+2] == '_':
                            possible_moves.append((row,col,row+2,col+2))
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
            if player == 'bk':
                if row > 0:
                    if col > 0:
                        if self.board[row-1][col-1] == '_':
                            possible_moves.append((row,col,row-1,col-1))
                    if col < 7:
                        if self.board[row-1][col+1] == '_':
                            possible_moves.append((row,col,row-1,col+1))
                if row > 1:
                    if col > 1:
                        if self.board[row-1][col-1] == 'w' and self.board[row-2][col-2] == '_':
                            possible_moves.append((row,col,row-2,col-2))
                    if col < 6:
                        if self.board[row-1][col+1] == 'w' and self.board[row-2][col+2] == '_':
                            possible_moves.append((row,col,row-2,col+2))
        return possible_moves

    def can_jump(self, player):
        
        # Get directions possible to given player
        if player == 'w':
            directions = {'fr': (-1, 1), 'fl': (-1, -1), 'br': (1, 1), 'bl': (1, -1)}
        else:
            directions = {'fr': (1, 1), 'fl': (1, -1), 'br': (-1, 1), 'bl': (-1, -1)}
        
        # Check opponent piece in each direction
        self.opponent = 'b' if player == 'w' else 'w'

        # scan entire board to see if a jump is possible, if it is return true
        for row_index in range(len(self.board)):
            for col_index in range(len(self.board)):
                if self.board[row_index][col_index] == player:
                    for direction in directions:
                        dx, dy = directions[direction]
                        if self.is_valid_position(row_index + 2 * dx, col_index + 2 * dy) and self.board[row_index + dx][col_index + dy] == self.opponent and self.board[row_index + 2 * dx][col_index + 2 * dy] == '_':
                            return True
        return False

    def make_move(self, move, player):
        row, col = move[0]
        direction = move[1]
        dx, dy = 0, 0

        # Input Check for Direction
        # Check if direction is valid
        if direction not in ['fr', 'fl', 'bl', 'br']:
            self.boardRetryCounter += 1
            raise ValueError("Invalid direction, please enter 'fr', 'fl', 'bl', or 'br'.")
        
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
                dx, dy = 1, 1
            elif direction == 'fl':
                dx, dy = 1, -1
            elif direction == 'br':
                dx, dy = -1, 1
            elif direction == 'bl':
                dx, dy = -1, -1

        new_move = (row + dx, col + dy)

        # If the destination square is occupied, move one more square in the same direction
        if str(self.board[new_move[0]][new_move[1]]) != '_':
            make_jump = True
            new_move = (row, col, new_move[0] + dx, new_move[1] + dy)
        else:
            new_move = (row, col, new_move[0], new_move[1])
       
        # Check if move is possible
        possible_moves = self.get_possible_moves(player)

        print("possible moves: " + str(possible_moves))
        # Input Check for Moves
        if new_move not in possible_moves:
            self.boardRetryCounter += 1
            raise ValueError("Invalid move, please try again.")
        elif self.must_jump:
            if str(self.board[new_move[2]-dx][new_move[3]-dy]) == self.opponent and self.must_jump:
                pass
            else:
                self.boardRetryCounter += 1
                raise ValueError("Invalid move, you must jump the opponents piece.")
        else:
            pass

        # Update piece on board 
        if new_move[0] == new_move[2] - 2 or new_move[0] == new_move[2] + 2:
            self.board[(new_move[0] + new_move[2]) // 2][(new_move[1] + new_move[3]) // 2] = '_'
        self.board[new_move[2]][new_move[3]] = self.board[new_move[0]][new_move[1]]
        self.board[new_move[0]][new_move[1]] = '_'

        # Check if the piece has reached the opposite end of the board
        if player == 'w' and new_move[2] == 7:
            # King the piece
            self.board[new_move[2]][new_move[3]] = 'wk'
        elif player == 'b' and new_move[2] == 0:
            # King the piece
            self.board[new_move[2]][new_move[3]] = 'bk'
        
    def is_valid_position(self, row, col):
        return 0 <= row < len(self.board) and 0 <= col < len(self.board[0])
        
    def get_user_move(self, player):
        
        self.print_board(player)

        while True:
            # ask user to make a move
            move = input(f"{player}'s turn. Enter your move (e.g. '50 fr'): ")

            try:
                # Parse the move
                from_pos, direction = move.split()
                from_pos = (int(from_pos[0]), int(from_pos[1]))

                # Make the move    
                move = self.make_move(((from_pos[0], from_pos[1]), direction), player)
                self.move_list.append((player, (from_pos[0], from_pos[1]), direction))

                break  # if the move is valid, break the loop
            except ValueError as e:
                print(e)

                if self.boardRetryCounter >= 3:
                    # reprint board request
                    boardPrint = ''
                    while boardPrint != 'y' and boardPrint != 'n':
                        boardPrint = input("Would you like to print the board? (y/n): ")
                        if boardPrint == 'y':
                            self.print_board(player)
                            self.boardRetryCounter = 0
                        continue
    
    def user_move(self, player):
        user_jumped = False
        while True:
            # Jump Opponent Piece Check
            self.must_jump = self.can_jump(player)
            if self.must_jump:
                print(f"Player: {player} must jump the opponents piece.")
                self.get_user_move(player)
                user_jumped = True
            elif user_jumped == False:
                self.get_user_move(player)
                break
            else:
                break
            continue
        
    def swap_players(self, player):
        if player == 'w':
            player = 'b'
        else:
            player = 'w'
        return player
    
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
                self.winner_bool = True
                print("Black Wins!")
            elif self.black_pieces == 0:
                self.winner = 'w'
                self.winner_bool = True
                print("White Wins!")
            else:
                print(f" Number of white pieces remaining: {self.white_pieces}")
                print(f" Number of black pieces remaining: {self.black_pieces}")
                print("Moves Made so Far: " + str(self.move_list))
                return self.winner, self.winner_bool