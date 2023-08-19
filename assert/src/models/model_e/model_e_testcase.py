"""
ModelE Testcase Manager

"""
import logging

from src.lib.utils.logger import logger_setup
from src.lib.utils.paths import create_dir
from src.lib.earthsystems_testcase import EarthSystemsTestcase

logger = logger_setup(filename=__name__,
                      file_handler=True,
                      file_level=logging.DEBUG,
                      stream_handler=False)


class ModelETestcase(EarthSystemsTestcase):
    def __init__(self, test_cfg: list[dict], scratch_dir: str):
        """
        Parameters
        ----------
        test_cfg : List[dict]
            Information from the test configurations
        scratch_dir: str
            Scratch directory for the model

        """
        super().__init__(test_cfg, scratch_dir)

    def setup_tests(self, time_stamp: str = None) -> None:
        """
        Set up the directory structure for the tests

        Parameters
        ----------
        time_stamp : str
            Time stamp as a string (datetime)

        """
        # Keeps track of all the test paths
        if not time_stamp:
            time_stamp = ''

        for runtest in self.runnable:
            # Top-level test directory
            # ex. '/.../scratch/modelE/E1oM20...'
            top_dir = '/'.join([self.scratch_dir, 'modelE',
                                runtest['name'] + time_stamp])
            create_dir(top_dir)

            if isinstance(runtest['compilers'], list):
                comps = runtest['compilers']
            elif isinstance(runtest['compilers'], str):
                comps = [runtest['compilers']]
            else:
                logger.warning('No valid compilers.')
                comps = []
            if isinstance(runtest['modes'], list):
                modes = runtest['modes']
            elif isinstance(runtest['modes'], str):
                modes = [runtest['modes']]
            else:
                logger.warning('No valid modes.')
                modes = []

            # Contains list of directories to clone, build,
            # run, etc. within for a given test
            build_dirs: list[str] = list()
            for comp in comps:
                for mode in modes:
                    # Compiler specification directory
                    # ex. /.../scratch/modelE/E1oM20/intel-mpi...
                    spec_dir = '/'.join([top_dir,
                                         comp + '-' + mode])
                    create_dir(spec_dir)
                    build_dirs.append(spec_dir)

                    # 1st innermost directory to clone repo in
                    create_dir(spec_dir + '/code')
                    # 2nd innermost directory to run test in
                    create_dir(spec_dir + '/run')

                    logger.debug(f"{runtest['name']}/"
                                 f"{comp}-{mode} directory created")

            self.dirs[runtest['name']] = build_dirs
