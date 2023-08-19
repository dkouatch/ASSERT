"""
Main file for testing implementation of ASSERT

"""
import datetime as dt
import logging
import argparse

from pathlib import Path
from typing import Any
from src.lib.earthsystems_reg import EarthSystemsReg
from src.models.model_e.model_e_reg import ModelEReg
from src.lib.utils.logger import logger_setup


# Time stamp
start_time = dt.datetime.now()

# Command-line parser for the filename
parser = argparse.ArgumentParser(
    prog='ASSERT',
    description='Main Script for running ASSERT',
    usage='assert/main.py [options]'
)
parser.add_argument('filename', action='store',
                    help='Provide full file path')
parser.add_argument('-m', '--model', action='store', required=True,
                    help='Provide model type', dest='modeltype')
args = parser.parse_args()
filename = args.filename
modeltype = args.modeltype


# Removes default threshold level from root logger to allow
# Sub-loggers to have custom file and stream threshold levels
logging.basicConfig(level=logging.NOTSET)

# Logger setup
logger = logger_setup(filename=__name__,
                      file_handler=True,
                      file_level=logging.INFO,
                      stream_handler=True,
                      stream_level=logging.INFO)
pwd = Path.cwd()


# Main wrapper class
class Main:
    def __init__(self, model_type: str, file_name: str):
        """
        Wrapper for all the classes

        Parameters
        ----------
        model_type : str
            Model type
        file_name : str
            File name of YAML config file
        """
        # Our ASSERT class manager
        self.reg: EarthSystemsReg

        self.file_name = file_name
        self.model_type = model_type

        if model_type == 'modelE':
            self.reg = ModelEReg(file_name, dt.datetime.now())
        # elif model_type == 'GEOS':
        #     self.reg = GeosReg(file_name, dt.datetime.now())
        # elif model_type == 'GCE':
        #     self.reg = GceReg(file_name, dt.datetime.now())
        # elif model_type == 'NuWRF':
        #     self.reg = NuWrfReg(file_name, dt.datetime.now())
        else:
            self.reg = EarthSystemsReg(file_name, dt.datetime.now())

    def run(self) -> Any:
        """
        Runs entire regression test

        """
        logger.notice(f'Commencing {self.model_type} regression '
                      f'test of {self.file_name}')
        self.reg.reset_scratch()
        self.reg.initialize()
        self.reg.report(dt.datetime.now())
        logger.success('Regression Test Completed.')


head = Main(modeltype, filename)
head.run()

log_file = pwd / 'assert.log'
log_file.rename(str(log_file.parent) + f'/assert_' +
                f'{start_time.strftime("%Y-%m-%d_%H-%M-%S")}.log')
