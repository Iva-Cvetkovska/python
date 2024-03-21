from searching_framework.utils import Problem
from searching_framework.informed_search import *


def switch(orientation):
    if orientation == 'W':
        return "E"
    else:
        return "W"


def is_valid(state):
    farmer, cabbage, wolf, goat = state
    if wolf == goat and farmer != wolf:
        return False
    if goat == cabbage and farmer != goat:
        return False
    return True


class RiverCrossingPuzzle(Problem):
    def __init__(self, initial, goal):
        super().__init__(initial, goal)

    def successor(self, state):
        successors = dict()

        farmer, cabbage, wolf, goat = state

        # Farmer switches side
        new_state = (switch(farmer), cabbage, wolf, goat)
        if is_valid(new_state):
            successors["Farmer switches sides"] = new_state

        # Farmer carries the wolf
        if farmer == wolf:
            new_state = (switch(farmer), cabbage, switch(wolf), goat)
            if is_valid(new_state):
                successors["Farmer carries the wolf"] = new_state

        # Farmer carries the goat
        if farmer == goat:
            new_state = (switch(farmer), cabbage, wolf, switch(goat))
            if is_valid(new_state):
                successors["Farmer carries the goat"] = new_state

        # Farmer carries the cabbage
        if farmer == cabbage:
            new_state = (switch(farmer), switch(cabbage), wolf, goat)
            if is_valid(new_state):
                successors["Farmer carries the cabbage"] = new_state

        return successors

    def actions(self, state):
        return self.successor(state).keys()

    def result(self, state, action):
        return self.successor(state)[action]

    def h(self, node):
        counter = 0
        for state, goal in zip(node.state, self.goal):
            if state != goal:
                counter += 1
        return counter


if __name__ == '__main__':
    # E stands for East and W for West
    river_crossing_puzzle = RiverCrossingPuzzle(("E", "E", "E", "E"), ("W", "W", "W", "W"))
    result = astar_search(river_crossing_puzzle)
    print(result.solution())
