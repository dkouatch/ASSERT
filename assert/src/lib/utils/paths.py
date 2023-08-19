"""
Utilities for running commands.

  - Pathlib Attribute Functions
      * get_file_name
      * get_file_stem
      * get_file_suffix
      * get_file_anchor
      * get_parent
      * get_current_dir
      * get_home_dir

  - File/Directory Manipulation Functions
      * change_dir
      * create_dir
      * create_empty_file
      * copy_file

  - File/Directory Search Functions
      * check_file_exists
      * check_dir_exists
      * find_files
      * grep_file

  - Listing Functions (ls command)
      * list_all_paths
      * list_all
      * list_subfile_paths
      * list_subfiles
      * list_subdir_paths
      * list_subdirs
      * list_subfile_paths_ext
      * list_subfiles_ext

  - Tree Functions (tree command)
      * tree
      * tree_paths
      * are_dir_trees_equal

  - Other Functions
      * which
      * create_link

  - Command line arguments
      * parse_command_line_args

  - Run Commands
      * sp_call
      * sp_check_call_make_log
      * run_shell_command
      * run_configure

"""
import os
import sys
import shutil
import filecmp
import logging
import subprocess as sp

from pathlib import Path
from typing import Any
from src.lib.utils.logger import logger_setup

# Logger settings
logger = logger_setup(filename=__name__,
                      file_handler=True,
                      file_level=logging.WARNING,
                      stream_handler=False)


def check_file_exists(file_path: str) -> bool:
    """
    Check if file exists given its path.

    Parameters
    ----------
    file_path : str
        File path.

    Returns
    -------
    result : bool
        Whether file path exists or not
    """
    return Path(file_path).is_file()
    # logger.error(f'The file {file_path} does not exists!')


def check_dir_exists(dir_path: str) -> bool:
    """
    Check if a directory exists given its path.

    Parameters
    ----------
    dir_path : str
        File path.

    Returns
    -------
    result : bool
        Whether file path exists or not
    """
    return Path(dir_path).is_dir()
    # logger.error(f'The directory {dir_path} does not exists!')


def get_path_address(path: Path) -> str:
    """
    Returns the full path address of a Path object

    Parameters
    ----------
    path : Path
        A Path object

    Returns
    -------
    str
        The path address of the Path object

    """
    return str(path)


def get_name(path_name: str) -> str:
    """
    Extracts the file's name given its path
    Note that file does not need to actually exist
    and therefore does not check for that.

    Parameters
    ----------
    path_name : str
        The path of a file

    Returns
    -------
    file_name: str
        The file name of the given file path
    """
    logger.spam("Getting file's name")
    return Path(path_name).name


def get_stem(path_name: str) -> str:
    """
    Extracts the file's stem name given its path
    Note that file does not need to actually exist
    and therefore does not check for that.

    Parameters
    ----------
    path_name : str
        The path of a file

    Returns
    -------
    stem_name: str
        The stem name of the given file path
    """
    logger.spam("Getting file's stem name")
    return Path(path_name).stem


def get_suffix(path_name: str) -> str:
    """
    Extracts the file's suffix name given its path
    Note that file does not need to actually exist
    and therefore does not check for that.

    Parameters
    ----------
    path_name : str
        The path of a file

    Returns
    -------
    suffix_name: str
        The suffix name of the given file path
    """
    logger.spam("Getting file's suffix")
    return Path(path_name).suffix


def get_anchor(path_name: str) -> str:
    """
    Extracts the file's anchor given its path
    Note that file does not need to actually exist
    and therefore does not check for that.

    Parameters
    ----------
    path_name : str
        The path of a file

    Returns
    -------
    anchor: str
        The ancho of the given file path
    """
    logger.spam("Getting file's anchor")
    return Path(path_name).anchor


def get_parent(path_name: str) -> Path:
    """
    Extracts the file's/directory's parent directory given its path
    Note that file does not need to actually exist
    and therefore does not check for that.

    Parameters
    ----------
    path_name : str
        The path of a file

    Returns
    -------
    parent_name: Path
        The path object of the parent directory of the given file path
    """
    logger.spam("Getting file's parent")
    return Path(path_name).parent


def change_dir(dir_path: str) -> None:
    """
    Change the current directory

    Parameters
    ----------
    dir_path : str
        Path of the directory
    """
    if check_dir_exists(dir_path):
        os.chdir(Path(dir_path))
    else:
        logger.error(f'Directory {dir_path} does not exist.')


def get_current_dir() -> Path:
    """
    Get the current directory of the OS.

    Returns
    -------
    cwd: str
        The path object corresponding to the current working directory
    """
    return Path.cwd()


def get_home_dir() -> Path:
    """
    Get the home directory of the OS.

    Returns
    -------
    home_dir: str
        The path object corresponding to the current working directory
    """
    return Path.home()


def create_dir(dir_path: str) -> None:
    """
    Create a directory (with all its parents) and does error checking.

    Parameters
    ----------
    dir_path : str
       Full path of directory that we want to create.
    """
    try:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        logger.debug(f'Created the directory: {dir_path}')
    except FileExistsError:
        if Path(dir_path).exists():
            logger.warning(f'Directory already exists: {dir_path}',
                           exc_info=True)
        else:
            logger.error(f'Permission denied: cannot create {dir_path}',
                         exc_info=True)
            sys.exit()


def create_empty_file(file_path: str) -> None:
    """
    Equivalent to Linux 'touch' command

    Parameters
    ----------
    file_path : str
        The full file path or file name
    """
    try:
        Path(file_path).touch(exist_ok=True)
    except FileExistsError:
        logger.warning(f'Could not create the file: {file_path}',
                       exc_info=True)


def list_all_paths(dir_name: str) -> list[Path]:
    """
    Lists both directories and files within
    a directory given its path name

    Parameters
    ----------
    dir_name : str
        The path name of a directory

    Returns
    -------
    list[Path]
        The directories and files within a directory
        as a list of Path objects
    """
    dir_path = Path(dir_name)
    if dir_path.exists():
        return list(dir_path.iterdir())
    else:
        logger.error(f'The directory does not exist: {dir_name}')
        return []


def list_all(dir_name: str) -> list[str]:
    """
    Lists the Path objects of both directories and
    files within a directory given its path name

    Parameters
    ----------
    dir_name : str
        The path name of a directory

    Returns
    -------
    list[str]
        The names of directories and files within a directory
    """
    paths = list_all_paths(dir_name)
    return [obj.name for obj in paths]


def list_subfile_paths(dir_name: str) -> list[Path]:
    """
    Lists files as Path objects within a directory given
    the directory's path name

    Parameters
    ----------
    dir_name : str
        The path name of a directory

    Returns
    -------
    list[Path]
        The files within a directory as a list of Path objects
    """
    sub_all = list_all_paths(dir_name)
    return [obj for obj in sub_all if obj.is_file()]


def list_subfiles(dir_name: str) -> list[str]:
    """
    Lists files within a directory given its path name

    Parameters
    ----------
    dir_name : str
        The path name of a directory

    Returns
    -------
    list[str]
        The files within a directory
    """
    return [obj.name for obj in list_subfile_paths(dir_name)]


def list_subfile_paths_with_ext(dir_name: str, ext: str) -> list[Path]:
    """
    Lists files wit extension within a directory as Path objects
    given the directory's path name

    Parameters
    ----------
    dir_name : str
        The path name of a directory

    ext : str
        The desired file extension

    Returns
    -------
    list[Path]
        The files within a directory with the extension 'ext' as Path objects
    """
    return [obj for obj in list_subfile_paths(dir_name) if obj.suffix == ext]


def list_subfiles_with_ext(dir_name: str, ext: str) -> list[str]:
    """
    Lists files wit extension within a directory as Path objects
    given the directory's path name

    Parameters
    ----------
    dir_name : str
        The path name of a directory

    ext : str
        The desired file extension

    Returns
    -------
    list[str]
        The files within a directory with the extension 'ext'
    """
    return [obj.name for obj in list_subfile_paths_with_ext(dir_name, ext)]


def list_subdir_paths(dir_name: str) -> list[Path]:
    """
    Lists  files within a directory given its path name

    Parameters
    ----------
    dir_name : str
        The path name of a directory

    Returns
    -------
    list[Path]
        The directories within a directory as a list of Path objects
    """
    sub_all = list_all_paths(dir_name)
    return [obj for obj in sub_all if obj.is_dir()]


def list_subdirs(dir_name: str) -> list[str]:
    """
    Lists  files within a directory given its path name

    Parameters
    ----------
    dir_name : str
        The path name of a directory

    Returns
    -------
    list[str]
        The subdirectories within a directory
    """
    return [obj.name for obj in list_subdir_paths(dir_name)]


def tree(dir_name: str) -> None:
    """
    Prints out the tree structure of a directory given its path

    Parameters
    ----------
    dir_name : str
        The path name of a directory
    """
    dir_path = Path(dir_name)
    if not dir_path.exists():
        logger.error(f'The directory does not exist: {dir_name}')
    elif not dir_path.is_dir():
        logger.error(f'The path does not lead to a directory: {dir_name}')
    else:
        print(f"+ {dir_name}")
        for path in sorted(dir_path.rglob("*")):
            level = len(path.relative_to(dir_path).parts)
            space = "    " * level
            print(f"{space} + {path.name}")


def tree_given_path(dir_path: Path) -> None:
    """
    Prints out the tree structure of a directory given as a Path object

    Parameters
    ----------
    dir_path : Path
        The path object of a directory
    """
    dir_name = dir_path.name
    if not dir_path.exists():
        logger.error(f'The directory does not exist: {dir_name}')
    elif not dir_path.is_dir():
        logger.error(f'The path does not lead to a directory: {dir_name}')
    else:
        print(f"+ {dir_name}")
        for path in sorted(dir_path.rglob("*")):
            level = len(path.relative_to(dir_path).parts)
            space = "    " * level
            print(f"{space} + {path.name}")


def find_files(src_dir: str, pattern: str) -> list[str]:
    """
    Find files under 'src_dir' matching 'pattern'.

    Parameters
    ---------
    src_dir : str
        The name of top directory for file search
    pattern : str
        The pattern to be used to look for files matching it.

    Returns
    -------
    list[str]
        List of matched files
    """
    return [obj.name for obj in list(Path(src_dir).glob(pattern))]


def recurs_find_files(src_dir: str, pattern: str) -> list[str]:
    """
    Find files recursively under 'src_dir' matching 'pattern'.

    Parameters
    ----------
    src_dir : str
        The name of top directory for file search
    pattern : str
        The pattern to be used to look for files matching it.

    Returns
    -------
    list[str]
        List of matched files
    """
    return [str(obj) for obj in list(Path(src_dir).rglob(pattern))]


def clean_dir(adir: str) -> None:
    """
    'Safe' way to clean the contents of a directory

    Parameters
    ----------
    adir : directory
    """

    if adir == '/' or adir == "\\":
        logger.error('Cannot clean %s', adir)
        return
    else:
        for file_object in os.listdir(adir):
            logger.info('Will clean up %s', adir)
            file_object_path = os.path.join(adir, file_object)
            if os.path.isfile(file_object_path):
                os.unlink(file_object_path)
            else:
                try:
                    shutil.rmtree(file_object_path)
                except OSError:
                    logger.error('Permission denied: cannot remove '
                                 + file_object_path, exc_info=True)
                    sys.exit()


def clean_scratch(scratch_dir: str) -> None:
    """
    Clean the directory where the run will take place.

    Parameters
    ----------
    scratch_dir : str
        Directory where all the work will be performed
    """

    if not Path(scratch_dir).exists():
        logger.warning(f'The folder {scratch_dir} does not exists!')
    else:
        clean_dir(scratch_dir)


def copy_file(src: str, dest: str) -> None:
    """
    Copies from src file to dest file

    Parameters
    ----------
    src : str
        Source file
    dest : str
        Destination file
    """
    if not check_file_exists(src) or not check_file_exists(dest):
        logger.error('Source and destination files must both exist.')
    elif src == dest:
        logger.error('Source and destination files must be different')
    else:
        try:
            shutil.copy(src, dest)
        except OSError as e:
            logger.error(f'Error: {e}', exc_info=True)


def which(program: Any) -> Any:
    """
    Test if an executable program exists in the path - like unix's which

    Parameters
    ----------
    program : Any
        A program

    Returns
    -------
    Any
        Either the program, exe_file, or None
    """

    def is_exe(file_path):
        return os.path.isfile(file_path) and os.access(file_path, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file
    return None


def grep_file(file_name: str, pattern: str) -> bool:
    """
    Parameters
    ----------
    file_name : str
        The file name
    pattern : str
        The pattern to search for

    Returns
    -------
    bool
        True if pattern found in file, False otherwise.

    """
    with open(file_name, 'r') as file:
        for line in file:
            if pattern in line:
                return True
        return False


def create_link(target: str, directory: str, link_name: str) -> None:
    """
    Create link 'link_name' to 'target' in 'directory'.
    Implement the 'ln -s target directory/link_name' functionality

    Parameters
    ----------
    target : str
       The name of target file or directory.
    directory : str
    link_name : str

    """
    cmd = ['ln', '-s', target, directory + '/' + link_name]
    run = sp.check_call(cmd)


def are_dir_trees_equal(dir1, dir2) -> bool:
    """
    Compare two directories recursively. Files in each directory are
    assumed to be equal if their names and contents are equal.

    Parameters
    ----------
    dir1
        First directory path
    dir2
        Second directory path

    Returns
    -------
    bool
        True if the directory trees are the same and
        there were no errors while accessing the directories or files, 
        False otherwise.

   """
    dirs_cmp = filecmp.dircmp(dir1, dir2)
    if (len(dirs_cmp.left_only) > 0 or
            len(dirs_cmp.right_only) > 0 or
            len(dirs_cmp.funny_files) > 0):
        return False
    (_, mismatch, errors) = filecmp.cmpfiles(dir1, dir2,
                                             dirs_cmp.common_files, shallow=False)
    if len(mismatch) > 0 or len(errors) > 0:
        return False
    for common_dir in dirs_cmp.common_dirs:
        new_dir1 = os.path.join(dir1, common_dir)
        new_dir2 = os.path.join(dir2, common_dir)
        if not are_dir_trees_equal(new_dir1, new_dir2):
            return False
    return True


if __name__ == '__main__':
    """
    path = '/Users/deon.kouatchou/ASSERT'
    print()
    print(find_files(path, '*'))
    print()
    print(recurs_find_files(path, '*'))
    """
