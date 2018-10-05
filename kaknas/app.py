import os
from flask import Flask
from kaknas.cache import cache
from flask_apscheduler import APScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from kaknas.utils import git_utils
from pytz import utc

__copyright__ = "Copyright 2017, luavis"
__credits__ = ["luavis", ]
__license__ = "MIT"
__version__ = "0.1.0"
__status__ = "Development"


app = Flask(__name__, static_url_path='/static')
cache.init_app(app, config={'CACHE_TYPE': 'simple'})

if os.environ.get('GIT_REPOS_FOLDER') is not None:
    app.config['GIT_REPOS_FOLDER'] = os.environ.get('GIT_REPOS_FOLDER')
else:
    app.config['GIT_REPOS_FOLDER'] = '/app'
if os.environ.get('FLASK_CONFIG') is not None:
    app.config.from_object('kaknas.config.%s' % os.environ['FLASK_CONFIG'])
else:
    app.config.from_object('kaknas.config.DevelopmentConfig')
__import__('kaknas.router')

# in the future we can set up a webhook with github and call this function
# whenever a change is made to the repo on github
def check_latest_commit():
    """Repo periodically does a git fetch and calls compare_and_pull

    Args:
        None

    Returns:
        None
    """
    app.logger.info('Job is running')
    git_repo_folder = app.config['GIT_REPOS_FOLDER']
    os.chdir(git_repo_folder+'/terraform')
    app.logger.info('Currently in ' + git_repo_folder + '/terraform')
    git_utils.git("fetch", "origin")
    git_utils.compare_and_pull('terraform_current_commit')

    os.chdir(git_repo_folder+'/terraform-cognite-modules')
    app.logger.info('Currently in ' + git_repo_folder + '/terraform-cognite-modules')
    git_utils.git("fetch", "origin")
    git_utils.compare_and_pull('modules_current_commit')

# hack to make Flask run once
if not os.environ.get("WERKZEUG_RUN_MAIN") == "true":
    # git pull both repos
    git_utils.git("clone", "git@github.com:cognitedata/terraform.git",
                  app.config['GIT_REPOS_FOLDER']+'/terraform')
    git_utils.git("clone", "git@github.com:cognitedata/terraform-cognite-modules.git",
                  app.config['GIT_REPOS_FOLDER']+'/terraform-cognite-modules')
    git_utils.set_latest_commit_cache('/terraform', app.config['GIT_REPOS_FOLDER'])
    git_utils.set_latest_commit_cache('/terraform-cognite-modules', app.config['GIT_REPOS_FOLDER'])

# Create a scheduler to check latest commit every minute
scheduler = BackgroundScheduler(timezone=utc)
scheduler.add_job(check_latest_commit, 'interval', minutes=1)
scheduler.start()
