from random import shuffle


def is_valid_direction(x_position:int,y_position:int,direction:int,game_board:list,path_mark:int) -> bool:
    """Checks if the direction where the labyrith path is valid. Returns false if there is a wall, 
    the same path next to it or the path is going downwards to a dead end

    Args:
        x_position (int): the x coordinate of the current position before moving
        y_position (int): the y coordinate of the current position before moving
        direction (int): the direction where the path is moving to
        game_board (list): a list containing the game board (labyrinth)
        path_mark (int): the ascii character indicating the path

    Returns:
        bool: returns True if the direction is considered valid and False if it not
    """

    #Checks all the directions depending ont he direction the path is currently moving towards
    try:
        if direction == 1: #right
            x_position+=1
            if game_board[y_position][x_position+1] == f" {path_mark} " or game_board[y_position+1][x_position] == f" {path_mark} "\
or game_board[y_position-1][x_position] == f" {path_mark} " or game_board[y_position][x_position] == " x "\
or game_board[y_position][x_position] == f" {path_mark} ":
                return False
            else:
                return True
        elif direction == 2: #left
            x_position-=1
            if game_board[y_position][x_position-1] == f" {path_mark} " or game_board[y_position+1][x_position] == f" {path_mark} "\
or game_board[y_position-1][x_position] == f" {path_mark} " or game_board[y_position][x_position] == " x "\
or game_board[y_position][x_position] == f" {path_mark} ":
                return False
            else:
                return True
        elif direction == 3: #up
            y_position-=1
            if game_board[y_position][x_position+1] == f" {path_mark} " or game_board[y_position][x_position-1] == f" {path_mark} "\
or game_board[y_position-1][x_position] == f" {path_mark} " or game_board[y_position][x_position] == " x "\
or game_board[y_position][x_position] == f" {path_mark} ":
                return False
            else:
                return True
        elif direction == 4: #down
            if game_board[y_position][x_position+1] == " x " or game_board[y_position][x_position+2] == " x "\
or game_board[y_position][x_position-1] == " x " or game_board[y_position][x_position-2] == " x ":
                return False
            y_position+=1
            if game_board[y_position][x_position+1] == f" {path_mark} " or game_board[y_position][x_position-1] == f" {path_mark} "\
or game_board[y_position+1][x_position] == f" {path_mark} " or game_board[y_position][x_position] == " x "\
or game_board[y_position][x_position] == f" {path_mark} ":
                return False
            else:
                return True
    except IndexError:
        # print("Error here")
        return False


def define_route(size:int,start_position:int,board:list,path_mark:int) -> list:
    """Draws randomized routes on the game board (list) where the player can go

    Args:
        size (int): height and width of the game board (labyrith)
        start_position (int): starting x coordinate on the lowest y level
        board (list): the game_board as a nested list
        path_mark (int): the ascii character marking the current path

    Returns:
        list: a game board with one or more paths "drawn", one start and one exit
    """
    
    restart = True
    game_board = board
    
    while restart == True:
        next_x = start_position
        next_y = size - 2
        game_board[next_y][next_x] = f" {path_mark} "
        is_finished = False
        try:
            while is_finished == False:
                #Make a list of possible directions
                next_step = [1,2,3,4]
                #Randomize the direction for the path to go
                shuffle(next_step)
                direction = 0
                
            
                while is_finished == False:
                    if next_y == 1 and next_step[direction] == 3:
                        #Make 3 seperate routes that can go on top of eachother to get more places to go in the labyrinth
                        #Only one route has an ending
                        if path_mark <= 3:
                            #if there are less than 3 paths then to the define_route again until is_finished is True
                            game_board = define_route(size,start_position,game_board,path_mark+1)
                        else:
                            game_board[next_y-1][next_x] = f" {path_mark} "
                            for i in range(size):
                                for k in range(size):
                                    if game_board[i][k] == "   ":
                                        game_board[i][k] = " x "
                                    elif game_board[i][k] != " x ":
                                        game_board[i][k] = "   "

                        is_finished = True
                        restart = False
                        break
                    #Check if the direction is valid with a seperate method
                    if is_valid_direction(next_x,next_y,next_step[direction],game_board,path_mark):
                        #Depending on the direction the coordinates will change
                        if next_step[direction] == 1: #right
                            next_x += 1
                        elif next_step[direction] == 2: #left
                            next_x -= 1
                        elif next_step[direction] == 3: #up
                            next_y -= 1
                        else: #down
                            next_y += 1

                        game_board[next_y][next_x] = f" {path_mark} "
                        break
                    else:
                        direction += 1
                        continue
        except IndexError:
            # game_board = reset_board(game_board)
            path_mark+=1
            # print("Path ended in a loop")
            
    return game_board



def draw_reference_board(size:int,start_position:int)->tuple:
    """draws a game board of a chosen size to reference with everything randomized

    Args:
        size (int): the width and height of the board

    Returns:
        list: the randomized game board
    """
    game_board = []
    #path-mark for marking the different routes on the board. In the end all the path-marks will be changed to empty spaces
    path_mark = 1

    #Draws the board edges but making every row as a list and appending those row to the game_board list
    for i in range(size):
        temporary_board_level = []
        for k in range(size):
            if i == 0: #top row
                    temporary_board_level.append(" x ")
            elif i == size - 1: #bottom row
                if k == start_position:
                    temporary_board_level.append(f" {path_mark} ")
                else:
                    temporary_board_level.append(" x ")
            else:
                if k == 0 or k == size - 1:
                    temporary_board_level.append(" x ")
                else:
                    temporary_board_level.append("   ")

        game_board.append(temporary_board_level)
        
    #Draw rest of the board with define_route to make the reference board for the game
    game_board = define_route(size,start_position,game_board,path_mark)
    return tuple(game_board)