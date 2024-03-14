from searching_framework.utils import Problem
from searching_framework.uninformed_search import *


def move_forward(x, y, orientation):
    if orientation == 'S':
        return x, y - 1
    elif orientation == 'N':
        return x, y + 1
    elif orientation == 'E':
        return x + 1, y
    else:
        return x - 1, y


def turn_right(x, y, orientation):
    if orientation == 'S':
        return x - 1, y, 'W'
    elif orientation == 'N':
        return x + 1, y, 'E'
    elif orientation == 'E':
        return x, y - 1, 'S'
    else:
        return x, y + 1, 'N'


def turn_left(x, y, orientation):
    if orientation == 'S':
        return x + 1, y, 'E'
    elif orientation == 'N':
        return x - 1, y, 'W'
    elif orientation == 'E':
        return x, y + 1, 'N'
    else:
        return x, y - 1, 'S'


class Snake(Problem):
    def __init__(self, red_apples_pos, initial, goal=None):
        super().__init__(initial, goal)
        self.red_apples = red_apples_pos
        self.board_size = 10

    def successor(self, state):
        successors = dict()

        snake_position = list(state[0])
        orientation = state[1]
        green_apples_pos = list(state[-1])

        # MoveForward
        new_x, new_y = move_forward(snake_position[-1][0], snake_position[-1][1], orientation)
        if self.is_valid(new_x, new_y, snake_position):
            new_snake = snake_position.copy()
            new_snake.append((new_x, new_y))
            if (new_x, new_y) in green_apples_pos:
                successors['MoveForward'] = (tuple(new_snake), orientation,
                                                tuple([ga for ga in green_apples_pos if ga[0] != new_x or ga[1] != new_y]))
            else:
                new_snake.pop(0)
                successors['MoveForward'] = (tuple(new_snake), orientation, tuple(green_apples_pos))

        # TurnRight
        new_x, new_y, new_orientation = turn_right(snake_position[-1][0], snake_position[-1][1], orientation)
        if self.is_valid(new_x, new_y, snake_position):
            new_snake = snake_position.copy()
            new_snake.append((new_x, new_y))
            if (new_x, new_y) in green_apples_pos:
                successors['TurnRight'] = (tuple(new_snake), new_orientation,
                                            tuple([ga for ga in green_apples_pos if ga[0] != new_x or ga[1] != new_y]))
            else:
                new_snake.pop(0)
                successors['TurnRight'] = (tuple(new_snake), new_orientation, tuple(green_apples_pos))

        # TurnLeft
        new_x, new_y, new_orientation = turn_left(snake_position[-1][0], snake_position[-1][1], orientation)
        if self.is_valid(new_x, new_y, snake_position):
            new_snake = snake_position.copy()
            new_snake.append((new_x, new_y))
            if (new_x, new_y) in green_apples_pos:
                successors['TurnLeft'] = (tuple(new_snake), new_orientation,
                                           tuple([ga for ga in green_apples_pos if ga[0] != new_x or ga[1] != new_y]))
            else:
                new_snake.pop(0)
                successors['TurnLeft'] = (tuple(new_snake), new_orientation, tuple(green_apples_pos))

        return successors

    def is_valid(self, x, y, snake_pos):
        return (0 <= x < self.board_size and 0 <= y < self.board_size and (x, y) not in self.red_apples and
                (x, y) not in snake_pos)

    def actions(self, state):
        return self.successor(state).keys()

    def result(self, state, action):
        return self.successor(state)[action]

    def goal_test(self, state):
        return len(state[-1]) == 0


if __name__ == '__main__':
    num_green_apples = int(input())
    green_apples = [eval(input()) for _ in range(num_green_apples)]

    num_red_apples = int(input())
    red_apples = [eval(input()) for _ in range(num_red_apples)]

    snake = Snake(red_apples, (((0, 9), (0, 8), (0, 7)), 'S', tuple(green_apples)))
    result = breadth_first_graph_search(snake)

    print(result.solution())
