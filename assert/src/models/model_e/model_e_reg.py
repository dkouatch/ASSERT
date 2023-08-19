"""
ModelE Regression Manager

"""
import src.lib.utils.config as config
import datetime as dt
import logging
import src.lib.utils.paths as paths
import subprocess as sp

from pathlib import Path
from src.lib.earthsystems_reg import EarthSystemsReg
from src.lib.earthsystems_testcase import EarthSystemsTestcase

from src.models.model_e.model_e_testcase import ModelETestcase
from src.models.model_e.model_e_report import ModelEReport
from src.lib.utils.logger import logger_setup

logger = logger_setup(filename=__name__,
                      file_handler=True,
                      file_level=logging.INFO,
                      stream_handler=True,
                      stream_level=logging.INFO)


class ModelEReg(EarthSystemsReg):
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
        ModelE implementation of get_repo_type()

        Returns
        -------
        str
            ModelE uses git

        """
        return 'git'

    def get_repo_url(self):
        """
        ModelE implementation of get_repo_url()

        Returns
        -------
        str
            Repository URL

        """
        return self.model_cfg['repository']

    def get_repo_branch(self):
        """
        ModelE implementation of get_repo_branch()

        May not exist???

        Returns
        -------
        str
            Repository branch

        """
        branch_name = config.get_yaml_variable_value(
            self.model_cfg, var_name='repo_branch', default=None
        )
        return branch_name

    def get_scratch_dir(self) -> str:
        """
        ModelE implementation of get_scratch_dir()

        Returns
        -------
        str
            Scratch directory

        """
        return self.system_cfg['scratchdir']

    def set_test_cfg(self, yaml_dict: dict) -> ModelETestcase:
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
        return ModelETestcase(
            config.get_testcases(yaml_dict,
                                 section_name='testcases'),
            scratch_dir=self.get_scratch_dir()
        )

    def set_report_cfg(self, yaml_dict: dict) -> ModelEReport:
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
        return ModelEReport(
            model_cfg=self.model_cfg,
            system_cfg=self.system_cfg,
            report_cfg=yaml_dict['reportconfig'],
            start_time=self.start_time
        )

    def setup(self) -> None:
        """
        ModelE implementation of setup()

        """
        self.test_cfg.set_runnable_tests()
        self.test_cfg.setup_tests(
            time_stamp=self.start_time.strftime('%Y%m%d_%H%M%S')
        )
        logger.notice('ModelE — setup successful')

    def compile(self, test_name: str, cwd: str) -> None:
        """
        ModelE implementation of compile()

        Parameters
        ----------
        test_name : str
            Name of test whose imported code will be compiled
        cwd : str
            Current working directory (should be appropriate)

        """
        logger.info(f'ModelE — Building {test_name}...')

        # run_cmd(['make', 'rundeck', test_name])
        # run_cmd(['make', 'gcm', test_name])

    def run(self, test_name: str, cwd: str) -> None:
        """
        ModelE implementation of run()

        Parameters
        ----------
        test_name : str
            Name of test whose imported code will be compiled
        cwd : str
            Current working directory (should be appropriate)

        """
        logger.info(f'ModelE — Running {test_name}...')

    def compare(self, test_name: str, cwd: str) -> None:
        """
        ModelE implementation of compare()

        Parameters
        ----------
        test_name : str
            Name of test whose imported code will be compiled
        cwd : str
            Current working directory (should be appropriate)

        """
        logger.info(f'ModelE — Comparing {test_name}...')

    def initialize(self) -> None:
        """
        ModelE implementation of initialize()

        """
        self.setup()

        for testname, testdirs in self.test_cfg.get_dirs().items():
            test_result = True
            for testdir in testdirs:
                compiler = Path(testdir).stem.split('-')[0]
                mode = Path(testdir).stem.split('-')[1]
                test_report = {'RUNDECK': testname,
                               'COMPILER': compiler,
                               'MODE': mode,
                               'CLONE': False,
                               'BUILD': False,
                               'RUN': False,
                               'COMPARE': False}
                paths.change_dir(testdir)
                dir_name = testdir + '/code'

                try:
                    self.get_repo(directory_name=dir_name,
                                  overwrite=True)
                except:
                    test_result = False
                else:
                    test_report['CLONE'] = True
                    try:
                        self.compile(test_name=testname, cwd=testdir)
                    except:
                        test_result = False
                    else:
                        test_report['BUILD'] = True
                        try:
                            self.run(test_name=testname, cwd=testdir)
                        except:
                            test_result = False
                        else:
                            test_report['RUN'] = True
                            try:
                                self.compare(test_name=testname,
                                             cwd=testdir)
                            except:
                                test_result = False
                            else:
                                test_report['COMPARE'] = True
                finally:
                    if test_result:
                        pass
                        # Clears out test directory if it passes
                        paths.clean_dir(testdir)
                    self.report_cfg.add_test(test_report)

            logger.notice(f'ModelE — {testname} tests complete...')

        if self.system_cfg['cleanscratch']:
            self.reset_scratch()

    def report(self, end_time: dt.datetime) -> None:
        """
        ModelE implementation of report()

        Parameters
        ----------
        end_time : dt.datetime

        """
        logger.notice(f'ModelE — Creating report...')
        final_report = self.report_cfg.send_report(end_time)

        # Writing the report in a temporary file
        report_file = f'assert_report_' \
                      f'{end_time.strftime("%Y-%m-%d_%H-%M-%S")}'
        with open(report_file, 'w') as fid:
            fid.write(final_report)

        # Getting mailing info
        subject = f"\"[ASSERT] {self.report_cfg.get_subject()}\""
        addresses = ', '.join(self.report_cfg.get_addresses())

        # Generating mailing command
        if self.report_cfg.get_html():
            prefix = 'mutt -e "set content_type=text/html" -s'
        else:
            prefix = '/usr/bin/mail -s'
        cmd = ' '.join([prefix, subject, addresses, '<', report_file])
        sp.call(cmd, shell=True)

        Path.unlink(Path.cwd() / report_file, missing_ok=False)

        # print(final_report)
        logger.success(f'ModelE — Report sent to {addresses}')
