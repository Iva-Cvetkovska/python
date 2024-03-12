def calculate_grade(subjects):
    grades = []
    for subject in subjects:
        total_points = subject[1] + subject[2] + subject[3]
        if 0 <= total_points <= 50:
            grade = 5
        elif 50 < total_points <= 60:
            grade = 6
        elif 60 < total_points <= 70:
            grade = 7
        elif 70 < total_points <= 80:
            grade = 8
        elif 80 < total_points <= 90:
            grade = 9
        else:
            grade = 10
        grades.append(f'{subject[0]}: {grade}')
    return '\n----'.join(str(grade) for grade in grades)


if __name__ == '__main__':
    students = dict()
    entry = input()

    while entry != 'end':
        name, surname, index, subject_name, points_for_theory, points_for_practical_part, points_for_labs = entry.split(
            ',')
        if index in students:
            students[index]['subjects'].append((subject_name, int(points_for_theory), int(points_for_practical_part),
                                                int(points_for_labs)))
        else:
            students[index] = {'name': name, 'surname': surname,
                               'subjects': [(subject_name, int(points_for_theory), int(points_for_practical_part),
                                             int(points_for_labs))]}
        entry = input()

    for student in students.values():
        grades_per_subject = calculate_grade(student["subjects"])

        print(f"""Student: {student['name']} {student['surname']}
----{grades_per_subject}\n""")


