from vk_api_local import vk1
import pickle

vostokovedine = {"year5": "https://vk.com/as2016hse",
                 "year4": "https://vk.com/asianstudies2017",
                 "year3": "https://vk.com/asianstudies2018",
                 "year2": "https://vk.com/asianstudies2019",
                 "year1": "https://vk.com/oriental25"}

design = {"year3": "https://vk.com/club168623995",
          "year2": "https://vk.com/designers_19_20",
          "year1": "https://vk.com/hsedesign2021"}

history = {"year5": "https://vk.com/sthistorians1620",
           "year4": "https://vk.com/sthistorians1721",
           "year3": "https://vk.com/histfaq1822",
           "year2": "https://vk.com/histfaq1924",
           "year1": "https://vk.com/historia2025"}

politics = {"year4": "https://vk.com/politscience2017",
            "year3": "https://vk.com/politfox18",
            "year2": "https://vk.com/politfox19",
            "year1": "https://vk.com/polit_foxes"}

sociology = {"year4": "https://vk.com/hsespb_sociology_17",
             "year3": "https://vk.com/sedova1822",
             "year2": "https://vk.com/sedova1923",
             "year1": "https://vk.com/sasi2024"}

logistics = {"year4": "https://vk.com/logistician2017",
             "year3": "https://vk.com/fromcuratorswithlove",
             "year2": "https://vk.com/logistics2019",
             "year1": "https://vk.com/logistics2024"}

management = {"year4": "https://vk.com/hse_spb_management_2017_2021",
              "year3": "https://vk.com/hse_management18_22",
              "year2": "https://vk.com/hse_management19_23",
              "year1": "https://vk.com/hse_management20_24"}

uags = {"year4": "https://vk.com/waaaags",
        "year3": "https://vk.com/uags1822",
        "year2": "https://vk.com/uags_2019",
        "year1": "https://vk.com/uagstut"}

economics = {"year4": "https://vk.com/becon2017",
             "year3": "https://vk.com/becon2018",
             "year2": "https://vk.com/becon2019",
             "year1": "https://vk.com/becon2020"}

law = {"year4": "https://vk.com/hselawyers",
       "year3": "https://vk.com/ius_team",
       "year2": "https://vk.com/iushse",
       "year1": "https://vk.com/iushse20"}

philology = {"year4": "https://vk.com/philologhse",
             "year3": "https://vk.com/philologyhse",
             "year2": "https://vk.com/philologyofhse",
             "year1": "https://vk.com/hsephilology20"}

hse = (vostokovedine, design, history, politics, sociology, logistics,
       management, uags, economics, law, philology)

majors = ('vostokovedine', 'design', 'history', 'politics', 'sociology', 'logistics',
          'management', 'uags', 'economics', 'law', 'philology')


def extract_all_groups():
    # get all subscribers of all groups
    all_students = []

    for i, major in enumerate(majors):

        all_courses = list(hse[i].items())
        for course in all_courses:
            year = int(course[0].split("year")[1])

            grid = course[1].split("vk.com/")[-1]

            if "club" in course[1]:
                grid = course[1].split("vk.com/club")[-1]

            students_local = vk1.groups.getMembers(
                group_id=grid, offset=0, count=1000, fields="sex, bdate, city, education")['items']

            contacts_here = vk1.groups.getById(group_id=grid, fields="contacts")[0]['contacts']

            gr_key = ''.join([major, str(year)])
            all_students.append({gr_key: {"students": students_local, "contacts": contacts_here}})
    with open("all_students_raw.pickle", 'wb') as f:
        pickle.dump(all_students, f)


class Student:
    def __init__(self, major, stid, name, surname, gender, year, in_contacts):
        self.major = major
        self.stid = stid
        self.name = name
        self.surname = surname
        self.gender = gender
        self.year = year
        self.in_contacts = in_contacts


def final_students():
    with open("all_students_raw.pickle", "rb") as f:
        all_students_raw = pickle.load(f)
    list_students = []

    # {stid: [op_n, op_n]}
    all_students_dict = dict()

    all_contacts_dict = dict()

    undefined_students = dict()

    for program_course in all_students_raw:
        # get a list of students
        key = list(program_course.keys())[0]
        students = program_course[key]['students']
        for student in students:
            stid = student['id']
            try:
                all_students_dict[stid].append(key)
            except KeyError:
                all_students_dict.update({stid: [key]})

        try:
            # create a list of those mentioned in the "contacts" section
            contacts = program_course[key]['contacts']
            for contact in contacts:
                contactid = contact['user_id']
                try:
                    all_contacts_dict[contactid].append(key)
                except KeyError:
                    all_contacts_dict.update({contactid: [key]})
        except KeyError:
            # if there are no contacts, ignore
            pass

    for program_course in all_students_raw:
        # grkey - key like *program**year_number* (freshmen - 1, sophomores - 2, etc.)
        grkey = list(program_course.keys())[0]
        program, course = grkey[:-1], int(grkey[-1])
        for student in program_course[grkey]['students']:
            in_contacts = False

            stid = student['id']
            # if a student is in the group of only one program and one year

            if len(all_students_dict[stid]) == 1:
                # then vars program and course are assigned to her/him
                pass
            else:
                op_in = set([i[:-1] for i in all_students_dict[stid]])
                if len(op_in) == 1:
                    # if the student "belongs" only to one major
                    # Студент только в одной ОП

                    # is he in the "contacts" section anywhere?
                    # Есть ли он в контактах где-то?
                    if stid in list(all_contacts_dict.keys()):
                        # only once?
                        # он встречается только один раз?
                        if len(all_contacts_dict[stid]) == 1:
                            # if she/he is too old, discard
                            # если возраст слишком большой, выбрасываем
                            try:
                                if student['bdate'].count(".") == 2:
                                    if int(student['bdate'][-4:]) < 1994:
                                        undefined_students.update({stid: all_students_dict[stid]})
                                        continue
                            except KeyError:
                                pass

                            else:
                                # seemingly ok, make it +1 year
                                # предположительно всё нормально, ставим год на курс старше
                                course = int(all_contacts_dict[stid][0][-1]) + 1
                                in_contacts = True

                                if ((program == "history") or (program == "vostokovedine")) and course > 5:
                                    continue
                                elif course > 4:
                                    continue

                        else:
                            undefined_students.update({stid: all_students_dict[stid]})
                            continue
                    else:
                        # is "graduation" specified?
                        # указан ли graduation?
                        try:
                            graduation = student['graduation']
                        except KeyError:
                            continue

                        if graduation == 0:
                            undefined_students.update({stid: all_students_dict[stid]})
                            continue
                        elif graduation < 2020:
                            continue
                        else:
                            # calculate year (freshmen - 1, sophomores - 2, etc.)
                            if program == "vostokovedine":
                                if graduation < 2022:
                                    course = 5
                                else:
                                    course = 2020 - (graduation - 5) + 1
                            elif program == "history":
                                if graduation < 2024:
                                    course = 2020 - (graduation - 4) + 1
                                else:
                                    course = 2020 - (graduation - 5) + 1
                            elif program == "law":
                                if graduation <= 2023:
                                    course = 2020 - (graduation - 4) + 1
                                else:
                                    course = 2020 - (graduation - 5) + 1
                            else:
                                course = 2020 - (graduation - 4) + 1
                            # final check
                            if course > 5:
                                undefined_students.update({stid: all_students_dict[stid]})
                                continue

                else:
                    undefined_students.update({stid: all_students_dict[stid]})
                    continue

            # get sex
            gender = student['sex']
            if gender == 0:
                gender = None
            elif gender == 1:
                gender = "f"
            else:
                gender = "m"

            # let it just be here
            # я не помню, куда правильно вставлять эту проверку, поэтому пока оставлю здесь
            if program == "design" and course > 3:
                continue

            student_object = Student(major=program, stid=stid, name=student['first_name'], surname=student['last_name'],
                                     gender=gender, year=course, in_contacts=in_contacts)
            list_students.append(student_object)

    students_sure = dict()
    for student in list_students:
        students_sure.update({student.stid: {"id": student.stid,
                                             "major": student.major,
                                             "name": student.name,
                                             "surname": student.surname,
                                             "gender": student.gender,
                                             "year": student.year,
                                             "in_contacts": student.in_contacts}})

    with open("students_sure.pickle", "wb") as f:
        pickle.dump(students_sure, f)

    with open("students_unsure.pickle", "wb") as f1:
        pickle.dump(undefined_students, f1)

# file students_unsure.pickle is processed by hand
# I will not provide it here for privacy reasons
# As a result, another file is created named all_students.pickle
