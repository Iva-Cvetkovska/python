import math

from searching_framework.utils import Problem
from searching_framework.informed_search import astar_search


def move_house(x, direction, board_size):
    if x == board_size - 1:
        return x - 1, 'levo'
    if x == 0:
        return x + 1, 'desno'
    if direction == 'desno':
        return x + 1, 'desno'
    if direction == 'levo':
        return x - 1, 'levo'


class Climber(Problem):
    def __init__(self, allowed_pos, initial):
        super().__init__(initial)
        self.allowed_pos = allowed_pos
        self.possible_house_position = [(0, 8), (1, 8), (2, 8), (3, 8), (4, 8)]
        self.N = 5
        self.M = 9

    def successor(self, state):
        successors = dict()

        human_x, human_y = state[0]
        house_x, house_y = state[1]
        house_dir = state[-1]

        new_house_x, new_house_dir = move_house(house_x, house_dir, self.N)

        # Stoj
        successors['Stoj'] = ((human_x, human_y), (new_house_x, house_y), new_house_dir)

        # Gore 1
        new_y = human_y + 1
        if self.is_valid(human_x, new_y) or (human_x, new_y) == (new_house_x, house_y):
            successors['Gore 1'] = ((human_x, new_y), (new_house_x, house_y), new_house_dir)

        # Gore 2
        new_y = human_y + 2
        if self.is_valid(human_x, new_y) or (human_x, new_y) == (new_house_x, house_y):
            successors['Gore 2'] = ((human_x, new_y), (new_house_x, house_y), new_house_dir)

        # Gore-desno 1
        new_x, new_y = human_x + 1, human_y + 1
        if self.is_valid(new_x, new_y) or (new_x, new_y) == (new_house_x, house_y):
            successors['Gore-desno 1'] = ((new_x, new_y), (new_house_x, house_y), new_house_dir)

        # Gore-desno 2
        new_x, new_y = human_x + 2, human_y + 2
        if self.is_valid(new_x, new_y) or (new_x, new_y) == (new_house_x, house_y):
            successors['Gore-desno 2'] = ((new_x, new_y), (new_house_x, house_y), new_house_dir)

        # Gore-levo 1
        new_x, new_y = human_x - 1, human_y + 1
        if self.is_valid(new_x, new_y) or (new_x, new_y) == (new_house_x, house_y):
            successors['Gore-levo 1'] = ((new_x, new_y), (new_house_x, house_y), new_house_dir)

        # Gore-levo 2
        new_x, new_y = human_x - 2, human_y + 2
        if self.is_valid(new_x, new_y) or (new_x, new_y) == (new_house_x, house_y):
            successors['Gore-levo 2'] = ((new_x, new_y), (new_house_x, house_y), new_house_dir)

        return successors

    def is_valid(self, x, y):
        return 0 <= x < self.N and 0 <= y < self.M and (x, y) in self.allowed_pos

    def actions(self, state):
        return self.successor(state).keys()

    def result(self, state, action):
        return self.successor(state)[action]

    def goal_test(self, state):
        return state[0] == state[1]

    def h(self, node):
        human_cord = node.state[0]
        house_cord = node.state[1]
        return (house_cord[1] - human_cord[1])/2


if __name__ == '__main__':
    human = eval(input())
    house = eval(input())
    house_direction = input()
    allowed = [(1, 0), (2, 0), (3, 0), (1, 1), (2, 1), (0, 2), (2, 2), (4, 2), (1, 3), (3, 3), (4, 3), (0, 4), (2, 4),
               (2, 5), (3, 5), (0, 6), (2, 6), (1, 7), (3, 7)]

    climber = Climber(allowed, (human, house, house_direction))

    result = astar_search(climber)
    if result is None:
        print([])
    else:
        print(result.solution())
