import itertools

from constraint import *


def check_row_and_column(r1, r2):
    r1_x, r1_y = r1[0], r1[1]
    r2_x, r2_y = r2[0], r2[1]
    return r1_x != r2_x and r1_y != r2_y


def check_column(r1, r2):
    return r1 != r2


if __name__ == '__main__':
    N = 8
    problem = Problem()

    # Solution 1:
    # variables = ['R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8']
    # domain = [(i, j) for j in range(N) for i in range(N)]
    # problem.addVariables(variables, domain)
    # pairs = list(itertools.combinations(variables, 2))
    # for pair in pairs:
    #     problem.addConstraint(check_row_and_column, pair)

    # Solution 2:
    variables = range(N)  # Each number represent the row that the rook is placed at
    domain = range(N)
    problem.addVariables(variables, domain)
    pairs = list(itertools.combinations(variables, 2))
    for pair in pairs:
        # AddConstraint sends the domain of the variable as a function argument
        problem.addConstraint(check_column, pair)

    # Solution 3::
    # problem.addConstraint(AllDifferentConstraint(), variables)

    solution = problem.getSolution()
    print(solution)
