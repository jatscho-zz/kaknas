from flask import current_app as app, render_template, jsonify
from kaknas.utils import diff_utils, git_utils
from kaknas.app import cache
#from kaknas import cache
from collections import OrderedDict
import json
import os

@cache.cached(timeout=600, key_prefix='module_state_map')
def state():
    ret = {}
    ret["data"] = []
    git_folder = app.config['GIT_REPOS_FOLDER']
    module_state_map = git_utils.get_latest_commits(git_folder, {})
    test_mod = sorted(module_state_map.items(), key=lambda x: module_state_map[x]['module_source'])
    #app.logger.info(test_mod)
    for mod in test_mod:
        app.logger.info(mod)
    for key, value in module_state_map.items():
        new_module_obj = {}
        new_module_obj["id"] = key
        for item_info_key, item_info_val in value.items():
            new_module_obj[item_info_key] = item_info_val
        ret["data"].append(new_module_obj)

    return jsonify(test_mod)
    #return render_template('state.html', module_state_map=module_state_map)
