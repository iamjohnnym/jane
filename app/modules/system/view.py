from flask import render_template, flash, redirect, session, url_for, Blueprint
from app.modules.domain.forms.form import AddDomain
from app.modules.user.forms.form import UserForm
from app.modules.domain.main import Domain

mod = Blueprint('domains', __name__)
@mod.route('/domains-list', methods = ['GET', 'POST'])
def list():
    return render_template("domain/template/list.html",
        title = 'domains list',
        test = 'Hello World',
        )   

@mod.route('/domains-add', methods = ['GET', 'POST'])
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
        except Exception, e:
            return render_template("domain/template/add.html",
                title = 'domains add',
                test = 'Hello World',
                form = form,
                user_form = user_form,
                error="Unable to process your request: {0}".format(e)
                )   
        return render_template("domain/template/list.html",
            title = 'domains list',
            test = 'Hello World',
            form = form,
            user_form = user_form,
            success = "{0} has been added".format(form.domain_name.data)
            )   

    return render_template("domain/template/add.html",
        title = 'domains add',
        test = 'Hello World',
        form = form,
        user_form = user_form,
        )   
