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
        print "\n optimal_move:" + str(self.optimal_move)
        #print "\n successors:" + self.successors

    # generate the rest of the game tree by depth-first search
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

    # generate all successors of the current node
    def generate_successors(self):
        successors = []
        moves = get_valid_moves(self.state)
        for move in moves:
            successor_state = get_successor_state(self.state, self.turn_of, move)
            node = GameNode(successor_state, switch_player(self.turn_of), move)
            successors.append(node)
        return successors

    # get the node that results from taking a given move at the current node
    def get_successor_node(self, move):
        for node in self.successors:
            if node.move_from_parent == move:
                return node
        raise Exception("move doesn't lead to a successor state, or game tree is corrupted")
        
