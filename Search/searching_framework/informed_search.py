from sys import maxsize as infinity

from searching_framework.utils import Node, PriorityQueue

"""
Informed search in graphs
"""


def memoize(fn, slot=None):
    """ Remember the calculated value for any given list of arguments.
    If slot is specified, store the result in that slot as first argument.
    If slot is None, save the results in a dictionary.

    :param fn: assigned function
    :type fn: function
    :param slot: name of the attribute in which we store the results from the function
    :type slot: str
    :return: function with a modified logic for storing the results
    :rtype: function
    """
    if slot:
        def memoized_fn(obj, *args):
            if hasattr(obj, slot):
                return getattr(obj, slot)
            else:
                val = fn(obj, *args)
                setattr(obj, slot, val)
                return val
    else:
        def memoized_fn(*args):
            if args not in memoized_fn.cache:
                memoized_fn.cache[args] = fn(*args)
            return memoized_fn.cache[args]

        memoized_fn.cache = {}
    return memoized_fn


def best_first_graph_search(problem, f):
    """Look through the successors of a problem to find a goal.
     Use an evaluation function for deciding which neighbour is worth exploring.
     If two different paths reach the same state, use the better one.

    :param problem: assigned problem
    :type problem: Problem
    :param f: assigned function for evaluation
    :type f: function
    :return: Node or None
    :rtype: Node
    """
    f = memoize(f, 'f')
    node = Node(problem.initial)
    if problem.goal_test(node.state):
        return node
    frontier = PriorityQueue(min, f)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            return node
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                incumbent = frontier[child]
                if f(child) < f(incumbent):
                    del frontier[incumbent]
                    frontier.append(child)
    return None


def greedy_best_first_graph_search(problem, h=None):
    """ Greedy best-first search is executed if f(n) = h(n) is specified.

    :param problem: assigned problem
    :type problem: Problem
    :param h: assigned heuristic function
    :type h: function
    :return: Node or None
    """
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, h)


def astar_search(problem, h=None):
    """ A* search is best-first graph search where f(n) = g(n) + h(n).

    :param problem: assigned problem
    :type problem: Problem
    :param h: assigned heuristic function
    :type h: function
    :return: Node or None
    """
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n))


def recursive_best_first_search(problem, h=None):
    """Recursive best first search - it limits the recursion by
    following the f-value of the best alternative path
    from any ancestor Node (looking one step further).

    :param problem: assigned problem
    :type problem: Problem
    :param h: assigned heuristic function
    :type h: function
    :return: Node or None
    """
    h = memoize(h or problem.h, 'h')

    def RBFS(problem, node, flimit):
        if problem.goal_test(node.state):
            return node, 0  # (втората вредност е неважна)
        successors = node.expand(problem)
        if len(successors) == 0:
            return None, infinity
        for s in successors:
            s.f = max(s.path_cost + h(s), node.f)
        while True:
            # Подреди ги според најниската f вредност
            successors.sort(key=lambda x: x.f)
            best = successors[0]
            if best.f > flimit:
                return None, best.f
            if len(successors) > 1:
                alternative = successors[1].f
            else:
                alternative = infinity
            result, best.f = RBFS(problem, best, min(flimit, alternative))
            if result is not None:
                return result, best.f

    node = Node(problem.initial)
    node.f = h(node)
    result, bestf = RBFS(problem, node, infinity)
    return result