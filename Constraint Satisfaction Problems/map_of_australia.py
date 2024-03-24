from constraint import *


def different(a, b):
    return a != b


if __name__ == '__main__':
    problem = Problem()

    variables = ['WA', 'NT', 'SA', 'Q', 'NSW', 'V', 'T']
    domain = ['red', 'green', 'blue']
    neighbours = [('WA', 'NT'), ('WA', 'SA'), ('SA', 'NSW'), ('SA', 'Q'), ('NT', 'Q'), ('Q', 'NSW'), ('NSW', 'V')]

    problem.addVariables(variables, domain)

    # Add constraint for each pair of neighbour nodes
    for pair in neighbours:
        problem.addConstraint(different, pair)

    # Get all possible solutions
    solutions = problem.getSolutions()
    print(solutions)
