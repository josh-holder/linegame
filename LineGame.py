from itertools import combinations

def getGames(initial_board, history):
    """
    Finds every possible (meaningful) game that can be played from a given board
    INPUTS:
    -initial board is a bag of integers representing the groups of lines to cut
    -history: a list of lists containing the board states over the course of that game.
    """
    
    new_history = list(history)
    new_history.append(initial_board)
    
    used_lines = []
    
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
                    getGames(new_board, new_history);

                
            
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
                    getGames(new_board, new_history)
    else:
        games.append(new_history)


                        


def convertBoardToDict(board):
    """
    i.e. Converts a board with a row of 3 lines and two rows of 1 line from the form:
    [3, 1, 1]
    to
    {3:1,1:2}
    """
    board_dict = {}
    for row in board:
        board_dict.setdefault(row, 0)
        board_dict[row] += 1
    return board_dict

def convertBoardToList(board):
    """
    i.e. Converts a board with a row of 3 lines and two rows of 1 line from the form:
    {3:1,1:2}
    to
    [3, 1, 1]
    """
    board_list = []
    for row, num_rows in board.items():
        for i in range(num_rows):
            board_list.append(row)

    return board_list


def getBoardRepresentationToPrint(board):
    """
    Returns a string which provides a visual representation of game board.

                    |||
    {3:1,1:2} ->     |
                     |

            OR

                    |||
    [3, 1, 1] ->     |
                     |      
    """
    if type(board) == dict: board = convertBoardToList(board)
    board_str = "\n"
    max_row = max(board)

    starts_with_odd = (max_row%2)

    for row in sorted(board,reverse=True):
        is_odd = (row%2)
        if starts_with_odd and not is_odd: odd_even_pad = (row-1)%2
        elif not starts_with_odd and is_odd: odd_even_pad = row%2
        else: odd_even_pad = 0
        pad_num = int((max_row-row)/2) + odd_even_pad
        pad = ' '*pad_num
        lines = '|'*row

        board_str += f"{pad}{lines}\n"
    
    return board_str
        


def findPrevBoards(board, largest_row, add_factor=0, use_add_factor=False):
    """
    Given a board state and the largest row in the initial board, returns a list of possible boards that could have preceded the board state.

    INPUTS - 
    -<dict> board, boardgame in dictionary form as output by convertBoardToDict
    -<int> largest_row, the largest row in the initial board which bounds the maximum size of the previous rows
    OUTPUTS - 
    -<list of dicts> previous boards that could've led to the forced loss, in dictionary form
    """

    previous_boards = []

    #creates [loss, y] forced win - forced wins by adding an entirely new row to the board
    for i in range(1,largest_row+1):
        prev_board = dict(board) #copy board

        #if theres already a row of size i in the board, add another one. Otherwise, add a new row with a value of 1
        prev_board.setdefault(i,0)
        prev_board[i] += 1

        previous_boards.append(prev_board)
        
    #creates [x] forced win - forced wins by adding more lines to each existing row
    #iterates over each line in the loss
    for line in board:
        #iterates from (the digit+1) to the highest number
        for i in range(line+1, largest_row+1):

            #removes old number, adds new numbers
            prev_board = dict(board)

            #removes values from the one you're turning into x
            if prev_board[line] > 1:
                prev_board[line] -= 1
            else:
                prev_board.pop(line)

            #if i is not a key in the dictionary, set it to 0. Then add 1 of these types of lines to the board
            prev_board.setdefault(i,0)
            prev_board[i] += 1;

            previous_boards.append(prev_board)

    #creates previous boards which got to the current board by splitting an earlier one
    combinations_of_rows = combinations(convertBoardToList(board), 2)
    combos_checked = set() 
    for rows in combinations_of_rows:
        rows_set = frozenset(rows)

        #Only check if this combo hasn't been added before
        if rows_set not in combos_checked:
            combos_checked.add(rows_set)

            min_size_of_containing_row = sum(rows) + 1
            for i in range(min_size_of_containing_row,largest_row):
                prev_board = dict(board)

                prev_board[rows[0]] -= 1
                prev_board[rows[1]] -= 1

                prev_board.setdefault(i,0)
                prev_board[i] += 1

                previous_boards.append(prev_board)

    return previous_boards

    
def findWinningMove(initial_board):
    """
    Given initial board, will return the forced winner of the game and the move which continues this forced win.
    INPUTS:
    - <list of ints> initial_board, a list of integers corresponding to rows in the boards
    OUTPUTS:
    - <bool> true if the game is not over, false if the game is over.
        During function execution, prints information on optimal move to take to console.
    """
    #converts the board into the correct format for the computer
    initial_board = convertBoardToDict(initial_board)
    
    largest_row = max(initial_board.keys());

    forced_losses = [{1:1}]
    new_forced_losses = [{1:1}]
    forced_wins = []
    new_forced_wins = []
    add_factor = 0

    #iterates until you've found a forced win for player 1
    while (initial_board not in forced_wins) and (initial_board not in forced_losses):
        #prevents it from being stuck in an infinite loop. Adds more and more to each digit until it finds a new forced loss
        if new_forced_losses == []:
            add_factor += 1
            new_forced_losses = n_f_l_copy #reset new_forced_losses
        else:
            add_factor = 0
        
        #creates copy of new_forced_losses to iterate over
        n_f_l_copy = list(new_forced_losses)
        
        for loss in n_f_l_copy:
            #uses findPrevBoards to find the possible states that could've preceded these forced losses:
            #These are forced wins, so add them to forced_wins and new_forced_wins
            previous_boards = findPrevBoards(loss, largest_row)
            

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
                    if (line + 1 + add_factor) <= largest_row:
                        win_copy[line] -= 1
                        if win_copy[line] == 0:
                            win_copy.pop(line)
                        win_copy.setdefault(line+1+add_factor,0)
                        win_copy[line + 1 + add_factor] += 1
                        candidate_nfl.append(win_copy)
                
                #adds candidate with split 

            #clear new forced wins
            new_forced_wins = []
            
            #removes duplicates from candidate_nfl's to save time in the recursive search:
            candidate_nfl1 = []
            for cand in candidate_nfl:
                if cand not in candidate_nfl1:
                    candidate_nfl1.append(cand)

            #runs candidate forced losses through getGames to find all possible games
            for loss in candidate_nfl1:     
                
                global games
                games = []

                getGames(loss, [])

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
            previous_moves = findPrevBoards(pot_move, largest_row)
            if initial_board in previous_moves:
                if pot_move == {1:1}:
                    print()
                    if human_game:
                        print(f"Cross out a line accordingly to reach {getBoardRepresentationToPrint({1:1})} You win!")
                    else:
                        print(f"Computer moved - new board state (you lose :/): {getBoardRepresentationToPrint({1:1})}")
                    return False
                else:
                    print()
                    if human_game:
                        print(f"Cross out a line accordingly to reach {getBoardRepresentationToPrint(pot_move)}")
                    else:
                        print(f"Computer moved - new board state: {getBoardRepresentationToPrint(pot_move)}")
                    print()
                    return True
                break
            
    else:
        if human_game:
            print("Assuming your opponent plays perfectly, you will lose. Use your best judgement")
            return True
        else:
            if initial_board != {1:1}:
                random_line = list(initial_board.keys())[0]
                initial_board[random_line] -= 1
                if initial_board[random_line] == 0: initial_board.pop(random_line)
                print(f"Computer moved - new board state (you're on track to win!): {getBoardRepresentationToPrint(initial_board)}")

                return True
            else:
                print("You win!")
                return False


if __name__ == "__main__":
    global human_game
    print("Type of game? (type 0 to play against the computer, type 1 for assistance in a human game)")
    human_game = int(input(""))
    if human_game != 0 and human_game != 1: 
        print("Invalid input")
    
    print(f"Input the board at the start of the game. For example, input the following board:\n{getBoardRepresentationToPrint([3,1,1])}\nas '3 1 1'.")
    print("-------------------")
    ask_again = True
    
    first_ask = True
    while ask_again == True:
        if first_ask: first_ask = False
        else:
            if human_game:
                print("Board state after opponent move?")
            else:
                print("Board state after your move?")
        
        input_board = input("")
        initial_board = [int(x) for x in input_board.split()] #convert string of numbers to ints
        print(getBoardRepresentationToPrint(initial_board))
        ask_again = findWinningMove(initial_board)