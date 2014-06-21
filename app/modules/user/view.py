from flask import render_template, flash, redirect, session, url_for, Blueprint
from app import db, models
from app.modules.user.forms.form import UserForm
from app.modules.user.main import User as U
import datetime

mod = Blueprint('users', __name__, url_prefix='/users')
@mod.route('/', methods = ['GET', 'POST'])
@mod.route('/list', methods = ['GET', 'POST'])
def Users():
    return render_template("user/template/index.html",
        title = 'users',
        test = 'Hello World',
        users=models.User.query.all()
        )   


@mod.route('/add', methods = ['GET', 'POST'])
def add():
    form = UserForm()
    if form.validate_on_submit():
        try:
            u = models.User(first_name=form.first_name.data,
                            last_name=form.last_name.data,
                            username=form.user_name.data,
                            email=form.email.data,
                            domain_access='ohaiworld.com',
                            passwd=form.password.data,
                            created=datetime.datetime.utcnow(),
                            sudoer=form.sudoer.data,
                            shell=form.shell.data,
                           )
            db.session.add(u)
            db.session.commit()
            user = U(username=form.user_name.data,
                        passwd=form.password.data,
                        domain='ohaiworld.com',
                        web_root="/var/www/vhosts/{0}".format('ohaiworld.com'),
                        shell=form.shell.data,
                       ).run()
        except Exception, e:
            return render_template("user/template/add.html",
                title = 'domains add',
                form = form,
                error = "Unable to process your request: {0}".format(e)
                )   
        flash("User: {0} has been successfully added".format(form.user_name.data))
        return redirect("/users")   

    return render_template("user/template/add.html",
        title = 'domains add',
        form = form,
        )   


@mod.route('/edit/<users>', methods = ['GET', 'POST'])
def edit(users):
    form = UserForm()
    if form.validate_on_submit():
        try:
            print 'test'
            pass
        except Exception, e:
            return render_template("user/template/edit.html",
                title = 'domains add',
                form = form,
                error = "Unable to process your request: {0}".format(e)
                )   
    else:
        for r in models.User.query.filter(models.User.username.in_([users])).all():
            form.first_name.data = r.first_name
            form.last_name.data = r.last_name
            form.user_name.data = r.username
            form.email.data = r.email
            form.sudoer.data = r.sudoer
            form.shell.data = r.shell
        return render_template("user/template/edit.html",
            title = 'domains add',
            test = users,
            form = form,
            )   

