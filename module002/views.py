from flask import Blueprint, render_template, abort, flash, redirect, url_for, request
from models import get_db, User, Course, Post, Follow
from flask_login import login_required, current_user

from module002.forms import *

module002 = Blueprint("module002", __name__,static_folder="static",template_folder="templates")

db = get_db()

@module002.route('/')
@login_required
def module002_index():
    if current_user.profile in ('admin','staff','student'):
        follows = Follow.query.filter_by(user_id=current_user.id)
        return render_template("module002_index.html",module="module002", routes=follows)
    else:
        flash("Access denied!")
#        abort(404,description="Access denied!")
        return redirect(url_for('index'))

@module002.route('/post/<course>', methods=['GET','POST'])
@login_required
def module002_post(course):
    form = PostForm()
    course_query = Course.query.filter_by(name=course).first()
    if request.method == 'POST':
        if form.validate_on_submit():
            post = Post(body=form.body.data, author_id=current_user.id, course_id=course_query.id)
            db.session.add(post)
            db.session.commit()
            flash("Mensaje envidado con exito!")

            posts = Post.query.filter_by(course_id=course_query.id).order_by(Post.timestamp.desc())

    else:
        posts = Post.query.filter_by(course_id=course_query.id).order_by(Post.timestamp.desc())


    follows = Follow.query.filter_by(user_id=current_user.id)
    return render_template("module002_post.html",module="module002", form=form, rows=posts, routes=follows, course=course)



@module002.route('/test')
def module002_test():
    return 'OK'
