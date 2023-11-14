import random
import string

import pyfiglet
from colorama import Back, Fore, Style

BLUE_WHITE_STYLE = Fore.WHITE + Back.BLUE
RED_WHITE_STYLE = Fore.WHITE + Back.RED
GREEN_WHITE_STYLE = Fore.WHITE + Back.GREEN
NUMBER_OF_SHIPS = 3
NUMBER_OF_MISSILES = NUMBER_OF_SHIPS
BATTLEFIELD_MIN_SIZE = 4
BATTLEFIELD_MAX_SIZE = 10
HIDE_COMPUTER_SHIPS = True


def fire_missile(battlefield, target):
    """
    Marks a field on the battlefield if hitted by a missile

    Args:
        battlefield (list of list): 2D list representing the battlefield
        target (list of int): Coordination of 'missile impact'

    Returns:
        Bool: Returns if spaceship was hitted
    """
    row, col = target
    if 'o' in battlefield[row][col]:
        battlefield[row][col] = "| x "
        return True
    else:
        print("Miss!")
        return False


def user_turn(battlefield):
    hits = 0
    for _ in range(NUMBER_OF_MISSILES):
        target = input("Enter target coordinates (e.g., A1): ").upper()
        row = int(target[1:]) - 1
        col = string.ascii_uppercase.index(target[0])
        if fire_missile(battlefield, (row, col)):
            hits += 1
    return hits


def place_spaceship(battlefield, size, style):
    """
    Places an 'L' shaped spaceship on the battlefield. Each spaceship occupies
    3 fields, with one central and side fields forming the 'L' shape. Function
    ensures that the spaceship does not overlap with existing ships and fits
    within the battlefield

    Args:
        battlefield (list of list): 2D list representing the battlefield
        size (int): Size of the battlefield (number of rows and columns)
        style (str): Style string for coloring the spaceship
    """
    while True:
        "# Create random coordinate for center of spaceship"
        spaceship_center_row = random.randint(0, size - 1)
        spaceship_center_col = random.randint(0, size - 1)
        "# Assign random orientation of spaceship, 4 orientations possible"
        orientation = random.randint(1, 4)
        if (
            orientation == 1
            and spaceship_center_row < size - 1
            and spaceship_center_col < size - 1
        ):
            spaceship_coords = [
                (spaceship_center_row, spaceship_center_col),
                (spaceship_center_row + 1, spaceship_center_col),
                (spaceship_center_row, spaceship_center_col + 1),
            ]
        elif (
            orientation == 2
            and spaceship_center_row < size - 1
            and spaceship_center_col > 0
        ):
            spaceship_coords = [
                (spaceship_center_row, spaceship_center_col),
                (spaceship_center_row + 1, spaceship_center_col),
                (spaceship_center_row, spaceship_center_col - 1),
            ]
        elif orientation == 3 and spaceship_center_row > 0 and spaceship_center_col > 0:
            spaceship_coords = [
                (spaceship_center_row, spaceship_center_col),
                (spaceship_center_row - 1, spaceship_center_col),
                (spaceship_center_row, spaceship_center_col - 1),
            ]
        elif (
            orientation == 4
            and spaceship_center_row > 0
            and spaceship_center_col < size - 1
        ):
            spaceship_coords = [
                (spaceship_center_row, spaceship_center_col),
                (spaceship_center_row - 1, spaceship_center_col),
                (spaceship_center_row, spaceship_center_col + 1),
            ]
        else:
            continue
        "# Check if spaceship_cords can be placed on battlefield"
        if all(battlefield[row][column] == "| - " for row, column in spaceship_coords):
            for row, column in spaceship_coords:
                battlefield[row][column] = "|" + str(style + " o " + Style.RESET_ALL)
            break


def setup_battlefields(size, numberOfShips):
    """
    Initializes battlefields for user and computer with randomly placed spaceships
    Each battlefield is represented as a 2D list,

    Args:
        size (int): Size of the battlefield.
        numberOfShips (int): Amount of spaceships placed on battlefield

    Returns:
        tuple: Tuple containing two lists of lists, representing the user's and the computer's battlefields
    """
    user_battlefield = create_battlefield(size)
    computer_battlefield = create_battlefield(size)

    for _ in range(numberOfShips):
        place_spaceship(user_battlefield, size, GREEN_WHITE_STYLE)
        place_spaceship(computer_battlefield, size, RED_WHITE_STYLE)

    return user_battlefield, computer_battlefield


def get_valid_battlefield_size():
    """
    Prompts user to enter a valid battlefield size, must be within a specified range
    Continuously asks for input until a valid size is entered

    Returns:
        int: The validated size of the battlefield entered by the user
    """
    while True:
        try:
            size = int(
                input(
                    f"Enter the size of the battlefield, size should be between {BATTLEFIELD_MIN_SIZE} and {BATTLEFIELD_MAX_SIZE}: "
                )
            )
            if size < BATTLEFIELD_MIN_SIZE or size > BATTLEFIELD_MAX_SIZE:
                print(
                    f"Invalid input, please enter a number value between {BATTLEFIELD_MIN_SIZE} and {BATTLEFIELD_MAX_SIZE}."
                )
            else:
                return size
        except ValueError:
            print("Invalid input. Please enter a valid integer size.")


def create_battlefield(size):
    """
    Creates an empty battlefield of a given size, represented as a 2D list,
    with each cell initialized to an empty state

    Args:
        size (int): Size of the battlefield (number of rows and columns)

    Returns:
        list of lists: 2D list representing the empty battlefield
    """
    return [["| - " for _ in range(size)] for _ in range(size)]


def print_battlefield(battlefield, style, hide_ships):
    """
    Prints the current state of the battlefield, displayed with
    row and column indicators, each cell shows its current state

    Args:
        battlefield (list of list): 2D list representing the battlefield
        style (str): Style string for coloring the output
        hide_ships (boolean): Bool to hide ships
    """
    top_indices = (
        "   || " + " | ".join(string.ascii_uppercase[: len(battlefield)]) + " ||"
    )
    print(style + top_indices + Style.RESET_ALL)

    for i, row in enumerate(battlefield):
        print(style + f"{i + 1:2d}", end=" " + Style.RESET_ALL + "|")
        for cell in row:
            if hide_ships and 'o' in cell:
                print("| - ", end="")
            else:
                print(cell, end="")
        print("||")

def main():
    """
    Main function to run the Spaceships game. It sets up the game, creates the battlefields,
    and manages the game flow.
    """
    title = pyfiglet.figlet_format("SpaceShips", font="computer")
    print(BLUE_WHITE_STYLE + "\n" + "\n" + "\n" + title + Style.RESET_ALL)
    print(
        "\n" + "\n" + "Welcome to Spaceships, a variant of the classic BattleShip game"
    )
    size = get_valid_battlefield_size()

    user_battlefield, computer_battlefield = setup_battlefields(size, NUMBER_OF_SHIPS)

    print("\n" + "Your battlefield")
    print_battlefield(user_battlefield, BLUE_WHITE_STYLE, False)

    print("\n" + "Enemy battlefield")
    print_battlefield(computer_battlefield, RED_WHITE_STYLE, HIDE_COMPUTER_SHIPS)
    
    print("\nUser's turn to fire!")
    user_hits = user_turn(computer_battlefield)
    print(f"\nResults:\nUser hits: {user_hits}")



main()
