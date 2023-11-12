# import pyfiglet module 
import pyfiglet
#import colorama for color styling of the console
from colorama import Fore, Back, Style


def main():
    title = pyfiglet.figlet_format("SpaceShips",font="computer") 
    print(Fore.RED + Back.GREEN + "\n" + "\n" + "\n" + title)
    print(Style.RESET_ALL)
    print("\n" + "Welcome to Spaceships, a variant of the classic BattleShip game")
    
main()
    



