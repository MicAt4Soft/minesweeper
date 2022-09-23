from enum import Enum
from functools import reduce
from math import ceil
from random import randint

MINE_SIGN = '*'
EXPLODED_MINE = "X"
COVERED_SIGN = "?"


class Difficulty(Enum):
    EASY = 1 / 8
    MEDIUM = 1 / 6
    HARD = 1 / 4
    EXTREME = 3 / 4


def generate_field(height, width, difficulty):
    field = [[0] * width for i in range(height)]
    covered_field = [[COVERED_SIGN] * width for i in range(height)]
    number_of_mines = ceil(difficulty.value * height * width)
    generate_mines(number_of_mines, field)
    # print_all(field)
    # print()
    print_all(covered_field)
    return field, covered_field, number_of_mines


def generate_mines(amount, field):
    while amount > 0:
        rand_y = randint(0, len(field) - 1)
        rand_x = randint(0, len(field[0]) - 1)

        if not is_mine(field, rand_x, rand_y):
            amount -= 1
            set_value(field, rand_x, rand_y, MINE_SIGN)
            fill_fields(field, rand_x, rand_y)


def fill_fields(field, x, y):
    increment_field(field, x - 1, y - 1)
    increment_field(field, x - 1, y)
    increment_field(field, x - 1, y + 1)
    increment_field(field, x, y - 1)
    increment_field(field, x, y + 1)
    increment_field(field, x + 1, y - 1)
    increment_field(field, x + 1, y)
    increment_field(field, x + 1, y + 1)


def increment_field(field, x, y):
    if is_not_in_bounds(field, x, y):
        return

    if is_mine(field, x, y):
        return

    increment_value(field, x, y)


def is_mine(field, x, y):
    return get_value(field, x, y) == MINE_SIGN


def print_all(field):
    for row in field:
        line = "|"
        for value in row:
            line += str(value) + "|"
        print(line)


def get_value(field, x, y):
    return field[y][x]


def set_value(field, x, y, value):
    field[y][x] = value


def get_height(field):
    return len(field)


def get_width(field):
    return len(field[0])


def increment_value(field, x, y):
    field[y][x] += 1


def is_not_in_bounds(field, x, y):
    height = get_height(field)
    width = get_width(field)

    return (x < 0 or x >= width or y < 0 or y >= height)


def uncover_field(field, covered_field, x, y):
    if is_not_in_bounds(field, x, y):
        return

    if get_value(covered_field, x, y) != COVERED_SIGN:
        return

    if is_mine(field, x, y):
        set_value(covered_field, x, y, EXPLODED_MINE)
        print("BOOOOOOOOOOOOOOOOOOOOM you died hahaha")
        return False

    set_value(covered_field, x, y, get_value(field, x, y))
    uncover_surrounding_fields(field, covered_field, x, y);

    return True

def uncover_surrounding_fields(field, covered_field, x, y):
    if get_value(covered_field, x, y) != 0:
        return

    uncover_field(field, covered_field, x - 1, y - 1)
    uncover_field(field, covered_field, x - 1, y)
    uncover_field(field, covered_field, x - 1, y + 1)
    uncover_field(field, covered_field, x, y - 1)
    uncover_field(field, covered_field, x, y + 1)
    uncover_field(field, covered_field, x + 1, y - 1)
    uncover_field(field, covered_field, x + 1, y)
    uncover_field(field, covered_field, x + 1, y + 1)

def foobar(field, covered_field, x, y):
    value = get_value(field, x, y)
    if value == '0':
        set_value(covered_field, x, y, '0')

def read_line():
    line = input().split(",")
    x = int(line[0])
    y = int(line[1])
    return x, y

def count_convered_elements_in_line(count, value):
    return count + 1 if value == COVERED_SIGN else count

def count_covered_fields(line_sum, line):
    return reduce(count_convered_elements_in_line, line, line_sum)

def are_all_fields_except_mines_uncovered(covered_field, number_of_mines):
    total = reduce(count_covered_fields, covered_field, 0)
    print("Still covered " + str(total))

    if total == number_of_mines:
        print("You rock! Best playa eva!")
        return True

    return False


height = 5
width = 5
difficulty = Difficulty.EASY
running = True

field, covered_field, number_of_mines = generate_field(height, width, difficulty)

while running:
    print("Please select x,y values")
    x, y = read_line()
    if (is_not_in_bounds(field, x, y)):
        print("x must be smaller than " + str(get_width(field)) + " and y must be smaller than " + str(
            get_height(field)) + ".")
        continue

    not_exploded = uncover_field(field, covered_field, x, y)
    if not_exploded:
        success = are_all_fields_except_mines_uncovered(covered_field, number_of_mines)
        if success:
            print_all(field)
            running = False
        else:
            print_all(covered_field)
    else:
        set_value(field, x, y, EXPLODED_MINE)
        print_all(field)
        running = False
