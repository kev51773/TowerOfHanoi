# Towers of Hanoi - Terminal Game

This project is a terminal-based implementation of the classic Towers of Hanoi puzzle, developed as a portfolio project for CS 101: Introduction to Programming.

## Description

The game allows users to play Towers of Hanoi directly in their terminal. It features:

* Interactive gameplay with keyboard input.
* Visual representation of the pegs and disks using `colorama`.
* Save and load functionality using `pickle`.
* Input validation to prevent illegal moves.
* Cross-platform input handling.
* A clean and user-friendly terminal interface.

## Prerequisites

Before running the game, ensure you have the following installed:

* Python 3.x
* `colorama` (`pip install colorama`)
* `pynput` (`pip install pynput`)

## Installation

1.  Clone the repository to your local machine:

    ```bash
    git clone [Your GitHub Repository Link]
    cd [Repository Directory]
    ```

2.  Install the required Python packages:

    ```bash
    pip install colorama pynput
    ```

## Usage

To run the game, execute the following command in your terminal:

```bash
python main.py


Follow the on-screen instructions to play.

Use 1, 2, and 3 keys to select pegs.
Use U to undo the last move.
Use L to load a saved game.
Use S to save the current game.
Use R to restart the game.
Use Q to quit the game.

File Structure
TowerOfHanoi/
├── main.py         # Main game file
├── README.md       # Project documentation
└── .toh_save       # Save file (created when saving)
