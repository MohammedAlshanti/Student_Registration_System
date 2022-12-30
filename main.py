import mariadb
import datetime as dt
import math
import datetime
from datetime import timedelta
from datetime import date
from flask import Flask
from flask import render_template
import jinja2

conn = mariadb.connect(
    user = 'root',
    password = 'root',
    host = 'localhost',
    database = 'finalproject_db'
)
cur = conn.cursor()

def commit_and_close():
    conn.commit()
    conn.close()
# table_name = f""" courses """
# query = f""" select * from {table_name}"""
# cur.execute(query)
# for row in cur:
#     print(row)
while True:
    input_message = """ select
    1-Register new student
    2-Enroll course
    3-Create new course
    4-Create new course schedule
    5-Display student courses schedule
    """
    user_input = input(input_message)
    if user_input in [1 , '1']:
        student_name = input("Enter student name: ")
        bod_inp = input("Enter birth of day: ")
        data_format = "%d-%m-%Y"
        bod = dt.datetime.strptime(bod_inp,data_format)
        level = input("Select level [A,B,C,D]: ")
        mobile_number = input("Enter mobile number: ")
        email = input("Enter the email: ")
        cur.execute(f"insert into contact(mobile_number,email) values('{mobile_number}' , '{email}') ")
        contact_id = cur.lastrowid
        cur.execute(f"insert into level(level_name) values('{level}')")
        cur.execute(f"select level_id from level where level_name='{level}'")
        level_id = cur.fetchone()[0]
        cur.execute(f"insert into students(student_name,BOD,contact_id,level_id) values('{student_name}' , '{bod}' , '{contact_id}', '{level_id}')")
        commit_and_close()

    elif user_input in [2 , '2']:
        std_id = int(input("Enter student id: "))
        crs_id = int(input("Enter course id: "))
        query = f"SELECT level_id FROM students WHERE student_id = '{std_id}'"
        cur.execute(query)
        student_level_id = cur.fetchone()

        # retrieve course data
        query = f"SELECT level_id FROM courses WHERE course_id = '{crs_id}'"
        cur.execute(query)
        course_level_id = cur.fetchone()

        # check if course is full
        cur.execute(f"select max_capacity from courses where course_id = '{crs_id}'")
        mx_cap = cur.fetchone()
        cur.execute(f"select count(student_id) as course_capacity from enrollment_history where course_id = '{crs_id}'")
        course_len = cur.fetchone()
        cur.execute(f"select course_id from enrollment_history where course_id = '{crs_id}'")
        result = cur.fetchone()
        if (course_len == mx_cap):
            print("Error: course is full")

        # check levels
        elif  student_level_id != course_level_id:
            print("Error: course level does not match student level")
            print("success")

       #check is enrolled before?
        elif result!=None:
            print("Error: student has already enrolled in course")
        else:
            total_hours=input("Enter total hours: ")
            date = date.today()
            cur.execute(f"select rate_per_hour from courses")
            rate = cur.fetchone()
            rate = int(rate[0])
            cur.execute(f"insert into enrollment_history(student_id,course_id,enrol_date, total_hours) values('{std_id}','{crs_id}','{date}','{total_hours}')")
            cur.execute(f"update enrollment_history set total = total_hours * '{rate}' where course_id = {crs_id} and student_id = {std_id}")
        commit_and_close()
    elif user_input in [3 , '3']:
        course_id = int(input("Enter course id: "))
        course_name = input("Enter course name: ")
        max_capacity = input("Enter max capacity: ")
        hour_rate = input("Enter hour rate: ")
        course_level = input("Enter course level [A,B,C,D]: ")
        cur.execute(f"select level_id from level where level_name='{course_level}'")
        cl = cur.fetchone()
        cl = cl[0]
        print(cl)
        cur.execute(f"insert into courses (course_id,course_name,max_capacity,rate_per_hour,level_id) values('{course_id}', '{course_name}', '{max_capacity}', '{hour_rate}', '{cl}')")
        commit_and_close()
    elif user_input in [4 , '4']:
        day = input("Select day: ")
        cour_id = input("Enter course id: ")
        start_time = input("Enter start time: [hh:mm:ss]")
        duration = int(input("Enter a duration: "))
        end_time = datetime.datetime.strptime(start_time, "%H:%M:%S") + datetime.timedelta(hours=duration)
        cur.execute(f"select day, start_time, duration from course_schedule where day = '{day}' and start_time = '{start_time}' and duration = {duration} ")
        dd = cur.fetchone()
        if not dd:
            cur.execute(f"insert into course_schedule (day,course_id,start_time,duration,end_time) values('{day}', '{cour_id}', '{start_time}', '{duration}', '{end_time}')")
            commit_and_close()
        else:
            print("you have another course in the same time")
    elif user_input in [5 ,'5']:
        student_id = input("Enter student id: ")
        cur.execute(f"select * from course_schedule WHERE student_id = '{student_id}'")
        que = cur.fetchone()
        print(que)
        commit_and_close()
    else:
        print("Your choice not exist...Try Again!")