from pprint import pprint
from datetime import datetime

import psycopg2 as pg

CONFIG = {
        'database': 'unnamed_db',
        'user': 'user',
        'password': 'password',
        'host': '127.0.0.1',
        'port': '8890'
    }

def create_course():
    with pg.connect(**CONFIG) as connect:
        cur = connect.cursor()
        cur.execute("""
        insert into Course(course_id, course_name) values(%s, %s);
        """, ('1', 'Python'))

def create_db(): # создает таблицы
    with pg.connect(**CONFIG) as connect:
        cursor = connect.cursor()
        cursor.execute(
            '''
            create table if not exists Student(student_id serial primary key not null,
            name varchar(100) not null,
            gpa numeric(10,2) null,
            birth timestamp with time zone null);
            
            create table if not exists Course(course_id serial primary key not null,
            course_name varchar(100) not null);
            
            create table if not exist student_course (
            id serial primary key,
            student_id integer references Student(student_id),
            course_id integer references  C,ourse(course_id));
            '''
            )

def get_students(course_id): # возвращает студентов определенного курса
    with pg.connect(**CONFIG) as connect:
        cursor = connect.cursor()
        cursor.execute(
            f'''
            select name, student_id from Student
            inner join Course
            on Student.student_id = Course.course_id
            where course_id={course_id}
            '''
            )
        print(cur.fetchall())

def add_students(course_id, students): # создает студентов и 
                                       # записывает их на курс
    with pg.connect(**CONFIG) as connect:
        cursor = connect.cursor()
        for student in students:
            cursor.execute(
                f'''
                insert into Student(name, gpa, birth) 
                values ({student["name"]}, {student["gpa"]}, {student["birth"]})
                '''
                )
            student_id = cursor.fetchone()
            cursor.execute(
                    f'''
                    insert into student_course (student_id, course_id)
                    values({student_id}, {course_id})
                    '''
                )


def add_student(student): # просто создает студента
    with pg.connect(**CONFIG) as connect:
        cursor = connect.cursor()
        cursor.execute(
                f'''
                insert into Student(name, gpa, birth) 
                values ({student["name"]}, {student["gpa"]}, {student["birth"]})
                '''
                )

def get_student(student_id):
    with pg.connect(**CONFIG) as connect:
        cursor = connect.cursor()
        cursor.execute(
                f'''
                select * from Student where student_id={student_id}
                '''
            )
        print(cursour.fetchone())
        
if __name__ == '__main__':
    create_db()
    create_course()

    student = {'name': 'bob', 'gpa': 5.56, 'birth': '1988-01-31'}
    #add_student(student)
    # get_student(9)
    students = [{'name': 'bob', 'gpa': 5.56, 'birth': '1988-01-31'},
                {'name': 'barbara', 'gpa': 2.32, 'birth': '1990-05-11'},
                {'name': 'frank', 'gpa': 4.89, 'birth': '1982-08-21'},
                ]
    add_students(1, students)
    get_students(1)