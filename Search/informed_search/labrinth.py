from searching_framework.utils import Problem
from searching_framework.informed_search import astar_search


class Labrinth(Problem):
    def __init__(self, board_size, walls, initial, goal):
        super().__init__(initial, goal)
        self.board_size = board_size
        self.walls = walls

    def successor(self, state):
        successors = dict()

        human_x, human_y = state[0], state[1]

        # Right 2
        new_x = human_x + 2
        no_walls = self.no_walls_to_the_right(human_x, human_y, 2)
        if self.is_valid(new_x, human_y) and no_walls:
            successors['Right 2'] = (new_x, human_y)
        # Right 3
        new_x = human_x + 3
        no_walls = self.no_walls_to_the_right(human_x, human_y, 3)
        if self.is_valid(new_x, human_y) and no_walls:
            successors['Right 3'] = (new_x, human_y)
        # Up
        new_y = human_y + 1
        if self.is_valid(human_x, new_y):
            successors['Up'] = (human_x, new_y)
        # Down
        new_y = human_y - 1
        if self.is_valid(human_x, new_y):
            successors['Down'] = (human_x, new_y)
        # Left
        new_x = human_x - 1
        if self.is_valid(new_x, human_y):
            successors['Left'] = (new_x, human_y)

        return successors

    def no_walls_to_the_right(self, x, y, moves):
        for move in range(1, moves + 1):
            if (x + move, y) in self.walls:
                return False
        return True

    def is_valid(self, x, y):
        return 0 <= x < self.board_size and 0 <= y < self.board_size and (x, y) not in self.walls

    def actions(self, state):
        return self.successor(state).keys()

    def result(self, state, action):
        return self.successor(state)[action]

    def h(self, node):
        human_x, human_y = node.state[0], node.state[1]
        house_x, house_y = self.goal[0], self.goal[1]
        if house_x <= human_x:
            return abs(human_x - house_x) + abs(human_y - house_y)
        else:
            return (house_x - human_x)/3


if __name__ == '__main__':
    N = int(input())
    num_walls = int(input())
    wall_positions = [eval(input()) for i in range(num_walls)]
    human_cord = eval(input())
    house_cord = eval(input())

    labrinth = Labrinth(N, wall_positions, human_cord, house_cord)

    result = astar_search(labrinth)
    if result is None:
        print([])
    else:
        print(result.solution())
