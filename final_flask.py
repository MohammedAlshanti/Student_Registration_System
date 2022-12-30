from flask import Flask, request, render_template, jsonify
import json
import jinja2
import mariadb


conn = mariadb.connect(
    user = 'root',
    password = 'root',
    host = 'localhost',
    database = 'finalproject_db'
)
cur = conn.cursor()

app = Flask(__name__)
print(app)

cur.execute(f"select * from courses")
all_courses= cur.fetchall()
# print(all_courses)
cur.execute(f"select * from students")
all_students = cur.fetchall()
print(all_students)
# students =  dict(all_students)
#
# print(students)
cur.execute(f"select * from course_schedule")
scedules=cur.fetchall()

@app.route("/courses")
def courses():
    return render_template("courses.html", title="courses",page_head="all courses stored",all_courses=all_courses)

@app.route("/students")
def students():
    return render_template("students.html",title="students",page_head = "all students regestered",all_students=all_students)

@app.route("/courses_schedule")
def schedule():
    return render_template("courses_schedule.html",title="schedule",page_head="courses schedule",scedules=scedules)




API_KEY = "abcdefghijklmnopqrstuvwxyz"
@app.route("/student/<int:student_id>", methods=["GET"])
def get_student_details(student_id):
    if "Authorization" not in request.headers:
        return "API key is missing", 401

    api_key = request.headers["Authorization"]

    if api_key != API_KEY:
        return "Invalid API key", 401

    student = next((item for item in all_students if item[0] == student_id), None)

    if student is None:
        return 'Student not found', 404
    else:
        return jsonify(student),200
        # return json.dumps(student, default=str), 200


if __name__ == '__main__':
    app.run(debug=True)

