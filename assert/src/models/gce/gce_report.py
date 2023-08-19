"""
GCE Reporting Manager

"""
import datetime as dt
import logging

from typing import Any
from src.lib.utils.logger import logger_setup
from src.lib.earthsystems_report import EarthSystemsReport

logger = logger_setup(filename=__name__,
                      file_handler=False,
                      stream_handler=False,
                      level=logging.INFO)


class GceReport(EarthSystemsReport):
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
        GCE implementation of set_subject()

        Returns
        -------
        str
            Email subject message

        """
        pass

    def set_addresses(self) -> list[str]:
        """
        GCE implementation of set_addresses()

        Returns
        -------
        list[str]
            List of email addresses
        """
        pass

    def set_html(self) -> bool:
        """
        GCE implementation of set_html()

        Returns
        -------
        bool
            True if using HTML format, False if not.
        """
        pass

    def set_header(self) -> list[str]:
        """
        GCE implementation of set_header()

        Returns
        -------
        list[str]
            A model-specific header

        """
        return list()

    def set_legend(self) -> dict[str, str]:
        """
        GCE implementation of set_legend()

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
        GCE implementation of interpret_test()

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

    def add_test_report(self) -> None:
        """
        GCE implementation of add_test_report()

        """
        logger.info('GCE — Test results added to report.')

    def send_report(self, end_time: dt.datetime) -> str:
        """
        GCE implementation of send_report()

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
MODEL TYPE: GCE      
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

        logger.notice('GCE — Report Complete.')
        return self.report
