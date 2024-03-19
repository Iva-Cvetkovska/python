from searching_framework.utils import Problem
from searching_framework.informed_search import *


class SlidingPuzzle(Problem):
    def __init__(self, initial, goal):
        super().__init__(initial, goal)
        self.board_size = 3

    def successor(self, state):
        """
        state = '*32415678'
            0 1 2
            3 4 5
            6 7 8
        """
        # successors = dict()
        successors: dict[str, str] = {}
        i = state.index('*')  # Find the index of the star

        # Up i - 3, i
        """
            Basically, in order to move up, it would have to go 3 indexes to the left of where it is
            there are 3 indexes before 6 in order to reach 3. So, if the star is at 6, then 6 - 3 gets it to 3, 
            which is above the 6.
        """
        if i >= 3:
            temp = list(state)
            temp[i], temp[i - 3] = temp[i - 3], temp[i]
            new_state = ''.join(temp)
            successors["Up"] = new_state
        # Down
        if i <= 5:
            temp = list(state)
            temp[i], temp[i + 3] = temp[i + 3], temp[i]
            new_state = ''.join(temp)
            successors["Down"] = new_state
        # Left
        if i % 3 != 0:
            temp = list(state)
            temp[i], temp[i - 1] = temp[i - 1], temp[i]
            new_state = ''.join(temp)
            successors["Left"] = new_state
        # Right
        if i % 3 != 2:
            temp = list(state)
            temp[i], temp[i + 1] = temp[i + 1], temp[i]
            new_state = ''.join(temp)
            successors["Right"] = new_state

        return successors

    def actions(self, state):
        return self.successor(state).keys()

    def result(self, state, action):
        return self.successor(state)[action]

    def h(self, node):
        """
        a = [1, 2 , 3], b = [a, b, c]
        zip(a, b) = [(1, a), (2, b), (3, c)]
        """
        # Heuristic: How many fields are displaced?
        counter = 0
        for x, y in zip(node.state, self.goal):
            if x != y:
                counter += 1
        return counter


if __name__ == '__main__':
    sliding_puzzle = SlidingPuzzle('*32415678', '*12345678')
    result = astar_search(sliding_puzzle)
    print(result.solve())
