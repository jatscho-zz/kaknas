import os
from os import environ

import importlib
import subprocess
from subprocess import call
from flask import Flask
from flask_caching import Cache
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from flask_apscheduler import APScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from pathlib import Path

__copyright__ = "Copyright 2017, luavis"
__credits__ = ["luavis", ]
__license__ = "MIT"
__version__ = "0.1.0"
__status__ = "Development"

def git(*args):
    return subprocess.check_call(['git'] + list(args))

def git_output(*args):
    return str(subprocess.check_output(['git'] + list(args)).strip().decode())

# periodically git fetch and check if there are any latest commits
# in the future we can set up a webhook with github and call this function
# whenever a change is made to the repo on github
def check_latest_commit():
    app.logger.info('Job is running')
    git_repo_folder = app.config['GIT_REPOS_FOLDER']
    os.chdir(git_repo_folder+'/terraform')
    app.logger.info('Currently in ' + git_repo_folder + '/terraform')
    git("fetch", "origin")
    terraform_latest_commit = git_output("rev-parse", "HEAD")
    terraform_current_commit = cache.get('terraform_current_commit')
    app.logger.info('terraform_current_commit is ' + terraform_current_commit)
    if terraform_latest_commit != terraform_current_commit:
        app.logger.info('currently pulling')
        git("pull")
        cache.set('terraform_current_commit', terraform_latest_commit)

    os.chdir(git_repo_folder+'/terraform-cognite-modules')
    app.logger.info('Currently in ' + git_repo_folder + '/terraform-cognite-modules')
    git("fetch", "origin")
    modules_latest_commit = git_output("rev-parse", "HEAD")
    modules_current_commit = cache.get('modules_current_commit')
    app.logger.info('modules_current_commit is ' + str(modules_current_commit))
    if modules_latest_commit != modules_current_commit:
        app.logger.info('currently pulling')
        git("pull")
        cache.set('modules_latest_commit', modules_latest_commit)

app = Flask(__name__, static_url_path='/static')
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

if os.environ.get('GIT_REPOS_FOLDER') is not None:
    app.config['GIT_REPOS_FOLDER'] = os.environ.get('GIT_REPOS_FOLDER')
else:
    app.config['GIT_REPOS_FOLDER'] = '/app'
if os.environ.get('FLASK_CONFIG') is not None:
    app.config.from_object('kaknas.config.%s' % os.environ['FLASK_CONFIG'])
else:
    app.config.from_object('kaknas.config.DevelopmentConfig')
__import__('kaknas.router')

# hack to make Flask run once
if not os.environ.get("WERKZEUG_RUN_MAIN") == "true":
    # git pull both repos
    git("clone", "git@github.com:cognitedata/terraform.git",
        app.config['GIT_REPOS_FOLDER']+'/terraform')
    os.chdir(app.config['GIT_REPOS_FOLDER']+'/terraform')
    terraform_current_commit = git_output("rev-parse", "HEAD")
    cache.set('terraform_current_commit', terraform_current_commit)
    app.logger.info('first pull for terraform is ' + str(terraform_current_commit))
    os.chdir(app.config['GIT_REPOS_FOLDER'])
    git("clone", "git@github.com:cognitedata/terraform-cognite-modules.git",
        app.config['GIT_REPOS_FOLDER']+'/terraform-cognite-modules')
    os.chdir(app.config['GIT_REPOS_FOLDER']+'/terraform-cognite-modules')
    modules_current_commit = git_output("rev-parse", "HEAD")
    app.logger.info('first pull for modules is ' + str(modules_current_commit))
    cache.set('modules_current_commit', modules_current_commit)

# Create a scheduler to check latest commit every minute
scheduler = BlockingScheduler(timezone="Europe/Oslo")
scheduler.add_job(check_latest_commit, 'interval', minutes=1)
scheduler.start()
