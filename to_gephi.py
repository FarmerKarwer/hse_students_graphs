import pickle
import csv


def tie_friends_students():
    """
    Execute to tie students with their friends (writes a dictionary)
    """
    with open("all_students.pickle", "rb") as f1:
        all_students = pickle.load(f1)

    with open("friends_only.pickle", "rb") as f2:
        friends_only = pickle.load(f2)

    student_ids = tuple(all_students.keys())

    final_file = dict()

    for stid in student_ids:
        fr_count = friends_only[stid]["count"]
        friends = friends_only[stid]["friends"]
        pre_dictionary = all_students[stid]
        pre_dictionary.update({"fr_count": fr_count, "friends": friends})

    with open("tie_friends_students.pickle", "wb") as f3:
        pickle.dump(final_file, f3)



def create_nodes(students_objects):
    """
    Creates nodes for Gephi

    :param students_objects: list of students objects
    """

    heading = ["id", "major", "name", "surname", "gender", "year", 'gr_count', 'fr_count']
    _students = []
    name = "students_nodes.csv"

    # drag only necessary parameters from each student_object, then put them into a tuple
    for student in students_objects:
        _students.append((student.id_, student.major, student.name, student.surname,
                          student.gender, student.year, student.fr_count)
                         )
    # write it as a csv
    write_file(heading=heading, file=_students, name=name)


def create_edges(students_objects):
    network = []
    all_ids = set([i.id_ for i in students_objects])  # get list of all the students' ids

    for student in students_objects:
        friend_list = student.friends

        if friend_list:  # if list of friends isn't empty
            for friend in friend_list:
                friend_id = str(friend['id'])
                student_id = student.id_
                if friend_id in all_ids:  # we only add connections between students, not any people
                    network.append((student_id, friend_id))

    heading = ["Source", "Target"]
    write_file(heading=heading, file=network, name="students_edges.csv")


class Student:
    all_students = []

    def __init__(self, id_, major, name, surname, gender,
                 year, friends, fr_count):
        self.id_ = str(id_)
        self.major = major
        self.name = name
        self.surname = surname
        self.gender = gender
        self.year = str(year)
        self.friends = friends
        self.fr_count = str(fr_count)


def write_file(heading, file, name):
    """
    This function writes an iterable object to a .CSV file

    :param heading: header
    :param file: iterable object containing parameters
    :param name: name of the file
    """
    with open(name, "w", newline='', encoding='UTF-8') as f:
        writer = csv.writer(f)
        writer.writerow(heading)
        for student in file:
            writer.writerow(student)


def add_students():
    """
    This function gets parameters of each students to form a Student object for further manipulation
    """
    with open("tie_friends_students.pickle", "rb") as f1:
        students = pickle.load(f1)

    ids = tuple(students.keys())
    for uid in ids:
        current_st = students[uid]
        temp_student = Student(id_=current_st["id"], major=current_st["major"], name=current_st["name"],
                               surname=current_st["surname"], gender=current_st["gender"], year=current_st["year"],
                               friends=current_st["friends"], fr_count=current_st["fr_count"])
        Student.all_students.append(temp_student)


# BEGIN

add_students()  # create students as objects
create_nodes(Student.all_students)  # create nodes
create_edges(Student.all_students)  # create edges
