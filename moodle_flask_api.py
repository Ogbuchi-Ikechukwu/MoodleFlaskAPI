from flask import Flask, request
from tables import Description
import moodle_api
app = Flask(__name__)
from flask_sqlalchemy import SQLAlchemy
#configuring db with SQLALCHEMY for Flask App
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///moodledata.db'
db = SQLAlchemy(app)

#class def of Model (properties) first step

class Attendance(db.Model):
    userid=db.Column(db.Integer,primary_key=True)
    courseid=db.Column(db.Integer)
    examscore=db.Column(db.String(120))
    quiztotal=db.Column(db.String(120))
    journal=db.Column(db.String(120))
    attendance=db.Column(db.String(120))
    attendance_plugin=db.Column(db.String(120))
    username=db.Column(db.String(80),unique=True,nullable=False)
    

    def __repr__(self):
        return f"{self.userid}-{self.username}-{self.examscore}-{self.quiztotal}-{self.journal}-{self.attendance_plugin}"

#Adding all selected contents into a table built with SQLALCHEMY
out=moodle_api.call("gradereport_user_get_grade_items",courseid=2)
correct_json=out["usergrades"]
lst_dict=[]
db.create_all()
for i in range(len(correct_json)):
        lst_dict.append({'userid':correct_json[i]['userid'],'username':correct_json[i]['userfullname'],
                   'courseid':correct_json[i]['courseid'], 'examscore':correct_json[i]['gradeitems'][1]['gradeformatted'],
                    'quiztotal':correct_json[i]['gradeitems'][2]['gradeformatted'],
                     'journal':correct_json[i]['gradeitems'][3]['gradeformatted'],
                    'attendance':correct_json[i]['gradeitems'][4]['gradeformatted'],
                    'attendance_plugin':correct_json[i]['gradeitems'][5]['graderaw']})
for i in range(len(lst_dict)):
        value1=Attendance(username=lst_dict[i]['username'], userid=lst_dict[i]['userid'],examscore=lst_dict[i]['examscore'],quiztotal=lst_dict[i]['quiztotal'], journal=lst_dict[i]['journal'], attendance=lst_dict[i]['attendance'])
        db.session.add(value1)
        db.session.commit()

#main page route
@app.route('/')
def index():
    return 'Hello User. Welcome to the Moodle Attendance API'

#attendance route for all data
#first API route, all columns
@app.route('/all')
def get_all():
    out=moodle_api.call("gradereport_user_get_grade_items",courseid=2)
    correct_json=out["usergrades"]
    lst_dict=[]
    for i in range(len(correct_json)):
        lst_dict.append({'userid':correct_json[i]['userid'],'username':correct_json[i]['userfullname'],
                   'courseid':correct_json[i]['courseid'], 'examscore':correct_json[i]['gradeitems'][1]['gradeformatted'],
                    'quiztotal':correct_json[i]['gradeitems'][2]['gradeformatted'],
                     'journal':correct_json[i]['gradeitems'][3]['gradeformatted'],
                    'attendance':correct_json[i]['gradeitems'][4]['gradeformatted'],
                    'attendance_plugin':correct_json[i]['gradeitems'][5]['graderaw']})

    return {'all':lst_dict}

#second api route - just attendance
@app.route('/attendance')
def get_attendance():
    out=moodle_api.call("gradereport_user_get_grade_items",courseid=2)
    correct_json=out["usergrades"]
    lst_dict=[]
    for i in range(len(correct_json)):
        lst_dict.append({'userid':correct_json[i]['userid'],'username':correct_json[i]['userfullname'],
                    'attendance':correct_json[i]['gradeitems'][5]['gradeformatted']})

    return {'attendance':lst_dict}

#third Route to Get attendance values by userid
@app.route('/attendance/<userid>')
def get_attendan(userid):
    valueattendance=Attendance.query.get(userid)
    if valueattendance is None:
        return {"error":"Userid not found try again"}
    else:
        return {"username":valueattendance.username,"userid":valueattendance.userid,"attendance score":valueattendance.attendance}

