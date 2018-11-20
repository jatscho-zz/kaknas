from kaknas.app import app
from flask import render_template, request, redirect, Response, jsonify
from dulwich import porcelain
from dulwich.repo import Repo
from kaknas.utils import diff_utils
from kaknas.app import cache
#from kaknas import cache
import random, json

@cache.cached(timeout=60, key_prefix='ret')
def display_diff():
    git_folder = app.config['GIT_REPOS_FOLDER']
    rep = Repo(git_folder + '/terraform/')
    repowlkr = rep.get_walker(max_entries=1)
    lastfcommit = next(iter(repowlkr)).commit

    modules_repo = Repo(git_folder + '/terraform-cognite-modules')
    repowlkr_modules = modules_repo.get_walker(max_entries=1)
    lastfcommit_modules = next(iter(repowlkr_modules)).commit

    all_files = porcelain.ls_files(rep)
    state_map = {}

    ret = cache.get('ret')
    if ret is None:
        ret = {}

    diff_utils.set_state_map(state_map, all_files, lastfcommit)
    ret["all_subpath_commits"] = {}

    for folder_path, modules in state_map['cognitedata-greenfield'].items():
        for module, module_info in modules.items():
            ret["all_subpath_commits"][module] = {}
            ret["all_subpath_commits"][module]["module_commits"] = []
            for full_module_path, git_ref in module_info.items():
                dirfnm = full_module_path.encode('utf-8')
                repowlkr_subpath = modules_repo.get_walker(paths=[dirfnm])
                repowlkr = modules_repo.get_walker()

                iterator = iter(repowlkr)
                iterator_subpath = iter(repowlkr_subpath)

                all_commits = []
                subpath_commits = []

                diff_utils.create_all_commits_list(iterator, all_commits)
                diff_utils.create_subpath_commits_list(iterator_subpath, subpath_commits)

                for commit in subpath_commits:
                    parsed_commit = commit.as_pretty_string().decode().split('\n')
                    committer = parsed_commit[2]
                    description = parsed_commit[-2]
                    # sometimes them commit description has 2 new lines at the end
                    if len(description) == 0:
                        description = parsed_commit[-3]
                    sha_commit = commit.id.decode()
                    commit_info = {}
                    commit_info["committer"] = committer
                    commit_info["description"] = description
                    commit_info["sha_commit"] = sha_commit
                    ret["all_subpath_commits"][module]["module_commits"].append(commit_info)
                greenfield_commit = diff_utils.get_commit_in_subpath(git_ref, all_commits, subpath_commits)
                ret["all_subpath_commits"][module]["cognitedata-greenfield"] = greenfield_commit.id.decode()

                for project in state_map:
                    if project != 'cognitedata-greenfield':
                        project_commit = None
                        if folder_path in state_map[project]:
                            if module in state_map[project][folder_path]:
                                project_commit = project + '_commit'
                                project_commit = diff_utils.get_commit_in_subpath(state_map[project][folder_path][module][full_module_path],
                                                                             all_commits, subpath_commits)

                                if module in ret["all_subpath_commits"]:
                                    ret["all_subpath_commits"][module][project] = project_commit.id.decode()
                                if module not in ret:
                                    ret[module] = {}
                                ret[module]["greenfield"] = greenfield_commit.id.decode()
                                ret[module][project] = project_commit.id.decode()
                            else:
                                continue

                        else:
                            continue

                        if project_commit is None:
                            # raise a flag if equinor's git ref is invalid
                            continue
    return jsonify(ret)
