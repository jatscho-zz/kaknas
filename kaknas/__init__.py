import os
import importlib
from flask import Flask
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
import subprocess
import logging

__author__ = "luavis"
__copyright__ = "Copyright 2017, luavis"
__credits__ = ["luavis", ]
__license__ = "MIT"
__version__ = "0.1.0"
__status__ = "Development"

def git(*args):
    return subprocess.check_call(['git'] + list(args))

app = Flask(__name__, static_url_path='/static')

if os.environ.get('GIT_REPOS_FOLDER') is not None:
    app.config['GIT_REPOS_FOLDER'] = os.environ.get('GIT_REPOS_FOLDER')
else:
    app.config['GIT_REPOS_FOLDER'] = '/app'
if os.environ.get('FLASK_CONFIG') is not None:
    app.config.from_object('kaknas.config.%s' % os.environ['FLASK_CONFIG'])
else:
    app.config.from_object('kaknas.config.DevelopmentConfig')
migrate = Migrate(app, importlib.import_module('kaknas.database').db)
__import__('kaknas.router')


def main(app):
    # hack to make Flask run once
    if not os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        git("clone", "git@github.com:cognitedata/terraform.git",
            app.config['GIT_REPOS_FOLDER']+'/terraform')
        git("clone", "git@github.com:cognitedata/terraform-cognite-modules.git",
            app.config['GIT_REPOS_FOLDER']+'/terraform-cognite-modules')
    manager = Manager(app)
    manager.add_command('db', MigrateCommand)
    manager.add_command('runserver', Server(host='0.0.0.0', port=5000, threaded=True))

    manager.run()
