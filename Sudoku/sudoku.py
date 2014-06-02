#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A simple backtracking Sudoku generator
"""

import math
import random

from decorators import handle_negative, check_length, requires_solution

MIN = -1
EASY = 0
MEDIUM = 1
HARD = 2
EXPERT = 3
INSANE = 4
GOOD_LUCK = 5


class Sudoku(object):
    VALID_SIZES = (2, 3, 4, 5)
    SCALE = {
        MIN: 0.65,
        EASY: 0.45,
        MEDIUM: 0.35,
        HARD: 0.30,
        EXPERT: 0.24,
        INSANE: 0.17,
        GOOD_LUCK: 0.12,
    }
    BLOCK_PERMUTATIONS = {
        "012": "a",
        "021": "b",
        "102": "c",
        "120": "d",
        "201": "e",
        "210": "f",
    }
    grid_size = 0
    difficulty = 0

    def __init__(self, grid_size=3, difficulty=MEDIUM):
        self.set_grid_size(grid_size)
        self.set_difficulty(difficulty)
        self.side_length = self.grid_size ** 2
        self.square = self.side_length ** 2
        self.possibles = set([i + 1 for i in range(self.side_length)])
        self.solution = []
        self._masked = None
        self.iterations = 0

        self.clear()

    def init_grid(self, values):
        """Initializes the grid with some existing values."""

        validate = lambda value: (str(value).isdigit() and 0 < value <= self.side_length) and value or None
        if len(values) == self.square:
            # 1-dimensional list of values
            self.solution = [validate(v) for v in values]
        elif len(values) == self.side_length:
            # multi-dimensional list of values: [[row 1], [row 2], ..., [row n]]
            for i, row in enumerate(values):
                self.set_row(i, [validate(v) for v in row])

    def clear(self):
        """Cleans up the Sudoku solution"""

        self.solution = [None for i in range(self.square)]

    def row_col_to_index(self, row, col):
        """Translates a (row, col) into an index in our 1-dimensional list"""

        return (row * self.side_length) + col

    def index_to_row_col(self, index):
        """Translates an index in our 1-dimensional list to a (row, col)"""

        return divmod(index, self.side_length)

    def set_grid_size(self, grid_size):
        """Sets the grid size"""

        if grid_size in self.VALID_SIZES:
            self.grid_size = grid_size
        else:
            raise ValueError('Invalid size.  Options are: %s' % (self.VALID_SIZES, ))

    def set_difficulty(self, difficulty):
        """Sets the difficulty level for a masked grid"""

        valid_diff = self.SCALE.keys()
        valid_diff.remove(MIN)

        if difficulty in valid_diff:
            self.difficulty = difficulty
        else:
            raise ValueError('Invalid difficulty level.  Options are: %s' % (valid_diff,))

    @property
    @requires_solution
    def masked_grid(self):
        """Generates and caches a Sudoku with several squares hidden"""

        if self._masked is None:
            min_difficulty = math.floor(Sudoku.SCALE[self.difficulty] * self.square)
            max_difficulty = math.ceil(Sudoku.SCALE.get(self.difficulty - 1, min_difficulty) * self.square)
            numbers_to_show = random.randint(min_difficulty, max_difficulty)

            self._masked = [True for i in range(numbers_to_show)] + \
                           ['_' for i in range(self.square - numbers_to_show)]
            random.shuffle(self._masked)
            for i, value in enumerate(self.solution):
                if self._masked[i]:
                    self._masked[i] = value

        return self._masked

    @handle_negative
    def get_row(self, row):
        """Returns all values for the specified row"""

        start = row * self.side_length
        end = start + self.side_length
        return self.solution[start:end]

    def get_row_by_index(self, index):
        """Returns all values for the row at the given index"""

        row, col = self.index_to_row_col(index)
        return self.get_row(row)

    @check_length
    def set_row(self, row, values):
        """Sets the values for the specified row"""

        start = row * self.side_length
        end = start + self.side_length
        self.solution[start:end] = values

    @handle_negative
    def get_col(self, col):
        """Returns all values for the specified column"""

        return self.solution[col::self.side_length]

    def get_col_by_index(self, index):
        """
        Returns all values for the column at the given index
        """

        row, col = self.index_to_row_col(index)
        return self.get_col(col)

    @check_length
    def set_col(self, col, values):
        """Sets the values for the specified column"""

        self.solution[col::self.side_length] = values

    def get_region(self, row, col):
        """Returns all values for the region at the given (row, col)"""

        start_row = int(row / self.grid_size) * self.grid_size
        start_col = int(col / self.grid_size) * self.grid_size

        values = []
        for i in range(self.grid_size):
            start = (start_row + i) * self.side_length + start_col
            end = start + self.grid_size
            values.extend(self.solution[start:end])

        return values

    def get_region_by_index(self, index):
        """Returns all values for the region at the given index"""

        row, col = self.index_to_row_col(index)
        return self.get_region(row, col)

    def get_used(self, row, col):
        """Returns a list of all used values for a row, column, and region"""

        r = self.get_row(row)
        c = self.get_col(col)
        region = self.get_region(row, col)

        return r + c + region

    def get_used_by_index(self, index):
        """Returns a list of all used values for a row, col, and region"""

        row, col = self.index_to_row_col(index)
        return self.get_used(row, col)

    def is_valid_value(self, row, col, value):
        """
        Validates whether or not a value will work in the grid, without using
        the pre-generated solution
        """

        return value not in self.get_used(row, col)

    def is_valid_value_for_index(self, index, value):
        """Validates a value for the given index"""

        row, col = self.index_to_row_col(index)
        return self.is_valid_value(row, col, value)

    def fill_square(self, index=0):
        """
        Recursively populates each square on the Sudoku grid until a solution
        is found.  Most of this method was inspired by Jeremy Brown
        """

        if self.solution[index]:
            if index + 1 >= self.square:
                return True
            return self.fill_square(index + 1)

        used = self.get_used_by_index(index)
        possible = list(self.possibles.difference(used))
        if len(possible) == 0:
            return False

        #if self.iterations % 50000 == 0: print index, possible #, row, col, region
        random.shuffle(possible)

        for new_value in possible:
            self.solution[index] = new_value
            self.iterations += 1

            if index + 1 >= self.square or self.fill_square(index + 1):
                return True

            self.solution[index] = None

        return False

    def solve(self):
        self.iterations = 0
        self.fill_square(0)

    def get_block_permutation(self, n, index, get):
        positions = [[i, get(index * self.grid_size + i).index(n)] for i in range(0, 3)]
        positions = sorted(positions, key=lambda e: e[1])
        positions = "".join(map(lambda e: str(e[0]), positions))
        return self.BLOCK_PERMUTATIONS[positions]

    def get_block_col_permutation_n(self, n, col):
        return self.get_block_permutation(n, col, self.get_col)

    def get_block_row_permutation_n(self, n, row):
        return self.get_block_permutation(n, row, self.get_row)

    def get_block_col_permutation(self, col):
        permutations = ""
        for i in range(1, 10):
            permutations += self.get_block_col_permutation_n(i, col)
        return permutations

    def get_block_row_permutation(self, row):
        permutations = ""
        for i in range(1, 10):
            permutations += self.get_block_row_permutation_n(i, row)
        return permutations

    def swap(self, n1, n2):
        self.solution = [e if e != n1 else 0 for e in self.solution]
        self.solution = [e if e != n2 else n1 for e in self.solution]
        self.solution = [e if e != 0 else n2 for e in self.solution]

    def normalize_type(self):
        row_permutation = self.get_block_row_permutation_n
        change = True
        while change:
            change = False
            for i in range(1, 9):
                if row_permutation(i + 1, 0) < row_permutation(i, 0):
                    self.swap(i, i+1)
                    change = True

    def get_type(self):
        permutations = ""
        for i in range(0, 3):
            permutations += self.get_block_row_permutation(i) + " - "
            permutations += self.get_block_col_permutation(i) + "\n"
        return permutations

    def block_col_permute(self, col1, col2):
        for i in range(0, 3):
            col11 = self.get_col(col1 * 3 + i)
            self.set_col(col1 * 3 + i, self.get_col(col2 * 3 + i))
            self.set_col(col2 * 3 + i, col11)

    def block_row_permute(self, row1, row2):
        for i in range(0, 3):
            row11 = self.get_row(row1 * 3 + i)
            self.set_row(row1 * 3 + i, self.get_col(row2 * 3 + i))
            self.set_row(row2 * 3 + i, row11)

    @requires_solution
    def print_grid(self, grid):
        """Prints a nicely formatted version of the Sudoku grid"""

        field_width = len(str(self.side_length)) + 2
        grid_format = ''.join(['%s' for i in range(self.grid_size)])
        grid_format = '|'.join([grid_format for i in range(self.grid_size)])

        for row in range(self.side_length):
            start = row * self.side_length
            end = start + self.side_length
            values = tuple(str(val).center(field_width) for val in grid[start:end])
            print grid_format % values

            # print a dividing line for each set of regions
            if row < self.side_length - 1 and (row + 1) % self.grid_size == 0:
                print '+'.join('-' * field_width * self.grid_size for i in range(self.grid_size))

    def print_solution(self):
        """Prints the generated solution nicely formatted"""

        return self.print_grid(self.solution)

    def print_masked(self):
        """Prints a masked version of the grid"""

        return self.print_grid(self.masked_grid)


def main():
    import sys
    try:
        size = int(sys.argv[1])
    except IndexError:
        size = 3
    s = Sudoku(size, difficulty=EASY)
    s.print_solution()
    print s.get_type()
    print ""
    s.normalize_type()
    s.print_solution()
    print s.get_type()

if __name__ == '__main__':
    main()
