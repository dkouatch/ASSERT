"""
Contains EarthSystemsReport class which acts as a generic manager
for reports in the regression tests

"""
import datetime as dt
import logging

from typing import Any
from src.lib.utils.logger import logger_setup

logger = logger_setup(filename=__name__,
                      file_handler=True,
                      file_level=logging.INFO,
                      stream_handler=True,
                      stream_level=logging.INFO)


class EarthSystemsReport:
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

        #

        # Starting Report Setup
        self.report: str = ""

        # List of test results to be added to table in report
        self.test_reports: list[dict] = list()

        # Header for table in report
        self.header: list[str] = self.set_header()

        # Legend for table in report
        self.legend: dict[str, str] = self.set_legend()

        # Start time
        self.start_time = start_time

        # Passed on config info
        self.model_cfg = model_cfg
        self.system_cfg = system_cfg
        self.report_cfg = report_cfg

        # Email address to send report to
        self.addresses: list[str] = self.set_addresses()

        # Whether to use HTML format in email report
        self.use_html: bool = self.set_html()

        # Subject message for report email
        self.subject = self.set_subject()

    def set_subject(self) -> str:
        """
        Sets the email report subject message.

        Implemented by child class (model-dependent).

        Returns
        -------
        str
            Email subject message

        """
        pass

    def set_addresses(self) -> list[str]:
        """
        Sets the email addresses to send report to

        Implemented by child class (model-dependent).

        Returns
        -------
        list[str]
            List of email addresses
        """
        pass

    def set_html(self) -> bool:
        """
        Sets the html flag status

        Implemented by child class (model-dependent).

        Returns
        -------
        bool
            True if using HTML format, False if not.
        """
        pass

    def set_header(self) -> list[str]:
        """
        Sets the table head for model-specific classes

        Implemented by child classes (model-dependent).

        Returns
        -------
        list[str]
            A model-specific header

        """
        return list()

    def set_legend(self) -> dict[str, str]:
        """
        Sets legend for model-specific classes

        Implemented by child classes (model-dependent).

        Returns
        ----------
        dict[str, str]
            A model-specific legend

        """
        legend = {'+': 'Operation success',
                  '-': 'Operation failure',
                  '*': 'Operation not performed'}
        return legend

    def get_subject(self) -> str:
        """
        Accessor method for subject field

        Returns
        -------
        str
            Subject message

        """
        return self.subject

    def get_addresses(self) -> list[str]:
        """
        Accessor method for email addresses

        Returns
        -------
        list(str)
            Email addresses
        """
        return self.addresses

    def get_html(self) -> bool:
        """
        Accessor method for use_html field

        Returns
        -------
        bool
            HTML flag

        """
        return self.use_html

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
        pass

    def add_test(self, test_report: dict) -> None:
        """
        Stores result of a test

        Parameters
        ----------
        test_report : dict
            Results of a test

        """
        self.test_reports.append(test_report)

    def add_test_report(self) -> None:
        """
        Adds the test results to the report

        Implemented by child class (model-specific).

        """
        logger.info('ESM — Test results added to report.')

    def add_legend_report(self) -> None:
        """
        Adds the legend to the report

        """
        legend_report = """
---------------------------------
Legend:
---------------------------------
"""
        for symbol, meaning in self.legend.items():
            legend_report += (symbol + " : " + meaning + "\n")

        self.report += f"\n{legend_report}"
        logger.info('ESM — Legend added to report.')

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
{'=' * 80}
ASSERT: A Software Suite for Earth-systems Regression Testing
{'=' * 80}
MODEL TYPE: None      
"""
        self.add_test_report()
        self.add_legend_report()

        # Add start datetime, end datetime, and elapsed time
        elapsed_time = (end_time - self.start_time).total_seconds()

        self.report += f"""\n
{'=' * 80}
Start Time:         {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}
End Time:           {end_time.strftime('%Y-%m-%d %H:%M:%S')}
Total Time Elapsed: {elapsed_time}
{'=' * 80}
"""
        if self.use_html:
            self.report += "</pre><html>\n"

        logger.notice('ESM — Report Complete.')
        return self.report
