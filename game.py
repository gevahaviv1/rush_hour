#################################################################
# FILE : game.py
# WRITER : Geva Haviv
# DESCRIPTION:
# WEB PAGES I USED:
# NOTES:
#################################################################

import sys
import helper
from board import Board
from car import Car


class Game:
    """
    Add class description here
    """

    def __init__(self, board):
        """
        Initialize a new Game object.
        :param board: An object of type board
        """
        self.__board = board
        self.__legal_names = ['R', 'G', 'W', 'O', 'B', 'Y']
        self.__legal_direction = ['u', 'd', 'l', 'r']

    def __check_name(self, choose):
        """
        :param choose:
        :return:
        """
        choose_lst = choose.split(',')

        if len(choose_lst) != 2:
            return False

        car_name = choose_lst[0]
        if car_name not in self.__legal_names:
            return False

        for i in range(self.__board.get_board_size()):
            for j in range(self.__board.get_board_size()):
                if car_name == self.__board.cell_content((i, j)):
                    return True

        return False

    def __check_direction(self, choose):
        """
        :param choose:
        :return:
        """
        choose_lst = choose.split(',')

        if len(choose_lst) != 2:
            return False

        car_name = choose_lst[0]
        direction = choose_lst[1]
        if direction not in self.__legal_direction:
            return False

        return self.__board.move_car(car_name, direction)

    def __single_turn(self):
        """
        Note - this function is here to guide you and it is *not mandatory*
        to implement it. 

        The function runs one round of the game :
            1. Get user's input of: what color car to move, and what 
                direction to move it.
            2. Check if the input is valid.
            3. Try moving car according to user's input.

        Before and after every stage of a turn, you may print additional 
        information for the user, e.g., printing the board. In particular,
        you may support additional features, (e.g., hints) as long as they
        don't interfere with the API.
        """

        choose = input('Choose car and direction: ')
        while not self.__check_name(choose) or not self.__check_direction(choose):
            choose = input('Not good, again: ')

        print('Good, you change the board to: ')
        print(self.__board)

    def play(self):
        """
        The main driver of the Game. Manages the game until completion.
        :return: None
        """
        while self.__board.cell_content(self.__board.target_location()) is None:
            self.__single_turn()
        print('You won!')


if __name__ == "__main__":
    board = Board()
    cars = helper.load_json(sys.argv[1])
    for car in cars:
        car_to_add = Car(car, cars[car][0], cars[car][1], cars[car][2])
        board.add_car(car_to_add)
    game = Game(board)
    game.play()
