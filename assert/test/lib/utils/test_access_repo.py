import pytest
from pathlib import Path

from src.lib.utils.access_repo import *

repo_urls = ["https://github.com/JulesKouatchou/temperature_converter",
             "https://github.com/dkouatch/empty.git",
             "https://git.smce.nasa.gov/astg/gce_regression.git",
             "https://google.com",
             ]
dir_names = [None, None, 'GCE', 'Google_Test']
branch_names = ['main', None, 'jkouatch-main-patch-75779', None]
clone_depths = [None, None, 5, -4]
overwrites = [True, False, False, True]
host_names = [None, None, None, None]
confirms = [True, True, True, False]


@pytest.mark.parametrize(
    "repo_url, dir_name, branch_name, clone_depth,"
    "overwrite, host_name, confirm",
    [(repo_urls[0], dir_names[0], branch_names[0], clone_depths[0],
      overwrites[0], host_names[0], confirms[0]),
     (repo_urls[1], dir_names[1], branch_names[1], clone_depths[1],
      overwrites[1], host_names[1], confirms[1]),
     (repo_urls[2], dir_names[2], branch_names[2], clone_depths[2],
      overwrites[2], host_names[2], confirms[2]),
     (repo_urls[3], dir_names[3], branch_names[3], clone_depths[3],
      overwrites[3], host_names[3], confirms[3])
     ])
def test_git_clone(repo_url, dir_name, branch_name, clone_depth,
                   overwrite, host_name, confirm):
    pass
    """
    try:
        git_clone(repo_url=repo_url,
                  directory_name=dir_name,
                  branch_name=branch_name,
                  clone_depth=clone_depth,
                  overwrite=overwrite,
                  host_name=host_name)
    except Exception:
        pass
    else:
        if not dir_name:
            dir_name = Path(repo_url).stem
        assert confirm == confirm_git_clone(dir_name)
        """


@pytest.mark.parametrize("repo_type, repo_url, dir_name, branch_name,"
                         "clone_depth, overwrite, host_name, confirm",
                         [('git', repo_urls[0], dir_names[0],
                           branch_names[0], clone_depths[0],
                           overwrites[0], host_names[0], confirms[0]),
                          ('git', repo_urls[1], dir_names[1],
                           branch_names[1], clone_depths[1],
                           overwrites[1], host_names[1], confirms[1]),
                          ('git', repo_urls[2], dir_names[2],
                           branch_names[2], clone_depths[2],
                           overwrites[2], host_names[2], confirms[2]),
                          ('git', repo_urls[3], dir_names[3],
                           branch_names[3], clone_depths[3],
                           overwrites[3], host_names[3], confirms[3])
                          ])
def test_access_repo(repo_type, repo_url, dir_name, branch_name,
                     clone_depth, overwrite, host_name, confirm):
    pass
    """
    try:
        get_repo(repo_type=repo_type, repo_url=repo_url,
                 directory_name=dir_name, branch_name=branch_name,
                 clone_depth=clone_depth, host_name=host_name)
    except Exception:
        pass
    else:
        if not dir_name:
            dir_name = Path(repo_url).stem
        assert confirm == confirm_git_clone(dir_name)
        """
