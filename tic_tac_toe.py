from tic_tac_toe_utilities import *

# play tic tac toe
def play():

    # player initializations ----------------------------------------------------------
    player_symbols = {'player_1': 'x', 'player_2': 'o'}
    player_type = {'player_1': 'human', 'player_2': 'human'}
    human_playing = is_human_playing(player_type)
    # record tracks player_1 wins, player_2 wins, and ties respectively
    record = [0,0,0]

    # meta-game loop -----------------------------------------------------------
    done = False
    games_played = 0
    max_games = 100
    while not done and games_played < max_games:

        if human_playing:
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
            # if a human is playing, then print an updated game state
            if human_playing:
                print_state(state)
            # test if a terminal state has been reached
            game_over = terminal_test(state, printResult=True)
            # switch player
            turn_of = switch_player(turn_of)

        games_played += 1
        update_record(state, record)

    print_record(record)

play()
