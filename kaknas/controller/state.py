from flask import current_app as app, render_template
from kaknas.utils import diff_utils, git_utils
from kaknas.app import cache
#from kaknas import cache
import json
import os

@cache.cached(timeout=600, key_prefix='module_state_map')
def state():
    git_folder = app.config['GIT_REPOS_FOLDER']
    module_state_map = git_utils.get_latest_commits(git_folder, {})
    return render_template('state.html', module_state_map=module_state_map)
