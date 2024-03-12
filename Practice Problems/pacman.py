import random


class Player:
    def __init__(self, state=None):
        if state is None:
            state = [0, 0]
        self.state = state

    def move(self, position):
        self.state[0] = position[0]
        self.state[1] = position[1]
        print(self.state)


class Game:
    def __init__(self, board, food):
        self.board = board
        self.food = food


def get_neighbors(rows, cols, i, j, food):
    neighbors = []

    offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for offset_i, offset_j in offsets:
        neighbor_i = i + offset_i
        neighbor_j = j + offset_j

        # Check if the neighbor position is within the bounds of the matrix
        if 0 <= neighbor_i < rows and 0 <= neighbor_j < cols:
            if (neighbor_i, neighbor_j) in food:
                return [(neighbor_i, neighbor_j)]
            else:
                neighbors.append((neighbor_i, neighbor_j))

    return neighbors


class Pacman:
    def __init__(self, player, matrix):
        self.player = player
        self.board = matrix.board
        self.food = matrix.food

    def play_game(self):  # Game logic
        while len(food_position):
            i, j = self.player.state[0], self.player.state[1]
            neighbors = get_neighbors(len(self.board), len(self.board[0]), i, j, self.food)

            if len(neighbors) == 1:  # If only one element is in the array then certainly it has food
                self.player.move(neighbors[0])
                self.food.remove(neighbors[0])
            else:
                random_position = random.randint(0, len(neighbors) - 1)
                self.player.move(neighbors[random_position])


if __name__ == '__main__':
    N = int(input())
    M = int(input())
    matrix = [list(input()) for i in range(N)]
    food_position = [(i, j) for i in range(N) for j in range(M) if matrix[i][j] == '.']
    print(food_position)
    print(matrix)

    player = Player()  # default position is (0, 0)
    game = Game(matrix, food_position)

    pacman = Pacman(player, game)
    pacman.play_game()
