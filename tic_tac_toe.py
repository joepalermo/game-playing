from random import randint

# simple utility functions ------------------------------------------------------------

# return an empty 3x3 grid, represented by a list of lists with only None values
def init_grid():
    grid = []
    for _ in range(3):
        grid.append([None, None, None])
    return grid

# pretty-print the grid
def print_grid(grid):
    print
    for i in range(0,len(grid)):
        row_string = str(grid[i][0]) + ' | ' + str(grid[i][1]) + ' | ' + \
                     str(grid[i][2])
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
    assert False

# utility functions to get player moves ----------------------------------------

# get a player's next move as a tuple of integer values
def get_move(turn_of, grid):
    move = None
    # loop until a valid move is selected (i.e. until move is not None)
    while not move:
        if player_type[turn_of] == 'human':
            raw_move_input = raw_input('\n' + turn_of + ', enter your move:')
            move = valid_raw_move_input(raw_move_input, grid)
            if move and not valid_move(move, grid):
                move = None
        else:
            move = get_random_move(turn_of, grid)
    return move


# if raw_move_input represents a valid move, then return a parsed representation
# of it as a tuple of integer values; otherwise, return None
def valid_raw_move_input(raw_move_input, grid):
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
def valid_move(move, grid):
    (x, y) = move
    is_valid_move = not grid[x][y]
    if not is_valid_move:
        print "Invalid input. You can only place a symbol on an empty square"
    return is_valid_move

# get a list of valid moves
def get_valid_moves(grid):
    valid_moves = []
    for i in range(0,3):
        for j in range(0,3):
            if not grid[i][j]:
                valid_moves.append((i,j))
    return valid_moves

# get a random valid move
def get_random_move(turn_of, grid):
    valid_moves = get_valid_moves(grid)
    move_index = randint(0,len(valid_moves)-1)
    return valid_moves[move_index]

# utility functions to check end-game conditions -------------------------------

# check if any game-ending conditions are satisfied
# game can end if:
#   - there is a row, column, or diagonal containing 3 of only 1 kind of symbol
#    (i.e. a player has won)
#   - or, symbols have been placed in all 9 positions (i.e. tie game)
def check_if_done(grid):
    done = False
    winner = get_winner(grid)
    # if winner is not None, then announce them as a winner and return True
    if winner:
        done = True
        if winner == 'player_1':
            print '\n' + 'Player 1 is the winner!'
        else:
            print '\n' + 'Player 2 is the winner!'
    elif check_if_full_grid(grid):
        done = True
        print '\n' + 'The game was a tie.'
    return done

# if a player_1 has won the game, return player_1
# if player_2 has won the game, return player_2
# else return None
def get_winner(grid):
    # check the rows
    for i in range(0, len(grid)):
        if check_squares_for_win(grid[i][0], grid[i][1], grid[i][2]):
            return from_symbol_to_player(grid[i][0])
    # check the columns
    for i in range(0, len(grid)):
        if check_squares_for_win(grid[0][i], grid[1][i], grid[2][i]):
            return from_symbol_to_player(grid[0][i])
    # check the diagonals
    # top-left to bottom-right
    if check_squares_for_win(grid[0][0], grid[1][1], grid[2][2]):
        return from_symbol_to_player(grid[0][0])
    # top-right to bottom-left
    if check_squares_for_win(grid[0][2], grid[1][1], grid[2][0]):
        return from_symbol_to_player(grid[2][0])
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

# check if the grid is full with symbols
def check_if_full_grid(grid):
    for row in grid:
        for square in row:
            if square == None:
                return False
    return True


# initializations --------------------------------------------------------------
player_symbols = {'player_1': 'x', 'player_2': 'o'}
player_type = {'player_1': 'human', 'player_2': 'ai'}
grid = init_grid()
turn_of = 'player_1'
game_over = False



# game loop --------------------------------------------------------------------
while not game_over:
    (x,y) = get_move(turn_of, grid) # loop until a valid move is selected
    grid[x][y] = player_symbols[turn_of]
    print_grid(grid)
    game_over = check_if_done(grid)
    turn_of = switch_player(turn_of)
