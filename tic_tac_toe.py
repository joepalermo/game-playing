from random import randint

# simple utility functions ------------------------------------------------------------

# return an empty 3x3 state, represented by a list of lists with only None values
def init_state():
    state = []
    for _ in range(3):
        state.append([None, None, None])
    return state

# pretty-print the state
def print_state(state):
    print
    for i in range(0,len(state)):
        row_string = str(state[i][0]) + ' | ' + str(state[i][1]) + ' | ' + \
                     str(state[i][2])
        print row_string.replace('None', ' ')

# if turn_of is 'player_1' return 'player_2', and vice versa
def switch_player(turn_of):
    if turn_of == 'player_1':
        return 'player_2'
    else:
        return 'player_1'

# get the player who uses a particular symbol
def from_symbol_to_player(symbol):
    for player in player_symbols.keys():
        if player_symbols[player] == symbol:
            return player
    # this line should never be reached, if it is, then symbol doesn't match
    # any player in player_symbols
    raise Exception("symbol " + symbol + ", doens't correspond to a player")

# utility functions to get player moves ----------------------------------------

# get a player's next move as a tuple of integer values
def get_move(turn_of, state):
    move = None
    # loop until a valid move is selected (i.e. until move is not None)
    while not move:
        if player_type[turn_of] == 'human':
            raw_move_input = raw_input('\n' + turn_of + ', enter your move:')
            move = valid_raw_move_input(raw_move_input, state)
            if move and not valid_move(move, state):
                move = None
        else:
            #todo
            #move = get_optimal_move(turn_of, state)
            move = get_random_move(turn_of, state)
    return move


# if raw_move_input represents a valid move, then return a parsed representation
# of it as a tuple of integer values; otherwise, return None
def valid_raw_move_input(raw_move_input, state):
    move = None
    # check that a comma was supplied to separate values
    if ',' in raw_move_input:
        raw_move_components = raw_move_input.split(',')
        # check that the raw input can be converted into a pair of integers
        if raw_move_components[0].isdigit() and \
           raw_move_components[1].isdigit():
            # convert the components to integers
            move_components = [int(raw_move_components[0]),
                               int(raw_move_components[1])]
            # check that the integer inputs are bounded by 0 and 2
            if (0 <= move_components[0] and move_components[0] <= 2) and \
               (0 <= move_components[1] and move_components[1] <= 2):
               move = (move_components[0], move_components[1])
            else:
                print '\n' + 'Invalid input. The components are not in range'
        else:
            print '\n' + 'Invalid input. Remember to supply 2 integer values'
    else:
        print '\n' + 'Invalid input. Remember to separate values by a comma'
    return move

# validate a move
def valid_move(move, state):
    (x, y) = move
    is_valid_move = not state[x][y]
    if not is_valid_move:
        print "Invalid input. You can only place a symbol on an empty square"
    return is_valid_move

# get a list of valid moves
def get_valid_moves(state):
    valid_moves = []
    for i in range(0,3):
        for j in range(0,3):
            if not state[i][j]:
                valid_moves.append((i,j))
    return valid_moves

# get a random valid move
def get_random_move(turn_of, state):
    valid_moves = get_valid_moves(state)
    move_index = randint(0,len(valid_moves)-1)
    return valid_moves[move_index]

# utility functions to check end-game conditions -------------------------------

# check if any game-ending conditions are satisfied
# game can end if:
#   - there is a row, column, or diagonal containing 3 of only 1 kind of symbol
#    (i.e. a player has won)
#   - or, symbols have been placed in all 9 positions (i.e. tie game)
def check_if_done(state):
    done = False
    winner = get_winner(state)
    # if winner is not None, then announce them as a winner and return True
    if winner:
        done = True
        if winner == 'player_1':
            print '\n' + 'Player 1 is the winner!'
        else:
            print '\n' + 'Player 2 is the winner!'
    elif is_full_state(state):
        done = True
        print '\n' + 'The game was a tie.'
    return done

# if a player_1 has won the game, return player_1
# if player_2 has won the game, return player_2
# else return None
def get_winner(state):
    # check the rows
    for i in range(0, len(state)):
        if check_squares_for_win(state[i][0], state[i][1], state[i][2]):
            return from_symbol_to_player(state[i][0])
    # check the columns
    for i in range(0, len(state)):
        if check_squares_for_win(state[0][i], state[1][i], state[2][i]):
            return from_symbol_to_player(state[0][i])
    # check the diagonals
    # top-left to bottom-right
    if check_squares_for_win(state[0][0], state[1][1], state[2][2]):
        return from_symbol_to_player(state[0][0])
    # top-right to bottom-left
    if check_squares_for_win(state[0][2], state[1][1], state[2][0]):
        return from_symbol_to_player(state[2][0])
    return None

# check to see if a sequence of squares have equal values
def check_squares_for_win(x, y, z):
    is_win = False
    # make sure at least one value isn't None
    if x:
        # check that all 3 values are equal
        if x == y and y == z:
            is_win = True
    return is_win

# check if the state is full with symbols
def is_full_state(state):
    for row in state:
        for square in row:
            if square == None:
                return False
    return True


# initializations --------------------------------------------------------------
player_symbols = {'player_1': 'x', 'player_2': 'o'}
player_type = {'player_1': 'human', 'player_2': 'ai'}
state = init_state()
turn_of = 'player_1'
game_over = False



# game loop --------------------------------------------------------------------
while not game_over:
    (x,y) = get_move(turn_of, state) # loop until a valid move is selected
    state[x][y] = player_symbols[turn_of]
    print_state(state)
    game_over = check_if_done(state)
    turn_of = switch_player(turn_of)
