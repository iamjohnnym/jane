from flask import render_template, flash, redirect, session, url_for
from app import app, db, modules
from models import User
from app.modules.domain.view import mod as domain
from app.modules.database.view import mod as database
from app.modules.user.view import mod as user
from app.modules.system.main import System

app.register_blueprint(domain)
app.register_blueprint(database)
app.register_blueprint(user)

@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
def index():
    s = System()
    system = {'Hostname': s.getHostname(),
              'IP Address(es)': s.getIps(),
              'Operating System': s.getOs(),
              'Kernel Version': s.getKernel(),
              'zeusCp Version': s.getZcpVersion(),
            }
    graph = {'Disk Usage - Used | Total': {'used': s.getDiskUsed(),
                                           'total': s.getDiskTotal(),
                                           'percent': s.getDiskTotal() / s.getDiskUsed(),
                                          },
             'RAM Usage - Used | Total': {'used': s.getUsedPhyMemory(),
                                          'total': s.getTotalPhyMemory(),
                                          'percent': s.getPercentPhyMemory(),
                                         },
            },
    services = {'Web Service': s.getWebService(),
                'Database Service': s.getDatabaseService(),
               }
    view_more = {'Domains': {'number': s.getNumberOfDomains(),
                             'url': '/domains',
                            },
                 'Databases': {'number': s.getNumberOfDatabases(),
                               'url': '/databases',
                              },
                 'Users': {'number': s.getNumberOfUsers(),
                           'url': '/users',
                          },
        }

    return render_template("sb-admin/index.html",
        title = 'overview',
        system = system,
        services = services,
        graph = graph,
        view_more = view_more,
        )

@app.errorhandler(404)
def page_not_found(e):
    return render_template("sb-admin/404.html"), 404
