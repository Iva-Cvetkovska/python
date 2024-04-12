from constraint import *


def constraint_function(marija, simona, petar, meeting):
    simona_free_time = (13, 14, 16, 19)
    marija_free_time = (14, 15, 18)
    petar_free_time = (12, 13, 16, 17, 18, 19)

    if meeting not in simona_free_time or simona == 0 or (marija == 0 and petar == 0):
        return False
    if meeting not in marija_free_time and marija == 1:
        return False
    if meeting not in petar_free_time and petar == 1:
        return False

    return True


if __name__ == '__main__':
    problem = Problem(BacktrackingSolver())

    # --- Variables and domains ---
    problem.addVariable("Simona_attendance", [0, 1])
    problem.addVariable("Marija_attendance", [0, 1])
    problem.addVariable("Petar_attendance", [0, 1])
    problem.addVariable("Meeting_time", [12, 13, 14, 15, 16, 17, 18, 19])
    # -----------------------------

    # --- Constraints ---
    problem.addConstraint(constraint_function,
                          ("Marija_attendance", "Simona_attendance", "Petar_attendance", "Meeting_time"))
    # -------------------

    [print(solution) for solution in problem.getSolutions()]
    # solutions = problem.getSolutions()

    # for solution in solutions:
    #     reordered_solution = {'Simona_attendance': solution['Simona_attendance'],
    #                           'Marija_attendance': solution['Marija_attendance'],
    #                           'Petar_attendance': solution['Petar_attendance'],
    #                           'meeting_time': solution['Meeting_time']}
    #     print(reordered_solution)
