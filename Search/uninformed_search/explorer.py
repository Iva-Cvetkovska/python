from searching_framework.utils import Problem
from searching_framework.uninformed_search import *


def move_obstacle(obstacle, grid_size):
    if obstacle[2] == 1:  # up
        if obstacle[1] == grid_size[1] - 1:  # reached the top of the board
            obstacle[2] = -1
            obstacle[1] -= 1
        else:
            obstacle[1] += 1
    else:  # down
        if obstacle[1] == 0:
            obstacle[2] = 1
            obstacle[1] += 1
        else:
            obstacle[1] -= 1
    return obstacle


class Explorer(Problem):
    def __init__(self, initial, goal=None):
        super().__init__(initial, goal)
        self.grid_size = [8, 6]

    def successor(self, state):
        # n = -1 (down), n = 1 (up)
        # state = (x, y, (p1, p2, n1), (p1, p2, n2))
        successors = dict()

        man_x = state[0]
        man_y = state[1]

        obstacle1 = list(state[2])
        obstacle2 = list(state[3])

        obstacle1 = move_obstacle(obstacle1, self.grid_size)
        obstacle2 = move_obstacle(obstacle2, self.grid_size)

        obstacles = [(obstacle1[0], obstacle1[1]), (obstacle2[0], obstacle2[1])]

        # right, x = x + 1
        if man_x < self.grid_size[0] and (man_x + 1, man_y) not in obstacles:
            successors["Right"] = (man_x + 1, man_y, tuple(obstacle1), tuple(obstacle2))

        # left, x = x - 1
        if man_x > 0 and (man_x - 1, man_y) not in obstacles:
            successors["Left"] = (man_x - 1, man_y, tuple(obstacle1), tuple(obstacle2))

        # up, y = y + 1
        if man_y < self.grid_size[1] and (man_x, man_y + 1) not in obstacles:
            successors["Up"] = (man_x, man_y + 1, tuple(obstacle1), tuple(obstacle2))

        # down, y = y - 1
        if man_y > 0 and (man_x, man_y - 1) not in obstacles:
            successors["Down"] = (man_x, man_y - 1, tuple(obstacle1), tuple(obstacle2))

        return successors

    def actions(self, state):
        return self.successor(state).keys()

    def result(self, state, action):
        return self.successor(state)[action]

    def goal_test(self, state):
        return state[0] == self.goal[0] and state[1] == self.goal[1]


if __name__ == '__main__':
    initial_state = (0, 2)
    goal_state = (7, 4)
    obstacle_1 = (2, 5, -1)
    obstacle_2 = (5, 0, 1)
    explorer = Explorer((initial_state[0], initial_state[1], obstacle_1, obstacle_2), goal_state)

    result = breadth_first_graph_search(explorer)
    print(result.solution())
