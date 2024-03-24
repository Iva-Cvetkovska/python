from constraint import *

if __name__ == '__main__':
    N = 4
    problem = Problem()
    variables = range(N ** 2)
    domain = range(1, N ** 2 + 1)
    problem.addVariables(variables, domain)

    problem.addConstraint(AllDifferentConstraint(), variables)

    '''
    0   1   2   3
    4   5   6   7
    8   9   10  11
    12  13  14  15
    '''
    #  Each row needs to have a sum of 34
    for row in range(N):
        problem.addConstraint(ExactSumConstraint(34), [row * 4 + i for i in range(N)])
    #  Each column needs to have a sum of 34
    for col in range(N):
        problem.addConstraint(ExactSumConstraint(34), [col + 4 * i for i in range(N)])
    #  Values in both diagonals need to have a sum of 34
    problem.addConstraint(ExactSumConstraint(34), range(0, 16, 5))
    problem.addConstraint(ExactSumConstraint(34), range(3, 13, 3))

    solution = problem.getSolution()
    print(solution)
