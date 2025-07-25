import sys

# == Exit Codes ==
DRAW = 0
WIN_P1 = 1
WIN_P2 = 2
INCOMPLETE = 3
ILLEGAL_CONTINUE = 4
ILLEGAL_ROW = 5
ILLEGAL_COLUMN = 6
ILLEGAL_GAME = 7
INVALID_FILE = 8
FILE_ERROR = 9


class Board:
    """Represents the game board for Connect-Z using a column-based structure."""


    def __init__(self, X, Y):
        """
        Initialize the board with X columns and Y rows.
        
        Args:
            X (int): Number of columns.
            Y (int): Number of rows.
        """
        self.X = X
        self.Y = Y
        self.board = [[] for _ in range(X)]

    def place_piece(self, col, player):
        """
        Place a player's piece in the specified column.

        Args:
            col (int): The column to place the piece in.
            player (int): The player number (1 or 2).

        Returns:
            int: The row index where the piece was placed.
        """
        self.board[col].append(player)
        return len(self.board[col]) - 1

    def check_win(self, col, row, player, Z):
        """
        Check if the current move results in a win.

        Args:
            col (int): Column of the last move.
            row (int): Row of the last move.
            player (int): Player number.
            Z (int): Number of pieces needed to win.

        Returns:
            bool: True if the move wins the game, False otherwise.
        """
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for dx, dy in directions:
            if self.__check_direction(col, row, dx, dy, player, Z):
                return True
        return False

    def __check_direction(self, x, y, dx, dy, player, Z):
        """
        Check one direction and its opposite for consecutive player pieces.

        Args:
            x (int): Starting column.
            y (int): Starting row.
            dx (int): Delta x direction.
            dy (int): Delta y direction.
            player (int): Player number.
            Z (int): Number of pieces needed to win.

        Returns:
            bool: True if enough consecutive pieces are found.
        """
        count = 1
        count += self.__count_direction(x, y, dx, dy, player)
        count += self.__count_direction(x, y, -dx, -dy, player)
        return count >= Z

    def __count_direction(self, x, y, dx, dy, player):
        """
        Count consecutive player pieces in one direction.

        Args:
            x (int): Starting column.
            y (int): Starting row.
            dx (int): Delta x direction.
            dy (int): Delta y direction.
            player (int): Player number.

        Returns:
            int: Number of consecutive pieces in the direction.
        """
        cx, cy = x + dx, y + dy
        count = 0
        while 0 <= cx < self.X and 0 <= cy < len(self.board[cx]):
            if self.board[cx][cy] != player: # dont check directions which aren't the players counters
                break
            count += 1
            cx += dx
            cy += dy
        return count

    def is_full(self):
        """
        Check if the board is full.

        Returns:
            bool: True if all columns are full, False otherwise.
        """
        return all(len(col) >= self.Y for col in self.board)


class Game:
    """Manages the game state and flow for Connect-Z."""

    def __init__(self, X, Y, Z):
        """
        Initialize the game with board size and win condition.

        Args:
            X (int): Number of columns.
            Y (int): Number of rows.
            Z (int): Number of pieces in a row to win.
        """
        self.board = Board(X, Y)
        self.Z = Z
        self.turn = 1 # begin with player 1
        self.winner = None 
        self.game_over = False

    def play_move(self, col):
        """
        Attempt to play a move in the specified column.

        Args:
            col (int): The column to drop the piece in.

        Returns:
            exit_code (int or None): Error code if invalid move, else None.
        """
        if self.game_over:
            return ILLEGAL_CONTINUE
        if not (0 <= col < self.board.X):
            return ILLEGAL_COLUMN
        if len(self.board.board[col]) >= self.board.Y:
            return ILLEGAL_ROW

        row = self.board.place_piece(col, self.turn)
        if self.board.check_win(col, row, self.turn, self.Z):
            self.game_over = True
            self.winner = WIN_P1 if self.turn == 1 else WIN_P2
        self.turn = 2 if self.turn == 1 else 1 # Alternate between player 1 and player 2
        return None

    def is_draw(self):
        """
        Check if the game ended in a draw.

        Returns:
            bool: True if the game is a draw, False otherwise.
        """
        return not self.game_over and self.board.is_full()


class ParseFile:
    """Parses and manages reading of the game file input."""

    def __init__(self, path):
        """
        Initialize parser with the path to the game file.

        Args:
            path (str): File path to the input file.
        """
        self.path = path
        self.file = None

    def get_config(self):
        """
        Read the first line and extract board configuration.

        Args:
            path (str): File path to the input file.

        Returns:
            tuple(int, int, int) or int: (X, Y, Z) if valid, else error code.
        """
        try:
            self.file = open(self.path, 'r')
            first_line = next(self.file).strip()
            X, Y, Z = map(int, first_line.split())
            if Z < 1 or Z > max(X, Y):
                self.file.close()
                return ILLEGAL_GAME
            if X <= 0 or Y <= 0 or Z <= 0:
                self.file.close()
                return ILLEGAL_GAME
        except:
            if self.file:
                self.file.close()
            return INVALID_FILE
        return X, Y, Z

    def next_line(self):
        """
        Read the next move from the file.

        Returns:
            int: Next move as integer, or INVALID_FILE if invalid.
        """
        try:
            move = next(self.file).strip()
            if not move.isdigit():
                raise ValueError
            return int(move)
        except (TypeError, ValueError, StopIteration): 
            raise

    def close(self):
        """Close the opened game file."""
        if self.file:
            self.file.close()
    

def process_game_file(path: str):
    parser = ParseFile(path)
    result = parser.get_config()
    if isinstance(result, int): # check the configuration format is correct
        return result
    X, Y, Z = result
    game = Game(X, Y, Z)

    try:
        while True:
            try:
                move = parser.next_line() - 1
            except StopIteration:
                break
            except:
                return INVALID_FILE

            exit_code = game.play_move(move)
            if exit_code is not None:
                return exit_code
            
        parser.close()

        if game.winner is not None:
            return game.winner
        if game.is_draw():
            return DRAW
        return INCOMPLETE

    except FileNotFoundError:
        return FILE_ERROR
    except Exception as e:
        print(f"Unexpected error, {e}, occured.")
        return INVALID_FILE
    

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("connectz.py: Provide one input file")
        sys.exit(0)

    print(process_game_file(sys.argv[1]))