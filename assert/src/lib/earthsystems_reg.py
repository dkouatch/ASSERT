"""
Contains EarthSystemsReg class which acts as a generic manager
for the regression testing tool

"""
import datetime as dt
import src.lib.utils.config as config
import src.lib.utils.paths as paths
import logging

from src.lib.earthsystems_testcase import EarthSystemsTestcase
from src.lib.earthsystems_report import EarthSystemsReport

from src.lib.utils.logger import logger_setup
from src.lib.utils.server import get_hostname
from src.lib.utils.access_repo import get_repo

logger = logger_setup(filename=__name__,
                      file_handler=True,
                      file_level=logging.INFO,
                      stream_handler=True,
                      stream_level=logging.INFO)


class EarthSystemsReg:
    def __init__(self, yaml_file: str, start_time: dt.datetime):
        """
        Parameters
        ----------
        yaml_file : str
            YAML config file name
        start_time : dt.datetime
            Starting time as a datetime object

        """
        # Timestamp
        self.start_time: dt.datetime = start_time

        # Get dictionary from config file
        yaml_dict: dict = config.get_yaml_dict(yaml_file)

        # Model Config Info
        self.model_cfg: dict = yaml_dict['modelconfig']

        # System Config Info
        self.system_cfg: dict = yaml_dict['systemconfig']

        # Test Config Class
        self.test_cfg = self.set_test_cfg(yaml_dict)

        # Report Config Class
        self.report_cfg = self.set_report_cfg(yaml_dict)

    def get_repo_type(self) -> str:
        """
        Retrieves the type of repository from the config file.

        Implemented by child classes (model-dependent).

        Returns
        -------
        str
            Repository type: either 'git', 'cvs', or 'svn'

        """
        pass

    def get_repo_url(self) -> str:
        """
        Retrieves the URL of the repository to checkout/clone
        from the config file.

        Implemented by child classes (model-dependent).

        Returns
        -------
        str
            Repository URL

        """
        pass

    def get_repo_branch(self) -> str:
        """
        Retrieves the branch of the desired repository from
        the config file.

        Implemented by child classes (model-dependent).

        Returns
        -------
        str
            Repository branch

        """
        pass

    def get_scratch_dir(self) -> str:
        """
        Retrieves the scratch directory from the config file.

        Implemented by child classes (model-dependent).

        Returns
        -------
        str
            Scratch directory

        """
        pass

    def get_repo(self, directory_name: str, **kwargs) -> None:
        """
        Wrapper for get_repo() utility function to fit needs
        of reg classes.

        Exceptions raised in utility file if it fails.

        Parameters
        ----------
        directory_name : str
            Directory to put remote repository in
        kwargs : dict[str, Any]
            Appropriate keyword arguments for
            get_repo() utility function

        """
        get_repo(repo_type=self.get_repo_type(),
                 repo_url=self.get_repo_url(),
                 branch_name=self.get_repo_branch(),
                 directory_name=directory_name,
                 host_name=get_hostname(),
                 **kwargs)

    def set_test_cfg(self, yaml_dict: dict) -> EarthSystemsTestcase:
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
            Testcase manager class object that can be model_specific

        """
        return EarthSystemsTestcase(
            config.get_testcases(yaml_dict,
                                 section_name='testcases'),
            scratch_dir=self.get_scratch_dir()
        )

    def set_report_cfg(self, yaml_dict: dict) -> EarthSystemsReport:
        """
        Sets the report cfg class according to the model.

        Implemented by child classes (model-dependent).

        Parameters
        ----------
        yaml_dict : dict
            Config dictionary

        Returns
        -------
        EarthSystemsReport
            Report manager class object that can be model_specific

        """
        return EarthSystemsReport(
            model_cfg=self.model_cfg,
            system_cfg=self.system_cfg,
            report_cfg=yaml_dict['reportconfig'],
            start_time=self.start_time
        )

    def setup(self) -> None:
        """
        Sets up directory structures for tests.

        Implemented by child classes (model-dependent).

        """
        logger.notice('ESM — Setting up model...')

    def compile(self, test_name: str, cwd: str) -> None:
        """
        Compiles a test given its name and the appropriate
        current working directory.

        Implemented by child classes (model-dependent).

        Parameters
        ----------
        test_name : str
            Name of test whose imported code will be compiled
        cwd : str
            Current working directory (should be appropriate)

        """
        logger.info(f'ESM — Compiling {test_name}...')

    def run(self, test_name: str, cwd: str) -> None:
        """
        Runs a test given its name and the appropriate
        current working directory

        Implemented by child classes (model-dependent).

        Parameters
        ----------
        test_name : str
            Name of test whose imported code will be compiled
        cwd : str
            Current working directory (should be appropriate)

        """
        logger.info(f'ESM — Running {test_name}...')

    def compare(self, test_name: str, cwd: str) -> None:
        """
        Compares a test given its name and the appropriate
        current working directory

        Implemented by child classes (model-dependent).

        Parameters
        ----------
        test_name : str
            Name of test whose imported code will be compiled
        cwd : str
            Current working directory (should be appropriate)

        """
        logger.info(f'ESM — Comparing {test_name}...')

    def initialize(self) -> None:
        """
        Initializes the regression testing process.

        Implemented by child classes (model-dependent).

        """
        logger.info('ESM — Initializing regression test...')

    def report(self, end_time: dt.datetime) -> None:
        """
        Sends final report

        Implemented by child classes (model-dependent).

        Parameters
        ----------
        end_time : dt.datetime

        """
        report = self.report_cfg.send_report(end_time)
        logger.notice('ESM — Generating report...')
        print(report)

    def reset_scratch(self) -> None:
        """
        Resets the scratch directory

        """
        logger.notice('ESM — Resetting scratch directory...')
        paths.clean_dir(self.get_scratch_dir())
