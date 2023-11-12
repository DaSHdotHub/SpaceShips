# import pyfiglet module 
import pyfiglet
from colorama import Fore, Back, Style


result = pyfiglet.figlet_format("SpaceShips",font="shadow") 
print(Fore.RED + Back.GREEN + "\n" + "\n" + "\n" + result)
print(Style.RESET_ALL)
print("\n" + "Welcome to Spaceships, a variant of the classic BattleShip game")


