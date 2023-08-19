import pytest
import tempfile as tmp
# import yaml

import src.lib.utils.config as config

text1 = """\
USERCONFIG:
  name: ASTG
  mail_to: ssaihq
  logger: yes
  repo_type: git
  repo_url: https://gitlab.smce.nasa.gov/astg/nothing.git
COMPCONFIG: 
  name: o2levels
  nodes: 2
  baseline: no
"""
load1 = {'USERCONFIG': {'name': 'ASTG',
                        'mail_to': 'ssaihq',
                        'logger': True,
                        'repo_type': 'git',
                        'repo_url': 'https://gitlab.smce.nasa.gov/'
                                    'astg/nothing.git'
                        },
         'COMPCONFIG': {'name': 'o2levels',
                        'nodes': 2,
                        'baseline': False
                        }
         }
file1 = tmp.NamedTemporaryFile(suffix='.yaml', mode='w', delete=False)
file1.write(text1)
file1_path = file1.name


@pytest.mark.parametrize('config_file, result',
                         [(file1_path, load1)])
def test_get_yaml_dict_is_dict(config_file, result):
    res = config.get_yaml_dict(config_file)
    assert isinstance(res, dict) and res == result


"""def test_get_yaml_dict_repo_type(config_file):
    with open(config_file, 'r') as file:
        config_data = yaml.safe_load(file)
    assert config_data['repo_type'] == 'git'"""


@pytest.mark.parametrize('section_name, var_name, result',
                         [('USERCONFIG', 'name', 'ASTG'),
                          ('USERCONFIG', 'cvs_update', None),
                          ('COMPCONFIG', 'nodes', 2),
                          ('TESTCONFIG', 'any', None)])
def test_get_yaml_variable_value(section_name,
                                 var_name, result):
    try:
        res = config.get_yaml_variable_value(yaml_dict=load1,
                                             section_name=section_name,
                                             var_name=var_name)
    except:
        assert result is None
    else:
        assert res == result


file1.close()

load2 = {
    'modelconfig': {'model': 'ESM'},
    'systemconfig': {'scratchdir': '/Users/deon.kouatchou/scratch'},
    'reportconfig': {'message': 'ASSERT'},
    'testcases': {'Test Case 1': {'variables': ['some', 2, True]},
                  'Test Case 2': {'variables': ['other', 3, False]}
                  }
}
testcases = [
    dict(name='Test Case 1',
         variables=['some', 2, True]),
    dict(name='Test Case 2',
         variables=['other', 3, False])
]


@pytest.mark.parametrize("yaml_dict, section_name, ignore, result",
                         [(load2, 'testcases', None, testcases),
                          (load2, None, ['modelconfig',
                                         'systemconfig',
                                         'reportconfig'], testcases),
                          (load2, 'testcases', ['modelconfig',
                                                'systemconfig',
                                                'reportconfig'],
                           testcases)
                          ])
def test_get_testcases(yaml_dict, section_name, ignore, result):
    assert config.get_testcases(yaml_dict, section_name, ignore) == result
