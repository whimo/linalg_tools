from polynomial import Polynomial


class Matrix(object):
    def __init__(self, values):
        self.values = list(list(row) for row in values)
        self.height = len(self.values)
        self.width = len(self.values[0])
        self.check_width()

    def check_width(self):
        assert all(len(row) == self.width for row in self.values)

    def __eq__(self, other):
        return self.values == other.values

    def __add__(self, other):
        if not isinstance(other, Matrix):
            raise TypeError('Can only add another matrix to matrix, not {}'
                            .format(type(other).__name__))

        assert self.height == other.height and self.width == other.width
        res = [[sum(t) for t in zip(row1, row2)] for row1, row2 in zip(self.values, other.values)]

        return Matrix(res)

    def __sub__(self, other):
        if not isinstance(other, Matrix):
            raise TypeError('Can only subtract another matrix from matrix, not {}'
                            .format(type(other).__name__))

        assert self.height == other.height and self.width == other.width
        res = [[v1 - v2 for v1, v2 in zip(row1, row2)] for row1, row2 in zip(self.values, other.values)]

        return Matrix(res)

    def __mul__(self, other):
        if isinstance(other, Matrix):
            assert self.width == other.height
            res = [[sum(self.values[i][k] * other.values[k][j] for k in range(self.width))
                    for j in range(other.width)]
                   for i in range(self.height)]

        elif isinstance(other, int) or isinstance(other, float) or isinstance(other, Polynomial):
            res = [[self.values[i][j] * other for j in range(self.width)] for i in range(self.height)]

        else:
            raise TypeError('Can only multiply matrix by another matrix or number, not {}'
                            .format(type(other).__name__))

        return Matrix(res)

    def __rmul__(self, other):
        if isinstance(other, int) or isinstance(other, float) or isinstance(other, Polynomial):
            return self * other
        return NotImplemented

    def __truediv__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return self * (1.0 / other)
        return NotImplemented

    def __pow__(self, other):
        assert self.width == self.height

        if isinstance(other, int):
            if other == 0:
                return Matrix.identity(self.height)

            if other < 0:
                res = self.inverse()
            else:
                res = self
            for _ in range(abs(other) - 1):
                res *= self

            return res

        return NotImplemented

    def __neg__(self):
        return self * -1

    def __repr__(self):
        s = [[str(e) for e in row] for row in self.values]
        lens = [max(map(len, col)) for col in zip(*s)]
        fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
        table = [fmt.format(*row) for row in s]
        return '\n'.join(table)

    def transpose(self):
        return Matrix(zip(*self.values))

    @property
    def T(self):
        return self.transpose()

    def determinant(self):
        assert self.width == self.height
        if self.height == 1:
            return self.values[0][0]

        result = 0
        decapped_rows = [row[1:] for row in self.values]

        for i in range(self.height):
            result += (((-1) ** i) * self.values[i][0] *
                       Matrix(decapped_rows[:i] + decapped_rows[i + 1:]).determinant())
        return result

    @property
    def det(self):
        return self.determinant()

    def trace(self):
        assert self.width == self.height
        return sum(self.values[i][i] for i in range(self.height))

    @property
    def tr(self):
        return self.trace()

    def minor(self, i, j):
        '''Compute (i + 1, j + 1)-minor or the matrix'''
        assert self.width == self.height
        submatrix_values = [[self.values[_i][_j] for _j in range(self.width) if _j != j]
                            for _i in range(self.height) if _i != i]

        return Matrix(submatrix_values).det

    def adjugate(self):
        assert self.width == self.height
        adjugate_values = [[((-1) ** (i + j)) * self.minor(i, j)
                            for j in range(self.width)]
                           for i in range(self.height)]
        return Matrix(adjugate_values).T

    def inverse(self):
        return self.adjugate() / self.det

    @classmethod
    def identity(cls, size):
        '''Identity matrix aka E'''
        values = [[0 for i in range(size)] for i in range(size)]
        for i in range(size):
            values[i][i] = 1

        return cls(values)

    @classmethod
    def zeros(cls, height, width=None):
        '''Zero-filled matrix'''
        return cls([[0 for i in range(width or height)] for i in range(height)])
