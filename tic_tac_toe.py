from tic_tac_toe_utilities import *

# play tic tac toe

def play():

    # initializations for human vs machine game ------------------------------------
    player_symbols = {'player_1': 'x', 'player_2': 'o'}
    player_type = {'player_1': 'human', 'player_2': 'ai'}
    state = init_state()
    turn_of = 'player_1'
    game_over = False

    # game loop --------------------------------------------------------------------
    while not game_over:
        (x,y) = get_move(turn_of, player_type, state) # loop until a valid move is selected
        state[x][y] = player_symbols[turn_of]
        turn_of = switch_player(turn_of)
        print_state(state)
        game_over = terminal_test(state)


play()
