from kaknas.app import app
from flask import render_template, request, redirect, Response, jsonify
from dulwich import porcelain
from dulwich.repo import Repo
from kaknas.utils import diff_utils
from kaknas.app import cache
#from kaknas import cache
import random, json

@app.route('/diff_check', methods=['POST'])
def diff_check():
    data = request.get_json()
    for key, val in data.items():
        full_module_path = key
        for greenfield_sha, other_sha in val.items():
            greenfield_ref = greenfield_sha
            other_ref = other_sha

    # get latest commits of repos
    git_folder = app.config['GIT_REPOS_FOLDER']
    rep = Repo(git_folder + '/terraform/')
    repowlkr = rep.get_walker(max_entries=1)
    lastfcommit = next(iter(repowlkr)).commit

    modules_repo = Repo(git_folder + '/terraform-cognite-modules')
    repowlkr_modules = modules_repo.get_walker(max_entries=1)
    lastfcommit_modules = next(iter(repowlkr_modules)).commit
    diff_module_map = {}
    all_files = porcelain.ls_files(rep)

    dirfnm = full_module_path.encode('utf-8')
    repowlkr_subpath = modules_repo.get_walker(paths=[dirfnm])
    repowlkr = modules_repo.get_walker()

    iterator = iter(repowlkr)
    iterator_subpath = iter(repowlkr_subpath)

    all_commits = []
    diff_utils.create_all_commits_list(iterator, all_commits)

    subpath_commits = []
    diff_utils.create_subpath_commits_list(iterator_subpath, subpath_commits)

    greenfield_commit = diff_utils.get_commit_in_subpath(greenfield_ref, all_commits, subpath_commits)
    other_commit = diff_utils.get_commit_in_subpath(other_ref, all_commits, subpath_commits)
    if greenfield_commit and other_commit:
        #app.logger.info(greenfield_commit.id.decode() + ' ' + other_commit.id.decode())
        if greenfield_commit.id.decode() != other_commit.id.decode():
            return jsonify('False')
        else:
            return jsonify('True')
    else:
        return jsonify('Not found')
