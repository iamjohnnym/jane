from flask import render_template, flash, redirect, session, url_for, Blueprint
from app import models, db
from app.modules.domain.forms.form import AddDomain, EditDomain
from app.modules.user.forms.form import UserForm
from app.modules.domain.main import Domain
from app.modules.user.main import User
import datetime

mod = Blueprint('domains', __name__, url_prefix='/domains')
@mod.route('/', methods = ['GET', 'POST'])
@mod.route('/list', methods = ['GET', 'POST'])
def list():
    return render_template("domain/template/list.html",
        title = 'domains list',
        test = 'Hello World',
        domains=models.Domain.query.all()
        )   

@mod.route('/edit/<control>', methods = ['GET', 'POST'])
def edit(control):
    form = EditDomain()
    if form.validate_on_submit():
        try:
            domain = Domain(domain=form.domain_name.data,
                            service='httpd',
                            document_root="/var/www/vhosts")
            domain.writeVirtualHost(form.vhost.data)
            domain.writePhpini(form.phpini.data)
            flash("Domain: {0} has successfully been updated".format(form.domain_name.data))
        except Exception, e:
            return render_template("domain/template/edit.html",
                title = 'domains add',
                test = control,
                form = form,
                error = "Unable to process your request: {0}".format(e)
                )   
    domain = Domain(domain=control,
                    service='httpd',
                    document_root='/var/www/vhosts',
                    )
    form.domain_name.data = control
    form.phpini.data = domain.getDomainPhpini()
    form.vhost.data = domain.getDomainVirtualHost()
    return render_template("domain/template/edit.html",
        title = 'domains add',
        test = control,
        form = form,
        )   

@mod.route('/add', methods = ['GET', 'POST'])
def add():
    form = AddDomain()
    user_form = UserForm()
    if form.validate_on_submit():
        try:
            domain = Domain(domain=form.domain_name.data,
                            service='httpd',
                            document_root="/var/www/vhosts")
            domain.writeVirtualHost(form.vhost.data)
            domain.writePhpini(form.phpini.data)
            d = models.Domain(domain=form.domain_name.data,
                              usage=0,
                              created=datetime.datetime.utcnow()
                             )
            db.session.add(d)
            db.session.commit()
        except Exception, e:
            return render_template("domain/template/add.html",
                title = 'domains add',
                test = 'Hello World',
                form = form,
                user_form = user_form,
                error="Unable to process your request: {0}".format(e)
                )   
        try:
            u = models.User(first_name=user_form.first_name.data,
                            last_name=user_form.last_name.data,
                            username=user_form.user_name.data,
                            email=user_form.email.data,
                            domain_access=form.domain_name.data,
                            passwd=user_form.password.data,
                            created=datetime.datetime.utcnow(),
                            sudoer=user_form.sudoer.data,
                            shell=user_form.shell.data,
                           )
            db.session.add(u)
            db.session.commit()
            user = User(username=user_form.user_name.data,
                        passwd=user_form.password.data,
                        domain=form.domain_name.data,
                        web_root="/var/www/vhosts/{0}".format(form.domain_name.data),
                        shell=user_form.shell.data,
                       ).run()
        except Exception, e:
            return render_template("domain/template/add.html",
                title = 'domains add',
                test = 'Hello World',
                form = form,
                user_form = user_form,
                error="Unable to process your request: {0}".format(e)
                )   
        flash("Domain: {0} has been successfully added".format(form.domain_name.data))
        flash("User: {0} has been successfully added".format(user_form.user_name.data))
        return redirect("/domains")   

    return render_template("domain/template/add.html",
        title = 'domains add',
        test = 'Hello World',
        form = form,
        user_form = user_form,
        )   
