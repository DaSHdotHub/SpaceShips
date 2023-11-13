# import pyfiglet module 
import string
import pyfiglet
#import colorama for color styling of the console
from colorama import Fore, Back, Style

BLUE_WHITE_STYLE = Fore.WHITE + Back.BLUE

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
        list of list: A 2D list representing the battlefield.
    """
    return [['| -' for _ in range(size)] for _ in range(size)]


def print_battlefield(battlefield):
    """
    Print the state of the battlefield.

    Args:
        battlefield (list of list): The 2D list representing the battlefield.
    """
    top_indices = '   || ' + ' | '.join(string.ascii_uppercase[:len(battlefield)]) + ' |'
    print(BLUE_WHITE_STYLE + top_indices + Style.RESET_ALL)
    
    for i, row in enumerate(battlefield):
        print(BLUE_WHITE_STYLE + f"{i + 1:2d}", end=' ' + Style.RESET_ALL + '|')
        print(" ".join(row) + ' |')


def main():
    title = pyfiglet.figlet_format("SpaceShips",font="computer") 
    print(BLUE_WHITE_STYLE + "\n" + "\n" + "\n" + title + Style.RESET_ALL)
    print("\n" + "\n" + "Welcome to Spaceships, a variant of the classic BattleShip game")
    size = get_valid_battlefield_size()
    battlefield = create_battlefield(size)
    print_battlefield(battlefield)
    
    
main()
    