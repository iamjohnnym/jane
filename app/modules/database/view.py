from flask import render_template, flash, redirect, session, url_for, Blueprint

mod = Blueprint('databases', __name__, url_prefix="/databases")
@mod.route('/', methods = ['GET', 'POST'])
@mod.route('/list', methods = ['GET', 'POST'])
def db():
    return render_template("database/template/index.html",
        title = 'database',
        test = 'Hello World',
        )   

@mod.route('/edit', methods = ['GET', 'POST'])
def db():
    return render_template("database/template/index.html",
        title = 'database',
        test = 'Hello World',
        )   

@mod.route('/add', methods = ['GET', 'POST'])
def db():
    return render_template("database/template/index.html",
        title = 'database',
        test = 'Hello World',
        )   

