import msvcrt
from random import randrange, shuffle
import game_board_building


def draw_start_board(size:int, start_position:int)->tuple:
    """Draws the game_board list as a board for a visual representation of the start of the game.

    Args:
        loc_x (int): The x value on the game board (0-9) of the players current position
        loc_y (int): The y value on the game board (0-9) of the players current position
    """
    #Introduce a new list to be used as the game board visible to the player
    game_board = []
    #Draw the edges and the current location of the player
    for i in range(size):
        #Introduced a temporary list to insert the values of a row which is the appended to the game_board
        temporary_list = []
        for k in range(size):
            if i == 0: #top row
                    temporary_list.append(" x ")
            elif i == size - 1: #bottom row
                if k == start_position:
                    temporary_list.append(r"\o>")
                else:
                    temporary_list.append(" x ")
            else:
                if k == 0 or k == size - 1:
                    temporary_list.append(" x ")
                else:
                    temporary_list.append("   ")
        #here the newly made row is appended to the game_board and the loop starts again to make the next row
        game_board.append(temporary_list)

    return tuple(game_board)

    

def draw_location(game_board:tuple,reference_game_board:tuple,location_x:int,location_y:int,direction:bytes)-> list:
    """draw the new location of the player on the game_board

    Args:
        game_board (tuple): The current game board to be drawn on
        reference_game_board (tuple): The gameboard to reference the locations of walls
        location_x (int): The new x location where to draw the player
        location_y (int): The new y location where to draw the player
        direction (bytes): the direction key pressed by the player from (w,a,s,d)

    Returns:
        list: the game_board with the new location of the player added and old removed
    """
    #A temporary list is made to be used as the board in this function
    temporary_board = list(game_board)
    #The player is droawn in the new location
    temporary_board[location_y][location_x] = r"\o>"

    #depending on the direction key pressed the player is erased from the previous location
    if direction.lower() == b"w": #up
        temporary_board[location_y+1][location_x] = "   "
    elif direction.lower() == b"s": #down
        temporary_board[location_y-1][location_x] = "   "
    elif direction.lower() == b"a": #left
        temporary_board[location_y][location_x+1] = "   "
    elif direction.lower() == b"d": #right
        temporary_board[location_y][location_x-1] = "   "

    #The locasions around the player are drawn on the map
    sight_radius_y = location_y-1
    sight_radius_x = location_x-1
    for i in range(3):
        for k in range(3):
            try:
                #The value from the reference board is drawn if it is not the current place of the player
                if temporary_board[sight_radius_y+i][sight_radius_x+k] != r"\o>":
                    temporary_board[sight_radius_y+i][sight_radius_x+k] = reference_game_board[sight_radius_y+i][sight_radius_x+k]
            except IndexError:
                print("went here")
                pass

    return temporary_board
        


def valid_direction(reference_game_board:list,loc_x, loc_y)->bool:
    """Check if the position is out of bounds or on an element containing " x ".

    Args:
        loc_x (int): The x value on the game board (0-9)
        loc_y (int): The y value on the game board (0-9)

    Returns:
        bool: returns True if the locasion is valid and False if the location is invalid (Index out of bounds or element "x")
    """
    try:
        if reference_game_board[loc_y][loc_x] == " x ":
            return False
        else:
            return True
    except IndexError:
        return False

def draw_board(game_board: list):
    """Draws the guven board as a visual representation of the current game state

    Args:
        game_board (list): the game_board to be drawn
    """
    for i in range(len(game_board)):
        for k in range(len(game_board)):
            print(game_board[i][k],end="")
        print("")

def main():
    #Introdeuce the attribute size for the player to later choose
    size = None

    #print the information text for the player
    print("Welcome to the labyrinth")
    while True:
        try:
            #Ask for the size of the game_board minimum of 5
            size = int(input("Choose the size of the labyrinth: "))
            if size < 5:
                print("please choose a size larger than 4")
            else:
                break
        except ValueError:
            print("That is an invalid size.\nPlease choose a number larger than 4.")
    
    #Randomize tha starting position
    direction_x = randrange(1,size-1)
    direction_y = size-1
    #Build the reference game board with the chosen size
    game_board_ref = game_board_building.draw_reference_board(size,direction_x)
    #Build the game_board for the player
    game_board = draw_start_board(size, direction_x)
    #Draw the starting board for the player to see
    draw_board(game_board)
    
    #Print the instructions to play
    print("""You are the o.
Try to find your way out trough the labyrith.""")

    #The player chooses the direction to go and msvcrt recieves the input without Enter
    while True:
        #The direction attribute will change depending on the direction chosen
        #or the loop will break and the game will end if the player chooses Q
        print("Choose a direction (W = up, S = down, A = left, D = right)\
        \nOr quit the game by choosin Q")
        #depending on the direction chosen the location attributes are changed for the new location of the player
        direction = msvcrt.getch()
        if direction.lower() == b"w":
            direction_y -=1
        elif direction.lower() == b"s":
            direction_y +=1
        elif direction.lower() == b"a":
            direction_x -=1
        elif direction.lower() == b"d":
            direction_x +=1
        elif direction.lower() == b"q":
            print("You quit the game.")
            break
        else:
            print("This is not a valid input. Please try again")

        #Check the chosen direction with valid_directions and if it returns false a new direction is asked
        if valid_direction(game_board_ref,direction_x,direction_y) == True:
            #the location of the player is checked and if it is on the highest row then the game ends with a victory message
            #The is only one valid sopt to be on the highest row
            if direction_y == 0:
                #draw the pleyer with a victory pose in the end location
                game_board[direction_y][direction_x] = r"\o/"
                game_board[direction_y+1][direction_x] = r"   "
                draw_board(game_board)
                print("Congratulations! You found your way out!")
                break
            #inserts the player in it new location and draws the board for the player
            new_board = draw_location(game_board, game_board_ref, direction_x, direction_y, direction)
            draw_board(new_board)
        else:
            #If the direction was not valid the direction y and x are returnde to their previous values
            if direction.lower() == b"w":
                direction_y +=1
            elif direction.lower() == b"s":
                direction_y -=1
            elif direction.lower() == b"a":
                direction_x +=1
            elif direction.lower() == b"d":
                direction_x -=1
            #Draws the board again for the player to see
            draw_board(new_board)
            print("There is a wall in this direction, please choose another way.")

#Start the main loop
if __name__ == "__main__":
    main()