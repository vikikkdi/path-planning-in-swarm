class HungarianError(Exception):
    pass

try:
    import numpy as np
except ImportError:
    raise HungarianError("NumPy is not installed.")


class Hungarian:
    def __init__(self, input_matrix=None, is_profit_matrix=False):
        if input_matrix is not None:
            my_matrix = np.array(input_matrix)
            self._input_matrix = np.array(input_matrix)
            self._maxColumn = my_matrix.shape[1]
            self._maxRow = my_matrix.shape[0]

            matrix_size = max(self._maxColumn, self._maxRow)
            pad_columns = matrix_size - self._maxRow
            pad_rows = matrix_size - self._maxColumn
            if is_profit_matrix:
                my_matrix = self.make_cost_matrix(my_matrix)

            self._cost_matrix = my_matrix
            self._size = len(my_matrix)
            self._shape = my_matrix.shape

            self._results = []
            self._totalPotential = 0
        else:
            self._cost_matrix = None

    def get_results(self):
        return self._results

    def get_total_potential(self):
        return self._totalPotential

    def calculate(self, input_matrix=None, is_profit_matrix=False):
        if input_matrix is None and self._cost_matrix is None:
            raise HungarianError("Invalid input")
        elif input_matrix is not None:
            self.__init__(input_matrix, is_profit_matrix)

        result_matrix = self._cost_matrix.copy()

        for index, row in enumerate(result_matrix):
            result_matrix[index] -= row.min()

        for index, column in enumerate(result_matrix.T):
            result_matrix[:, index] -= column.min()
        total_covered = 0
        while total_covered < self._size:
            cover_zeros = CoverZeros(result_matrix)
            covered_rows = cover_zeros.get_covered_rows()
            covered_columns = cover_zeros.get_covered_columns()
            total_covered = len(covered_rows) + len(covered_columns)

            if total_covered < self._size:
                result_matrix = self._adjust_matrix_by_min_uncovered_num(result_matrix, covered_rows, covered_columns)

        expected_results = min(self._maxColumn, self._maxRow)
        zero_locations = (result_matrix == 0)
        while len(self._results) != expected_results:
            if not zero_locations.any():
                raise HungarianError("Unable to find results. Algorithm has failed.")

            matched_rows, matched_columns = self.__find_matches(zero_locations)

            total_matched = len(matched_rows) + len(matched_columns)
            if total_matched == 0:
                matched_rows, matched_columns = self.select_arbitrary_match(zero_locations)

            for row in matched_rows:
                zero_locations[row] = False
            for column in matched_columns:
                zero_locations[:, column] = False

            self.__set_results(zip(matched_rows, matched_columns))

        value = 0
        for row, column in self._results:
            value += self._input_matrix[row, column]
        self._totalPotential = value

    @staticmethod
    def make_cost_matrix(profit_matrix):
        matrix_shape = profit_matrix.shape
        offset_matrix = np.ones(matrix_shape, dtype=int) * profit_matrix.max()
        cost_matrix = offset_matrix - profit_matrix
        return cost_matrix

    def _adjust_matrix_by_min_uncovered_num(self, result_matrix, covered_rows, covered_columns):
        elements = []
        for row_index, row in enumerate(result_matrix):
            if row_index not in covered_rows:
                for index, element in enumerate(row):
                    if index not in covered_columns:
                        elements.append(element)
        min_uncovered_num = min(elements)

        adjusted_matrix = result_matrix
        for row in covered_rows:
            adjusted_matrix[row] += min_uncovered_num
        for column in covered_columns:
            adjusted_matrix[:, column] += min_uncovered_num
        m_matrix = np.ones(self._shape, dtype=int) * min_uncovered_num
        adjusted_matrix -= m_matrix

        return adjusted_matrix

    def __find_matches(self, zero_locations):
        marked_rows = np.array([], dtype=int)
        marked_columns = np.array([], dtype=int)

        for index, row in enumerate(zero_locations):
            row_index = np.array([index])
            if np.sum(row) == 1:
                column_index, = np.where(row)
                marked_rows, marked_columns = self.__mark_rows_and_columns(marked_rows, marked_columns, row_index,
                                                                           column_index)
        for index, column in enumerate(zero_locations.T):
            column_index = np.array([index])
            if np.sum(column) == 1:
                row_index, = np.where(column)
                marked_rows, marked_columns = self.__mark_rows_and_columns(marked_rows, marked_columns, row_index,
                                                                           column_index)

        return marked_rows, marked_columns

    @staticmethod
    def __mark_rows_and_columns(marked_rows, marked_columns, row_index, column_index):
        new_marked_rows = marked_rows
        new_marked_columns = marked_columns
        if not (marked_rows == row_index).any() and not (marked_columns == column_index).any():
            new_marked_rows = np.insert(marked_rows, len(marked_rows), row_index)
            new_marked_columns = np.insert(marked_columns, len(marked_columns), column_index)
        return new_marked_rows, new_marked_columns

    @staticmethod
    def select_arbitrary_match(zero_locations):
        rows, columns = np.where(zero_locations)
        zero_count = []
        for index, row in enumerate(rows):
            total_zeros = np.sum(zero_locations[row]) + np.sum(zero_locations[:, columns[index]])
            zero_count.append(total_zeros)

        indices = zero_count.index(min(zero_count))
        row = np.array([rows[indices]])
        column = np.array([columns[indices]])

        return row, column

    def __set_results(self, result_lists):
        for result in result_lists:
            row, column = result
            if row < self._maxRow and column < self._maxColumn:
                new_result = (int(row), int(column))
                self._results.append(new_result)


class CoverZeros:
    def __init__(self, matrix):
        self._zero_locations = (matrix == 0)
        self._shape = matrix.shape

        self._choices = np.zeros(self._shape, dtype=bool)

        self._marked_rows = []
        self._marked_columns = []

        self.__calculate()

        self._covered_rows = list(set(range(self._shape[0])) - set(self._marked_rows))
        self._covered_columns = self._marked_columns

    def get_covered_rows(self):
        return self._covered_rows

    def get_covered_columns(self):
        return self._covered_columns

    def __calculate(self):
        while True:
            self._marked_rows = []
            self._marked_columns = []

            for index, row in enumerate(self._choices):
                if not row.any():
                    self._marked_rows.append(index)
            if not self._marked_rows:
                return True
            num_marked_columns = self.__mark_new_columns_with_zeros_in_marked_rows()
            if num_marked_columns == 0:
                return True
            while self.__choice_in_all_marked_columns():
                num_marked_rows = self.__mark_new_rows_with_choices_in_marked_columns()

                if num_marked_rows == 0:
                    return True

                num_marked_columns = self.__mark_new_columns_with_zeros_in_marked_rows()
                if num_marked_columns == 0:
                    return True
            choice_column_index = self.__find_marked_column_without_choice()

            while choice_column_index is not None:
                choice_row_index = self.__find_row_without_choice(choice_column_index)

                new_choice_column_index = None
                if choice_row_index is None:
                    choice_row_index, new_choice_column_index = \
                        self.__find_best_choice_row_and_new_column(choice_column_index)

                    self._choices[choice_row_index, new_choice_column_index] = False

                self._choices[choice_row_index, choice_column_index] = True

                choice_column_index = new_choice_column_index

    def __mark_new_columns_with_zeros_in_marked_rows(self):
        num_marked_columns = 0
        for index, column in enumerate(self._zero_locations.T):
            if index not in self._marked_columns:
                if column.any():
                    row_indices, = np.where(column)
                    zeros_in_marked_rows = (set(self._marked_rows) & set(row_indices)) != set([])
                    if zeros_in_marked_rows:
                        self._marked_columns.append(index)
                        num_marked_columns += 1
        return num_marked_columns

    def __mark_new_rows_with_choices_in_marked_columns(self):
        num_marked_rows = 0
        for index, row in enumerate(self._choices):
            if index not in self._marked_rows:
                if row.any():
                    column_index, = np.where(row)
                    if column_index in self._marked_columns:
                        self._marked_rows.append(index)
                        num_marked_rows += 1
        return num_marked_rows

    def __choice_in_all_marked_columns(self):
        for column_index in self._marked_columns:
            if not self._choices[:, column_index].any():
                return False
        return True

    def __find_marked_column_without_choice(self):
        for column_index in self._marked_columns:
            if not self._choices[:, column_index].any():
                return column_index

        raise HungarianError(
            "Could not find a column without a choice. Failed to cover matrix zeros. Algorithm has failed.")

    def __find_row_without_choice(self, choice_column_index):
        row_indices, = np.where(self._zero_locations[:, choice_column_index])
        for row_index in row_indices:
            if not self._choices[row_index].any():
                return row_index

        return None

    def __find_best_choice_row_and_new_column(self, choice_column_index):
        row_indices, = np.where(self._zero_locations[:, choice_column_index])
        for row_index in row_indices:
            column_indices, = np.where(self._choices[row_index])
            column_index = column_indices[0]
            if self.__find_row_without_choice(column_index) is not None:
                return row_index, column_index

        from random import shuffle

        shuffle(row_indices)
        column_index, = np.where(self._choices[row_indices[0]])
        return row_indices[0], column_index[0]


if __name__ == '__main__':
    profit_matrix = [
        [62, 75, 80, 93, 95, 97],
        [75, 80, 82, 85, 71, 97],
        [80, 75, 81, 98, 90, 97],
        [78, 82, 84, 80, 50, 98],
        [90, 85, 85, 80, 85, 99],
        [65, 75, 80, 75, 68, 96]]

    hungarian = Hungarian(profit_matrix, is_profit_matrix=True)
    hungarian.calculate()
    print("Expected value:\t\t543")
    print("Calculated value:\t", hungarian.get_total_potential())  # = 543
    print("Expected results:\n\t[(0, 4), (2, 3), (5, 5), (4, 0), (1, 1), (3, 2)]")
    print("Results:\n\t", hungarian.get_results())
    print("-" * 80)

    cost_matrix = [
        [4, 2, 8],
        [4, 3, 7],
        [3, 1, 6]]
    hungarian = Hungarian(cost_matrix)
    print('calculating...')
    hungarian.calculate()
    print("Expected value:\t\t12")
    print("Calculated value:\t", hungarian.get_total_potential())  # = 12
    print("Expected results:\n\t[(0, 1), (1, 0), (2, 2)]")
    print("Results:\n\t", hungarian.get_results())
    print("-" * 80)

    profit_matrix = [
        [62, 75, 80, 93, 0, 97],
        [75, 0, 82, 85, 71, 97],
        [80, 75, 81, 0, 90, 97],
        [78, 82, 0, 80, 50, 98],
        [0, 85, 85, 80, 85, 99],
        [65, 75, 80, 75, 68, 0]]
    hungarian = Hungarian()
    hungarian.calculate(profit_matrix, is_profit_matrix=True)
    print("Expected value:\t\t523")
    print("Calculated value:\t", hungarian.get_total_potential())  # = 523
    print("Expected results:\n\t[(0, 3), (2, 4), (3, 0), (5, 2), (1, 5), (4, 1)]")
    print("Results:\n\t", hungarian.get_results())
    print("-" * 80)