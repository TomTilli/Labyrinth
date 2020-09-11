#Build the reference board for the correct layout
game_board_ref = [
    [" x "," x "," x "," x " ," x "," x "," x ","   "," x "," x "],
    [" x "," x "," x ","   ","   ","   ","   ","   "," x "," x "],
    [" x ","   ","   ","   "," x ","   "," x "," x "," x "," x "],
    [" x ","   "," x ","   "," x "," x "," x ","   ","   "," x "],
    [" x ","   "," x ","   "," x "," x "," x ","   "," x "," x "],
    [" x ","   "," x ","   ","   ","   ","   ","   "," x "," x "],
    [" x ","   "," x "," x "," x "," x "," x ","   "," x "," x "],
    [" x "," x ","   ","   ","   "," x "," x ","   "," x "," x "],
    [" x "," x ","   "," x ","   ","   ","   ","   "," x "," x "],
    [" x "," x ","   "," x "," x "," x "," x "," x "," x "," x "]]

#Build an empty board for the player
game_board = []
for i in range(10):
    game_board.append([])

#Starting posisition for the player in x y coordinates
start_x = 2
start_y = 9

def draw_on_board(loc_x:int,loc_y:int):
    """adds the current location of the player to the game_board reference list as an element " o "

    Args:
        loc_x (int): The x value on the game board (0-9) of the players current position
        loc_y (int): The y value on the game board (0-9) of the players current position
    """
    try:
        game_board[loc_y][loc_x] = game_board_ref[loc_y][loc_x]
    except IndexError:
        pass


def draw_board(loc_x:int, loc_y:int):
    """Draws the game_board list as a board for a visual representation of the current state of game.

    Args:
        loc_x (int): The x value on the game board (0-9) of the players current position
        loc_y (int): The y value on the game board (0-9) of the players current position
    """
    for i in range(10):
        for k in range(10):
            if i == 0:
                    game_board[i].append(" x ")
            elif i == 9:
                if k == 2:
                    game_board[i].append("   ")
                else:
                    game_board[i].append(" x ")
            else:
                if k == 0 or k == 9:
                    game_board[i].append(" x ")
                else:
                    game_board[i].append("   ")

    if game_board_ref[loc_y][loc_x] != " x ":
            game_board[loc_y][loc_x] = " o "
            draw_on_board(loc_x,loc_y - 1) #pohjonen
            draw_on_board(loc_x,loc_y + 1) #etelä
            draw_on_board(loc_x + 1,loc_y) #itä
            draw_on_board(loc_x - 1,loc_y) #länsi
    
        
    else:
        print("seinä")

    for i in range(10):
        for k in range(10):
            print(game_board[i][k],end="")
        print("")

def valid_direction(loc_x, loc_y)->bool:
    """Check if the position is out of bounds or on an element containing " x ".

    Args:
        loc_x (int): The x value on the game board (0-9)
        loc_y (int): The y value on the game board (0-9)

    Returns:
        bool: returns True if the locasion is valid and False if the location is invalid (Index out of bounds or element "x")
    """
    try:
        if game_board_ref[loc_y][loc_x] == " x ":
            return False
        else:
            return True
    except IndexError:
        return False

#The main game loop
def main():
    draw_board(start_x,start_y)
    direction_x = start_x
    direction_y = start_y
    print("""You are the o in the labyrinth
Try to find your way out.""")
    while True:
        direction = input("Choose a direction (W = up, S = down, A = left, D = right)\
        \nOr quit the game by choosin Q\n:")
        if direction.lower() == "w":
            direction_y -=1
        elif direction.lower() == "s":
            direction_y +=1
        elif direction.lower() == "a":
            direction_x -=1
        elif direction.lower() == "d":
            direction_x +=1
        elif direction.lower() == "q":
            print("You quit the game.")
            break
        else:
            print("This is not a valid input. Please try again")

        if valid_direction(direction_x,direction_y) == True:
            if direction_x == 7 and direction_y == 0:
                print("Congratulations! You found your way out!")
                break
            draw_board(direction_x,direction_y)
        else:
            if direction.lower() == "w":
                direction_y +=1
            elif direction.lower() == "s":
                direction_y -=1
            elif direction.lower() == "a":
                direction_x +=1
            elif direction.lower() == "d":
                direction_x -=1
            print("There is a wall in this direction, please choose another way.")

if __name__ == "__main__":
    main()
