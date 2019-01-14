import os
import sqlite3

dbcon = sqlite3.connect('schedule.db')

def print_table(list_of_tuples):
    for item in list_of_tuples:
        print(item)

def partOne(cursor, iteration):
    cursor.execute("SELECT * FROM classrooms WHERE current_course_id = 0")
    classroom = cursor.fetchone()
    cursor.execute("SELECT * FROM courses WHERE class_id = ?", (str(classroom[0])))
    course = cursor.fetchone()
    if (classroom is not None and course is not None):
        print("(" + str(iteration) + ") " + classroom[1] + ": " + course[1] + " is scheduled to start")
        cursor.execute("UPDATE classrooms SET current_course_id = ?, current_course_time_left = ?"
                       " WHERE id = ?", (course[0], course[3], classroom[0]))
        dbcon.commit()
        cursor.execute("UPDATE courses SET class_id = ? WHERE id = ?", (classroom[0], course[0]))
        dbcon.commit()

def partTwo(cursor, iteration):
    cursor.execute("SELECT * FROM classrooms JOIN courses on current_course_id = courses.id"
                   " WHERE current_course_id > 0")
    listOfClasses = cursor.fetchall()
    for _class in listOfClasses:
        print("(" + str(iteration) + ") " + _class[1] + ": occupied by " + _class[5])
        cursor.execute("UPDATE classrooms SET current_course_time_left = current_course_time_left-1"
                       " WHERE current_course_id = ?", (_class[4]))
        dbcon.commit()

def partThree(cursor, iteration):
    cursor.execute("SELECT * FROM classrooms JOIN courses on current_course_id = courses.id"
                   " WHERE current_course_id > 0 and current_course_time_left = 0")
    listOfClasses = cursor.fetchall()
    for _class in listOfClasses:
        print("(" + str(iteration) + ") " + _class[1] + ": " + _class[5] + " is done")
        cursor.execute("DELETE FROM courses WHERE current_course_id = ?", (_class[4]))
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

            partOne(cursor, iteration)
            partTwo(cursor, iteration)
            partThree(cursor, iteration)
            partOne(cursor, iteration)

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
            isDataBaseExists = False



if __name__=="__main__":
    main()
    dbcon.close()
