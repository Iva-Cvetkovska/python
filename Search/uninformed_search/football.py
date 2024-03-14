from searching_framework.utils import Problem
from searching_framework.uninformed_search import *


class Football(Problem):
    def __init__(self, initial, goal):
        super().__init__(initial, goal)
        self.N = 8
        self.M = 6
        self.enemies = ((3, 3), (5, 4))
        self.enemy_neighbours = (
            (2, 2), (2, 3), (2, 4), (3, 2), (3, 4), (4, 2), (4, 3), (4, 4), (4, 5), (5, 3), (5, 5), (6, 3), (6, 4),
            (6, 5))

    def successor(self, state):
        successors = dict()

        hx, hy = state[0][0], state[0][1]
        bx, by = state[1][0], state[1][1]

        # Up
        new_x, new_y = hx, hy + 1
        if self.check_player_position(new_x, new_y):
            new_bx, new_by = bx, by + 1
            if (new_x, new_y) == (bx, by) and self.check_ball_position(new_bx, new_by):
                successors['Push the ball up'] = ((new_x, new_y), (new_bx, new_by))
            else:
                successors['Move the player up'] = ((new_x, new_y), (bx, by))

        # Down
        new_x, new_y = hx, hy - 1
        if self.check_player_position(new_x, new_y):
            new_bx, new_by = bx, by - 1
            if (new_x, new_y) == (bx, by) and self.check_ball_position(new_bx, new_by):
                successors['Push the ball down'] = ((new_x, new_y), (new_bx, new_by))
            else:
                successors['Move the player down'] = ((new_x, new_y), (bx, by))

        # Right
        new_x, new_y = hx + 1, hy
        if self.check_player_position(new_x, new_y):
            new_bx, new_by = bx + 1, by
            if (new_x, new_y) == (bx, by) and self.check_ball_position(new_bx, new_by):
                successors['Push the ball right'] = ((new_x, new_y), (new_bx, new_by))
            else:
                successors['Move the player right'] = ((new_x, new_y), (bx, by))

        # Up-right diagonally
        new_x, new_y = hx + 1, hy + 1
        if self.check_player_position(new_x, new_y):
            new_bx, new_by = bx + 1, by + 1
            if (new_x, new_y) == (bx, by) and self.check_ball_position(new_bx, new_by):
                successors['Push the ball diagonally up-right'] = ((new_x, new_y), (new_bx, new_by))
            else:
                successors['Move the player diagonally up-right'] = ((new_x, new_y), (bx, by))

        # Down-right diagonally
        new_x, new_y = hx + 1, hy - 1
        if self.check_player_position(new_x, new_y):
            new_bx, new_by = bx + 1, by - 1
            if (new_x, new_y) == (bx, by) and self.check_ball_position(new_bx, new_by):
                successors['Push the ball diagonally down-right'] = ((new_x, new_y), (new_bx, new_by))
            else:
                successors['Move the player diagonally down-right'] = ((new_x, new_y), (bx, by))

        return successors

    def check_player_position(self, x, y):
        return 0 <= x < self.N and 0 <= y < self.M and (x, y) not in self.enemies

    def check_ball_position(self, x, y):
        return 0 <= x < self.N and 0 <= y < self.M and (x, y) not in self.enemy_neighbours

    def actions(self, state):
        return self.successor(state).keys()

    def result(self, state, action):
        return self.successor(state)[action]

    def goal_test(self, state):
        return state[1] in self.goal


if __name__ == '__main__':
    human = eval(input())
    ball = eval(input())

    football = Football((human, ball), ((7, 2), (7, 3)))
    result = breadth_first_graph_search(football)

    print(result.solution())
