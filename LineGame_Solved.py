def get_games(initial_board, turn, history):
#Finds every possible (meaningful) game that can be played from a given board
#-intial board is a bag of integers representing the groups of lines to cut
#-turn is a boolean value- the value is True when it is playyer 1s turn, and vice versa
#-history: a list of lists containing the board states over the course of that game.

    
    new_history = list(history);
    new_history.append(initial_board)
    
    used_lines = [];
    
    #IF CASE
    if initial_board == {1:1}:
        games.append(new_history)
        
    
    else:
        #iterates through every line it's possible to cut
        for line in initial_board:

            #makes sure the player isn't instantly losing the game for no reason
            add_amount = 1;
            if sum(initial_board.values()) == 1:
                add_amount = 0;

                
            #iterates through how many lines you're cutting, starting with 1 and 
            #ending in the size of the line
            for num_crossed in range(1, line+add_amount):                   
                #amount of lines that are left after the crossout
                working_amount = line - num_crossed;
            
                #if you've crossed out a whole row:
                if working_amount == 0:
                    #removes the entire line from the board
                    new_board = dict(initial_board);
                    new_board[line] -= 1
                    if new_board[line] == 0:
                        new_board.pop(line)
                    
                
                #if there's anything left, change turn and run program again on this board.
                    new_turn = not(turn);
                    get_games(new_board, new_turn, new_history);

                
            
                #iterates through where you are cutting the line, starting at 0, ending at (working_amount-1).
                #in each one of these scenarios, run the program recursively to determine whther you win
                for line_1 in range(working_amount):
                    #define the size of the new line in this scenario
                    line_2 = working_amount - line_1;

                    #create a copy of the initial_board and remove line from it
                    new_board = dict(initial_board);
                    new_board[line] -= 1
                    if new_board[line] == 0:
                        new_board.pop(line)
                
                    #add the lines to the board if they're not 0
                    if line_1 != 0:
                        new_board.setdefault(line_1, 0)
                        new_board[line_1] += 1
                    if line_2 != 0:
                        new_board.setdefault(line_2, 0)
                        new_board[line_2] += 1
                
                    #change turn, and run the program on the new version of board
                    new_turn = not(turn);
                    #if get_games(new_board, new_turn, new_history) != new_turn:
                    get_games(new_board, new_turn, new_history)
                        


   
    
def find_winning_game(initial_board):
#Given initial board, will return the forced winner of the game and the best sequence of moves

    #find largest row
    highest_num = max(initial_board.keys());
    num_rows = sum(initial_board.values())

    forced_losses = [{1:1}]
    new_forced_losses = [{1:1}];
    forced_wins = [];
    new_forced_wins = [];

    #iterates until you've found a forced win for player 1
    while (initial_board not in forced_wins) and (initial_board not in forced_losses):

        #creates copy of new_forced_losses to iterate over
        n_f_l_copy = list(new_forced_losses)
        
        #iterate over each loss you've found, initializing the states that win when given to player 1 and adding them to
        #forced wins

##        print("-")
##        print("NEW BATCH OF FORCED LOSSES:")
##        print(new_forced_losses)
##        print("-")
        
        for loss in n_f_l_copy:
##            print("Generating forced wins for the following forced loss:")
##            print(loss)
##            print()
            loss_keys = loss.keys();
            
            #creates [loss, y] forced win
            for i in range(1,highest_num+1):
                forced_win = dict(loss)

                #if theres already a row of size i in the board, add another one. Otherwise, add a new row with a value of 1
                forced_win.setdefault(i,0)
                forced_win[i] += 1

                forced_wins.append(forced_win)
                new_forced_wins.append(forced_win)

            #creates [x] forced win
            #iterates over each line in the loss

            
            for line in loss:
                #iterates from (the digit+1) to the highest number
                for i in range(line+1, highest_num+1):

                    #removes old number, adds new numbers
                    forced_win = dict(loss)

                    #removes values from the one you're turning into x
                    if forced_win[line] > 1:
                        forced_win[line] -= 1
                    else:
                        forced_win.pop(line)

                    #if i is not a key in the dictionary, set it to 0. Then add 1 of these types of lines to the board
                    forced_win.setdefault(i,0)
                    forced_win[i] += 1;

                    forced_wins.append(forced_win)
                    new_forced_wins.append(forced_win)

##            print("Forced wins are: ")
##            print(new_forced_wins)
##            print()
            #after you create the forced wins from the loss, remove it from new_forced_losses
            new_forced_losses.remove(loss)

##            print("Finding candidate forced losses for these forced wins:")

            candidate_nfl = []

            #creates candidate new_forced_losses by adding one number
            for win in new_forced_wins:

                win_copy = dict(win)
                #adds a candidate with just an extra row of one
                if (sum(win_copy.values()) + 1) <= num_rows:
                    win_copy.setdefault(1,0)
                    win_copy[1] += 1
                    candidate_nfl.append(win_copy)

                #adds candidate with one extra line on each row
                for line in win:
                    win_copy = dict(win)
                    if (line + 1) <= highest_num:
                        win_copy[line] -= 1
                        if win_copy[line] == 0:
                            win_copy.pop(line)
                        win_copy.setdefault(line+1,0)
                        win_copy[line + 1] += 1
                        candidate_nfl.append(win_copy)

            #clear new forced wins
            new_forced_wins = []
##            print(candidate_nfl)
##
##            print()
##            print("Beginning to investigate candidate forced losses:")

            #removes duplicates from candidate_nfl's:
            candidate_nfl1 = []
            for cand in candidate_nfl:
                if cand not in candidate_nfl1:
                    candidate_nfl1.append(cand)

            
            #runs candidate forced losses through get_games to find all possible games
            for loss in candidate_nfl1:
##                print()
##                print("CFL:")
##                print(loss)       
                
                global games
                games = [];

                get_games(loss, False, [])

##                print("Games possible from this CFL:")
##                print(games)
                
                #define is_forced_loss to be True. If you find that theres an opportunity for the game not to be a loss, then set this to false
                is_forced_loss = True;

                for game in games:
                    if game[1] not in forced_wins:
                        is_forced_loss = False
                        break

##                print("Forced wins for reference:")
##                print(forced_wins)
##                print()
##                print("Is this a forced loss?  " + str(is_forced_loss))

                #if it is a forced loss (every second state is a forced win for the first player) then add it to forced losses.
                if is_forced_loss:
                    forced_losses.append(loss)
                    new_forced_losses.append(loss)

    if initial_board in forced_wins:
        print("This starting board is a forced win.")
        
    elif initial_board in forced_losses:
        print("This starting board is a forced loss. Give up now...")
    else:
        print("???")
        
                
        
initial_board = {2:2}
find_winning_game(initial_board)
