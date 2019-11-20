from itertools import zip_longest
POWERS = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")


class Polynomial(object):
    def __init__(self, coefficients=[]):
        self.coefficients = coefficients
        self.strip()

    def strip(self):
        while len(self) > 1 and self.coefficients[0] == 0:
            self.coefficients.pop(0)

    def __call__(self, x):
        res = 0
        for i, coeff in enumerate(self.coefficients[::-1]):
            res += coeff * x ** i
        return res

    def __len__(self):
        return len(self.coefficients)

    def __eq__(self, other):
        return self.coefficients == other.coefficients

    def __add__(self, other):
        if isinstance(other, Polynomial):
            res = [sum(c) for c in zip_longest(self.coefficients[::-1],
                                               other.coefficients[::-1],
                                               fillvalue=0)][::-1]
        elif isinstance(other, int) or isinstance(other, float):
            if len(self) == 0:
                res = [other]
            else:
                res = self.coefficients[:]
                res[-1] += other

        else:
            raise TypeError('Can only add number or another polynomial to a polynomial, not {}'
                            .format(type(other).__name__))

        return Polynomial(res)

    def __sub__(self, other):
        if isinstance(other, Polynomial):
            res = [c1 - c2 for c1, c2 in zip_longest(self.coefficients[::-1],
                                                     other.coefficients[::-1],
                                                     fillvalue=0)][::-1]
        elif isinstance(other, int) or isinstance(other, float):
            if len(self) == 0:
                res = [other]
            else:
                res = self.coefficients[:]
                res[-1] -= other

        else:
            raise TypeError('Can only subtract number or another polynomial from a polynomial, not {}'
                            .format(type(other).__name__))

        return Polynomial(res)

    def __mul__(self, other):
        if isinstance(other, Polynomial):
            res = [0] * (len(self) + len(other) - 1)
            for pow1, coeff1 in enumerate(self.coefficients):
                for pow2, coeff2 in enumerate(other.coefficients):
                    res[pow1 + pow2] += coeff1 * coeff2

        elif isinstance(other, int) or isinstance(other, float):
            res = [coeff * other for coeff in self.coefficients]

        else:
            return NotImplemented

        return Polynomial(res)

    def __neg__(self):
        return self * -1

    def __radd__(self, other):
        return self + other

    def __rsub__(self, other):
        return -self + other

    def __rmul__(self, other):
        return self * other

    def __repr__(self):
        out = ""
        for i, coeff in enumerate(self.coefficients):
            power = len(self.coefficients) - i - 1
            mono_str = '{}{}{}'.format(abs(coeff), 'x' if power > 0 else '',
                                       str(power).translate(POWERS) if power > 1 else '')
            if coeff < 0:
                out += ' - {}'.format(mono_str)
            elif out:
                out += ' + {}'.format(mono_str)
            else:
                out += mono_str

        return out

    @classmethod
    def X(cls):
        '''Return a variable'''
        return cls([1, 0])
