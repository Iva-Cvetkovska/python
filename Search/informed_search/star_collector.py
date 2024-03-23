import random
from searching_framework.utils import Problem
from searching_framework.informed_search import *


def check_for_visited_edges(current_node, adjacent_node, visited_edges):
    x, y = current_node[0], current_node[1]
    new_x, new_y = adjacent_node[0], adjacent_node[1]
    current_node_key = str(x) + str(y)
    adjacent_node_key = str(new_x) + str(new_y)

    if (adjacent_node_key in visited_edges and current_node in visited_edges[adjacent_node_key]) or (
            current_node_key in visited_edges and adjacent_node in visited_edges[current_node_key]):
        return True, tuple(visited_edges.items())

    if current_node_key not in visited_edges:
        visited_edges[current_node_key] = (adjacent_node,)
    else:
        visited_edges[current_node_key] += (adjacent_node,)

    if adjacent_node_key not in visited_edges:
        visited_edges[adjacent_node_key] = (current_node,)
    else:
        visited_edges[adjacent_node_key] += (current_node,)

    return False, tuple(visited_edges.items())


class StarCollector(Problem):

    def __init__(self, initial):
        super().__init__(initial)
        self.board_size = 4
        self.starting_positions = [(1, 1), (1, 2), (2, 1), (2, 2)]
        self.restricted_move_up = ((3, 1), (0, 1))
        self.restricted_move_down = ((0, 2), (3, 2))
        self.restricted_move_left = ((2, 3), (2, 0))
        self.restricted_move_right = ((1, 0), (1, 3))

    def successor(self, state):
        successors = dict()
        goal = list(state[-1])

        if state[0] == -1:
            for s_p in self.starting_positions:
                successors[f"The explorer starts at position: {s_p}"] = (
                    s_p, (), tuple(goal))
            return successors

        human_x, human_y = state[0][0], state[0][1]
        visited_edges = {key: value for key, value in state[1]}

        # Up
        new_y = human_y + 1
        if self.is_valid(human_x, new_y) and (human_x, human_y) not in self.restricted_move_up:
            visited, mapped_edges = check_for_visited_edges((human_x, human_y), (human_x, new_y), visited_edges)
            if not visited:
                successors['Move up'] = (
                    (human_x, new_y), mapped_edges, tuple([s for s in goal if s[0] != human_x or s[1] != new_y]))

        # Down
        new_y = human_y - 1
        if self.is_valid(human_x, new_y) and (human_x, human_y) not in self.restricted_move_down:
            visited, mapped_edges = check_for_visited_edges((human_x, human_y), (human_x, new_y), visited_edges)
            if not visited:
                successors['Move down'] = (
                    (human_x, new_y), mapped_edges, tuple([s for s in goal if s[0] != human_x or s[1] != new_y]))

        # Left
        new_x = human_x - 1
        if self.is_valid(new_x, human_y) and (human_x, human_y) not in self.restricted_move_left:
            visited, mapped_edges = check_for_visited_edges((human_x, human_y), (new_x, human_y), visited_edges)
            if not visited:
                successors['Move left'] = (
                    (new_x, human_y), mapped_edges, tuple([s for s in goal if s[0] != new_x or s[1] != human_y]))

        # Right
        new_x = human_x + 1
        if self.is_valid(new_x, human_y) and (human_x, human_y) not in self.restricted_move_right:
            visited, mapped_edges = check_for_visited_edges((human_x, human_y), (new_x, human_y), visited_edges)
            if not visited:
                successors['Move right'] = (
                    (new_x, human_y), mapped_edges, tuple([s for s in goal if s[0] != new_x or s[1] != human_y]))

        # Diagonally down-right
        if (human_x, human_y) == (1, 2):
            new_x, new_y = human_x + 1, human_y - 1
            if self.is_valid(new_x, new_y):
                visited, mapped_edges = check_for_visited_edges((human_x, human_y), (new_x, new_y), visited_edges)
                if not visited:
                    successors['Move diagonally down-right'] = (
                        (new_x, new_y), mapped_edges, tuple([s for s in goal if s[0] != new_x or s[1] != new_y]))

        # Diagonally up-left
        if (human_x, human_y) == (2, 1):
            new_x, new_y = human_x - 1, human_y + 1
            if self.is_valid(new_x, new_y):
                visited, mapped_edges = check_for_visited_edges((human_x, human_y), (new_x, new_y), visited_edges)
                if not visited:
                    successors['Move diagonally up-left'] = (
                        (new_x, new_y), mapped_edges, tuple([s for s in goal if s[0] != new_x or s[1] != new_y]))

        return successors

    def actions(self, state):
        return self.successor(state).keys()

    def result(self, state, action):
        return self.successor(state)[action]

    def goal_test(self, state):
        return len(state[-1]) == 0

    def is_valid(self, x, y):
        return 0 <= x < self.board_size and 0 <= y < self.board_size

    def h(self, node):
        if node.state[0] == -1:
            return 10
        human_x, human_y = node.state[0][0], node.state[0][1]
        goal = node.state[-1]
        value = 0
        for star in goal:
            value += abs(human_x - star[0]) + abs(human_y - star[1])
        return value


if __name__ == '__main__':
    star_collector = StarCollector((-1, (), ((3, 0), (0, 3))))
    result = astar_search(star_collector)
    print(result.solution())
