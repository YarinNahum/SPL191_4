import sys
import os
import sqlite3

isDataBaseExists = os.path.isfile('schdule.db')
dbcon = sqlite3.connect('schedule.db')

with dbcon:
    cursor = dbcon.cursor()
    if not isDataBaseExists:
        cursor.execute("""CREATE TABLE classrooms(
        id INTEGER PRIMARY KEY,
        location TEXT NOT NULL,
        current_course_id INTEGER NOT NULL,
        current_course_time_left INTEGER NOT NULL)
        """)

        cursor.execute("""CREATE TABLE courses(
        id INTEGER PRIMARY KEY,
        course_name TEXT NOT NULL,
        student TEXT NUT NULL,
        number_of_students INTEGER NOT NULL,
        class_id INTEGER REFERENCES classrooms(id),
        course_length INTEGER NOT NULL)
        """)

        cursor.execute("""CREATE TABLE students(
        grade TEXT PRIMARY KEY,
        count INTEGER NOT NULL)
        """)


def addConfigFile(args):
    configFilePath = args[1]
    if not isDataBaseExists:
        with open(configFilePath) as configFile:
            for line in configFile:
                lineList = line.split(',')
                if lineList[0] == 'C':
                    addCourse(lineList)
                elif lineList[0] == 'S':
                    addStudent(lineList)
                elif lineList[0] == 'R':
                    addRoom(lineList)

            dbcon.commit();
            configFile.close()


def addCourse(lineList):
    cursor.execute("INSERT INTO courses VALUES(?,?,?,?,?,?)", (lineList[1], lineList[2], lineList[3], lineList[4], lineList[5], lineList[6]))


def addStudent(lineList):
    cursor.execute("INSERT INTO students VALUES(?,?)", (lineList[1], lineList[2]))


def addRoom(lineList):
    cursor.execute("INSERT INTO classrooms VALUES(?,?,?,?)", (lineList[1], lineList[2].strip('\n'), 0, 0))

if __name__ == '__main__':
    addConfigFile(sys.argv)

def print_table(list_of_tuples):
    for item in list_of_tuples:
        print(item)

cursor.execute("SELECT * FROM courses")
print("courses")
print_table(cursor.fetchall())

cursor.execute("SELECT * FROM classrooms")
print("classrooms")
print_table(cursor.fetchall())

cursor.execute("SELECT * FROM students")
print("students")
print_table(cursor.fetchall())
