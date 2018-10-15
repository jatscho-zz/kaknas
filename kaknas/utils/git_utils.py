import subprocess
import os
from dulwich.repo import Repo
from dulwich import porcelain
from kaknas.app import cache
from kaknas.utils import diff_utils

def git(*args):
    """Wrapper function that uses the git command line and returns the output

    Args:
        args: A list of arguments to pass to git command

    Returns:
        A String output of the git command
    """
    return str(subprocess.check_output(['git'] + list(args)).strip().decode())

def compare_and_pull(repo_path):
    """Compares the repo's current commit with the latest commit.
        If different, it does a git pull

    Args:
        repo_path: A string of the repo path

    Returns:
        None
    """
    latest_commit = git("rev-parse", "HEAD")
    current_commit = cache.get(repo_path)
    #app.logger.info('current commit ' + current_commit)
    if latest_commit != current_commit:
        #app.logger.info('currently pulling')
        git("pull")
        cache.set(repo_path, latest_commit)


def set_latest_commit_cache(repo_path):
    """Sets the repo's latest commit hash to cache

    Args:
        repo_path: A string of the repo path
        GIT_REPOS_FOLDER: A string to the git repo folder path

    Returns:
        None
    """
    os.chdir(repo_path)
    current_commit = git("rev-parse", "HEAD")
    cache.set(repo_path+'_current_commit', current_commit)

def get_latest_commits(git_folder, module_state_map):
    rep = Repo(git_folder + '/terraform/')
    repowlkr = rep.get_walker(max_entries=1)
    lastfcommit = next(iter(repowlkr)).commit
    all_files = porcelain.ls_files(rep)
    module_state_map = cache.get('module_state_map')
    if module_state_map is None:
        module_state_map = {}
        diff_utils.set_module_state_map(module_state_map, all_files, lastfcommit)
    cache.set('module_state_map', module_state_map)
    return module_state_map
