from collections import defaultdict


class Poly:
    def __init__(self, var_list: list):
        self.var_list = var_list
        self.num_var = len(var_list)
        self.poly_dict = defaultdict(int)

    def add(self, coefficient: int or float, power_list=None):
        if power_list is None:
            power_list = []
        if type(power_list) != list:
            raise TypeError("Power is not a list")
        if len(power_list) > self.num_var:
            raise ValueError("Length of the power list is larger than the number of variables")
        if len(power_list) < self.num_var:
            power_list.extend(0 for _ in range(self.num_var - len(power_list)))
        power_list = tuple(power_list)
        self.poly_dict[power_list] += coefficient
        if self.poly_dict[power_list] == 0:
            del self.poly_dict[power_list]

    def __str__(self):
        if len(self.poly_dict) == 0:
            return "0"
        else:
            result = ""
            poly_list = sorted(self.poly_dict.items(), key=lambda x: x[0])
            for i in range(len(poly_list)):
                coefficient = poly_list[i][1]
                if i == 0:
                    result += "" if coefficient > 0 else "- "
                else:
                    result += " + " if coefficient > 0 else " - "
                result += "{:g}".format(abs(coefficient)) if abs(coefficient) != 1 or list(poly_list[i][0]) == [0] * self.num_var else ""
                for j in range(self.num_var):
                    power = poly_list[i][0][j]
                    if power != 0:
                        result += self.var_list[j]
                        if power != 1:
                            result += "^{" + "{:g}".format(power) + "}"
            return result

    def __add__(self, other):
        if self.var_list != other.var_list:
            raise TypeError("Poly with different variables cannot be added")
        else:
            new_poly = Poly(self.var_list)
            for i in self.poly_dict:
                new_poly.add(self.poly_dict[i], list(i))
            for i in other.poly_dict:
                new_poly.add(other.poly_dict[i], list(i))
            return new_poly

    def __mul__(self, other):
        if self.var_list != other.var_list:
            raise TypeError("Poly with different variables cannot be added")
        else:
            new_poly = Poly(self.var_list)
            for i in self.poly_dict:
                for j in other.poly_dict:
                    a = []
                    for k in range(self.num_var):
                        a.append(i[k] + j[k])
                    new_poly.add(self.poly_dict[i] * other.poly_dict[j], a)
            return new_poly

    def __pow__(self, power: int):
        if power < 0:
            raise ValueError("Power is less than 0")
        if len(self.poly_dict) == 0:
            return Poly(self.var_list)
        if power == 0:
            a = Poly(self.var_list)
            a.add(1)
            return a
        return self * self ** (power - 1)

    def __neg__(self):
        a = Poly(self.var_list)
        a.add(-1)
        return self * a

    def __sub__(self, other):
        return self + (-other)

    def __abs__(self):
        a = Poly(self.var_list)
        for i in self.poly_dict:
            a.add(abs(self.poly_dict[i]), list(i))
        return a
