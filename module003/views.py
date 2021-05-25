from application import get_app
from flask_login import login_required, login_user, logout_user, current_user
from flask import render_template, request, redirect, url_for, flash, Blueprint, send_file, Response
from sqlalchemy import or_
from models import User, get_db, Course, Assignment, Follow, AssignmentSubmit
import datetime
from io import BytesIO
from werkzeug import FileWrapper


db = get_db()

from module003.forms import *

module003 = Blueprint("module003", __name__,static_folder="static",template_folder="templates")

@module003.route('/')
def module003_index():
    return render_template("module003_index.html",module='module003')


@module003.route('/create', methods=['GET', 'POST'])
def module003_create():
    form = AssignmentCreateForm()

    if request.method == 'POST':
        try:
            course = Course.query.get(form.course_id.data)
            assignment = Assignment(title = form.title.data,
                    body = form.description.data,
                    date_expire = datetime.datetime.combine(form.date_expire.data, form.time_expire.data),
                    course_id = course.id,
                    course_name = course.name,
                    institution_name = course.institution_name,
                    user_id=current_user.id)

            db.session.add(assignment)
            db.session.commit()
            flash("Tarea creda con exito")

        except:
            flash("Error creando tarea")


    for course in Course.query.filter_by(user_id=current_user.id):
        form.course_id.choices += [(course.id,  str(course.id) + ' - ' + course.institution_name + ' - ' + course.name)]

    assignments = Assignment.query.filter(Assignment.user_id==current_user.id)

    return render_template("module003_create.html",module='module003', form=form, rows=assignments)

@module003.route('/submit', methods=['GET', 'POST'])
def module003_submit():

    assignments = Assignment.query.join(Follow, Assignment.course_id == Follow.course_id).filter(Follow.user_id == current_user.id)

    submitted = []

    for assignment in assignments:
        if AssignmentSubmit.query.filter(AssignmentSubmit.assignment_id == assignment.id, AssignmentSubmit.user_id == current_user.id).count() >= 1:
            submitted.append("Si")

        else:
            submitted.append("No")


    return render_template("module003_submit.html",module='module003', rows=assignments , submitted=submitted)


@module003.route('/submit/<assignmentid>', methods=['GET', 'POST'])
def module003_submit_id(assignmentid):

    assignment = Assignment.query.filter(Assignment.id == assignmentid).first()

    if request.method == 'POST':
        try:

            assignmentquery = Assignment.query.filter(Assignment.id == assignmentid).first()

            assignment_submit = AssignmentSubmit(course_name=assignmentquery.course_name,
                                    institution_name = assignmentquery.institution_name,
                                    data = request.files['inputFile'].read(),
                                    grade = "-",
                                    assignment_id = assignmentid,
                                    user_id = current_user.id,
                                    course_id = assignmentquery.course_id)

            db.session.add(assignment_submit)
            db.session.commit()
            flash("Tarea entregada con exito")

            return redirect(url_for('module003.module003_submit'))

        except Exception as e:
            print(e)
            flash("Error entregando tarea")

    rows =  AssignmentSubmit.query.filter(AssignmentSubmit.assignment_id == assignment.id, AssignmentSubmit.user_id == current_user.id)

    return render_template("module003_submit_id.html",module='module003', rows=rows , assignment=assignment)



@module003.route('/grade', methods=['GET', 'POST'])
def module003_grade():

    submits = AssignmentSubmit.query.filter(AssignmentSubmit.assignment_id == request.args['rowid'])

    return render_template("module003_grade.html",module='module003', rows = submits)

@module003.route('/grade/<gradeid>', methods=['GET', 'POST'])
def module003_grade_id(gradeid):

    form = GradeForm()

    if request.method == 'POST':
        submit = AssignmentSubmit.query.get(gradeid)
        submit.grade = form.grade.data
        db.session.commit()

    submit = AssignmentSubmit.query.get(gradeid)

    return render_template("module003_grade_id.html",module='module003', form = form, submit = submit )

@module003.route('/download/<gradeid>', methods=['POST'])
def module003_download(gradeid):

    submit = AssignmentSubmit.query.get(gradeid)
    file = FileWrapper(BytesIO(submit.data))
    return Response(file, mimetype="application/zip" , direct_passthrough=True)

    #return send_file(BytesIO(submit.data),  mimetype='application/zip', attachment_filename="Hola.zip" , as_attachment=True)



@module003.route('/test')
def module003_test():
    return 'OK'