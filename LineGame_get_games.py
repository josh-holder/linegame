games = [];

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
                        

get_games({1:1, 3:1}, True, [])

print(games)
   
    
