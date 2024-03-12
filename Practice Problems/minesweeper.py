def get_field_value(board, i, j):
    if board[i][j] == '#':
        return '#'

    board_size = len(board)

    if i == 0 and j == 0:
        return [board[i][j + 1], board[i + 1][j], board[i + 1][j + 1]].count(
            '#')  # CHECK right, bottom and bottom-right neighbours
    elif i == 0 and j == board_size - 1:
        return [board[i + 1][j], board[i][j - 1], board[i + 1][j - 1]].count(
            '#')  # CHECK bottom, left, bottom-left neighbours
    elif j == 0 and i == board_size - 1:
        return [board[i - 1][j], board[i][j + 1], board[i - 1][j + 1]].count(
            '#')  # CHECK top, right top-right neighbours
    elif j == board_size - 1 and i == board_size - 1:
        return [board[i][j - 1], board[i - 1][j], board[i - 1][j - 1]].count(
            '#')  # CHECK left, top and top-left neighbours
    elif i == 0:
        return [board[i + 1][j], board[i + 1][j - 1], board[i + 1][j + 1], board[i][j - 1], board[i][j + 1]].count(
            '#')  # DON'T CHECK top, top-left and top-right neighbours
    elif j == 0:
        return [board[i - 1][j], board[i - 1][j + 1], board[i + 1][j], board[i + 1][j + 1], board[i][j + 1]].count(
            '#')  # DON'T CHECK left, top-left and bottom-left neighbours
    elif i == board_size - 1:
        return [board[i - 1][j], board[i - 1][j - 1], board[i - 1][j + 1], board[i][j - 1], board[i][j + 1]].count(
            '#')  # DON'T CHECK bottom, bottom-right and bottom-left neighbours
    elif j == board_size - 1:
        return [board[i - 1][j], board[i - 1][j - 1], board[i + 1][j], board[i + 1][j - 1], board[i][j - 1]].count(
            '#')  # DON'T CHECK right, top-right and bottom-right neighbours
    else:
        return [board[i - 1][j], board[i - 1][j - 1], board[i - 1][j + 1], board[i + 1][j], board[i + 1][j - 1],
                board[i + 1][j + 1], board[i][j - 1], board[i][j + 1]].count(
            '#')  # CHECK ALL NEIGHBOURS


def minesweeper(board):
    # we need both row and column indexes
    board_size = len(board)
    solution = [[get_field_value(board, i, j) for j in range(board_size)] for i in range(board_size)]

    return solution


if __name__ == '__main__':
    N = int(input())  # size of the matrix NxN
    M = int(input())
    matrix = [input().split('   ') for row in range(N)]
    result = minesweeper(matrix)

    [print('   '.join(str(el) for el in row)) for row in result]
