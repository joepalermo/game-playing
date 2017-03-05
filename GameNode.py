from tic_tac_toe_utilities import *

terminal_count = 0

# Use a minimax game tree to derive the optimal move
# GameNode properties:
# -move_from_parent
# -state
# -turn_of
# -utility
# -successors
# -optimal_move
#
class GameNode:

    def __init__(self, state, turn_of, move_from_parent):
        self.state = state
        self.turn_of = turn_of
        self.move_from_parent = move_from_parent
        self.utility = None
        self.successors = None
        self.optimal_move = None

    def toString(self):
        print_state(self.state)
        print "\n turn of:" + self.turn_of
        print "\n move from parent: " + str(self.move_from_parent)
        print "\n utility:" + str(self.utility)
        #print "\n successors:" + self.successors
        print "\n optimal_move:" + str(self.optimal_move)

    def generate_game_tree(self):
        if terminal_test(self.state):
            self.utility = utility(self.state, self.turn_of)
            # keep track of progress building the game tree by counting leaves
            global terminal_count
            terminal_count += 1
            if terminal_count % 10000 == 0:
                print terminal_count
            return
        else:
            self.successors = self.generate_successors()
            for successor_node in self.successors:
                successor_node.generate_game_tree()
            # at this point all successor nodes have utility values
            if self.turn_of == 'player_1':
                minimax_node = max(self.successors, key = attrgetter('utility'))
            elif self.turn_of == 'player_2':
                minimax_node = min(self.successors, key = attrgetter('utility'))
            self.utility = minimax_node.utility
            self.optimal_move = minimax_node.move_from_parent

    def generate_successors(self):
        successors = []
        moves = get_valid_moves(self.state)
        for move in moves:
            successor_state = get_successor_state(self.state, self.turn_of, move)
            node = GameNode(successor_state, switch_player(self.turn_of), move)
            successors.append(node)
        return successors

    def get_successor_node(self, move):
        for node in self.successors:
            if node.move_from_parent == move:
                return node
        raise Exception("move doesn't lead to a successor state, or game tree is corrupted")



# root_node = GameNode(init_state(), 'player_1', None)
# root_node.generate_game_tree()
# root_node.toString()
# for node in root_node.successors:
#     print node.toString()





#
# # if someone has won the game, return True
# def is_winner(state):
#     # check the rows
#     for i in range(0, len(state)):
#         if check_squares_for_win(state[i][0], state[i][1], state[i][2]):
#             return True
#     # check the columns
#     for i in range(0, len(state)):
#         if check_squares_for_win(state[0][i], state[1][i], state[2][i]):
#             return True
#     # check the diagonals
#     # top-left to bottom-right
#     if check_squares_for_win(state[0][0], state[1][1], state[2][2]):
#         return True
#     # top-right to bottom-left
#     if check_squares_for_win(state[0][2], state[1][1], state[2][0]):
#         return True
#     return False
#
#
# def derive_move(parent_state, state):
#     for row_i in parent_state:
#         for col_i in parent_state[row_i]:
#             if not parent_state[row_i][col_i] and state[row_i][col_i]:
#                 return (row_i, col_i)
#     raise Exception("Invalid input, parent_state should have a None where child state doesn't")
