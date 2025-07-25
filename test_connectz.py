import unittest
from connectz import Game, WIN_P1, WIN_P2, DRAW, INCOMPLETE


class TestConnectZGame(unittest.TestCase):

    def test_horizontal_win(self):
        game = Game(4, 4, 3)
        game.play_move(0)  # P1
        game.play_move(0)  # P2
        game.play_move(1)  # P1
        game.play_move(1)  # P2
        game.play_move(2)  # P1 - wins
        self.assertEqual(game.winner, WIN_P1)

    def test_vertical_win(self):
        game = Game(4, 4, 3)
        game.play_move(0)  # P1
        game.play_move(1)  # P2
        game.play_move(0)  # P1
        game.play_move(1)  # P2
        game.play_move(0)  # P1 - wins
        self.assertEqual(game.winner, WIN_P1)

    def test_draw(self):
        game = Game(2, 2, 3)
        game.play_move(0)  # P1
        game.play_move(1)  # P2
        game.play_move(1)  # P1
        game.play_move(0)  # P2
        self.assertTrue(game.is_draw())

    def test_illegal_move_out_of_bounds(self):
        game = Game(4, 4, 3)
        code = game.play_move(5)  # Invalid column
        self.assertIsNotNone(code)

    def test_illegal_move_column_full(self):
        game = Game(1, 2, 2)
        game.play_move(0)
        game.play_move(0)
        code = game.play_move(0)
        self.assertIsNotNone(code)

    def test_diagonal_win_bottom_left_to_top_right(self):
        game = Game(4, 4, 4)
        game.play_move(0)  # P1
        game.play_move(1)  # P2
        game.play_move(1)  # P1
        game.play_move(2)  # P2
        game.play_move(2)  # P1
        game.play_move(3)  # P2
        game.play_move(2)  # P1
        game.play_move(3)  # P2
        game.play_move(3)  # P1
        game.play_move(0)  # P2
        game.play_move(3)  # P1 - diagonal win
        self.assertEqual(game.winner, WIN_P1)

    def test_diagonal_win_bottom_right_to_top_left(self):
        game = Game(4, 4, 4)
        game.play_move(3)  # P1
        game.play_move(2)  # P2
        game.play_move(2)  # P1
        game.play_move(1)  # P2
        game.play_move(1)  # P1
        game.play_move(0)  # P2
        game.play_move(1)  # P1
        game.play_move(0)  # P2
        game.play_move(0)  # P1
        game.play_move(3)  # P2
        game.play_move(0)  # P1 - diagonal win
        self.assertEqual(game.winner, WIN_P1)

    def test_incomplete_game(self):
        game = Game(4, 4, 4)
        game.play_move(0)  # P1
        game.play_move(1)  # P2
        game.play_move(2)  # P1
        self.assertIsNone(game.winner)
        self.assertFalse(game.is_draw())


    def test_invalid_column_negative(self):
        game = Game(4, 4, 3)
        result = game.play_move(-1)
        self.assertIsNotNone(result)

    def test_invalid_column_non_integer(self):
        with self.assertRaises(TypeError):
            game = Game(4, 4, 3)
            game.play_move("a")  # Should raise TypeError

    def test_win_with_larger_board(self):
        game = Game(7, 6, 4)
        game.play_move(0)  # P1
        game.play_move(0)  # P2
        game.play_move(1)  # P1
        game.play_move(1)  # P2
        game.play_move(2)  # P1
        game.play_move(2)  # P2
        game.play_move(3)  # P1 - horizontal win
        self.assertEqual(game.winner, WIN_P1)

    def test_no_win_on_low_connect_requirement(self):
        game = Game(3, 3, 1)
        game.play_move(0)  # P1 should instantly win
        self.assertEqual(game.winner, WIN_P1)