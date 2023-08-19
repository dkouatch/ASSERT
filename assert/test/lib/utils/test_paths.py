import pytest

from src.lib.utils.paths import *

cwd = Path.cwd()
home = Path.home()


"""def test_check_file_exists(config_file):
    with open(config_file, 'r') as _:
        assert check_file_exists(config_file) is True"""


def test_get_current_dir():
    assert isinstance(get_current_dir(), Path)


def test_get_home_dir():
    assert isinstance(get_home_dir(), Path)


@pytest.mark.parametrize("path, name",
                         [('/Users/Guest/script.py', 'script.py'),
                          ('/Users/Guest/Downloads/', 'Downloads'),
                          ('/Users/Guest/Documents/.hidden', '.hidden')])
def test_get_name(path: str, name: str):
    assert get_name(path) == name


@pytest.mark.parametrize("path, stem",
                         [('/Users/Guest/script.py', 'script'),
                          ('/Users/Guest/Downloads/', 'Downloads'),
                          ('/Users/Guest/Documents/.hidden', '.hidden')])
def test_get_stem(path: str, stem: str):
    assert get_stem(path) == stem


@pytest.mark.parametrize("path, suffix",
                         [('/Users/Guest/script.py', '.py'),
                          ('/Users/Guest/Downloads/', ''),
                          ('/Users/Guest/Documents/.hidden', '')])
def test_get_suffix(path: str, suffix: str):
    assert get_suffix(path) == suffix


@pytest.mark.parametrize("path, anchor",
                         [('/Users/Guest/script.py', '/'),
                          ('/Users/Guest/Downloads/', '/'),
                          ('/Users/Guest/Documents/.hidden', '/')])
def test_get_anchor(path: str, anchor: str):
    assert get_anchor(path) == anchor


@pytest.mark.parametrize("path, parent",
                         [('/Users/Guest/script.py',
                           Path('/Users/Guest/')),
                          ('/Users/Guest/Downloads/',
                           Path('/Users/Guest/')),
                          ('/Users/Guest/Documents/.hidden',
                           Path('/Users/Guest/Documents/'))])
def test_get_parent(path: str, parent: Path):
    assert get_parent(path) == parent


@pytest.mark.parametrize("path, address",
                         [(Path('/Users/Guest/script.py'),
                           '/Users/Guest/script.py'),
                          (Path('/Users/Guest/Downloads/'),
                           '/Users/Guest/Downloads'),
                          (Path('/Users/Guest/Documents/.hidden'),
                           '/Users/Guest/Documents/.hidden')])
def test_get_path_address(path: Path, address: str):
    assert get_path_address(path) == address


@pytest.mark.parametrize("path, current_dir",
                         [(str(Path.home()), home),
                          (str(cwd), cwd)])
def test_change_dir(path, current_dir):
    change_dir(path)
    assert Path.cwd() == current_dir

