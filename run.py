import random
import string
import math
import pyfiglet
from colorama import Back, Fore, Style

BLUE_WHITE_STYLE = Fore.WHITE + Back.BLUE
RED_WHITE_STYLE = Fore.WHITE + Back.RED
GREEN_WHITE_STYLE = Fore.WHITE + Back.GREEN
NUMBER_OF_DEFAULT_SHIPS = 3
NUMBER_OF_MISSILES = NUMBER_OF_DEFAULT_SHIPS
NUMBER_OF_DEFAULT_SHIP_SEGMENTS = 3
BATTLEFIELD_MIN_SIZE = 4
BATTLEFIELD_MAX_SIZE = 10
HIDE_COMPUTER_SHIPS = True
USERNAME_LENGTH_FLOOR = 3
USERNAME_LENGTH_CEIL = 8


def fire_missile(battlefield, target, style):
    """
    Marks a field on the battlefield as hit or miss when a missile is fired.

    Args:
        battlefield (list of list): 2D list representing the battlefield.
        target (tuple of int): Coordinates (row, col) of the missile impact.
        style (str): Style string for coloring the hit marker.

    Returns:
        str: Returns 'hit' if a spaceship was hit, otherwise 'miss'.
    """
    row, col = target

    if "o" in battlefield[row][col]:
        battlefield[row][col] = "|" + str(style + " x " + Style.RESET_ALL)
        return "hit"
    else:
        battlefield[row][col] = "| * "
        return "miss"


def turn_validated_input(battlefield, turn_data):
    """
    Continuously prompts the user for target coordinates until valid and untargeted
    coordinates are given. Also updates the turn data with the new attempt.

    Args:
        battlefield (list of list): 2D list representing the battlefield.
        turn_data (dict): Dictionary containing data about the current turn,
                          including previously attempted targets.

    Returns:
        tuple: Validated target coordinates (row, col).
    """
    row, col = None, None
    while row is None or col is None:
        target_input = input("Enter target coordinates (e.g., A1): ").upper()
        if (
            len(target_input) < 2
            or not target_input[0].isalpha()
            or not target_input[1:].isdigit()
        ):
            print("Invalid format. Please enter coordinates like 'A1'.")
            row, col = None, None
            continue

        row = int(target_input[1:]) - 1
        col = string.ascii_uppercase.index(target_input[0])

        if row < 0 or row >= len(battlefield) or col < 0 or col >= len(battlefield[0]):
            print("Target out of range. Please choose a target within the battlefield.")
            row, col = None, None
            continue

        if (row, col) in turn_data["previous_attempts"]:
            print("Field already targeted. Choose another target.")
            row, col = None, None
            continue

    turn_data["previous_attempts"].add((row, col))
    return (row, col)


def computer_turn(battlefield, computer_turn_data, number_of_ship_segments):
    """
    Manages the computer's turn in the game, randomly firing missiles at the user's battlefield.

    Args:
        battlefield (list of list): 2D list representing the user's battlefield.
        turn_data (dict): Dictionary containing data about the computer's current turn,
                          including total hits and previous attempts.

    Returns:
        None: This function does not return a value but updates the battlefield
              and turn_data in-place.
    """
    missiles_fired = 0
    size = len(battlefield)
    while (
        missiles_fired < NUMBER_OF_MISSILES
        and computer_turn_data["total_hits"] < number_of_ship_segments
    ):
        row, col = random.randint(0, size - 1), random.randint(0, size - 1)
        if (row, col) in computer_turn_data["previous_attempts"]:
            continue

        computer_turn_data["previous_attempts"].add((row, col))
        result = fire_missile(battlefield, (row, col), RED_WHITE_STYLE)
        missiles_fired += 1
        if result == "hit":
            computer_turn_data["total_hits"] += 1
            if computer_turn_data["total_hits"] == number_of_ship_segments:
                print("All your ships have been hit! Computer wins!")
                break


def user_turn(battlefield, turn_data, number_of_ship_segments):
    """
    Manages the user's turn in the game, allowing them to fire missiles until‚
    they run out of missiles or hit all spaceship segments.

    Args:
        battlefield (list of list): 2D list representing the enemy's battlefield.
        turn_data (dict): Dictionary containing data about the current turn,
                          including total hits and previous attempts.

    Returns:
        None: This function does not return a value but updates the battlefield
              and turn_data in-place.
    """
    missiles_fired = 0
    turn_data["number_of_turns"] += 1
    while (
        missiles_fired < NUMBER_OF_MISSILES
        and turn_data["total_hits"] < number_of_ship_segments
    ):
        row, col = turn_validated_input(battlefield, turn_data)
        result = fire_missile(battlefield, (row, col), GREEN_WHITE_STYLE)
        missiles_fired += 1
        if result == "hit":
            turn_data["total_hits"] += 1

        if turn_data["total_hits"] == number_of_ship_segments:
            print("All enemy ships have been hit!")
            break


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
        # Create random coordinate for center of spaceship
        spaceship_center_row = random.randint(0, size - 1)
        spaceship_center_col = random.randint(0, size - 1)
        # Assign random orientation of spaceship, 4 orientations possible
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
        # Check if spaceship_cords can be placed on battlefield
        if all(battlefield[row][column] == "| - " for row, column in spaceship_coords):
            for row, column in spaceship_coords:
                battlefield[row][column] = "|" + str(style + " o " + Style.RESET_ALL)
            break


def setup_battlefields(size, number_of_ships):
    """
    Initializes battlefields for user and computer with randomly placed spaceships
    Each battlefield is represented as a 2D list,

    Args:
        size (int): Size of the battlefield.
        numberOfShips (int): Amount of spaceships placed on battlefield

    Returns:
        tuple: Tuple containing the user's and the computer's battlefields
    """
    user_battlefield = create_battlefield(size)
    computer_battlefield = create_battlefield(size)

    for _ in range(number_of_ships):
        place_spaceship(user_battlefield, size, GREEN_WHITE_STYLE)
        place_spaceship(computer_battlefield, size, RED_WHITE_STYLE)

    return user_battlefield, computer_battlefield


def get_valid_username():
    """
    Prompts the user to enter a username that meets the length criteria

    The function continuously requests input until the user provides a username that meets
    the length requirements defined by USERNAME_LENGTH_FLOOR and USERNAME_LENGTH_CEIL.

    Returns:
        str: The validated username that meets the length requirements.
    """
    while True:
        username = input(
            f"Enter your chosen username, length between {USERNAME_LENGTH_FLOOR} "
            + f"and {USERNAME_LENGTH_CEIL} chars: "
        )
        if (
            len(username) < USERNAME_LENGTH_FLOOR
            or len(username) > USERNAME_LENGTH_CEIL
        ):
            print("Your username does not meet the length requirement")
        else:
            return username


def get_valid_game_size():
    """
    Prompts user to enter a valid battlefield size, must be within a specified range
    Continuously asks for input until a valid size is entered

    Returns:
        int: The validated size of the battlefield entered by the user
        int: Number of spaceships participating for each player
        int: Number of ship segments based on the number of spaceships.
    """
    while True:
        try:
            size = int(
                input(
                    f"Enter the size of the battlefield, size should be between "
                    f"{BATTLEFIELD_MIN_SIZE} and {BATTLEFIELD_MAX_SIZE}: "
                )
            )
            if size < BATTLEFIELD_MIN_SIZE or size > BATTLEFIELD_MAX_SIZE:
                print(
                    f"Invalid input, please enter a number value between"
                    f"{BATTLEFIELD_MIN_SIZE} and {BATTLEFIELD_MAX_SIZE}."
                )
            else:
                number_of_ships = size - (
                    BATTLEFIELD_MIN_SIZE - NUMBER_OF_DEFAULT_SHIPS
                )
                number_of_ship_segments = (
                    NUMBER_OF_DEFAULT_SHIP_SEGMENTS * number_of_ships
                )
                return size, number_of_ships, number_of_ship_segments
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


def print_battlefield(battlefield, style, hide_ships, name):
    """
    Prints the current state of the battlefield, displayed with
    row and column indicators, each cell shows its current state

    Args:
        battlefield (list of list): 2D list representing the battlefield
        style (str): Style string for coloring the output
        hide_ships (boolean): Bool to hide ships
        name (str): Display name above battlefield grid
    """
    bname = style + f"{name.upper()} BATTLEFIELD" + Style.RESET_ALL
    b_topdown = (
        "##" * (len(battlefield) - BATTLEFIELD_MIN_SIZE) * 2 + "######################"
    )
    b_left = "#" * math.ceil((len(b_topdown) - len(name + " battlefield")) / 2)
    b_right = "#" * math.floor((len(b_topdown) - len(name + " battlefield")) / 2)

    print("\n" + b_topdown + "\n" + b_left + bname + b_right + "\n" + b_topdown)
    top_indices = (
        "   || " + " | ".join(string.ascii_uppercase[: len(battlefield)]) + " ||"
    )
    print(style + top_indices + Style.RESET_ALL)

    for i, row in enumerate(battlefield):
        print(style + f"{i + 1:2d}", end=" " + Style.RESET_ALL + "|")
        for cell in row:
            if hide_ships and "o" in cell:
                print("| - ", end="")
            else:
                print(cell, end="")
        print("||")


def main():
    """
    Main function to run the SpaceShips game. It sets up the game, creates the battlefields,
    and manages the game flow.
    """
    title = pyfiglet.figlet_format("SpaceShips", font="computer")
    print(BLUE_WHITE_STYLE + "\n" + "\n" + "\n" + title + Style.RESET_ALL)
    print(
        "\n" + "\n" + "Welcome to Spaceships, a variant of the classic BattleShip game"
    )
    username = get_valid_username()
    size, number_of_ships, number_of_ship_segments = get_valid_game_size()

    user_battlefield, computer_battlefield = setup_battlefields(size, number_of_ships)
    print_battlefield(user_battlefield, BLUE_WHITE_STYLE, False, username)

    print_battlefield(
        computer_battlefield, RED_WHITE_STYLE, HIDE_COMPUTER_SHIPS, "Enemy"
    )

    user_turn_data = {"total_hits": 0, "previous_attempts": set(), "number_of_turns": 0}
    computer_turn_data = {"total_hits": 0, "previous_attempts": set()}

    while (
        user_turn_data["total_hits"] < number_of_ship_segments
        and computer_turn_data["total_hits"] < number_of_ship_segments
    ):
        print("\nUser's turn to fire!")
        user_turn(computer_battlefield, user_turn_data, number_of_ship_segments)

        print("\nComputer's turn to fire!")
        computer_turn(user_battlefield, computer_turn_data, number_of_ship_segments)

        print_battlefield(user_battlefield, BLUE_WHITE_STYLE, False, "User")
        print_battlefield(
            computer_battlefield, RED_WHITE_STYLE, HIDE_COMPUTER_SHIPS, "Enemy"
        )

        if user_turn_data["total_hits"] == number_of_ship_segments:
            print(
                "\n"
                + "\n"
                + f"Congratulations {username.upper()}"
                + "\n"
                + "All enemy spacecraft destroyed. You win!"
            )
            break
        elif computer_turn_data["total_hits"] == number_of_ship_segments:
            print("All your spacecraft destroyed. Computer wins!")
            break


main()
