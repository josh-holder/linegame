def get_games(initial_board, history):
#Finds every possible (meaningful) game that can be played from a given board
#-initial board is a bag of integers representing the groups of lines to cut
#-history: a list of lists containing the board states over the course of that game.

    
    new_history = list(history);
    new_history.append(initial_board)
    
    used_lines = [];
    
    #IF CASE
    if initial_board == {1:1}:
        games.append(new_history)
        
    #Finds only the possible first moves. After it finds all the possible next moves (i.e. there are 2 items in new_history), ends the loop
    elif len(new_history) == 1:
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
                    
                
                #if there's anything left, run program again on this board.
                #Stops at move 2, because that's all that's necessary
                    get_games(new_board, new_history);

                
            
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
                    get_games(new_board, new_history)
    else:
        games.append(new_history)


                        


def convert(board):
#Converts a board with a row of 3 lines and two rows of 1 line from the form:
#[3 1 1]
#to
#{3:1,1:2}
    formatted_board = {}
    for row in board:
        formatted_board.setdefault(row, 0)
        formatted_board[row] += 1
    return formatted_board




def find_prev_moves(board, highest_num):
##Given a board state and the largest row in the initial board, returns a list of possible moves that could have preceded the board state.
    
    previous_moves = []

    #creates [loss, y] forced win

    for i in range(1,highest_num+1):
        prev_move = dict(board)

        #if theres already a row of size i in the board, add another one. Otherwise, add a new row with a value of 1
        prev_move.setdefault(i,0)
        prev_move[i] += 1

        previous_moves.append(prev_move)
        
    #creates [x] forced win
    #iterates over each line in the loss

    
    for line in board:
        #iterates from (the digit+1) to the highest number
        for i in range(line+1, highest_num+1):

            #removes old number, adds new numbers
            prev_move = dict(board)

            #removes values from the one you're turning into x
            if prev_move[line] > 1:
                prev_move[line] -= 1
            else:
                prev_move.pop(line)

            #if i is not a key in the dictionary, set it to 0. Then add 1 of these types of lines to the board
            prev_move.setdefault(i,0)
            prev_move[i] += 1;

            previous_moves.append(prev_move)


    return previous_moves




    
def find_winning_move(initial_board):
#Given initial board, will return the forced winner of the game and the move which continues this forced win
#initial_board, a list of the form [3 1]

    #converts the board into the correct format for the computer
    initial_board = convert(initial_board)
    
    #find largest row
    highest_num = max(initial_board.keys());

    forced_losses = [{1:1}]
    new_forced_losses = [{1:1}];
    forced_wins = [];
    new_forced_wins = [];
    add_factor = 0


    #iterates until you've found a forced win for player 1
    while (initial_board not in forced_wins) and (initial_board not in forced_losses):

##        print("NEW BATCH OF FORCED LOSSES:")
##        print(new_forced_losses)
##        print("-----------")
##        print("all forced losses")
##        print(forced_losses)


        #prevents it from being stuck in an infinite loop. Adds more and more to each digit until it finds a new forced loss
        if new_forced_losses == []:
            add_factor += 1
        else:
            add_factor = 0
        
        #creates copy of new_forced_losses to iterate over
        n_f_l_copy = list(new_forced_losses)
        
        for loss in n_f_l_copy:
            #uses find_prev_moves to find the possible states that could've preceded these forced losses:
            #These are forced wins, so add them to forced_wins and new_forced_wins
            previous_boards = find_prev_moves(loss, highest_num)
            

            forced_wins.extend(previous_boards)
            new_forced_wins.extend(previous_boards)


            #after you create the forced wins from the loss, remove it from new_forced_losses
            new_forced_losses.remove(loss)

            candidate_nfl = []

            #creates candidate new_forced_losses by adding one number
            for win in new_forced_wins:

                win_copy = dict(win)
                
                #adds a candidate with just an extra row of one
                win_copy.setdefault(1+add_factor,0)
                win_copy[1+add_factor] += 1
                candidate_nfl.append(win_copy)

                #adds candidate with one extra line on each row
                for line in win:
                    win_copy = dict(win)
                    if (line + 1 + add_factor) <= highest_num:
                        win_copy[line] -= 1
                        if win_copy[line] == 0:
                            win_copy.pop(line)
                        win_copy.setdefault(line+1+add_factor,0)
                        win_copy[line + 1 + add_factor] += 1
                        candidate_nfl.append(win_copy)

            #clear new forced wins
            new_forced_wins = []
            
            #removes duplicates from candidate_nfl's to save time in the recursive search:
            candidate_nfl1 = []
            for cand in candidate_nfl:
                if cand not in candidate_nfl1:
                    candidate_nfl1.append(cand)

            #runs candidate forced losses through get_games to find all possible games
            for loss in candidate_nfl1:     
                
                global games
                games = [];

                get_games(loss, [])

                #define is_forced_loss to be True. If you find that theres an opportunity for the game not to be a loss, then set this to false
                is_forced_loss = True;

                for game in games:
                    if game[1] not in forced_wins:

                        is_forced_loss = False
                        break

                #if it is a forced loss (every second state is a forced win for the first player) then add it to forced losses.
                if is_forced_loss:
                    forced_losses.append(loss)
                    new_forced_losses.append(loss)

    
    if initial_board in forced_wins:
        
        for pot_move in forced_losses:

            #finds previous moves for every forced_loss. If the initial board is a previous move for any of these forced losses, print this forced loss.
            previous_moves = find_prev_moves(pot_move, highest_num)
            if initial_board in previous_moves:
                if pot_move == {1:1}:
                    print()
                    print("Cross out a line accordingly to reach {1:1}. You win!")
                    return False
                else:
                    print()
                    print("Cross out a line accordingly to reach " + str(pot_move))
                    print()
                    print("Your opponent has moved.")
                    return True
                break
            
    else:
        print("This starting board is a FORCED LOSS.")
        return False

#Runs user input program:
print("Input the board at the start of the game. For example, input a board with one row of 3 lines and two rows of 1 line as '3 1 1'.")
print("-------------------")
ask_again = True
while ask_again == True:
    print("Current board state?")
    input_board = input("")
    initial_board = [int(x) for x in input_board.split()]
    print()
    ask_again = find_winning_move(initial_board)

