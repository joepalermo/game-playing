from tic_tac_toe_utilities import *

# play tic tac toe
def play():

    # initializations for human vs machine game --------------------------------
    player_symbols = {'player_1': 'x', 'player_2': 'o'}
    player_type = {'player_1': 'human', 'player_2': 'ai'}

    # meta-game loop -----------------------------------------------------------
    done = False
    while not done:
        user_input = raw_input("\nDo you want to play tic-tac-toe? " + \
                               "(type y or n) ")
        if user_input == 'n':
            done = True
            continue

        # initialize state for a new game
        state = init_state()
        turn_of = 'player_1'
        game_over = False

        # game loop ------------------------------------------------------------
        while not game_over:
            # get a move from the current player
            move = get_move(turn_of, player_type, state)
            (x,y) = move
            # update state with the move
            state[x][y] = player_symbols[turn_of]
            # switch player
            turn_of = switch_player(turn_of)
            print_state(state)
            # test if a terminal state has been reached
            game_over = terminal_test(state, printResult=True)

play()
