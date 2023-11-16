# SpaceShips Game

## Introduction
SpaceShips is a variant of the classic "Battleship" game where players aim to destroy enemy ships by guessing their locations. The objective is to defend spaceships while attempting to disable enemy ships by firing missiles.

![Responsive Mock](assets/media/responsive.webp)

## Table of Contents

- [Introduction](#introduction)
- [Technologies and Libraries Used](#technologies-and-libraries-used)
  - [Python Standard Libraries](#python-standard-libraries)
  - [External Libraries](#external-libraries)
- [Key Features and Algorithms](#key-features-and-algorithms)
- [Project Structure](#project-structure)
- [Unique Aspects to Highlight](#unique-aspects-to-highlight)

## Technologies and Libraries Used
### Python Standard Libraries
- `random`: For generating random numbers (ship placement, computer's moves).
- `string`: Handling strings, particularly for battlefield coordinates.
- `math`: Used for mathematical operations in print formatting.

### External Libraries
- `pyfiglet`: Creating ASCII art titles.
- `colorama`: Adding color and styles to the console output.

## Key Features and Algorithms
- **SpaceShip Class**: Manages the game state, including battlefield setup, ship placement, and turn management.
- **Ship Placement Algorithm**: Places 'L'-shaped ships randomly, ensuring they fit and don't overlap.
- **Missile Firing Logic**: Marks hits or misses on the battlefield.
- **User Input Validation**: Ensures valid targeting and username creation inputs.
- **Turn-Based Gameplay**: Alternates turns between the user and the computer.

## Project Structure
- **Constants and Styles**: Defined for easy modification (number of ships, color styles).
- **Class `SpaceShipsGame`**: Core of the game with methods for gameplay.
- **Utility Functions**: `get_valid_username`, `get_valid_game_size`, `display_rules` for game setup.
- **Main Function**: Orchestrates game setup and play loop.

## Unique Aspects to Highlight
- **ASCII Art and Colorful Console Output**: Enhances the user experience.
- **Adaptive Game Size and Number of Ships**: Dynamically adjusts based on battlefield size.
- **Customizable Styles**: Uses `colorama` for easy aesthetic customization.

## Deployment
- **Heroku**: For deployment it is needed to add two buildpacks from the _Settings_ tab.
    1. `heroku/python`
    2. `heroku/nodejs`
    __________________
    For deployment it is also needed to create the _Config Var_ called `PORT`. Set this to `8000`
    __________________
    For this repository, no credentials were used so far, in case thouse will be added in the future it is necesarry to create in Heroku a _Config Var_ called `CREDS` and paste the JSON into the value field.
    __________________
    After e.g. the GitHub repository was connected and the correct repo was chosen it can be deployed as normal.

## Constraints

The deployment terminal is set to 80 columns by 24 rows. That means that each line of text needs to be 80 characters or less otherwise it will be wrapped onto a second line.

## Credits

- **The deployment** process was taken from the template linked in this github-repo.

- **Figlet** were used for Creating ASCII art titles [click here fore examples on figlet.org](http://www.figlet.org/examples.html)

- **Pyfiglet** for easier figlet integration - "pyfiglet" import was used, find more information on [geeksforgeeks.org](https://www.geeksforgeeks.org/python-ascii-art-using-pyfiglet-module/)
- **Colorama** for bringing more than black and white to the console, have a look at [geeksforgeeks.org](https://www.geeksforgeeks.org/print-colors-python-terminal/)
- **ui.dev** for the responsive mock for this documentation, try it on [ui.dev/amiresponsive?](https://ui.dev/amiresponsive?)
