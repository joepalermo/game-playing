from tic_tac_toe_utilities import *

# count the number of leaf nodes found while constructing the game tree, so as
# to update the user on progress
leaf_count = 0

class GameNode:

    def __init__(self, state, turn_of, move_from_parent):
        self.state = state
        self.turn_of = turn_of
        self.move_from_parent = move_from_parent
        # set starting utility to a value that would never be chosen if there
        # was any other alternative
        if self.turn_of == 'player_1':
            self.utility = float("inf")
        else:
            self.utility = - float("inf")
        self.successors = None
        self.optimal_move = None

    def toString(self):
        print_state(self.state)
        print "\n turn of:" + self.turn_of
        print "\n move from parent: " + str(self.move_from_parent)
        print "\n utility:" + str(self.utility)
        print "\n optimal_move:" + str(self.optimal_move)

    # generate the rest of the game tree by depth-first search
    def generate_game_tree(self, alpha = -float("inf"), beta = float("inf")):
        self.alpha = alpha
        self.beta = beta
        if terminal_test(self.state):
            self.utility = utility(self.state, self.turn_of)
            # inform the parent node if it should kill its successor search
            return self.kill_test()
        else:
            self.successors = self.generate_successors()
            for successor_node in self.successors:
                kill = successor_node.generate_game_tree(alpha, beta)
                if kill:
                    # kill test again? should always be false
                    assert not self.kill_test()
                    return False

                if self.turn_of == 'player_1' and successor.utility > alpha:
                    alpha = successor.utility
                elif self.turn_of == 'player_2' and successor.utility < beta:
                    beta = successor.utility

            # at this point all successor nodes have utility values
            if self.turn_of == 'player_1':
                minimax_node = max(self.successors, key = attrgetter('utility'))
            elif self.turn_of == 'player_2':
                minimax_node = min(self.successors, key = attrgetter('utility'))
            self.utility = minimax_node.utility
            self.optimal_move = minimax_node.move_from_parent
            # inform the parent node if it should kill its successor search
            return self.kill_test()


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

    # test whether the parent node should kill its search
    def kill_test(self, alpha, beta):
        return (self.turn_of == 'player_1' and self.utility <= self.alpha) or
               (self.turn_of == 'player_2' and self.utility >= self.beta)
