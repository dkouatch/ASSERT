"""
GEOS Regression Manager Class

"""
import datetime as dt
import logging

from src.lib.utils.logger import logger_setup
from src.lib.earthsystems_reg import EarthSystemsReg
from src.models.geos.geos_report import GeosReport
from src.models.geos.geos_testcase import GeosTestcase

logger = logger_setup(filename=__name__,
                      file_handler=False,
                      stream_handler=True,
                      level=logging.INFO)


class GeosReg(EarthSystemsReg):
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
        GEOS implementation of get_repo_type()

        Returns
        -------
        str
            GEOS uses git

        """
        return 'git'

    def get_repo_url(self):
        """
        GEOS implementation of get_repo_url()

        Returns
        -------
        str
            Repository URL

        """
        pass

    def get_repo_branch(self):
        """
        GEOS implementation of get_repo_branch()

        May not exist???

        Returns
        -------
        str
            Repository branch

        """
        pass

    def get_scratch_dir(self) -> str:
        """
        GEOS implementation of get_scratch_dir()

        Returns
        -------
        str
            Scratch directory

        """
        return self.system_cfg['scratchdir']

    def set_test_cfg(self, yaml_dict: dict) -> GeosTestcase:
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
        return GeosTestcase(
            [dict()],
            scratch_dir=self.get_scratch_dir()
        )

    def set_report_cfg(self, yaml_dict: dict) -> GeosReport:
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
        return GeosReport(
            model_cfg=self.model_cfg,
            system_cfg=self.system_cfg,
            report_cfg=dict(),
            start_time=self.start_time
        )

    def setup(self) -> None:
        """
        GEOS implementation of setup()

        """
        self.test_cfg.set_runnable_tests()
        self.test_cfg.setup_tests(
            time_stamp=self.start_time.strftime('%Y%m%d_%H%M%S')
        )
        logger.notice('GEOS — setup successful')

    def compile(self, test_name: str, cwd: str) -> None:
        """
        GEOS implementation of compile()

        Parameters
        ----------
        test_name : str
            Name of test whose imported code will be compiled
        cwd : str
            Current working directory (should be appropriate)

        """
        logger.info(f'GEOS — Building {test_name}...')

        # run_cmd(['make', 'rundeck', test_name])
        # run_cmd(['make', 'gcm', test_name])

    def run(self, test_name: str, cwd: str) -> None:
        """
        GEOS implementation of run()

        Parameters
        ----------
        test_name : str
            Name of test whose imported code will be compiled
        cwd : str
            Current working directory (should be appropriate)

        """
        logger.info(f'GEOS — Running {test_name}...')

    def compare(self, test_name: str, cwd: str) -> None:
        """
        GEOS implementation of compare()

        Parameters
        ----------
        test_name : str
            Name of test whose imported code will be compiled
        cwd : str
            Current working directory (should be appropriate)

        """
        logger.info(f'GEOS — Comparing {test_name}...')

    def initialize(self) -> None:
        """
        GEOS implementation of initialize_reg()

        """
        self.setup()

        self.reset_scratch()

    def report(self, end_time: dt.datetime) -> None:
        """
        GEOS implementation of report()

        Parameters
        ----------
        end_time : dt.datetime

        """
        logging.notice(f'GEOS — Creating report...')
