from flask import current_app as app
from kaknas.utils import diff_utils
from dulwich import porcelain
from dulwich.repo import Repo
from kaknas.app import cache
import json
import os

@cache.cached(timeout=60, key_prefix='diff_module_map')
def diff_status():
    # get latest commits of repos
    git_folder = app.config['GIT_REPOS_FOLDER']
    rep = Repo(git_folder + '/terraform/')
    repowlkr = rep.get_walker(max_entries=1)
    lastfcommit = next(iter(repowlkr)).commit

    modules_repo = Repo(git_folder + '/terraform-cognite-modules')
    repowlkr_modules = modules_repo.get_walker(max_entries=1)
    lastfcommit_modules = next(iter(repowlkr_modules)).commit

    all_files = porcelain.ls_files(rep)
    state_map = {}
    diff_module_map = {}

    diff_utils.set_state_map(state_map, all_files, lastfcommit)
    count = 0
    ret = []
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

                diff_utils.create_all_commits_list(iterator, all_commits)
                diff_utils.create_subpath_commits_list(iterator_subpath, subpath_commits)

                greenfield_commit = diff_utils.get_commit_in_subpath(git_ref, all_commits, subpath_commits)
                for project in state_map:
                    if project != 'cognitedata-greenfield':
                        project_commit = None
                        if folder_path in state_map[project]:
                            if module in state_map[project][folder_path]:
                                project_commit = project + '_commit'
                                project_commit = diff_utils.get_commit_in_subpath(state_map[project][folder_path][module][full_module_path],
                                                                             all_commits, subpath_commits)
                            else:
                                app.logger.info('hi')
                                # raise a flag if module appears in greenfield but not in equinor
                                # diff_module_map[count] = {}
                                # diff_module_map[count]["module_name"] = module
                                # diff_module_map[count][project] = {}
                                # diff_module_map[count][project]["path_to_module"] = module + ' module not found in ' + project

                        else:
                            app.logger.info('hi')
                            # raise a flag if path appear in greenfield but not in equinor
                            # diff_module_map[count] = {}
                            # diff_module_map[count]["module_name"] = module
                            # diff_module_map[count][project] = {}
                            # diff_module_map[count][project]["module_source"] = folder_path + ' folder path not found in ' + project

                        if project_commit is None:
                            # raise a flag if equinor's git ref is invalid
                            continue

                        diff_utils.set_diff_module_map(project_commit, project, greenfield_commit, folder_path,
                                            module, full_module_path, subpath_commits, diff_module_map, count)
                        count += 1
    # for key, value in diff_module_map.items():
    #     new_module_obj = {}
    #     new_module_obj["id"] = key
    #     for item_info_key, item_info_val in value.items():
    #         new_module_obj[item_info_key] = item_info_val
    #     ret.append(new_module_obj)

    cache.set('diff_module_map', diff_module_map)
    return json.dumps(diff_module_map)
    # app.logger.info(diff_module_map)
