from src.lib.earthsystems_testcase import EarthSystemsTestcase


def test_get_testcase_names():
    data = [
        dict(name='Test Case 1', variables=['variable1', 'variable2', 'variable3']),
        dict(name='Test Case 2', variables=['variable4', 'variable5']),
        dict(name='Test Case 3', variables=['variable6'])
    ]

    test_cases = EarthSystemsTestcase(
        test_cfg=data, scratch_dir='/Users/deon.kouatchou/scratch'
    )
    names = test_cases.get_testcase_names()
    assert names == ['Test Case 1', 'Test Case 2', 'Test Case 3']


def test_set_runnable_tests():
    data = [
        dict(name='nonProduction_E_AR5_C12', compilers='intel',
             modes=['serial', 'mpi'], npes=[1, 4],
             verification='restartRun', run=True),
        dict(name='nonProduction_E4TcadC12', compilers='intel',
             modes=['serial', 'mpi'], npes=[1, 8],
             verification='restartRun', run=False),
        dict(name='EM20', compilers='intel',
             modes=['serial', 'mpi'], npes=[1, 4],
             verification='restartRun'),
        dict(name='E1oM20', compilers='intel',
             modes=['serial', 'mpi'], npes=[1, 4],
             verification='restartRun', run=True)
    ]

    runnable = [
        dict(name='nonProduction_E_AR5_C12', compilers='intel',
             modes=['serial', 'mpi'], npes=[1, 4],
             verification='restartRun', run=True),
        dict(name='E1oM20', compilers='intel',
             modes=['serial', 'mpi'], npes=[1, 4],
             verification='restartRun', run=True)
    ]

    test_cases = EarthSystemsTestcase(
        test_cfg=data, scratch_dir='/Users/deon.kouatchou/scratch'
    )
    test_cases.set_runnable_tests()
    assert test_cases.runnable == runnable


def test_get_runnable_names():
    data = [
        dict(name='nonProduction_E_AR5_C12', compilers='intel',
             modes=['serial', 'mpi'], npes=[1, 4],
             verification='restartRun', run=True),
        dict(name='nonProduction_E4TcadC12', compilers='intel',
             modes=['serial', 'mpi'], npes=[1, 8],
             verification='restartRun', run=False),
        dict(name='EM20', compilers='intel',
             modes=['serial', 'mpi'], npes=[1, 4],
             verification='restartRun'),
        dict(name='E1oM20', compilers='intel',
             modes=['serial', 'mpi'], npes=[1, 4],
             verification='restartRun', run=True)
    ]

    run_names = ['nonProduction_E_AR5_C12', 'E1oM20']

    test_cases = EarthSystemsTestcase(
        test_cfg=data, scratch_dir='/Users/deon.kouatchou/scratch'
    )
    test_cases.set_runnable_tests()
    assert test_cases.get_runnable_names() == run_names
