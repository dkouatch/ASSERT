"""
ModelE Reporting Manager

"""
import datetime as dt
import logging

from typing import Any
from src.lib.utils.logger import logger_setup
from src.lib.earthsystems_report import EarthSystemsReport

logger = logger_setup(filename=__name__,
                      file_handler=True,
                      file_level=logging.INFO,
                      stream_handler=True,
                      stream_level=logging.INFO)


class ModelEReport(EarthSystemsReport):
    def __init__(self, model_cfg: dict,
                 system_cfg: dict,
                 report_cfg: dict,
                 start_time: dt.datetime):
        """
        Parameters
        ----------
        model_cfg : dict
            Passed on model configuration info
        system_cfg : dict
            Passed on system configuration info
        report_cfg : dict
            Passed on report configuration info

        start_time : str
            Passed on reg start time from datetime module

        """
        super().__init__(model_cfg, system_cfg, report_cfg, start_time)

    def set_subject(self) -> str:
        """
        ModelE implementation of set_subject()

        Returns
        -------
        str
            Email subject message

        """
        return self.report_cfg['message']

    def set_addresses(self) -> list[str]:
        """
        ModelE implementation of set_addresses()

        Returns
        -------
        list[str]
            List of email addresses
        """
        mailto = self.report_cfg['mailto']
        if isinstance(mailto, str):
            return [mailto]
        elif isinstance(mailto, list):
            return mailto
        else:
            raise Exception('')

    def set_html(self) -> bool:
        """
        ModelE implementation of set_html()

        Returns
        -------
        bool
            True if using HTML format, False if not.
        """
        return self.report_cfg['html']

    def set_header(self) -> list[str]:
        """
        ModelE implementation of set_header()

        Returns
        -------
        list[str]
            ModelE report table header

        """
        header = ['RUNDECK', 'COMPILER', 'MODE',
                  'CLONE', 'BUILD', 'RUN', 'COMPARE']
        return header

    def set_legend(self) -> dict[str, str]:
        """
        ModelE implementation of set_legend()

        Returns
        ----------
        dict[str, str]
            A model-specific legend

        """
        legend = {'+': 'Operation success',
                  '-': 'Operation failure',
                  '*': 'Operation not performed'}
        return legend

    def interpret_test(self, res: Any) -> str:
        """
        Interprets test result to a legend symbol

        Implemented by child classes (model-dependent).

        Parameters
        ----------
        res : Any
            Information about a test result

        Returns
        -------
        str
            Legend symbol for test result

        """
        if isinstance(res, bool):
            if res:
                return '+'
            else:
                return '-'
        else:
            return '*'

    def add_test(self, test_report: dict) -> None:
        """
        Adds result of a test to the report table

        Parameters
        ----------
        test_report : dict
            Results of a test

        """
        self.test_reports.append(test_report)

    def add_test_report(self) -> None:
        """
        Adds the test results to the report

        """
        self.report += f"""
{'- ' * 60}
RUNDECK {' ' * 15} COMPILER      MODE     CLONE   BUILD   RUN   COMPARE
{'- ' * 60}
"""
        for test in self.test_reports:
            self.report += \
                f"{test['RUNDECK']:25.15s} " \
                f"{test['COMPILER']:<17} " \
                f"{test['MODE']:<15} " \
                f"{self.interpret_test(test['CLONE']):^7}" \
                f"{self.interpret_test(test['BUILD']):^14}" \
                f"{self.interpret_test(test['RUN']):^6}   " \
                f"{self.interpret_test(test['COMPARE']):^7}\n"
        self.report += f"{'- ' * 60}"

        logger.info('ModelE — Test results added to report.')

    def add_legend_report(self) -> None:
        """
        Adds the legend to the report

        """
        legend_report = """

Legend:
---------------------------------
"""
        for symbol, meaning in self.legend.items():
            legend_report += (symbol + " : " + meaning + "\n")

        self.report += f"\n{legend_report}"

        logger.info('ModelE — Legend added to report.')

    def send_report(self, end_time: dt.datetime) -> str:
        """
        Sends finalized report back up to the manager/reg class

        Implemented in child classes (model-dependent).

        Parameters
        ----------
        end_time : dt.datetime
            End time to add to report and get elapsed time

        Returns
        -------
        str
            Final report output

        """
        if self.use_html:
            self.report = "<html><pre>"
        self.report += f"""
{'=' * 60}
ASSERT: A Software Suite for Earth-systems Regression Testing
{'=' * 60}
MODEL TYPE: ModelE
"""
        self.add_test_report()
        self.add_legend_report()

        # Add start datetime, end datetime, and elapsed time
        elapsed_time = (end_time - self.start_time).total_seconds()

        self.report += f"""\n
{'=' * 60}
Start Time:         {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}
End Time:           {end_time.strftime('%Y-%m-%d %H:%M:%S')}
Total Time Elapsed: {elapsed_time}
{'=' * 60}
        """
        if self.use_html:
            self.report += "</pre><html>\n"

        logger.notice('ModelE — Report complete.')
        return self.report
