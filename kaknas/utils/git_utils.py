import subprocess
import os
from kaknas.app import cache
from kaknas.controller.github import github

def git(*args):
    """Wrapper function that uses the git command line

    Args:
        args: A list of arguments to pass to git command

    Returns:
        None
    """
    return subprocess.check_call(['git'] + list(args))

def git_output(*args):
    """Wrapper function that uses the git command line and returns the output

    Args:
        args: A list of arguments to pass to git command

    Returns:
        A String output of the git command
    """
    return str(subprocess.check_output(['git'] + list(args)).strip().decode())

def compare_and_pull(repo_current_commit):
    """Compares the repo's current commit with the latest commit.
        If different, it does a git pull

    Args:
        repo_current_commit: A string containing the repo's current commit

    Returns:
        None
    """
    latest_commit = git_output("rev-parse", "HEAD")
    current_commit = cache.get(repo_current_commit)
    #app.logger.info('current commit ' + current_commit)
    if latest_commit != current_commit:
        #app.logger.info('currently pulling')
        git("pull")
        cache.set(repo_current_commit, latest_commit)


def set_latest_commit_cache(repo, GIT_REPOS_FOLDER):
    """Sets the repo's latest commit hash to cache

    Args:
        repo: A string of the repo name
        GIT_REPOS_FOLDER: A string to the git repo folder path

    Returns:
        None
    """
    os.chdir(GIT_REPOS_FOLDER+repo)
    current_commit = git_output("rev-parse", "HEAD")
    if repo == '/terraform':
        cache.set('terraform_current_commit', current_commit)
    elif repo == '/terraform-cognite-modules':
        cache.set('modules_current_commit', current_commit)
