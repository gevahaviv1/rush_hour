from board import Board
from car import Car


def test_car_init():
    car = Car('Y', 3, (1, 0), 1)
    assert car._Car__name == 'Y'
    assert car._Car__length == 3
    assert car._Car__location == (1, 0)
    assert car._Car__orientation == 1
    assert Car('O', 3, (1, 0), 1)._Car__name == 'O'


def test_coordinates():
    assert Car('Y', 2, (4, 2), 1).car_coordinates() == [(4, 2), (4, 3)]
    assert Car('Y', 2, (0, 0), 0).car_coordinates() == [(0, 0), (1, 0)]
    assert Car('Y', 4, (3, 3), 1).car_coordinates() == [(3, 3), (3, 4), (3, 5), (3, 6)]
    assert Car('Y', 3, (1, 1), 0).car_coordinates() == [(1, 1), (2, 1), (3, 1)]


def test_possible_moves():
    assert isinstance(Car('Y', 2, (0, 0), 0).possible_moves(), dict)
    assert isinstance(Car('Y', 2, (0, 0), 1).possible_moves(), dict)

    assert set(Car('Y', 2, (0, 0), 0).possible_moves().keys()) == {'u', 'd'}
    assert set(Car('Y', 2, (0, 0), 1).possible_moves().keys()) == {'l', 'r'}

    for v in Car('Y', 2, (0, 0), 0).possible_moves().values(): assert isinstance(v, str)
    for v in Car('Y', 2, (0, 0), 1).possible_moves().values(): assert isinstance(v, str)


def test_movement_requirements():
    # vertical
    assert Car('Y', 2, (1, 1), 0).movement_requirements('r') == [(1, 2), (2, 2)]
    assert Car('Y', 2, (1, 1), 0).movement_requirements('l') == [(1, 0), (2, 0)]
    assert Car('Y', 2, (1, 1), 0).movement_requirements('d') == [(3, 1)]
    assert Car('Y', 2, (1, 1), 0).movement_requirements('u') == [(0, 1)]

    # horizontal
    assert Car('Y', 2, (1, 1), 1).movement_requirements('r') == [(1, 3)]
    assert Car('Y', 2, (1, 1), 1).movement_requirements('l') == [(1, 0)]
    assert Car('Y', 2, (1, 1), 1).movement_requirements('d') == [(2, 1), (2, 2)]
    assert Car('Y', 2, (1, 1), 1).movement_requirements('u') == [(0, 1), (0, 2)]

    # long cars
    assert Car('Y', 4, (1, 1), 0).movement_requirements('d') == [(5, 1)]
    assert Car('Y', 4, (1, 1), 0).movement_requirements('u') == [(0, 1)]

    assert Car('Y', 4, (1, 1), 1).movement_requirements('r') == [(1, 5)]
    assert Car('Y', 4, (1, 1), 1).movement_requirements('l') == [(1, 0)]


def test_move():
    car1 = Car('Y', 4, (0, 0), 0)
    car2 = Car('R', 2, (0, 1), 1)

    # vertical
    assert car1.move('r') == False
    assert car1.move('l') == False
    assert car1.move('u') == True
    assert car1.move('d') == True

    # horizontal
    assert car2.move('r') == True
    assert car2.move('l') == True
    assert car2.move('u') == False
    assert car2.move('d') == False

    # illegal move
    assert car1.move('h') == False


def test_get_name():
    for name in ['Y', 'B', 'O', 'W', 'G', 'R']:
        assert Car(name, 2, (0, 0), 0).get_name() == name

def test_board_str():
    assert isinstance(Board().__str__(), str)


def test_cell_list():
    assert set(Board().cell_list()) == {(i, j) for i in range(7) for j in range(7)}.union({(3, 7)})


def test_add_car():
    board = Board()

    assert board.add_car(Car('A', 2, (3,2), 1)) == True
    assert board.add_car(Car('B', 3, (0, 6), 0)) == True
    assert board.add_car(Car('C', 2, (2, 5), 1)) == False
    assert board.add_car(Car('D', 2, (4, 5), 1)) == True
    assert board.add_car(Car('E', 3, (5,5), 1)) == False
    assert board.add_car(Car('F', 2, (-1, 0), 0)) == False
    assert board.add_car(Car('G', 2, (0, -1), 0)) == False
    assert board.add_car(Car('H', 8, (6, 0), 1)) == False


def test_move_car():
    board = Board()

    board.add_car(Car('A', 2, (3, 2), 1))
    board.add_car(Car('B', 3, (0, 6), 0))
    board.add_car(Car('D', 2, (4, 5), 1))

    # horizontal
    assert board.move_car('D', 'r') == False
    for _ in range(5):
        assert board.move_car('D', 'l') == True
    assert board.move_car('D', 'l') == False
    assert board.move_car('D', 'd') == False
    assert board.move_car('D', 'u') == False
    assert board.move_car('D', 'z') == False

    # vertical
    assert board.move_car('B', 'u') == False
    assert board.move_car('B', 'l') == False
    assert board.move_car('B', 'r') == False
    for _ in range(4):
        assert board.move_car('B', 'd') == True
    assert board.move_car('B', 'd') == False
    assert board.move_car('B', 'u') == True
    assert board.move_car('B', 'd') == True

    # exit
    assert board.move_car('A', 'l') == True
    for _ in range(5):
        assert board.move_car('A', 'r') == True
    assert board.move_car('A', 'r') == False
    assert board.move_car('A', 'l') == True
    assert board.move_car('B', 'u') == False


def board_test_possible_moves():
    board = Board()

    board.add_car(Car('A', 2, (3, 5), 1))
    board.add_car(Car('B', 3, (3, 6), 0))
    board.add_car(Car('D', 2, (0, 5), 1))

    assert set([move[:2] for move in board.possible_moves()]) == {('A', 'l'), ('A', 'r'), ('D', 'l')}


def test_target_location():
    assert Board().target_location() == (3, 7)


def test_cell_content():
    board = Board()

    board.add_car(Car('A', 2, (3, 5), 1))
    board.add_car(Car('B', 3, (0, 6), 0))
    board.add_car(Car('D', 2, (5, 0), 1))

    assert board.cell_content((3, 5)) == 'A'
    assert board.cell_content((2, 6)) == 'B'
    assert board.cell_content((4, 6)) is None
    assert board.cell_content((2, 5)) is None
    assert board.cell_content((5, 1)) == 'D'

    assert board.cell_content((3, 7)) is None
    board.move_car('A', 'r')
    assert board.cell_content((3,7)) == 'A'
    assert board.cell_content((3, 5)) is None
