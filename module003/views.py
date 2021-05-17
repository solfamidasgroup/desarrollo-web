from application import get_app
from flask_login import login_required, login_user, logout_user, current_user
from flask import render_template, request, redirect, url_for, flash, Blueprint
from sqlalchemy import or_
from models import User, get_db, Course, Assignment
import datetime

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


@module003.route('/test')
def module003_test():
    return 'OK'