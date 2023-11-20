# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 12:41:17 2023

@author: Zdrey
"""
import numpy as np
import random
#from qtable import Q

# Define the game board and the initial positions of the pieces
board_size = 8
board = np.full((board_size, board_size), 'o')
board[1::2, ::2] = 'x'
board[::2, 1::2] = 'x'

for i, row in enumerate(board):
    for j, val in enumerate(row):
        if val == 'x':
            continue
        if i < 3:
            board[i, j] = 'b'
        elif i > 4:
            board[i, j] = 'r'

# Define the rules of the game
def is_valid_move(board, player, move):
    # Check if the move is within the bounds of the board
    if move[0] < 0 or move[0] > 7 or move[1] < 0 or move[1] > 7 or move[2] < 0 or move[2] > 7 or move[3] < 0 or move[3] > 7:
        return False
    # Check if the move is diagonal
    if abs(move[0] - move[2]) != abs(move[1] - move[3]):
        return False
    # Check if the move is forward for regular pieces
    if player == "b" and move[0] >= move[2]:
        return False
    if player == "r" and move[0] <= move[2]:
        return False
    # Check if the move is a capture
    if abs(move[0] - move[2]) == 2:
        x = (move[0] + move[2]) // 2
        y = (move[1] + move[3]) // 2
        if board[x, y] == "o" or board[x, y] == player:
            return False
        # Check if the move is within the bounds of the board
        if move[0] < 0 or move[0] > 7 or move[1] < 0 or move[1] > 7 or move[2] < 0 or move[2] > 7 or move[3] < 0 or move[3] > 7:
            return False
        # Check if the move is diagonal
        if abs(move[0] - move[2]) != abs(move[1] - move[3]):
            return False
        # Check if the move is forward for regular pieces
        if player == "b" and move[0] >= move[2]:
            return False
        if player == "r" and move[0] <= move[2]:
            return False

        # Define the values of alpha and reward
        alpha = 0.1
        reward = 0.5

        # Check if state and action are defined and if they exist in the Q table
        #q = Q()
        #if 'state' in locals() and 'action' in locals():
         #   q.update(state, action, reward)
        #else:
         #   state = q.get_state(board, player)
          #  actions = get_valid_moves(board, player)
           ##    return False
            #action = q.get_action(state, actions)
        #if state not in q:
         #   q[state] = {}
        #if action not in q[state]:
        #    q[state][action] = 0
        #q.update(state, action, reward, board)
        #q[state][action] = (1 - alpha) * q[state][action] + alpha * reward
        #return True

        # Check if the move is a capture
        if abs(move[0] - move[2]) == 2:
            x = (move[0] + move[2]) // 2
            y = (move[1] + move[3]) // 2
            if board[x, y] == "o" or board[x, y] == player:
                return False
            if move[2] - move[0] > 0:
                if move[3] - move[1] > 0:
                    if board[move[2]+1, move[3]+1] != "o":
                        return False
                else:
                    if board[move[2]+1, move[3]-1] != "o":
                        return False
            else:
                if move[3] - move[1] > 0:
                    if board[move[2]-1, move[3]+1] != "o":
                        return False
                else:
                    if board[move[2]-1, move[3]-1] != "o":
                        return False
            # Check if the piece should be kinged
            if player == "b" and move[2] == 7:
                board[move[2], move[3]] = "B"
            elif player == "r" and move[2] == 0:
                board[move[2], move[3]] = "R"
            return True

    return True

def get_valid_moves(board, player):
    moves = []
    for i in range(8):
        for j in range(8):
            if board[i, j] == player or board[i, j] == player.upper():
                if board[i, j] == "b" or board[i, j] == "B":
                    if is_valid_move(board, player, [i, j, i+1, j+1]):
                        moves.append([i, j, i+1, j+1])
                    if is_valid_move(board, player, [i, j, i+1, j-1]):
                        moves.append([i, j, i+1, j-1])
                    if is_valid_move(board, player, [i, j, i+2, j+2]):
                        moves.append([i, j, i+2, j+2])
                    if is_valid_move(board, player, [i, j, i+2, j-2]):
                        moves.append([i, j, i+2, j-2])
                if board[i, j] == "r" or board[i, j] == "R":
                    if is_valid_move(board, player, [i, j, i-1, j+1]):
                        moves.append([i, j, i-1, j+1])
                    if is_valid_move(board, player, [i, j, i-1, j-1]):
                        moves.append([i, j, i-1, j-1])
                    if is_valid_move(board, player, [i, j, i-2, j+2]):
                        moves.append([i, j, i-2, j+2])
                    if is_valid_move(board, player, [i, j, i-2, j-2]):
                        moves.append([i, j, i-2, j-2])
    return moves

def make_move(board, move):
    x1, y1, x2, y2 = move
    board[x2, y2] = board[x1, y1]
    board[x1, y1] = "o"
    if abs(x1 - x2) == 2:
        x = (x1 + x2) // 2
        y = (y1 + y2) // 2
        board[x, y] = "o"
    # Check if the piece should be kinged
    if board[x2, y2] == "b" and x2 == 7:
        board[x2, y2] = "B"
    elif board[x2, y2] == "r" and x2 == 0:
        board[x2, y2] = "R"

# Implement a function to display the current state of the game board
def display_board(board):
    print("   0 1 2 3 4 5 6 7")
    print("  +----------------")
    for i in range(8):
        row = str(i) + " |"
        for j in range(8):
            if board[i, j] == "o":
                row += " "
            else:
                row += board[i, j]
            row += "|"
        print(row)
    print("  +----------------")

# Implement a function to get the user's move and update the game board accordingly
def get_user_move(board):
    while True:
        try:
            piece_pos, move_pos = input("Enter the piece you want to move and the move destination separated by a space (e.g. '1,2 2,3'): ").split()
            move = [int(piece_pos[0]), int(piece_pos[2]), int(move_pos[0]), int(move_pos[2])]
            if is_valid_move(board, "b", move):
                piece_pos = [int(x) for x in piece_pos.split(',')]
                move_pos = [int(x) for x in move_pos.split(',')]
                make_move(board, move)
                display_board(board)
                break
            else:
                display_board(board)
                print("Invalid move, try again.")
        except ValueError:
            pass

    # Remove pieces that were taken
    for i in range(8):
        for j in range(8):
            pass
            if board[i, j] == "r" and i < 6 and ((j > 0 and board[i+1, j-1] == "b" and board[i+2, j-2] == "o") or (j < 7 and board[i+1, j+1] == "b" and board[i+2, j+2] == "o")):
                print("You captured a piece!")
                board[i+1, j-1] = "o"
                board[i+2, j-2] = "o"
            elif board[i, j] == "b" and i > 1 and ((j > 0 and board[i-1, j-1] == "r" and board[i-2, j-2] == "o") or (j < 7 and board[i-1, j+1] == "r" and board[i-2, j+2] == "o")):
                print("You captured a piece!")
                board[i-1, j-1] = "o"
                board[i-2, j-2] = "o"

    # Count remaining pieces
    num_b = np.count_nonzero(board == "b") + np.count_nonzero(board == "B")
    num_r = np.count_nonzero(board == "r") + np.count_nonzero(board == "R")
    print(f"You have {num_b} pieces remaining.")
    print(f"The AI has {num_r} pieces remaining.")

# Implement a function to generate the AI's move using reinforcement learning
def get_ai_move(board):
    # TODO: Implement reinforcement learning algorithm to generate AI move
    moves = get_valid_moves(board, "r")
    if len(moves) == 0:
        return None
    else:
        return random.choice(moves)


# Initialize Q-table with zeros
Q = {}

# Define state encoding function
def encode_state(board):
    state = 0
    for i in range(8):
        for j in range(8):
            if board[i, j] == "b":
                state += 2**(i*8+j)
            elif board[i, j] == "r":
                state += 2**(i*8+j+32)
    return state

# Define action decoding function
def decode_action(action):
    x1, y1, x2, y2 = action
    return x1*8+y1, x2*8+y2

# Define reward function
def get_reward(board, player):
    if player == "b" and np.count_nonzero(board == "r") == 0:
        return 1
    elif player == "r" and np.count_nonzero(board == "b") == 0:
        return 1
    else:
        return 0

# Define Q-learning update function
def update_q_table(state, action, reward, next_state):
    alpha = 0.1
    gamma = 0.9

    # def decode_board(state):
    #     board = np.zeros((8, 8), dtype=np.str)
    #     for i in range(8):
    #         for j in range(8):
    #             if state & 1 == 1:
    #                 board[i, j] = "b"
    #             elif state & 2 == 2:
    #                 board[i, j] = "r"
    #             state >>= 2
    #     return board
    
    make_move(board, action)
    display_board(board)
    next_state = encode_state(board)
    Q[state][action] = (1 - alpha) * Q[state][action] + alpha * (reward + gamma * np.max(Q[next_state]))
    pass

# Define function to update AI model based on game outcome
def update_ai_model(board, player):
    state = encode_state(board)
    reward = get_reward(board, player)
    if reward == 1:
        update_q_table(state, None, reward, None)
    else:
        moves = get_valid_moves(board, player)
        if len(moves) > 0:
            q_values = Q.get(state, np.zeros(8))[moves]
            action = moves[np.argmax(q_values)]
            if is_valid_move(board, "r", action):
                make_move(board, action)
                display_board(board)
                if np.count_nonzero(board == "b") == 0:
                    print("AI wins!")
                    return
                update_q_table(state, action, 0, encode_state(board))
            else:
                print("Invalid move, skipping AI's turn.")
        else:
            print("AI can't move, you win!")
            return

# Implement a loop to play the game until one side wins
while True:
    play_again = input("Would you like to play Checkers? (yes/no): ")
    if play_again.lower() != "yes":
        break

    board = np.full((board_size, board_size), 'o')
    board[1::2, ::2] = 'x'
    board[::2, 1::2] = 'x'
    for i, row in enumerate(board):
        for j, val in enumerate(row):
            if val == 'x':
                continue
            if i < 3:
                board[i, j] = 'b'
            elif i > 4:
                board[i, j] = 'r'

    display_board(board)

    while True:
        # User's turn
        get_user_move(board)
        if np.count_nonzero(board == "r") == 0:
            print("You win!")
            break

        # AI's turn
        ai_move = get_ai_move(board)
        if ai_move is None:
            print("AI can't move, you win!")
            break
        update_ai_model(board, "r")
        if np.count_nonzero(board == "b") == 0:
            print("AI wins!")
            break

