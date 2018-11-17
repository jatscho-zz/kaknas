from flask import current_app as app, render_template, jsonify, request
from kaknas.utils import diff_utils, git_utils
from kaknas.app import cache
#from kaknas import cache
from collections import OrderedDict
import json
import os

#@cache.cached(timeout=600, key_prefix='module_state_map')
def state():
    ret = {}
    ret["data"] = []
    ret["sortOrder"] = request.args.get('sort')
    ret["sorted_modules_keys"] = []
    ret["reversed_modules_keys"] = []
    git_folder = app.config['GIT_REPOS_FOLDER']
    module_state_map = git_utils.get_latest_commits(git_folder, {})
    sorted_module_source_list = sorted(module_state_map.keys(), key=lambda x: module_state_map[x]['module_source'])
    reverse_sorted_module_source_list = list(reversed(sorted_module_source_list))

    for key, value in module_state_map.items():
        new_module_obj = {}
        new_module_obj["id"] = key
        for item_info_key, item_info_val in value.items():
            new_module_obj[item_info_key] = item_info_val
        ret["data"].append(new_module_obj)

    ret["sorted_modules_keys"].append(sorted_module_source_list)
    ret["reversed_modules_keys"].append(reverse_sorted_module_source_list)
    return jsonify(ret)
    #return render_template('state.html', module_state_map=module_state_map)
