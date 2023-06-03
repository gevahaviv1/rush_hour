class Board:
    """
    The purpose of the class is to create and support board game.
    """
    __SIZE = 7

    def __init__(self):
        self.__board = [['-' for _ in range(self.__SIZE)] for _ in range(self.__SIZE)]
        self.__board[3].append('-')
        self.__dict_of_cars = dict()

    def __str__(self):
        """
        This function is called when a board object is to be printed.
        :return: A string of the current status of the board
        """
        return '\n'.join(''.join(self.__board[i][j] + ' ' for j in range((len(self.__board[i]))))
                         for i in range(len(self.__board)))

    def cell_list(self):
        """ This function returns the coordinates of cells in this board
        :return: list of coordinates
        """
        return [(i, j) for i in range(len(self.__board)) for j in range(len(self.__board[i]))]

    def __get_car_length(self, car_name):
        """
        This function check the length of car only by her name.
        :param car_name: String, the name of the car we want to check her length.
        :return: Int.
        """
        length = 0
        for row in self.__board:
            length += row.count(car_name)

        return length

    def __get_car_direction(self, car_name):
        """
        This function check the direction of the car only by her name.
        :param car_name: String, the name of the car we want to check her direction.
        :return: Int.
        """
        if 'u' in self.__dict_of_cars[car_name]:
            return 0

        return 1

    def __have_possible_moves(self, cell_content, i, j):
        """
        This function check if there is a possible moves to specific car.
        :param cell_content: The car we check.
        :param i: The row of the car.
        :param j: The column of the car.
        :return: Boolean.
        """
        direction = self.__get_car_direction(cell_content)

        if direction == 1:  # Direction is 1.
            for cell in self.__board[i]:
                if cell != cell_content:
                    return True

        else:  # Direction is 0
            for row in self.__board:
                if row[j] != cell_content:
                    return True

        return False

    def __possible_moves_helper(self, car_name, row_number, column_number):
        """
        This function returns the legal moves of single car in this board.
        :param car_name: The name of the car we want to check.
        :param row_number: The row number of the car.
        :param column_number: The column number of the car.
        :return: List.
        """
        car_length = self.__get_car_length(car_name)
        car_direction = self.__get_car_direction(car_name)
        possible_moves_lst = []

        if car_direction == 1:

            if column_number > 0 and self.__board[row_number][column_number-1] == '-':
                possible_moves_lst.append((car_name, 'l', 'You can go to the left.'))

            if column_number + car_length-1 <= len(self.__board[row_number])\
                    and self.__board[row_number][column_number + car_length] == '-':
                possible_moves_lst.append((car_name, 'r', 'You can go to the right.'))

        else:

            if row_number > 0 and self.__board[row_number-1][column_number] == '-':
                possible_moves_lst.append((car_name, 'u', 'You can go up.'))

            if row_number + car_length-1 <= len(self.__board)\
                    and self.__board[row_number+car_length][column_number] == '-':
                possible_moves_lst.append((car_name, 'd', 'You can go down.'))

        return possible_moves_lst

    def possible_moves(self):
        """ This function returns the legal moves of all cars in this board
        :return: list of tuples of the form (name,movekey,description)
                 representing legal moves
        """
        _check_lst = []
        _possible_moves_lst = []

        for i in range(len(self.__board)):
            for j in range(len(self.__board[i])):
                if self.__board[i][j] == '-' or self.__board[i][j] in _check_lst:
                    continue

                if self.__have_possible_moves(self.__board[i][j], i, j):
                    for possible_move in self.__possible_moves_helper(self.__board[i][j], i, j):
                        _possible_moves_lst.append(possible_move)

                _check_lst.append(self.__board[i][j])

        return _possible_moves_lst

    def target_location(self):
        """
        This function returns the coordinates of the location which is to be filled for victory.
        :return: (row,col) of goal location
        """
        return 3, 7

    def cell_content(self, coordinate):
        """
        Checks if the given coordinates are empty.
        :param coordinate: tuple of (row,col) of the coordinate to check
        :return: The name if the car in coordinate, None if empty
        """
        if (coordinate[0] < 0 or coordinate[1] < 0) or (coordinate[0] >= self.__SIZE or coordinate[0] >= self.__SIZE):
            return None
        elif self.__board[coordinate[0]][coordinate[1]] == '-':
            return None

        return self.__board[coordinate[0]][coordinate[1]]

    def __car_is_good(self, car):
        """
        This function check all the conditions needed to add car to the game.
        :param car: Car object of car we check to add.
        :return: Bool.
        """
        _legal_location = [(i, j) for i in range(self.__SIZE) for j in range(self.__SIZE)]

        for coordinate in car.car_coordinates():
            if coordinate not in _legal_location or self.cell_content(coordinate) is not None:
                return False

        for row in self.__board:
            if car.get_name() in row:
                return False

        return True

    def add_car(self, car):
        """
        Adds a car to the game.
        :param car: car object of car to add
        :return: True upon success. False if failed
        """
        if self.__car_is_good(car):
            for coordinate in car.car_coordinates():
                self.__board[coordinate[0]][coordinate[1]] = car.get_name()
                self.__dict_of_cars[car.get_name()] = car.possible_moves()
            return True

        return False

    def __found_start_indexs(self, car_name):
        """
        This function found the row start of car only by her name.
        :param car_name: String, the name of the car we want to found.
        :return: Int, row number.
        """
        for i in range(len(self.__board)):
            for j in range(len(self.__board[i])):
                if car_name == self.__board[i][j]:
                    return i, j

        return None

    def __in_possible_moves(self, name, movekey, possible_moves):
        """
        This function check if the move for the specific car is in the possible moves.
        :param name: String, the car name we check.
        :param movekey: Key of move in car to activate.
        :param possible_moves: List of possivle moves.
        :return: Bool.
        """
        for cell in possible_moves:
            if cell[0] == name and cell[1] == movekey:
                return True

        return False

    def move_car(self, name, movekey):
        """
        moves car one step in given direction.
        :param name: name of the car to move
        :param movekey: Key of move in car to activate
        :return: True upon success, False otherwise
        """
        start_indexs_number = self.__found_start_indexs(name)
        if start_indexs_number is None:  # If the car not in the game board.
            return False
        car_length = self.__get_car_length(name)
        possible_moves = self.possible_moves()

        if self.__in_possible_moves(name, movekey, possible_moves):
            if movekey == 'r':
                self.__board[start_indexs_number[0]][start_indexs_number[1]] = '-'
                self.__board[start_indexs_number[0]][start_indexs_number[1] + car_length] = name

            elif movekey == 'l':
                self.__board[start_indexs_number[0]][start_indexs_number[1] + car_length - 1] = '-'
                self.__board[start_indexs_number[0]][start_indexs_number[1] - 1] = name

            elif movekey == 'd':
                self.__board[start_indexs_number[0]][start_indexs_number[1]] = '-'
                self.__board[start_indexs_number[0] + car_length][start_indexs_number[1]] = name

            elif movekey == 'u':
                self.__board[start_indexs_number[0] + car_length - 1][start_indexs_number[1]] = '-'
                self.__board[start_indexs_number[0] - 1][start_indexs_number[1]] = name

            return True
        return False

    def get_board_size(self):
        """
        This function return the board size.
        :return: Int.
        """
        return self.__SIZE

