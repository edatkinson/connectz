# Connect-Z

## How it works:

1. **Parse Configuration:**
   - The first line of the input file should contain three integers: `X Y Z`
     - `X`: Number of columns
     - `Y`: Number of rows
     - `Z`: Number of consecutive pieces needed to win
   - These values are validated to ensure legality.

2. **Initialize Board:**
   - The board is represented column-wise using a list of stacks to mimic gravity-based piece drops.

3. **Stream Input Efficiently:**
   - Game moves (subsequent lines in the file) are read line-by-line.
   - This avoids memory blow-up on million+ line files.

4. **Move Validation:**
   - Each move is converted from 1-based to 0-based indexing.
   - The move is validated to ensure:
     - The game hasn't already ended.
     - The column exists.
     - The column isn’t already full.

5. **Gameplay Logic:**
   - The current player's piece is appended to the chosen column stack.
   - After each move, the game checks whether this move caused a win in one of four directions (horizontal, vertical, or two diagonals).
   - Symmetry is used to check both directions from the move's origin point.

6. **Endgame Scenarios:**
   - If a win is detected, an appropriate exit code is returned (`WIN_P1` or `WIN_P2`).
   - If all columns are full and no win, it's a draw (`DRAW`).
   - If the file ends before a result, it's considered incomplete (`INCOMPLETE`).

7. **Testing**
   - `Game()` class is set up to be compatible with unittests. The game can be simulated using the method .play_move(move: int), where the move is the integer which is supplied by the file. This is an example of why OOP is useful and beneficial. Some simple example tests are shown in `test_connectz.py`
  - Furthermore, modularity improves debugging time and readability. 
  

---

## Exit Codes

| Code | Meaning            |
|------|--------------------|
| 0    | DRAW               |
| 1    | WIN_P1             |
| 2    | WIN_P2             |
| 3    | INCOMPLETE         |
| 4    | ILLEGAL_CONTINUE   |
| 5    | ILLEGAL_ROW        |
| 6    | ILLEGAL_COLUMN     |
| 7    | ILLEGAL_GAME       |
| 8    | INVALID_FILE       |
| 9    | FILE_ERROR         |

---

## Usage

```bash
python connectz.py path/to/input.txt
```

---

## Development Setup

This project was built using Python 3.6 with conda:

```bash
conda create -n connectz python=3.6
conda activate connectz
```

or equally assuming python 3.6 is installed:

```bash 
python3.6 -m venv connectz
source connectz/bin/activate
```

---

## Design Notes

- **Board Representation:** A list of lists, where each sublist represents a column. This matches real-world gravity behavior in Connect Four-like games.
- **Efficiency:** Avoids loading the entire input file into memory.
- **Modularity:** Uses OOP to isolate parsing, game logic, and win-checking logic.

