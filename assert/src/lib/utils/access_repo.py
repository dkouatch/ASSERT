#!/usr/bin/env python

"""
Contains a function for accessing Git repositories:

 - git_clone
 - confirm_git_clone
"""

import logging
import subprocess as sp
import os

from pathlib import Path
from src.lib.utils.config import config_section_map
from src.lib.utils.paths import check_dir_exists, check_file_exists
from src.lib.utils.server import is_valid_url
from src.lib.utils.logger import logger_setup

# Logger format settings
logger = logger_setup(filename=__name__,
                      file_handler=True,
                      file_level=logging.INFO,
                      stream_handler=False)


def get_repo(repo_type: str,
             local: bool = False,
             configs: bool = False,
             **kwargs) -> None:
    """

    Parameters
    ----------
    repo_type : str
        Type of repository: git/cvs/svn
    local : bool
        For CVS – True if a local repo checkout, False otherwise
    configs : bool
        For CVS – True if kwargs is just 'config', False otherwise
    kwargs : dict
        Rest of appropriate entries for respective repository
        access functions

    """
    if repo_type == 'git':
        git_clone(**kwargs)
    elif repo_type == 'cvs':
        if configs:
            cvs_checkout_repository(**kwargs)
        elif local:
            cvs_checkout(**kwargs)
        else:
            cvs_checkout_repos(**kwargs)
    elif repo_type == 'svn':
        svn_checkout_repository(**kwargs)
    else:
        raise Exception('Repo type must be git, cvs, or svn.')


def run_cmd(cmd: list[str], **kwargs) -> bool:
    """
    Supporting function for running commands related to cloning

    Parameters
    ----------
    cmd : list[str]
       List of strings to run as command in command-line
    kwargs
       Dictionary of other args for sp

    Returns
    -------
    bool
        True if command run was successful, False otherwise.

    """
    run = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE, **kwargs)

    output = run.communicate()
    return_code = run.wait()
    if return_code != 0:
        logger.error(f'0: {output[0].decode("UTF-8")} \n'
                     f'1: {output[1].decode("UTF-8")}')
        return False
    else:
        return True


def rm_dir(directory_name: str) -> bool:
    """
    Removes a directory and all its contents given its path

    Parameters
    ----------
    directory_name : str
        Path/name of directory

    Returns
    -------
    bool
        Returns True if removal was complete and
        False if it failed or error arises.

    """
    remove_cmd = ['rm', '-fr', directory_name]

    logger.debug(f'Removing {directory_name} directory...')
    return run_cmd(remove_cmd)


def check_repo_url(repo_url: str) -> bool:
    """
    Checks if the repo_url is a valid URL address or a valid local
    repository/directory.

    Parameters
    ----------
    repo_url : str
        Repository address

    Returns
    -------
    bool
        True if valid URL or local repository, False otherwise.

    """
    return is_valid_url(repo_url) or check_dir_exists(repo_url)


def config_git_clone(repo_url: str,
                     directory_name: str = None,
                     branch_name: str = None,
                     clone_depth: int = None,
                     host_name: str = None) -> list[str]:
    """
    Configures the command to run git clone

    Parameters
    ----------
    repo_url : str
        Directory to clone from
    directory_name : str
        Custom local directory name for repository,
        if None checkout repo name
    branch_name : str
        Check out tag branch_name, if None checkout
        default tag of repo
    clone_depth : int
        The depth to which to clone
    host_name : str
        Host name

    Returns
    -------
    list[str]
        List of commands to be run in the form:
        ...git clone -b <branch_name> --depth <clone_depth>
           <repo_url> <directory_name>

    """
    # Logger Information for branch_name
    if branch_name:
        logger.info(f'Configuring clone command for '
                    f'[repo: {repo_url}, tag: {branch_name}]...')
    else:
        logger.info(f'Configuring clone command for '
                    f'[repo: {repo_url}]...')

    # Configuration based on host_name for git clone command
    if host_name == 'DISCOVER':
        cmd = ['/usr/local/other/git/2.30.2/libexec/git-core/git',
               'clone']
    elif host_name == 'PLEIADES':
        cmd = ['/nobackup/gmao_SIteam/git/git-2.21.0/bin/git',
               'clone']
    else:
        cmd = ['git', 'clone']

    # Configuration for repo branch name argument
    if branch_name:
        cmd.extend(['-b', ''.join(branch_name)])

    # Configuration for clone depth argument
    if clone_depth:
        if clone_depth > 0:
            cmd.extend(['--depth', str(clone_depth)])
        else:
            logger.error('Invalid clone depth. Quitting git clone...')
            raise Exception('git clone failed.')

    # Configuration for repo url argument
    cmd.append(repo_url)

    # Configuration for local directory destination argument
    if directory_name:
        cmd.append(directory_name)

    return cmd


def git_clone(repo_url: str,
              directory_name: str = None,
              branch_name: str = None,
              clone_depth: int = None,
              overwrite: bool = False,
              host_name: str = None) -> None:
    """
    Clone model from git repository.

    NOTE: Clones model in the directory it is called
          from and returns output of git command

    Parameters
    ----------
    repo_url : str
        Directory to clone from
    directory_name : str
        Custom local directory name for repository,
        if None checkout repo name
    branch_name : str
        Check out tag branch_name, if None checkout
        default tag of repo
    clone_depth : int
        The depth to which to clone
    overwrite : bool
        Whether to overwrite an existing directory with the same name
    host_name : str
        Host name

    """
    if not check_repo_url(repo_url):
        logger.error('Invalid repo address. Quitting git clone...')
        raise Exception('git clone failed.')

    if not directory_name:
        directory_name = Path(repo_url).stem

    full_dir_path = Path.cwd() / directory_name

    dir_exists = check_dir_exists(str(full_dir_path))

    if dir_exists and not overwrite:
        # Directory with same name already exists but client does not
        # want to overwrite existing directories
        logger.warning(f'Destination path {directory_name} already'
                       f' exists. Quiting git clone...')
        raise Exception('git clone failed.')
    elif dir_exists and overwrite:
        # Directory with same name exists but client wants to
        # overwrite pre-existing conflicts
        logger.debug(f'Overwriting existing {directory_name} '
                     f'directory...')
        if not rm_dir(directory_name):
            logger.error('Removal failed. Quitting git clone...')
            raise Exception('git clone failed.')

    try:
        cmd = config_git_clone(repo_url=repo_url,
                               directory_name=directory_name,
                               branch_name=branch_name,
                               clone_depth=clone_depth,
                               host_name=host_name)
    except:
        # Any error occurs in git clone command configuration such
        # as incorrect clone depth information
        return
    else:
        if not run_cmd(cmd):
            raise Exception('git clone failed.')
        else:
            logger.success('git clone successful.')
            if confirm_git_clone(directory_name):
                logger.success('git clone verified.')
            else:
                raise Exception('git clone could not be verified.')


def confirm_git_clone(directory_name: str,
                      ref_directory: str = str(Path.home())) -> bool:
    """
    Checks if git clone works externally

    NOTE: Clones model in the directory it is called from and returns
          output of git command

    Parameters
    ----------
    directory_name : str
        The name given to the directory containing the new repository
    ref_directory : str
        The name of the reference directory to search from

    Returns
    -------
    bool

    """
    pwd = Path.cwd()
    repo_directory = Path(directory_name)

    # Exception Instance 1: Repo directory does not exist
    if repo_directory not in list(pwd.glob('*')):
        # raise Exception('git clone failed – repo directory not created')
        logger.error('Repo directory not created.')
        return False

    # Exception Instance 2: Repo directory is empty
    # (i.e. doesn't at least contain .git file)
    if not list(repo_directory.iterdir()) and \
            not check_file_exists(directory_name + '/.git'):
        # raise Exception('git clone failed – repo directory is empty')
        logger.error('Repo directory is empty.')
        return False

    return True


def cvs_update(tag: str, mod: str = None) -> bool:
    """
    Query files that need to be updated and update those files.

    NOTE: needs to be called from src directory

    Parameters
    ----------
    tag : str
        CVS tag to check for new files
    mod : str
        Module directory being updated

    Returns
    -------
    bool
       True if files were updated, else returns False
    """

    if mod:
        logger.info(f'Updating {mod} to {tag}...')
    else:
        logger.info(f'Updating to {tag}...')

    # first query files that need to be updated
    cmd = ['cvs', '-nq', 'up', '-r', tag]
    run = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE)
    output = run.communicate()
    return_code = run.wait()
    if return_code != 0:
        print(f'0: {output[0].decode("UTF-8")} \n'
              f'1: {output[1].decode("UTF-8")}')
        raise Exception('CVS update query failed')
    upd_files = []
    changed_files = output[0].split('\n')
    for i in range(len(changed_files)):
        file = changed_files[i]
        if not file:
            break
        if file[0] == 'U':
            upd_files.append(file.split(' ')[1])
    if len(upd_files) == 0:
        logger.info('nothing to upd.\n')
        return False

    # now, update
    for i in range(len(upd_files)):
        cmd = ['cvs', 'up', '-r', tag, upd_files[i]]
        run = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE)
        output = run.communicate()
        return_code = run.wait()
        if return_code != 0:
            print(f'0: {output[0].decode("UTF-8")} \n'
                  f'1: {output[1].decode("UTF-8")}')
            raise Exception(f'CVS update failed for file '
                            f'[{upd_files[i]}]')

    logger.info('done.\n')

    # print list of updated files
    logger.info(f'Updated files tagged with {tag}:\n')
    for i in range(len(upd_files)):
        logger.info(f'   {upd_files[i]}\n')

    return True


def cvs_checkout(tag: str,
                 mod: str,
                 directory_name: str = None) -> tuple[bytes, bytes]:
    """
    Checkout model from CVS repository.

    NOTE: Checks out model in the directory it is
          called from and returns output of cvs command.

    Parameters
    ----------
    tag : str
        CVS tag to check out
    mod : str
        Corresponding module.
    directory_name : str
        Check out into directory_name instead,
        if None checkout into mod

    Returns
    -------
    tuple[bytes, bytes]
        A tuple containing output of command (stdout and stderr)
    """

    logger.info(f'Checking out [tag: {tag}, module: {mod}]...')

    cvs_root = os.environ['CVSROOT']

    if directory_name:
        cmd = ['cvs', '-d', cvs_root, 'co', '-P', '-r', tag, mod]
        # cmd = ['cvs', 'co', '-P', '-r', tag, '-d', directory_name, mod]
    else:
        cmd = ['cvs', 'co', '-P', '-r', tag, mod]
    print(cmd)
    run = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE)

    output = run.communicate()
    return_code = run.wait()
    if return_code != 0:
        print(f'0: {output[0].decode("UTF-8")} \n'
              f'1: {output[1].decode("UTF-8")}')
        raise Exception('CVS checkout failed')

    logger.info('done.\n')
    return output


def cvs_checkout_repository(config) -> None:
    """
    Cvs checkout repository function

    Parameters
    ----------
    config

    Returns
    -------

    """
    logger.info('Checkout user-specified cvs repository...')
    user_config = config_section_map(config, 'USERCONFIG')
    repo = user_config['repo_url']
    tag = user_config['repo_branch']
    user_id = user_config['repo_user_id']
    module = user_config['repo_module']

    cvs_repo = user_config['scratch_dir'] + '/builds'
    if not os.path.exists(cvs_repo):
        os.makedirs(cvs_repo)
    # if os.path.exists(cvs_repo):
    #   return
    cmd = (['cvs', '-Q', '-d', ':ext:' + user_id + '@' +
            repo, 'co', '-P', '-r', tag, module])

    logger.info(f'Checking out {repo} into {cvs_repo}')
    cwd = os.getcwd()
    os.chdir(cvs_repo)
    proc = sp.Popen(cmd)
    proc.wait()
    os.chdir(cwd)


def cvs_checkout_repos(tag: str,
                       mod: str,
                       repo_url: str,
                       user_id: str,
                       directory_name: str) -> None:
    """
    Cvs checkout repos function

    Parameters
    ----------
    tag : str
        CVS tag to check out
    mod : str
        Corresponding module.
    repo_url : str
        Location of remote repository
    user_id : str
        User ID
    directory_name : str
        Check out into directory_name instead,
        if None checkout into mod

    """
    cmd = (['cvs', '-Q', '-d', ':ext:' + user_id + '@' +
            repo_url, 'co', '-P', '-r', tag, mod])

    if not os.path.exists(directory_name):
        os.makedirs(directory_name)

    logger.info(f'Checking out {repo_url} into {directory_name}')
    cwd = os.getcwd()
    os.chdir(directory_name)
    proc = sp.Popen(cmd)
    proc.wait()
    os.chdir(cwd)


def confirm_cvs_checkouts():
    pass


def svn_checkout_repository(config) -> None:
    """
    Svn checkout repository function

    Parameters
    ----------
    config

    """
    logger.info('Checkout user-specified svn repository...')
    user_config = config_section_map(config, 'USERCONFIG')
    repo = user_config['repo_url']

    svn_repo = user_config['scratch_dir'] + '/builds/geosctm_repo'
    if os.path.exists(svn_repo):
        return
    cmd = (['svn', '--quiet', 'checkout', repo, svn_repo])

    logger.info(f'Checking out {repo} into {svn_repo}')
    cwd = os.getcwd()
    proc = sp.Popen(cmd)
    proc.wait()
    os.chdir(cwd)


def confirm_svn_checkout():
    pass


if __name__ == "__main__":
    repo_url1 = "https://github.com/dkouatch/empty.git"
    # git_clone(repo_url=repo_url1, overwrite=True)
    get_repo(repo_type='git', repo_url=repo_url1, overwrite=True)