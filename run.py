# import pyfiglet module 
import string
import random
import pyfiglet
#import colorama for color styling of the console
from colorama import Fore, Back, Style

BLUE_WHITE_STYLE = Fore.WHITE + Back.BLUE
RED_WHITE_STYLE = Fore.WHITE + Back.RED
GREEN_WHITE_STYLE = Fore.WHITE + Back.GREEN

def place_spaceship(battlefield, size, style):
    """
    Creates 'L' shaped spaceships and places them on the existing battlefield, 
    A Spaceship takes up 3 fields, 1 for the center and 1 for each wing.
    
    Args:
        size (int): The length and width of the battlefield.
        battlefield (list): list of lists: A 2D list representing the battlefield.

        
    """
    while True:
        # Create random coordinate for center of spaceship
        spaceship_center_row = random.randint(1, size - 1)
        spaceship_center_col = random.randint(1, size - 1)
        
        # Assign random orientation of spaceship, there can be 4 orientation of L shaped ship
        orientation = random.randint(1,4)
        ##for debug
        print('row ' + str(spaceship_center_row) + '  col ' + str(spaceship_center_col) + '  orient. ' + str(orientation) + '  size ' + str(size))
        #Orientation 1: wing down, wing right
        if orientation == 1 and spaceship_center_row < size - 1 and spaceship_center_col < size - 2:
            spaceship_coords = [(spaceship_center_row,      spaceship_center_col),
                                (spaceship_center_row + 1,  spaceship_center_col),
                                (spaceship_center_row,      spaceship_center_col + 1)]
        #Orientation 2: wing down, wing left
        elif orientation == 2 and spaceship_center_row < size - 1 and (spaceship_center_col < size - 1 and spaceship_center_col > 1):
            spaceship_coords = [(spaceship_center_row,      spaceship_center_col),
                                (spaceship_center_row + 1,  spaceship_center_col),
                                (spaceship_center_row,      spaceship_center_col - 1)]
        #Orientation 3: wing up, wing left
        elif orientation == 3 and (spaceship_center_row < size - 1 and spaceship_center_row > 1) and (spaceship_center_col < size - 1 and spaceship_center_col > 1):
            spaceship_coords = [(spaceship_center_row,      spaceship_center_col),
                                (spaceship_center_row - 1,  spaceship_center_col),
                                (spaceship_center_row,      spaceship_center_col - 1)]
        #Orientation 4: wing up, wing right
        elif orientation == 4 and (spaceship_center_row < size - 1 and spaceship_center_row > 1) and spaceship_center_col < size - 1:
            spaceship_coords = [(spaceship_center_row,      spaceship_center_col),
                                (spaceship_center_row - 1,  spaceship_center_col),
                                (spaceship_center_row,      spaceship_center_col + 1)]
        #Repick and craete new random coords
        else:
            continue
        
        # Check if spaceship_cords can be placed on battlefield
        if all(battlefield[row][column] == '| - ' for row, column in spaceship_coords):
            for row, column in spaceship_coords:
                battlefield[row][column] = '|' + str(style + ' o ' + Style.RESET_ALL)
            break
        
        
    

def get_valid_battlefield_size():
    """
    Prompt the user for a valid battlefield size within the specified range.

    Returns:
        int: The valid battlefield size.
    """
    while True:
        try:
            size = int(input("Enter the size of the battlefield, size should be between 5 and 10: "))
            if size < 5 or size > 10:
                print("Invalid input, please enter a number value between 5 and 10.")
            else:
                return size
        except ValueError:
            print("Invalid input. Please enter a valid integer size.")



def create_battlefield(size):
    """
    Create a battlefield of a given size filled with empty space ' - '.

    Args:
        size (int): The length and width of the battlefield.

    Returns:
        list of lists: A 2D list representing the battlefield.
    """
    return [['| - ' for _ in range(size)] for _ in range(size)]


def print_battlefield(battlefield, style):
    """
    Print the state of the battlefield.

    Args:
        battlefield (list of list): The 2D list representing the battlefield.
    """
    top_indices = '   || ' + ' | '.join(string.ascii_uppercase[:len(battlefield)]) + ' ||'
    print(style + top_indices + Style.RESET_ALL)
    
    for i, row in enumerate(battlefield):
        print(style + f"{i + 1:2d}", end=' ' + Style.RESET_ALL + '|')
        print(''.join(row) + '||')


def main():
    title = pyfiglet.figlet_format("SpaceShips",font="computer") 
    print(BLUE_WHITE_STYLE + "\n" + "\n" + "\n" + title + Style.RESET_ALL)
    print("\n" + "\n" + "Welcome to Spaceships, a variant of the classic BattleShip game")
    size = get_valid_battlefield_size()
    
    print('\n' + 'Your battlefield')
    battlefield = create_battlefield(size)
    place_spaceship(battlefield, size, GREEN_WHITE_STYLE)
    print_battlefield(battlefield, BLUE_WHITE_STYLE)
    
    print('\n' + 'Enemy battlefield')
    computer_battlefield = create_battlefield(size)
    place_spaceship(computer_battlefield, size, RED_WHITE_STYLE)
    print_battlefield(computer_battlefield, RED_WHITE_STYLE)

    
main()
    