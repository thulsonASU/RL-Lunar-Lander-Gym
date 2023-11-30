import numpy as np
import gym

# Maybe we'll need these modules:
#from gym import spaces, error, utils
#from gym.utils import seeding


class checkersEnv(gym.Env):
    '''
    A checkers board, with -1 for the white player and 1 for the black player
    Default player is 1 (black)
    '''

    def __init__(self, print_debug=True):
        self.board = None
        self.kings = None
        self.print_debug = print_debug
        self.reset()
        

    def reset(self):

        # Init board and set player positions

        tmp_board = np.zeros([3, 8])
        for q in range(0, 3):
            p = [[0, 0], [0, 2], [0, 4], [0, 6], [1, 1], [1, 3], [1, 5], [1, 7]]
            for j in p:
                tmp_board[j[0], j[1]] = 1

        self.board = np.vstack([
            tmp_board[1, :],
            tmp_board[0, :],
            tmp_board[1, :],
            tmp_board[2, :],
            tmp_board[2, :] * -1,
            tmp_board[0, :] * -1,
            tmp_board[1, :] * -1,
            tmp_board[0, :] * -1,
        ])

        # fix 'negative zero'
        for i in range(0, 8):
            for j in range(0, 8):
                if self.board[i, j] == 0:
                    self.board[i, j] = 0

        # Print board
        if self.print_debug:
            print("Init board")
            print(self.board)

    def get_my_orientation(self, player):
        # Returns the right orientation for the player
        if player == -1:
            return self.board
        return np.flipud(self.board)

    def is_capturing_move(self, player, original_position, new_position, direction_left_right, direction_up_down):
        '''
        Detect if this move is a capturing move
        Returns list [new_location, to_remove_location]
        '''
        if not (-1 < new_position[0] < 8):
            return False
        if not (-1 < new_position[1] < 8):
            return False

        # check if the opponent is on the new position
        if self.board[new_position[0], new_position[1]] != player * -1:
            return False
        capturing_new_position = [new_position[0] + direction_up_down, new_position[1] + direction_left_right]

        # check if capturing_new_position is possible
        if not (-1 < capturing_new_position[0] < 8):
            return False
        if not (-1 < capturing_new_position[1] < 8):
            return False

        if self.board[capturing_new_position[0], capturing_new_position[1]] == 0:
            # return new position + the to-delete node
            return [capturing_new_position, new_position]

        return False

    def get_required_move(self, player, skip_rotate=False):

        '''
        Find if there is a 'required move'
        '''

        # rotate grid for this player
        if player == 1 and not skip_rotate:
            self.board = np.flipud(self.board)

        required_moves = []  # list with required pawns

        my_pawns = np.where(self.board == player)
        for i in range(0, len(my_pawns[0])):
            pawn_loc = [my_pawns[0][i], my_pawns[1][i]]
            # if pawn_loc in self.kings:
            # TODO: force backwards
            direction_up_down = -1
            if self.is_capturing_move(player, pawn_loc, [pawn_loc[0] - 1, pawn_loc[1] - 1], -1, direction_up_down):
                required_moves.append([pawn_loc, [pawn_loc[0] - 1, pawn_loc[1] - 1]])

            if self.is_capturing_move(player, pawn_loc, [pawn_loc[0] + 1, pawn_loc[1] - 1], 1, direction_up_down):
                required_moves.append([pawn_loc, [pawn_loc[0] + 1, pawn_loc[1] - 1]])

        # revert rotation
        if player == 1 and not skip_rotate:
            self.board = np.flipud(self.board)

        return required_moves

    def fix_board_before_returning_false(self, player):
        if player == 1:
            self.board = np.flipud(self.board)

    def get_score(self, player):

        # Calculates score for player
        scores = {}
        for i in range(-1, 2, 2):
            scores[i] = 0
            my_pawns = np.where(self.board == player)
            for i in range(0, len(my_pawns[0])):
                if [my_pawns[0][i], my_pawns[1][i]] in self.kings:
                    scores[i] += 2  # king score
                else:
                    scores[i] += 1  # normal player score

        if player == 1:
            return scores[1] - scores[-1]
        return scores[-1] - scores[1]

    def step(self, player, original_position, direction_left_right, direction_up_down):

        '''
        Move a pawn
        - player: int  (-1 or 1)
        - original_position : list [x,y]
        - direction_left_right: int -1 for left, 1 for right
        - direction_up_down: int -1 for up, 1 for down
        '''

        score_before_step = self.get_score(player)

        # mirror board for player 1
        if player == 1:
            self.board = np.flipud(self.board)

        new_position = [original_position[0] + direction_up_down, original_position[1] + direction_left_right]

        # Move a pawn from _from to _to
        if self.print_debug:
            print("--Move ", original_position, "left" if direction_left_right == -1 else "right",
                  "up" if direction_up_down == -1 else "down", " to ", new_position)

        # DO VARIOUS CHECKS
        # - check if the original_position is on the board
        if original_position[0] < 0 or original_position[1] < 0 or original_position[0] > 7 or original_position[1] > 7:
            if self.print_debug:
                print("Original position is not on this board")
            self.fix_board_before_returning_false(player)
            return False
        # - check new location
        if not (-1 < new_position[1] < 8):
            if self.print_debug:
                print("New position is not on this board (left/right)")
            self.fix_board_before_returning_false(player)
            return False
        if not (-1 < new_position[0] < 8):
            if self.print_debug:
                print("New position is not on this board (up/down)")
            self.fix_board_before_returning_false(player)
            return False

        # - check, when this is a downwards move, if the pawn is a king
        if direction_up_down == 1 and original_position not in self.kings:
            if self.print_debug:
                print("Downwards move but not king")
            self.fix_board_before_returning_false(player)
            return False

        # - check if is own pawn:
        if self.board[original_position[0], original_position[1]] != player:
            if self.print_debug:
                print("Not moving your own pawn")
            self.fix_board_before_returning_false(player)
            return False

        # - check capturing
        capturing = self.is_capturing_move(player, original_position, new_position, direction_left_right,
                                           direction_up_down)

        if capturing != False:
            self.board[capturing[1][0], capturing[1][1]] = 0
            if capturing[1] in self.kings:
                # remove from kings list
                self.kings.remove(capturing[1])
            new_position = capturing[0]
            if self.print_debug:
                print("-- IS CAPTURING MOVE!!")

        # - check if spot is on-occupied
        if self.board[new_position[0], new_position[1]] != 0:
            if self.print_debug:
                print("Not a empty spot")
            self.fix_board_before_returning_false(player)
            return False

        # - check if required moves, and if this move applies
        rms = self.get_required_move(player, skip_rotate=True)

        if len(rms) > 0:
            if [original_position, new_position] not in rms:
                if self.print_debug:
                    print("You have a required set", rms)
                self.fix_board_before_returning_false(player)
                return False

        # -- (done with checks)

        # Update king list
        if new_position[0] == 0:
            if self.print_debug:
                print("Found a king")
            self.kings.append(new_position)

        if original_position in self.kings:
            self.kings.remove(original_position)
            if new_position[0] != 0:
                self.kings.append(new_position)

        self.board[original_position[0], original_position[1]] = 0
        self.board[new_position[0], new_position[1]] = player

        # re-do board mirroring
        if player == 1:
            self.board = np.flipud(self.board)

        if self.print_debug:
            print("-- Did move player ", player, " ", original_position,
                  "left" if direction_left_right == -1 else "right", "up" if direction_up_down == -1 else "down",
                  " to ", new_position)
            print(self.board)

        ## - step done
        if np.sum(np.abs(self.board)) == 0:
            self.done == True

        score_after_step = self.get_score(player)
        ## --return reward: score_after_step - score_before_step
        return score_after_step - score_before_step

    def get_score(self):
        '''
        Return list (score -1 , score 1)
        '''
        return [
            len(np.where(self.board == -1)[0]),
            len(np.where(self.board == 1)[0])
        ]

    def render(self):
        '''
        Prints the board
        '''
        print(self.board)

    def get_possible_actions(self, player, skip_rotate=False):
        '''
        Returns all possible actions in the format [position of pawn, new position]
        '''

        if player == 1 and not skip_rotate:
            self.board = np.flipud(self.board)

        # check if there are mandatory actions
        required_moves = self.get_required_move()
        if len(required_moves) != 0:
            if player == 1 and not skip_rotate:
                self.board = np.flipud(self.board)

            return required_moves

        # no mandatory actions, find all possible actions for this player
        possible_moves = []
        my_pawns = np.where(self.board == player)
        for i in range(0, len(my_pawns[0])):
            my_pawn = [my_pawns[0][i], my_pawns[1][i]]
            # add steps to possible moves
            possible_moves.append([my_pawn,  [my_pawn[0]-1, my_pawn[0]-1]])
            possible_moves.append([my_pawn, [my_pawn[0] - 1, my_pawn[0] + 1]])
            if [my_pawns[0][i], my_pawns[1][i]] in self.kings:
                # add backwards steps
                possible_moves.append([my_pawn, [my_pawn[0] + 1, my_pawn[0] - 1]])
                possible_moves.append([my_pawn, [my_pawn[0] + 1, my_pawn[0] + 1]])

        if player == 1 and not skip_rotate:
            self.board = np.flipud(self.board)

        return possible_moves