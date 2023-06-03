class Car:
    """
    This class represent car.
    """

    def __init__(self, name, length, location, orientation):
        """
        A constructor for a Car object
        :param name: A string representing the car's name
        :param length: A positive int representing the car's length.
        :param location: A tuple representing the car's head (row, col) location
        :param orientation: One of either 0 (VERTICAL) or 1 (HORIZONTAL)
        """
        self.__name = name
        self.__length = length
        self.__location = location
        self.__orientation = orientation

    def car_coordinates(self):
        """
        :return: A list of coordinates the car is in
        """
        if self.__orientation == 0:
            return [(i + self.__location[0], self.__location[1]) for i in range(self.__length)]
        else:
            return [(self.__location[0], j + self.__location[1]) for j in range(self.__length)]

    def possible_moves(self):
        """
        :return: A dictionary of strings describing possible movements permitted by this car.
        """
        if self.__orientation == 0:
            return {'u': 'You can go up.', 'd': 'You can go down.'}
        else:
            return {'l': 'You can go left.', 'r': 'You can go right.'}

    def __movement_requirements_helper(self, movekey):
        """
        :param movekey: A string representing the key of the required move.
        :return: A list of cell locations which must be empty in order for this move to be legal.
        """
        if movekey == 'r':
            i = 0
            j = 1
        elif movekey == 'l':
            i = 0
            j = -1
        elif movekey == 'd':
            i = 1
            j = 0
        elif movekey == 'u':
            i = -1
            j = 0

        return [(coordinates[0] + i, coordinates[1] + j) for coordinates in self.car_coordinates()]

    def movement_requirements(self, movekey):
        """
        :param movekey: A string representing the key of the required move.
        :return: A list of cell locations which must be empty in order for this move to be legal.
        """
        if self.__orientation == 0 and movekey == 'u':
            return [(self.__location[0]-1, self.__location[1])]
        elif self.__orientation == 0 and movekey == 'd':
            return [(self.__location[0]+1, self.__location[1])]
        elif self.__orientation == 1 and movekey == 'l':
            return [(self.__location[0], self.__location[1]-1)]
        elif self.__orientation == 1 and movekey == 'r':
            return [(self.__location[0], self.__location[1]+self.__length)]
        else:
            return self.__movement_requirements_helper(movekey)

    def move(self, movekey):
        """
        This function move the car.
        :param movekey: A string representing the key of the required move.
        :return: True upon success, False otherwise
        """
        if movekey in ['l', 'r'] and self.__orientation == 1:
            self.__location = self.movement_requirements(movekey)[0]
            return True
        elif movekey in ['u', 'd'] and self.__orientation == 0:
            self.__location = self.movement_requirements(movekey)[0]
            return True

        return False

    def get_name(self):
        """
        :return: The name of this car.
        """
        return self.__name

