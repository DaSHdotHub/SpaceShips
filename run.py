# Imports
import random
import string
import math
import pyfiglet
from colorama import Back, Fore, Style

# Constants
MAGENTA_CYAN_STYLE = Fore.CYAN + Style.BRIGHT + Back.MAGENTA
MAGENTA_WHITE_STYLE = Fore.WHITE + Style.BRIGHT + Back.MAGENTA
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


class SpaceShipsGame:
    """
    Initializes the SpaceShips game with specified battlefield size, number of ships, and username.

    Args:
        size (int): Size of the square battlefield (number of rows and columns).
        number_of_ships (int): Number of ships to be placed on the battlefield.
        username (str): Username of the player.

    Attributes:
        size (int): Size of the battlefield (both width and height).
        number_of_ships (int): Number of ships each player has.
        number_of_ship_segments (int): Total number of segments across all ships.
        user_battlefield (list of list): The user's battlefield grid.
        computer_battlefield (list of list): The computer's battlefield grid.
        username (str): The username of the player.
        user_turn_data (dict): Data about the user's current turn, including hits and attempts.
        computer_turn_data (dict): Data about the computer's current turn, including hits and attempts.
    """

    def __init__(self, size, number_of_ships, username):
        self.size = size
        self.number_of_ships = number_of_ships
        self.number_of_ship_segments = NUMBER_OF_DEFAULT_SHIP_SEGMENTS * number_of_ships
        self.user_battlefield = self.create_battlefield()
        self.computer_battlefield = self.create_battlefield()
        self.username = username
        self.user_turn_data = {
            "total_hits": 0,
            "previous_attempts": set(),
            "number_of_turns": 0,
        }
        self.computer_turn_data = {"total_hits": 0, "previous_attempts": set()}

        for _ in range(number_of_ships):
            self.place_spaceship(self.user_battlefield, GREEN_WHITE_STYLE)
            self.place_spaceship(self.computer_battlefield, RED_WHITE_STYLE)

    def create_battlefield(self):
        """
        Creates an empty battlefield of a given size, represented as a 2D list,
        with each cell initialized to an empty state

        Returns:
        list of lists: 2D list representing the empty battlefield
        """
        return [["| - " for _ in range(self.size)] for _ in range(self.size)]

    def place_spaceship(self, battlefield, style):
        """
        Places an 'L' shaped spaceship on the battlefield. Each spaceship occupies
        3 fields, with one central and side fields forming the 'L' shape. Function
        ensures that the spaceship does not overlap with existing ships and fits
        within the battlefield

        Args:
            battlefield (list of list): 2D list representing the battlefield
            style (str): Style string for coloring the spaceship
        """
        while True:
            # Create random coordinate for center of spaceship
            spaceship_center_row = random.randint(0, self.size - 1)
            spaceship_center_col = random.randint(0, self.size - 1)
            # Assign random orientation of spaceship, 4 orientations possible
            orientation = random.randint(1, 4)
            if (
                orientation == 1
                and spaceship_center_row < self.size - 1
                and spaceship_center_col < self.size - 1
            ):
                spaceship_coords = [
                    (spaceship_center_row, spaceship_center_col),
                    (spaceship_center_row + 1, spaceship_center_col),
                    (spaceship_center_row, spaceship_center_col + 1),
                ]
            elif (
                orientation == 2
                and spaceship_center_row < self.size - 1
                and spaceship_center_col > 0
            ):
                spaceship_coords = [
                    (spaceship_center_row, spaceship_center_col),
                    (spaceship_center_row + 1, spaceship_center_col),
                    (spaceship_center_row, spaceship_center_col - 1),
                ]
            elif (
                orientation == 3
                and spaceship_center_row > 0
                and spaceship_center_col > 0
            ):
                spaceship_coords = [
                    (spaceship_center_row, spaceship_center_col),
                    (spaceship_center_row - 1, spaceship_center_col),
                    (spaceship_center_row, spaceship_center_col - 1),
                ]
            elif (
                orientation == 4
                and spaceship_center_row > 0
                and spaceship_center_col < self.size - 1
            ):
                spaceship_coords = [
                    (spaceship_center_row, spaceship_center_col),
                    (spaceship_center_row - 1, spaceship_center_col),
                    (spaceship_center_row, spaceship_center_col + 1),
                ]
            else:
                continue
            # Check if spaceship_cords can be placed on battlefield
            if spaceship_coords and all(
                battlefield[row][column] == "| - " for row, column in spaceship_coords
            ):
                for row, column in spaceship_coords:
                    battlefield[row][column] = "|" + str(
                        style + " o " + Style.RESET_ALL
                    )
                break

    def fire_missile(self, battlefield, target, style):
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

    def turn_validated_input(self, battlefield, turn_data):
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
        while True:
            target_input = input("Enter target coordinates (e.g., A1): ").upper()
            if (
                len(target_input) < 2
                or not target_input[0].isalpha()
                or not target_input[1:].isdigit()
            ):
                print("Invalid format. Please enter coordinates like 'A1'.")
                continue

            row = int(target_input[1:]) - 1
            col = string.ascii_uppercase.index(target_input[0])

            if (
                row < 0
                or row >= len(battlefield)
                or col < 0
                or col >= len(battlefield[0])
            ):
                print(
                    "Target out of range. Please choose a target within the battlefield."
                )
                continue

            if (row, col) in turn_data["previous_attempts"]:
                print("Field already targeted. Choose another target.")
                continue

            turn_data["previous_attempts"].add((row, col))
            return row, col

    def computer_turn(self):
        """
        Manages the computer's turn in the game, randomly firing missiles at the user's battlefield.

        Returns:
            None: This function does not return a value but updates the battlefield
                and turn_data in-place.
        """
        missiles_fired = 0
        size = len(self.user_battlefield)
        while (
            missiles_fired < NUMBER_OF_MISSILES
            and self.computer_turn_data["total_hits"] < self.number_of_ship_segments
        ):
            row, col = random.randint(0, size - 1), random.randint(0, size - 1)
            if (row, col) in self.computer_turn_data["previous_attempts"]:
                continue

            self.computer_turn_data["previous_attempts"].add((row, col))
            result = self.fire_missile(
                self.user_battlefield, (row, col), RED_WHITE_STYLE
            )
            missiles_fired += 1
            if result == "hit":
                self.computer_turn_data["total_hits"] += 1
                if (
                    self.computer_turn_data["total_hits"]
                    == self.number_of_ship_segments
                ):
                    print("All your ships have been hit! Computer wins!")
                    break

    def user_turn(self):
        """
        Manages the user's turn in the game, allowing them to fire missiles until‚
        they run out of missiles or hit all spaceship segments.

        Returns:
            None: This function does not return a value but updates the battlefield
                and turn_data in-place.
        """
        missiles_fired = 0
        self.user_turn_data["number_of_turns"] += 1
        while (
            missiles_fired < NUMBER_OF_MISSILES
            and self.user_turn_data["total_hits"] < self.number_of_ship_segments
        ):
            row, col = self.turn_validated_input(
                self.computer_battlefield, self.user_turn_data
            )
            result = self.fire_missile(
                self.computer_battlefield, (row, col), GREEN_WHITE_STYLE
            )
            missiles_fired += 1
            if result == "hit":
                self.user_turn_data["total_hits"] += 1

            if self.user_turn_data["total_hits"] == self.number_of_ship_segments:
                print("All enemy ships have been hit!")
                break

    def print_battlefield(self, battlefield, style, hide_ships, name):
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
            "##" * (len(battlefield) - BATTLEFIELD_MIN_SIZE) * 2
            + "######################"
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

    def generate_turn_summary(self):
        """
        Generates and prints a summary of the attempts and hits for both the user and the computer.
        """

        def format_attempts(attempts):
            return ", ".join(
                [string.ascii_uppercase[col] + str(row + 1) for row, col in attempts]
            )

        user_attempts = format_attempts(self.user_turn_data["previous_attempts"])
        computer_attempts = format_attempts(
            self.computer_turn_data["previous_attempts"]
        )

        user_hits = sum(
            1
            for row, col in self.user_turn_data["previous_attempts"]
            if "x" in self.computer_battlefield[row][col]
        )
        computer_hits = sum(
            1
            for row, col in self.computer_turn_data["previous_attempts"]
            if "x" in self.user_battlefield[row][col]
        )

        print("\nTurn Summary:")
        print(f"User fired on fields {user_attempts}. Hits: {user_hits}.")
        print(f"Computer fired on fields {computer_attempts}. Hits: {computer_hits}.")

    def play_round(self):
        """
        Executes a single round of the game, which involves both the user's and computer's turns.
        The round starts with the user's turn, followed by the computer's turn, unless the user has
        already won the game. The battlefield status for both the user and computer is displayed.

        The round progresses as follows:
        - User's turn: User attempts to hit computer's ships.
        - Computer's turn: Computer attempts to hit user's ships (if user hasn't won yet).
        - Round is finished, a summary is printed.
        """
        self.print_battlefield(
            self.user_battlefield, BLUE_WHITE_STYLE, False, self.username
        )
        self.print_battlefield(
            self.computer_battlefield, RED_WHITE_STYLE, HIDE_COMPUTER_SHIPS, "Enemy"
        )
        print("\nUser's turn to fire!")
        self.user_turn()

        if self.user_turn_data["total_hits"] != self.number_of_ship_segments:
            print("\nComputer's turn to fire!")
            self.computer_turn()
        else:
            return

        self.generate_turn_summary()

    def check_winner(self):
        """
        Checks if there is a winner in the game based on the total hits recorded for each player.

        Returns:
            bool: Returns True if either the user or the computer has hit all segments of the opponent's
                  spaceships, indicating a win. Otherwise, returns False, indicating the game continues.
        """
        if self.user_turn_data["total_hits"] == self.number_of_ship_segments:
            print(
                f"\n\nCongratulations {self.username.upper()}! All enemy spacecraft destroyed. You win!"
            )
            return True
        elif self.computer_turn_data["total_hits"] == self.number_of_ship_segments:
            print("All your spacecraft destroyed. Computer wins!")
            return True
        return False

    def play_game(self):
        """_summary_"""
        while not self.check_winner():
            self.play_round()


def get_valid_username(style):
    """
    Prompts the user to enter a username that meets the length criteria

    The function continuously requests input until the user provides a username that meets
    the length requirements defined by USERNAME_LENGTH_FLOOR and USERNAME_LENGTH_CEIL.

    Args:
        style (str): Style string for coloring the output
    Returns:
        str: The validated username that meets the length requirements.
    """
    while True:
        username = input(
            style
            + "\n\nWhat your name captain?, enter a username with a length between"
            + f" {USERNAME_LENGTH_FLOOR} "
            + f"and {USERNAME_LENGTH_CEIL} chars:"
            + Style.RESET_ALL
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

                return size, number_of_ships
        except ValueError:
            print("Invalid input. Please enter a valid integer size.")


def display_rules(style, username):
    """
    Display an introduction and rules how the game should be played.

    Args:
        style (str): Style string for coloring the output
        username (str): Username of the player.

    Return:
        No return, outputs game information on the console.
    """
    L_SHIP = "\u255a"
    print(
        "\n\n"
        + style
        + "Welcome to SpaceShips, a variant of the classic BattleShip game."
        + f"\n\nCaptain {username} you'll be tasked to defend your SpaceShips crossing"
        ,"
        + f"\nenemy territory against the enemy forces. You're convoy are '{L_SHIP}'-class spaceships."
        + "\nMost likely youre enemy uses the same"
        + "\nThere will be also no intel on their orientation!"
        + "\nBe aware, the amount of SpaceShips rises with the size of the battlefield."
        + "\nPer round you'll have three attemps to disable enemy spaceships by"
        + "\nfiring missiles on the enemy battlefield, hit them before they do!"
        + "\n\nGOOD LUCK Captain!"
        + Style.RESET_ALL
        + "\n\n"
    )


def main():
    """
    The main function that initiates the game. It displays the game title, welcomes the player,
    and guides them through the process of setting up the game. This includes getting a valid username,
    determining the size of the battlefield, and initializing the game with these parameters.
    """
    title = pyfiglet.figlet_format("SpaceShips", font="computer")
    print(MAGENTA_CYAN_STYLE + "\n" + "\n" + "\n" + title + Style.RESET_ALL)

    play_again = True
    while play_again:
        username = get_valid_username(MAGENTA_WHITE_STYLE)
        display_rules(MAGENTA_WHITE_STYLE, username)
        size, number_of_ships = get_valid_game_size()
        game = SpaceShipsGame(size, number_of_ships, username)
        game.play_game()

        response = input("\nWould you like to play another round? (yes/no): ").lower()
        play_again = response == "yes"

        if play_again:
            print("\nStarting a new game...\n")
        else:
            print("\nThank you for playing! See you next time.\n")


main()
