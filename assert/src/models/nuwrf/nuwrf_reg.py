"""
NU-WRF Regression Manager Class

"""
import datetime as dt
import logging

from src.lib.utils.logger import logger_setup
from src.lib.earthsystems_reg import EarthSystemsReg
from src.models.nuwrf.nuwrf_report import NuWrfReport
from src.models.nuwrf.nuwrf_testcase import NuWrfTestcase

logger = logger_setup(filename=__name__,
                      file_handler=False,
                      stream_handler=True,
                      level=logging.INFO)


class NuWrfReg(EarthSystemsReg):
    def __init__(self, yaml_file: str, start_time: dt.datetime):
        """
        Parameters
        ----------
        yaml_file : str
            YAML config file name
        start_time : dt.datetime
            Starting time as a datetime object

        """
        super().__init__(yaml_file, start_time)

    def get_repo_type(self):
        """
        NU-WRF implementation of get_repo_type()

        Returns
        -------
        str
            NU-WRF uses git

        """
        return 'git'

    def get_repo_url(self):
        """
        NU-WRF implementation of get_repo_url()

        Returns
        -------
        str
            Repository URL

        """
        pass

    def get_repo_branch(self):
        """
        NU-WRF implementation of get_repo_branch()

        May not exist???

        Returns
        -------
        str
            Repository branch

        """
        pass

    def get_scratch_dir(self) -> str:
        """
        NU-WRF implementation of get_scratch_dir()

        Returns
        -------
        str
            Scratch directory

        """
        return self.system_cfg['scratchdir']

    def set_test_cfg(self, yaml_dict: dict) -> NuWrfTestcase:
        """
        Sets the test cfg class according to the model.

        Implemented by child classes (model-dependent).

        Parameters
        ----------
        yaml_dict : dict
            Config dictionary

        Returns
        -------
        EarthSystemsTestcase
            Testcase manager class object for modelE

        """
        return NuWrfTestcase(
            [dict()],
            scratch_dir=self.get_scratch_dir()
        )

    def set_report_cfg(self, yaml_dict: dict) -> NuWrfReport:
        """
        Sets the report cfg class according to the model.

        Implemented by child classes (model-dependent).

        Parameters
        ----------
        yaml_dict : dict
            Config dictionary

        Returns
        -------
        EarthSystemsTestcase
            Testcase manager class object for modelE

        """
        return NuWrfReport(
            model_cfg=self.model_cfg,
            system_cfg=self.system_cfg,
            report_cfg=dict(),
            start_time=self.start_time
        )

    def setup(self) -> None:
        """
        NU-WRF implementation of setup()

        """
        self.test_cfg.set_runnable_tests()
        self.test_cfg.setup_tests(
            time_stamp=self.start_time.strftime('%Y%m%d_%H%M%S')
        )
        logger.notice('NU-WRF — setup successful')

    def compile(self, test_name: str, cwd: str) -> None:
        """
        NU-WRF implementation of compile()

        Parameters
        ----------
        test_name : str
            Name of test whose imported code will be compiled
        cwd : str
            Current working directory (should be appropriate)

        """
        logger.info(f'NU-WRF — Building {test_name}...')

        # run_cmd(['make', 'rundeck', test_name])
        # run_cmd(['make', 'gcm', test_name])

    def run(self, test_name: str, cwd: str) -> None:
        """
        NU-WRF implementation of run()

        Parameters
        ----------
        test_name : str
            Name of test whose imported code will be compiled
        cwd : str
            Current working directory (should be appropriate)

        """
        logger.info(f'NU-WRF — Running {test_name}...')

    def compare(self, test_name: str, cwd: str) -> None:
        """
        NU-WRF implementation of compare()

        Parameters
        ----------
        test_name : str
            Name of test whose imported code will be compiled
        cwd : str
            Current working directory (should be appropriate)

        """
        logger.info(f'NU-WRF — Comparing {test_name}...')

    def initialize(self) -> None:
        """
        NU-WRF implementation of initialize_reg()

        """
        self.setup()

        self.reset_scratch()

    def report(self, end_time: dt.datetime) -> None:
        """
        NU-WRF implementation of report()

        Parameters
        ----------
        end_time : dt.datetime

        """
        logging.notice(f'NU-WRF — Creating report...')
