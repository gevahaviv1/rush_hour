import sys

if sys.version_info[0] < 3:
    print("ERROR")
    sys.exit("Python/Pytest must be running via python 3.6 at least!")

import tempfile
import json
import os
from pathlib import Path
from subprocess import Popen, PIPE


class Helper:
    def __init__(self, log=False):
        self._game_py = str(Helper.__find_game_py())
        self._python = sys.executable
        if log:
            print()
            print(f"Using game.py at {self._game_py}")
            print(f"Using python executable at {self._python}")
            print()

    def _run_game_process(self, json_file, input_txt):
        args = [self._python, self._game_py, json_file]
        _, err = Popen(args, universal_newlines=True, stdin=PIPE, stderr=PIPE).communicate(input_txt)

        # check for other errors(e.g compilation errors, type errors) that aren't
        # related to whether the program has finished successfully or not.
        if len(err) > 0 and "EOF" not in err:
            raise Exception(f"There was an unexpected error while running this test:\n"
                            f"Error message from your executing your program:\n\n{err}\n"
                            f"(this is a problem with your code)")
        return err

    def finishes_with_exact_moves(self, car_cfg, moves):

        # first I check that the given moves result in the program finishing
        # successfully
        moves_st = "\n".join(moves)
        err = self._run_game_process(car_cfg, moves_st)
        assert len(err) == 0, "The game should've terminated successfully after being given " \
                              "all valid moves, but instead it expected for more input."

        # Since the process library doesn't know if all standard input has been consumed/processed, I make another
        # test to ensure that we don't win when given less than the needed moves to win.
        not_enough_moves_st = "\n".join(moves[:-1])
        err = self._run_game_process(car_cfg, not_enough_moves_st)
        assert "EOF" in err, "When providing less than the exact moves for victory, the game should've " \
                             "errored(as it should expect for more input), but it has terminated successfully " \
                             "as if we have won."

    def fails_with_given_moves(self, car_cfg, moves):
        moves_st = "\n".join(moves)
        err = self._run_game_process(car_cfg, moves_st)
        # we expect an EOF error as we interrupted the process while it should've
        # waited for more input()
        assert "EOF" in err, "The game has terminated successfully despite not giving "\
                             "it enough moves to win! It should've expected more input"

    @staticmethod
    def __find_game_py():
        cur_dir = str(Path.cwd().parent)
        walk = os.walk(cur_dir, topdown=False)
        for cur_dir, _subdirs, files in walk:
            if "game.py" in files:
                return Path(cur_dir, "game.py")
        raise ValueError(f"Couldn't find game.py beginning at {cur_dir}\n."
                         f"Are you sure you placed the tests within the exercise9\n"
                         f"project folder(or in a subfolder inside it?)")


def test_ensure_tests_configured_corrrectly():
    _test_helper = Helper(log=True)


def create_car_config(cars_dict):
    with tempfile.NamedTemporaryFile(delete=False) as file:
        file.write(bytes(json.dumps(cars_dict), 'UTF-8'))
        return file.name

def test_valid_simple():
    cars = {
        "R": [2,[3,0],1],
        "O": [3,[1,4],0]
    }

    cfg_file = create_car_config(cars)
    test_helper = Helper()

    test_helper.finishes_with_exact_moves(cfg_file, ["O,u"] + ["R,r"] * 6)
    test_helper.finishes_with_exact_moves(cfg_file, ["O,u"] + ["R,r"] * 5 + ["R,l", "R,r", "R,r"])
    test_helper.finishes_with_exact_moves(cfg_file, ["O,u"] + ["Invalid,Cowabunga"] * 20 + ["O,u"] * 1337 + ["R,r"] * 6)
    test_helper.finishes_with_exact_moves(cfg_file, ["O,u"] + ["Invalid command"] * 20 + ["R,r"] * 6)

    test_helper.fails_with_given_moves(cfg_file, ["O,u"] + ["R,r"] * 2)
    test_helper.fails_with_given_moves(cfg_file, ["O,u"] + ["R,r"] * 1)

