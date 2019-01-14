import os
import sqlite3

dbcon = sqlite3.connect('schedule.db')

def print_table(list_of_tuples):
    for item in list_of_tuples:
        print(item)

def partOne(cursor, iteration, classroom):
    cursor.execute("SELECT * FROM courses WHERE class_id = ?", [classroom[0]])
    course = cursor.fetchone()
    if classroom is not None and course is not None:
        print("(" + str(iteration) + ") " + classroom[1] + ": " + course[1] + " is scheduled to start")
        cursor.execute("UPDATE classrooms SET current_course_id = ?, current_course_time_left = ?"
                       " WHERE id = ?", [course[0], course[5], classroom[0]])
        cursor.execute("UPDATE students SET count = count - ? WHERE grade = ?", [course[3], course[2]])
    else:
        cursor.execute("UPDATE classrooms SET current_course_id = 0, current_course_time_left = 0"
                       " WHERE id = ?", [classroom[0]])
    dbcon.commit()

def partTwo(cursor, iteration, classroom):
    cursor.execute("SELECT courses.course_name, courses.id, classrooms.current_course_time_left FROM courses JOIN classrooms ON courses.id = classrooms.current_course_id"
                   " WHERE classrooms.id = ?", [classroom[0]])
    course_class = cursor.fetchone()
    if course_class[2] > 1:
        print("(" + str(iteration) + ") " + classroom[1] + ": occupied by " + course_class[0])
    cursor.execute("UPDATE classrooms SET current_course_time_left = current_course_time_left-1"
                   " WHERE current_course_id = ?", [course_class[1]])
    dbcon.commit()

def partThree(cursor, iteration, classroom):
    cursor.execute("SELECT courses.course_name, courses.id FROM courses JOIN classrooms ON courses.id = classrooms.current_course_id"
                   " WHERE classrooms.id = ?", [classroom[0]])
    course_class = cursor.fetchone()
    print("(" + str(iteration) + ") " + classroom[1] + ": " + course_class[0] + " is done")
    cursor.execute("DELETE FROM courses WHERE id = ?", [course_class[1]])
    dbcon.commit()

def main():
    iteration=-1
    isDataBaseExists = os.path.isfile('schedule.db')
    with dbcon:
        cursor = dbcon.cursor()
        cursor.execute("SELECT * FROM courses")
        courses = cursor.fetchall()
        while isDataBaseExists and len(courses) > 0:

            iteration+=1
            cursor.execute("SELECT * FROM classrooms")
            classrooms = cursor.fetchall()

            for classroom in classrooms:

                if classroom[2] == 0:
                    partOne(cursor, iteration, classroom)
                elif classroom[3] != 0:
                    partTwo(cursor, iteration, classroom)
                    cursor.execute("SELECT * FROM classrooms WHERE id = ?", [classroom[0]])
                    classroom0 = cursor.fetchone()
                    if classroom0[3] == 0:
                        partThree(cursor, iteration, classroom0)
                        partOne(cursor, iteration, classroom0)

            cursor.execute("SELECT * FROM courses")
            print("courses")
            print_table(cursor.fetchall())

            cursor.execute("SELECT * FROM classrooms")
            print("classrooms")
            print_table(cursor.fetchall())

            cursor.execute("SELECT * FROM students")
            print("students")
            print_table(cursor.fetchall())

            cursor.execute("SELECT * FROM courses")
            courses = cursor.fetchall()



if __name__== "__main__":
    main()
    dbcon.close()
