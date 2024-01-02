import Link
import Poly
from itertools import product
import networkx as nx


def crossing_split(crossing):
    return {0: [[crossing.b1, crossing.b4], [crossing.b2, crossing.b3]],
            1: [[crossing.b1, crossing.b2], [crossing.b3, crossing.b4]]}


def merge_loops_list():
    pass


def kauffman_bracket(link, regions, outside, base_point):
    kauffman_bracket_poly = Poly.Poly(["q", "x"])
    kauffman_bracket_poly.add(0)
    arrangements = list(product([0, 1], repeat=len(link.crossings)))
    for arrangement in arrangements:
        state_sum = sum(arrangement)
        connect_regions = nx.Graph()
        connect_regions.add_nodes_from(list(range(len(regions))))
        cycle, cycle_b = 0, 0
        # each state
        for i in range(len(arrangement)):
            state = arrangement[i]
            split = crossing_split(link.crossings[i])[state]
            a, b = -1, -1
            for j in range(len(regions)):
                if {split[0][0], split[0][1]}.issubset(regions[j].nodes):
                    a = j
                if {split[1][0], split[1][1]}.issubset(regions[j].nodes):
                    b = j
            connect_regions.add_edge(a, b)
        connect_sets = list(nx.connected_components(connect_regions))
        for i in range(len(connect_sets)):
            if outside in connect_sets[i]:
                del connect_sets[i]
                break
        cycle = len(connect_sets)
        num = 0
        edge_list = []
        ignore_list = []
        while num < cycle:
            if num not in ignore_list:
                if base_point in connect_sets[num]:
                    ignore_list.append(num)
                    cycle_b += 1
                    for i in connect_sets[num]:
                        edge_list += regions[i].nodes
                    num = -1
                elif edge_list:
                    temp_list = []
                    for i in connect_sets[num]:
                        temp_list += regions[i].nodes
                    if set(edge_list) <= set(temp_list):
                        ignore_list.append(num)
                        cycle_b += 1
                        edge_list = list(set(temp_list) - set(edge_list))
                        num = -1
            num += 1
        cycle -= cycle_b
        p1 = Poly.Poly(['q', 'x'])
        p1.add((-1) ** state_sum, [state_sum])
        p2 = Poly.Poly(['q', 'x'])
        p2.add(1, [1])
        p2.add(1, [-1])
        p3 = Poly.Poly(['q', 'x'])
        p3.add(1, [1, 1])
        p3.add(1, [-1, -1])
        kauffman_bracket_poly += p1 * p2 ** cycle * p3 ** cycle_b
    return kauffman_bracket_poly


def annular_jones_polynomial(link, regions, outside, base_point):
    kauffman_bracket_poly = kauffman_bracket(link, regions, outside, base_point)
    writhe = link.writhe()
    n_plus = writhe[0]
    n_minus = writhe[1]
    p1 = Poly.Poly(['q', 'x'])
    p1.add((-1) ** n_minus)
    p2 = Poly.Poly(['q', 'x'])
    p2.add(1, [n_plus - 2 * n_minus])
    return kauffman_bracket_poly * p1 * p2


# Some examples

# Right-handed Trefoil 3_1
c1 = Link.Crossing(1, 5, 2, 4)
c2 = Link.Crossing(3, 1, 4, 6)
c3 = Link.Crossing(5, 3, 6, 2)
c_list = [c1, c2, c3]

# Figure-eight 4_1
# c1 = Link.Crossing(1, 6, 2, 7)
# c2 = Link.Crossing(5, 2, 6, 3)
# c3 = Link.Crossing(3, 1, 4, 8)
# c4 = Link.Crossing(7, 5, 8, 4)
# c_list = [c1, c2, c3, c4]

# 5_1
# c1 = Link.Crossing(1, 6, 2, 7)
# c2 = Link.Crossing(7, 2, 8, 3)
# c3 = Link.Crossing(3, 8, 4, 9)
# c4 = Link.Crossing(9, 4, 10, 5)
# c5 = Link.Crossing(5, 10, 6, 1)
# c_list = [c1, c2, c3, c4, c5]

# 5_2
# c1 = Link.Crossing(1, 8, 2, 9)
# c2 = Link.Crossing(3, 6, 4, 7)
# c3 = Link.Crossing(5, 10, 6, 1)
# c4 = Link.Crossing(7, 2, 8, 3)
# c5 = Link.Crossing(9, 4, 10, 5)
# c_list = [c1, c2, c3, c4, c5]

# Hopf Link
# c1 = Link.Crossing(1, 3, 2, 4)
# c2 = Link.Crossing(4, 2, 3, 1)
# c_list = [c1, c2]

# 2-component unlink
# c1 = Link.Crossing(3, 1, 4, 2)
# c2 = Link.Crossing(4, 1, 3, 2)
# c_list = [c1, c2]

# unknot
# c1 = Link.Crossing(1, 2, 2, 1)
# c_list = [c1]

# 8_18
# c1 = Link.Crossing(1, 13, 2, 12)
# c2 = Link.Crossing(7, 2, 8, 3)
# c3 = Link.Crossing(3, 14, 4, 15)
# c4 = Link.Crossing(9, 5, 10, 4)
# c5 = Link.Crossing(5, 1, 6, 16)
# c6 = Link.Crossing(11, 6, 12, 7)
# c7 = Link.Crossing(13, 9, 14, 8)
# c8 = Link.Crossing(15, 10, 16, 11)
# c_list = [c1, c2, c3, c4, c5, c6, c7, c8]

# 8_19
# c1 = Link.Crossing(1, 13, 2, 12)
# c2 = Link.Crossing(3, 9, 4, 8)
# c3 = Link.Crossing(4, 16, 5, 15)
# c4 = Link.Crossing(6, 12, 7, 11)
# c5 = Link.Crossing(9, 1, 10, 16)
# c6 = Link.Crossing(10, 6, 11, 5)
# c7 = Link.Crossing(13, 3, 14, 2)
# c8 = Link.Crossing(14, 8, 15, 7)
# c_list = [c1, c2, c3, c4, c5, c6, c7, c8]

# Goeritz unknot
# c1 = Link.Crossing(2, 17, 3, 18)
# c2 = Link.Crossing(4, 15, 5, 16)
# c3 = Link.Crossing(7, 13, 8, 12)
# c4 = Link.Crossing(9, 21, 10, 20)
# c5 = Link.Crossing(11, 1, 12, 22)
# c6 = Link.Crossing(13, 7, 14, 6)
# c7 = Link.Crossing(14, 3, 15, 4)
# c8 = Link.Crossing(16, 5, 17, 6)
# c9 = Link.Crossing(18, 1, 19, 2)
# c10 = Link.Crossing(19, 9, 20, 8)
# c11 = Link.Crossing(21, 11, 22, 10)
# c_list = [c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11]

# LL_2(1)
# c1 = Link.Crossing(8, 1, 9, 2)
# c2 = Link.Crossing(2, 9, 3, 10)
# c3 = Link.Crossing(3, 17, 4, 18)
# c4 = Link.Crossing(4, 24, 5, 25)
# c5 = Link.Crossing(27, 5, 28, 6)
# c6 = Link.Crossing(20, 6, 21, 7)
# c7 = Link.Crossing(14, 7, 1, 8)
# c8 = Link.Crossing(10, 18, 11, 19)
# c9 = Link.Crossing(11, 25, 12, 26)
# c10 = Link.Crossing(26, 12, 27, 13)
# c11 = Link.Crossing(19, 13, 20, 14)
# c12 = Link.Crossing(22, 16, 23, 15)
# c13 = Link.Crossing(16, 24, 17, 23)
# c14 = Link.Crossing(28, 22, 15, 21)
# c_list = [c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13, c14]

# LLL(0)
# c1 = Link.Crossing(2, 9, 3, 10)
# c2 = Link.Crossing(3, 17, 4, 18)
# c3 = Link.Crossing(4, 26, 5, 27)
# c4 = Link.Crossing(8, 1, 9, 2)
# c5 = Link.Crossing(10, 18, 11, 19)
# c6 = Link.Crossing(11, 27, 12, 28)
# c7 = Link.Crossing(14, 7, 1, 8)
# c8 = Link.Crossing(16, 26, 17, 25)
# c9 = Link.Crossing(19, 13, 20, 14)
# c10 = Link.Crossing(20, 6, 21, 7)
# c11 = Link.Crossing(22, 31, 23, 32)
# c12 = Link.Crossing(24, 22, 15, 21)
# c13 = Link.Crossing(28, 12, 29, 13)
# c14 = Link.Crossing(29, 5, 30, 6)
# c15 = Link.Crossing(30, 23, 31, 24)
# c16 = Link.Crossing(32, 16, 25, 15)
# c_list = [c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13, c14, c15, c16]

# LL_1(0, 0)
# c1 = Link.Crossing(2, 9, 3, 10)
# c2 = Link.Crossing(3, 24, 4, 23)
# c3 = Link.Crossing(4, 26, 5, 27)
# c4 = Link.Crossing(8, 1, 9, 2)
# c5 = Link.Crossing(10, 23, 11, 22)
# c6 = Link.Crossing(11, 27, 12, 28)
# c7 = Link.Crossing(14, 7, 1, 8)
# c8 = Link.Crossing(16, 26, 17, 25)
# c9 = Link.Crossing(18, 15, 19, 16)
# c10 = Link.Crossing(20, 7, 21, 6)
# c11 = Link.Crossing(21, 14, 22, 13)
# c12 = Link.Crossing(24, 18, 25, 17)
# c13 = Link.Crossing(28, 12, 29, 13)
# c14 = Link.Crossing(29, 5, 30, 6)
# c15 = Link.Crossing(30, 19, 15, 20)
# c_list = [c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13, c14, c15]


def main():
    link = Link.Link(c_list)
    n_plus, n_minus = link.writhe()
    regions = link.regions()
    print("Link:", link)
    print("n_plus:", n_plus)
    print("n_minus:", n_minus)
    print("Regions:")
    for i in range(len(regions)):
        print(i, regions[i].nodes())
    outside = int(input("Outside: "))
    base_point = int(input("Base point: "))

    print("Annular Jones Polynomial:", annular_jones_polynomial(link, regions, outside, base_point))


main()
