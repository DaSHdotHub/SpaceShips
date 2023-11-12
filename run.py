# import pyfiglet module 
import pyfiglet
#import colorama for color styling of the console
from colorama import Fore, Back, Style


def create_battlefield(size):
    return [['~' for _ in range(size)] for _ in range(size)]


def print_battlefield(battlefield):
    for row in battlefield:
        print(" ".join(row))


def main():
    title = pyfiglet.figlet_format("SpaceShips",font="computer") 
    print(Fore.RED + Back.GREEN + "\n" + "\n" + "\n" + title)
    print(Style.RESET_ALL)
    print("\n" + "Welcome to Spaceships, a variant of the classic BattleShip game")
    size = int(input("Enter the size of the battlefield: "))
    battlefield = create_battlefield(size)
    print_battlefield(battlefield)
main()
    