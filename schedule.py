import os
import sqlite3

isDataBaseExists = os.path.isfile('classes.db')
dbcon = sqlite3.connect('classes.db')

if __name__ == '__main__':
    cursor = dbcon.cursor()
    cursor.execute("SELECT * FROM courses")
    while isDataBaseExists and not cursor.fetchall().__len__() > 0:
        cursor.execute("SELECT * FROM courses")
        print("courses")
        for course in cursor.fetchall():
            print(course)

        cursor.execute("SELECT * FROM classrooms")
        print("classrooms")
        for classroom in cursor.fetchall():
            print(classroom)

        print("students")
        cursor.execute("SELECT * FROM students")
        for student in cursor.fetchall():
            print(student)

        cursor.execute("SELECT * FROM courses")
