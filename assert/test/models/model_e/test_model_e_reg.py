import pytest
import datetime as dt
import tempfile as tmp
import src.lib.utils.paths as paths

from pathlib import Path
from src.models.model_e.model_e_reg import ModelEReg

paths.create_dir('scratch_test-model-e-reg')
scratch_dir = Path.cwd() / 'scratch_test-model-e-reg'

yaml_text = f"""\
modelconfig:
   model: ESM
systemconfig:
  scratchdir: {str(scratch_dir)}
reportconfig:
  message: ASSERT
  mailto: ???
  html: no
testcases:
  Test Case 1:
    variables: [some, 2, yes]
  Test Case 2:
    variables: [other, 3, no]
"""

file1 = tmp.NamedTemporaryFile(suffix='.yaml', mode='w', delete=False)
file1.write(yaml_text)


def test_reset_scratch():
    reg = ModelEReg(yaml_file=file1.name, start_time=dt.datetime.now())
    reg.reset_scratch()
    assert not list(scratch_dir.iterdir())
    scratch_dir.rmdir()


file1.close()
