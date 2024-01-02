import networkx as nx


class Crossing:
    def __init__(self, b1, b2, b3, b4):
        self.b1 = b1
        self.b2 = b2
        self.b3 = b3
        self.b4 = b4

    def __str__(self):
        return f"C[{self.b1}, {self.b2}, {self.b3}, {self.b4}]"

    def to_list(self):
        return [self.b1, self.b2, self.b3, self.b4]

    def handedness(self):
        return 1 if self.b2 - self.b4 == 1 or self.b4 - self.b2 > 1 else -1


def start_node(graph):
    for i in graph.in_degree:
        if i[1] == 0:
            return i[0]


def end_node(graph):
    for i in graph.out_degree:
        if i[1] == 0:
            return i[0]


class Link:
    def __init__(self, crossings):
        self.crossings = crossings

    def __str__(self):
        link_str = "["
        for crossing in self.crossings:
            link_str += crossing.__str__() + ", "
        if len(link_str) == 1:
            link_str += ", "
        link_str = link_str[:-2] + "]"
        return link_str

    def regions(self):
        regions = []
        states = []
        for crossing in self.crossings:
            crossing = crossing.to_list()
            for k in range(len(states)):
                if states[k] == 0:
                    states[k] = 1
            for i in range(4):
                j = i + 1
                if j > 3:
                    j -= 4
                a, b = -1, -1
                c, d = -1, -1
                for k in range(len(regions)):
                    if states[k] == 1:
                        if (crossing[i], 0) in regions[k].out_degree:
                            a = k
                        if (crossing[j], 0) in regions[k].in_degree:
                            b = k
                    if states[k] == 0:
                        if (crossing[i], 0) in regions[k].out_degree:
                            c = k
                        if (crossing[j], 0) in regions[k].in_degree:
                            d = k
                if a > -1 and b == -1:
                    if d > -1 and start_node(regions[a]) == end_node(regions[d]):
                        regions[a].add_nodes_from(regions[d].nodes)
                        regions[a].add_edge(crossing[i], crossing[j])
                        regions[a].add_edges_from(regions[d].edges)
                        states[a] = -1
                        del regions[d]
                        del states[d]
                    else:
                        regions[a].add_node(crossing[j])
                        regions[a].add_edge(crossing[i], crossing[j])
                        states[a] = 0
                if a == -1 and b > -1:
                    if c > -1 and start_node(regions[c]) == end_node(regions[b]):
                        regions[c].add_nodes_from(regions[b].nodes)
                        regions[c].add_edge(crossing[i], crossing[j])
                        regions[c].add_edges_from(regions[b].edges)
                        states[c] = -1
                        del regions[b]
                        del states[b]
                    else:
                        regions[b].add_node(crossing[i])
                        regions[b].add_edge(crossing[i], crossing[j])
                        states[b] = 0
                if a > -1 and b > -1:
                    if a == b:
                        regions[a].add_edge(crossing[i], crossing[j])
                        states[a] = -1
                    else:
                        regions[a].add_nodes_from(regions[b].nodes)
                        regions[a].add_edge(crossing[i], crossing[j])
                        regions[a].add_edges_from(regions[b].edges)
                        states[a] = 0
                        del regions[b]
                        del states[b]
                if a == -1 and b == -1:
                    if -1 < c == d > -1:
                        regions[c].add_edge(crossing[i], crossing[j])
                        states[c] = -1
                    else:
                        add_region = nx.DiGraph()
                        add_region.add_nodes_from([crossing[i], crossing[j]])
                        add_region.add_edge(crossing[i], crossing[j])
                        regions.append(add_region)
                        if crossing[i] == crossing[j]:
                            states.append(-1)
                        else:
                            states.append(0)
        return regions

    def writhe(self):
        writhe = [0, 0]
        repeat_dict = {}
        ignore_crossing_set = set()

        for i in range(len(self.crossings)):
            a = [self.crossings[i].b1, self.crossings[i].b3]
            b = [self.crossings[i].b2, self.crossings[i].b4]
            frozenset_a = frozenset(a)
            frozenset_b = frozenset(b)
            if frozenset_a not in repeat_dict:
                repeat_dict[frozenset_a] = [[-1], [1 if a[0] < a[1] else -1], [i]]
            else:
                repeat_dict[frozenset_a][0].append(-1)
                repeat_dict[frozenset_a][1].append(1 if a[0] < a[1] else -1)
                repeat_dict[frozenset_a][2].append(i)
                if i not in ignore_crossing_set:
                    if len(set(repeat_dict[frozenset_a][0])) != 1:
                        if len(set(repeat_dict[frozenset_a][1])) == 1:
                            writhe[0] += len(set(repeat_dict[frozenset_a][2]))
                        else:
                            writhe[1] += len(set(repeat_dict[frozenset_a][2]))
                    else:
                        writhe[0] += 1
                        writhe[1] += 1
                ignore_crossing_set = ignore_crossing_set | set(repeat_dict[frozenset_a][2])
            if frozenset_b not in repeat_dict:
                repeat_dict[frozenset_b] = [[1], [1 if b[0] < b[1] else -1], [i]]
            else:
                repeat_dict[frozenset_b][0].append(1)
                repeat_dict[frozenset_b][1].append(1 if b[0] < b[1] else -1)
                repeat_dict[frozenset_b][2].append(i)
                if i not in ignore_crossing_set:
                    if len(set(repeat_dict[frozenset_b][0])) != 1:
                        if len(set(repeat_dict[frozenset_b][1])) == 1:
                            writhe[0] += len(set(repeat_dict[frozenset_b][2]))
                        else:
                            writhe[1] += len(set(repeat_dict[frozenset_b][2]))
                    else:
                        writhe[0] += 1
                        writhe[1] += 1
                ignore_crossing_set = ignore_crossing_set | set(repeat_dict[frozenset_b][2])

        for i in range(len(self.crossings)):
            if i not in ignore_crossing_set:
                if self.crossings[i].handedness() == 1:
                    writhe[0] += 1
                else:
                    writhe[1] += 1

        return writhe
