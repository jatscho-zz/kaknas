from flask import current_app as app
from kaknas.utils import utils
from kaknas.cache import cache
from dulwich import porcelain
from dulwich.repo import Repo
import sys
import json
import os

def github():
    # get latest commits of repos
    git_folder = app.config['GIT_REPOS_FOLDER']
    rep = Repo(git_folder + '/terraform/')
    repowlkr = rep.get_walker(max_entries=1)
    lastfcommit = next(iter(repowlkr)).commit

    modules_repo = Repo(git_folder + '/terraform-cognite-modules')
    repowlkr_modules = modules_repo.get_walker(max_entries=1)
    lastfcommit_modules = next(iter(repowlkr_modules)).commit

    if cache.get(lastfcommit) and cache.get(lastfcommit_modules) and cache.get('diff_module_map') is not None:
        return json.dumps(cache.get('diff_module_map'))


    all_files = porcelain.ls_files(rep)
    state_map = {}
    diff_module_map = {}


    utils.set_state_map(state_map, all_files, lastfcommit)

    # For now, we are comparing everything against Greenfield. We assume Greenfield is the most up to date project
    for folder_path, modules in state_map['cognitedata-greenfield'].items():
        for module, module_info in modules.items():
            for full_module_path, git_ref in module_info.items():
                dirfnm = full_module_path.encode('utf-8')
                repowlkr_subpath = modules_repo.get_walker(paths=[dirfnm])
                repowlkr = modules_repo.get_walker()

                iterator = iter(repowlkr)
                iterator_subpath = iter(repowlkr_subpath)

                all_commits = []
                subpath_commits = []

                utils.create_all_commits_list(iterator, all_commits)
                utils.create_subpath_commits_list(iterator_subpath, subpath_commits)

                greenfield_commit = utils.get_commit_in_subpath(git_ref, all_commits, subpath_commits)
                if folder_path in state_map['cognitedata-equinor']:
                    if module in state_map['cognitedata-equinor'][folder_path]:
                        equinor_commit = utils.get_commit_in_subpath(state_map['cognitedata-equinor'][folder_path][module][full_module_path],
                                                            all_commits, subpath_commits)
                    else:
                        # raise a flag if module appears in greenfield but not in equinor
                        diff_module_map[folder_path][module] = module + ' module not found in Equinor'
                else:
                    # raise a flag if path appear in greenfield but not in equinor
                    diff_module_map[folder_path] = folder_path + ' folder path not found in Equinor'
                    continue
                if equinor_commit is None:
                    # raise a flag if equinor's git ref is invalid
                    continue

                utils.set_diff_module_map(equinor_commit, greenfield_commit, folder_path,
                                    module, full_module_path, subpath_commits, diff_module_map)
    cache.set('diff_module_map', diff_module_map)
    cache.set(lastfcommit, True)
    cache.set(lastfcommit_modules, True)
    #print(diff_module_map, file=sys.stdout)
    return json.dumps(diff_module_map)
    # app.logger.info(diff_module_map)
    # return 'Check terminal'
