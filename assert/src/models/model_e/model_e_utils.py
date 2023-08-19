# This module contains tools to help setup the modelE regression tests
import string
from configparser import RawConfigParser
import re
import os
import subprocess as sp
import glob
import logging
import time
import reg_utils as util

logger = logging.getLogger('tools')


def setup_env(config, compconfig):
    # Setup modelE testing environment:
    logger.info('Setup testing environment')
    userconfig = util.config_section_map(config, 'USERCONFIG')
    makesystem = userconfig['makesystem']

    # Make sure - if specified - that work space is clean
    if userconfig['cleanscratch'] == 'yes':
        util.clean_scratch(config)

    if makesystem == "makeOld":
        setup_modele_env(config, compconfig)
    git_clone_repository(config)


def git_clone_repository(config):
    # Clone the model from the user-specified git repository
    logger.info('Clone user-specified git repository')
    userconfig = util.config_section_map(config, 'USERCONFIG')
    scratch = userconfig['scratchdir']
    repo = userconfig['repository']
    branch = userconfig['repobranch']
    base = userconfig['basedir']
    buildtype = userconfig['buildtype']

    clone = os.path.join(scratch, "scratch", branch, branch)
    filerepo = 'file://' + repo
    cmd = 'git clone ' + filerepo + ' ' + clone + ' --depth 1 --branch ' + branch

    resultsDir = os.path.join(userconfig['scratchdir'], "results", branch)

    cwd = os.getcwd()
    logger.info('Cloning %s into %s', repo, clone)

    util.sp_call(cmd)

    # Must use "repo" dir instead of "clone" dir to get more than 1 log entry
    os.chdir(repo)

    # traps tests have their own baseline, so use this to specify the path
    if buildtype == 'traps':
        traps = '_traps'
    else:
        traps = ''
    # Get date of last baseline update for use with git log
    datePath = base + '/' + branch + traps + '/lastGitDate'
    logger.info('datePath = ' + datePath)
    if os.path.exists(datePath):
        with open(datePath) as dateFile:
            baselineDate = dateFile.readline().strip() + " 00:00:01"
            logger.info('baseline date = ' + baselineDate)
        cmd = "git log --pretty=format:'%h - %an, %ad : %s' --date=short --since='" + baselineDate + "'"
        logger.debug('Log 7cmd: ' + cmd)
    else:
        # get last 3 log entries
        cmd = "git log --pretty=format:'%h - %an, %ad : %s' -3 --date=short"

    logPath = resultsDir + '/gitLog'
    os.system(cmd + '>' + logPath)

    ##If there are less than 3 entries in gitLog, get the last 3 instead
    # numEntries = len(open(logPath).readlines(  ))
    # if numEntries < 3:
    #    cmd = "git log --pretty=format:'%h - %an, %ad : %s' -3 --date=short"
    #    os.system(cmd + '>' + logPath)

    os.chdir(cwd)


def setup_modele_env(config, compconfig):
    # ModelE specific setup
    userconfig = util.config_section_map(config, 'USERCONFIG')
    branch = userconfig['repobranch']
    if not branch:
        branch = 'detached'
    resultsDir = os.path.join(userconfig['scratchdir'], "results", branch)
    scratchDir = os.path.join(userconfig['scratchdir'], "scratch", branch)
    makesystem = userconfig['makesystem']

    # the following directories are modelE specific:
    util.mkdir_p(os.path.join(scratchDir, "decks_repository"))
    util.mkdir_p(os.path.join(scratchDir, "cmrun"))
    util.mkdir_p(os.path.join(scratchDir, "exec"))
    util.mkdir_p(os.path.join(scratchDir, "savedisk"))

    # We need to get a list of compilers...
    compilers = util.get_compilers(compconfig)
    # and libraries/modules info...
    libsconfig = util.config_section_map(compconfig, 'COMPCONFIG')

    # ... to create modelErc file(s) for each compiler
    for comp in compilers:
        if not os.path.exists(scratchDir + comp):
            util.mkdir_p(os.path.join(resultsDir, comp))
            util.mkdir_p(os.path.join(scratchDir, comp))
        write_modelerc(libsconfig, scratchDir, comp, makesystem)
        # For planet branches we need SOCRATESPATH in modelErc
        if 'planet' in branch:
            with open(os.path.join(scratchDir, comp, 'modelErc.' + comp), 'a') as f:
                f.write('   SOCRATESPATH=/home/damundse/Software/socrates/modele_branch\n')

        # Make sure basedirs exist
        if userconfig['updatebase'] == 'yes':
            util.mkdir_p(os.path.join(userconfig['basedir'], branch, comp))


def write_modelerc(cfg, scratchDir, compiler, makesystem):
    # Write a compiler-specific modelErc file

    # boos = BUILD_OUT_OF_SOURCE
    boos = 'NO'
    if makesystem == 'makeNew':
        boos = 'YES'

    s = string.Template('\
   DECKS_REPOSITORY=$scr/decks_repository\n\
   CMRUNDIR=$scr/cmrun\n\
   EXECDIR=$scr/exec\n\
   SAVEDISK=$scr/savedisk\n\
   GCMSEARCHPATH=$datadir\n\
   BUILD_OUT_OF_SOURCE=$boos\n\
   COMPILER=$cm\n\
   MPIDISTR=$mn\n\
   MPIDIR=$md\n\
   NETCDFHOME=$nd\n\
   PNETCDFHOME=$pd\n\
   BASELIBDIR5=$bd\n\
   PFUNITSERIALDIR=$p1\n\
   PFUNITMPIDIR=$pn\n\
   OVERWRITE=YES\n\
   OUTPUT_TO_FILES=NO\n\
   VERBOSE_OUTPUT=YES\n')

    if compiler == 'gfortran':
        modelErc = s.substitute(cm=compiler,
                                scr=scratchDir,
                                datadir=cfg['modeldatadir'],
                                boos=boos,
                                mn=cfg['gccmpi'],
                                md=cfg['gccmpidir'],
                                nd=cfg['gccnetcdf'],
                                pd=cfg['gccpnetcdf'],
                                p1=cfg['gccserialpfunitdir'],
                                pn=cfg['gccmpipfunitdir'],
                                bd=cfg['gccesmf'])
    elif compiler == 'intel':
        modelErc = s.substitute(cm=compiler,
                                scr=scratchDir,
                                datadir=cfg['modeldatadir'],
                                boos=boos,
                                mn=cfg['intelmpi'],
                                md=cfg['intelmpidir'],
                                nd=cfg['intelnetcdf'],
                                pd=cfg['intelpnetcdf'],
                                p1=cfg['intelserialpfunitdir'],
                                pn=cfg['intelmpipfunitdir'],
                                bd=cfg['intelesmf'])
    elif compiler == 'nag':
        modelErc = s.substitute(cm=compiler,
                                scr=scratchDir,
                                datadir=cfg['modeldatadir'],
                                boos=boos,
                                mn=cfg['nagmpi'],
                                md=cfg['nagmpidir'],
                                nd=cfg['nagnetcdf'],
                                pd=cfg['nagpnetcdf'],
                                p1=cfg['nagserialpfunitdir'],
                                pn=cfg['nagmpipfunitdir'],
                                bd=cfg['nagesmf'])
    else:
        modelErc = s.substitute(cm=compiler,
                                scr=scratchDir,
                                datadir=cfg['modeldatadir'],
                                boos=boos,
                                mn=cfg['gccmpi'],
                                md=cfg['gccmpidir'],
                                nd=cfg['gccnetcdf'],
                                pd=cfg['gccpnetcdf'],
                                p1=cfg['gccserialpfunitdir'],
                                pn=cfg['gccmpipfunitdir'],
                                bd=cfg['gccesmf'])

    with open(os.path.join(scratchDir, compiler, 'modelErc.' + compiler), "w") as rcfile:
        rcfile.write(modelErc)
        rcfile.write('\n')
    logger.debug('Created modelErc file for compiler ' + compiler)


def setup_clone_tasks(config, compconfig, decklist):
    # For in-source builds we need a clone for each rundeck/compiler/mode combo
    compilers = util.get_compilers(compconfig)

    cloneTasks = []
    for deck in decklist:
        # since nonProduction rundeck names can be quite long, extract the
        # nonProduction_ part...
        dName = deck.name
        if re.search('nonProduction', deck.name):
            start = deck.name.find('nonProduction') + 14
            dName = deck.name[start:]

        for comp in deck.get_opt('compilers').split(','):
            for mode in deck.get_opt('modes').split(','):
                if comp.strip() in compilers:
                    commandString = util.git_clone_command(config, dName,
                                                           comp.strip(), mode.strip())
                    cloneTasks.append(commandString)
                else:
                    logger.error('Compiler ' + comp + ' is not defined in COMPCONFIG')

    for t in cloneTasks:
        logger.debug('CLONE TASK %s', t)
    return cloneTasks


def setup_runs(config, compconfig, decklist):
    # For out-of source builds, create directory for each rundeck/compiler/mode combo
    userconfig = util.config_section_map(config, 'USERCONFIG')
    compilers = util.get_compilers(compconfig)
    scratch = userconfig['scratchdir']
    branch = userconfig['repobranch']
    if not branch:
        branch = 'detached'
    os.chdir(os.path.join(scratch, 'scratch', branch))

    cwd = os.getcwd()
    for comp in compilers:
        util.mkdir_p(os.path.join(cwd, comp))
        os.chdir(os.path.join(cwd, comp))
        for deck in decklist:
            dName = deck.name
            if re.search('nonProduction', deck.name):
                start = deck.name.find('nonProduction') + 14
                dName = deck.name[start:]
            for mode in deck.get_opt('modes').split(','):
                adir = dName + '.' + mode.strip()
                if not os.path.isdir(adir):
                    util.mkdir_p(adir)
    setup_modele_env(config, compconfig)


def setup_script_tasks(config, compconfig, decklist):
    # Return a command to submit/execute a [batch] job
    logger.info('Prepare and execute tasks...')
    compilers = util.get_compilers(compconfig)

    scriptTasks1st = []
    scriptTasks2nd = []
    for deck in decklist:
        for comp in deck.get_opt('compilers').split(','):
            for mode in deck.get_opt('modes').split(','):
                if comp.strip() in compilers:
                    commandString = \
                        create_script_task(config, compconfig, deck,
                                           comp.strip(), mode.strip())
                    # scriptsTasks1st will contain rundecks with no dependencies
                    # (if not defined in *.cfg file, default dependencies = 'none')
                    if deck.get_opt('dependencies') == 'none':
                        scriptTasks1st.append(commandString)
                    else:
                        scriptTasks2nd.append(commandString)
                else:
                    logger.error(comp + ' is not defined in COMPCONFIG')

    if len(scriptTasks1st) > 0:
        for t in scriptTasks1st:
            logger.debug('SCRIPT TASK %s', t)
        for t in scriptTasks2nd:
            logger.debug('SCRIPT TASK %s', t)
    else:
        logger.debug('There is nothing to do.')
    return scriptTasks1st, scriptTasks2nd


def create_script_task(config, compconfig, deck, comp, mode):
    # Creates script to be submitted to batch system OR to be executed interactively
    # Batch system is assumed to be the one on NCCS-DISCOVER machines
    userconfig = util.config_section_map(config, 'USERCONFIG')
    modules = userconfig['modules']
    useBatch = userconfig['usebatch']
    branch = userconfig['repobranch']
    if not branch:
        branch = 'detached'
    resultsDir = os.path.join(userconfig['scratchdir'], 'results', branch, comp)
    scratchDir = os.path.join(userconfig['scratchdir'], 'scratch', branch, comp)
    sponsorID = userconfig['sponsorid']

    deckName = deck.name
    jobName = deckName
    if re.search('nonProduction', deckName):
        start = deckName.find('nonProduction') + 14
        jobName = deckName[start:]
    filename = resultsDir + '/' + jobName + '.' + mode + '.bash'
    fileHandle = open(filename, 'w')

    if useBatch == 'yes':

        cores = max(deck.get_opt('npes'))

        # If we are just compiling this rundeck
        if deck.get_opt('verification') == 'compileOnly':
            cores = 4
            walltime = '00:10:00'

        # customRun is a 2-month run
        elif deck.get_opt('verification') == 'customRun':
            if re.search('campi', deckName):
                walltime = '4:00:00'
            elif re.search('Tmatrix', deckName):
                walltime = '4:00:00'
            elif re.search('Ttomas', deckName):
                walltime = '4:00:00'
            elif re.search('cadi', deckName):
                walltime = '2:00:00'
            elif re.search('Toma', deckName):
                walltime = '2:00:00'
            elif re.search('obio', deckName):
                walltime = '1:00:00'
            elif re.search('C12', deckName):
                walltime = '0:30:00'
            elif re.search('M20', deckName):
                walltime = '0:30:00'
            else:
                walltime = '1:00:00'

        # regular runs (1hr and/or restart)
        else:
            if 'mpi' in mode:
                walltime = '01:30:00'
                if re.search('E4Tcad', deckName):
                    walltime = '04:00:00'

            else:  # serial
                cores = 1
                walltime = '00:50:00'
                if re.search('obio', deckName):
                    walltime = '01:00:00'
                elif re.search('cadi', deckName):
                    walltime = '04:00:00'
                elif re.search('lerner', deckName):
                    walltime = '01:00:00'
                elif re.search('E6Tdus', deckName):
                    walltime = '01:30:00'
                elif re.search('E_Tdus', deckName):
                    walltime = '01:00:00'
                elif re.search('P2SAq', deckName):
                    walltime = '01:10:00'
                elif re.search('P2SAp', deckName):
                    walltime = '01:10:00'
                elif re.search('P2SNo', deckName):
                    walltime = '00:55:00'
                elif re.search('P2Sxo', deckName):
                    walltime = '01:00:00'
                elif re.search('LL', deckName):
                    walltime = '01:00:00'
                elif re.search('E6F40', deckName):
                    walltime = '01:00:00'

            # Adjust the walltime for some rundecks
            if re.search('Mars', deckName):
                walltime = '00:55:00'
            elif re.search('SGP', deckName):
                walltime = '00:10:00'
            elif re.search('campi', deckName):
                walltime = '02:00:00'
            elif re.search('P2SAoF', deckName):
                walltime = '01:45:00'
            elif re.search('Toma', deckName):
                if 'mpi' in mode:
                    walltime = '03:00:00'
                else:
                    walltime = '04:00:00'
            elif re.search('ctomas', deckName):
                walltime = '02:00:00'
            elif re.search('Ttomas', deckName):
                walltime = '03:00:00'
            elif re.search('Tmatrix', deckName):
                walltime = '02:00:00'
            elif re.search('E_Tdus', deckName):
                walltime = '02:00:00'
            elif re.search('E6Twis', deckName):
                if 'mpi' in mode:
                    walltime = '02:00:00'
                else:
                    walltime = '01:00:00'
            elif re.search('E6Tlernerpsv', deckName):
                if 'mpi' in mode:
                    walltime = '04:00:00'  # parallel
                else:
                    walltime = '03:00:00'  # serial
            elif re.search('vsd', deckName):
                if 'mpi' in mode:
                    walltime = '07:00:00'  # parallel
                else:
                    walltime = '06:00:00'  # serial

        outname = os.path.join(resultsDir, jobName + '.' + mode + '.out')
        errname = os.path.join(resultsDir, jobName + '.' + mode + '.err')
        fileHandle.write('#!/bin/bash' + '\n')
        fileHandle.write('#SBATCH -J ' + jobName + '\n')
        fileHandle.write('#SBATCH -o ' + outname + '\n')
        fileHandle.write('#SBATCH -e ' + errname + '\n')
        fileHandle.write('#SBATCH --account=' + sponsorID + '\n')
        fileHandle.write('#SBATCH --ntasks=' + str(cores) + '\n')
        # CC: TESTING
        fileHandle.write('#SBATCH --time=' + walltime + '\n')

    # Create rest of script used in batch OR interactive jobs:

    if modules == 'yes':
        machine = sp.check_output(['uname', '-n']).decode()
        # If on NCCS-DISCOVER
        if 'borg' in machine or 'discover' in machine:
            fileHandle.write('. /usr/share/modules/init/bash' + '\n')
            # allow access to module mpi/impi-prov/* for COMPILE_WITH_TRAPS
            fileHandle.write('export MODULEPATH=${MODULEPATH}:' +
                             '/discover/swdev/gmao_SIteam/modulefiles-SLES12/' + '\n')
            fileHandle.write('module purge' + '\n')
            fileHandle.write('module load python/GEOSpyD/Ana2019.10_py3.7' + '\n')
        else:
            # CC: example from my MacBook
            fileHandle.write('#!/bin/bash' + '\n')
            fileHandle.write('. /opt/local/share/modules/init/bash' + '\n')
            fileHandle.write('module purge' + '\n')

        # Needed due to different naming convention for module names
        compvendor = comp
        if comp == 'gfortran':
            compvendor = 'gcc'

        modsconfig = util.config_section_map(compconfig, 'COMPCONFIG')
        for mod in modsconfig['modulelist'].split(','):
            if re.search(compvendor, mod):
                for mm in modsconfig[mod].split(','):
                    cmd = 'module load ' + mm + '\n'
                    fileHandle.write(cmd)

    fileHandle.write('umask 022' + '\n')
    fileHandle.write('ulimit -s unlimited' + '\n')
    makesystem = userconfig['makesystem']
    if makesystem == 'makeOld':
        decksDir = os.path.join(scratchDir, jobName + '.' + mode, 'decks')
    else:
        decksDir = os.path.join(scratchDir, jobName + '.' + mode)

    fileHandle.write('export DECKSDIR=' + decksDir + '\n')
    modelErc = os.path.join(scratchDir, 'modelErc.' + comp)
    fileHandle.write('export MODELERC=' + modelErc + '\n')

    if deck.get_opt('unittest') == 'yes':
        if 'mpi' in mode:
            cmd = "cat " + modelErc + "| grep PFUNITMPIDIR" + "| awk -F= '{print $2}'"
        else:
            cmd = "cat " + modelErc + "| grep PFUNITSERIALDIR" + "| awk -F= '{print $2}'"
        out = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.STDOUT, shell=True)
        pfunitDir = out.communicate()[0].rstrip()
        fileHandle.write('export PFUNIT=' + pfunitDir + '\n')

    fileHandle.write('cd ' + decksDir + '\n')
    fileHandle.write('python ' + os.path.join(userconfig['scriptsdir'], 'regression.py ') + deckName + '\n')
    fileHandle.write(' ' + '\n')
    fileHandle.close()

    create_reg_config(config, deck, modelErc, comp, jobName, mode)

    if useBatch == 'yes':
        commandString = 'sbatch ' + filename
    else:
        commandString = 'chmod +x ' + filename + ';' + filename

    return commandString


def create_reg_config(config, deck, modelErc, comp, jobName, mode):
    # Create a config file for regression.py script.
    # Note: there is one config file for each rundeck+compiler combination
    cfg = util.config_section_map(config, 'USERCONFIG')
    branch = cfg['repobranch']
    if not branch:
        branch = 'detached'
    resultsDir = os.path.join(cfg['scratchdir'], 'results', branch, comp)
    scratchDir = os.path.join(cfg['scratchdir'], 'scratch', branch, comp)

    makesystem = cfg['makesystem']
    if makesystem == 'makeOld':
        decksDir = os.path.join(scratchDir, jobName + '.' + mode, 'decks')
    else:
        decksDir = os.path.join(scratchDir, jobName + '.' + mode)

    # Regression tests do not run the regression script in standalone mode
    standalone = 'no'
    regconfig = RawConfigParser()
    regconfig.add_section('regSettings')
    regconfig.set('regSettings', 'rundeck', deck.name)
    regconfig.set('regSettings', 'modelerc', modelErc)
    regconfig.set('regSettings', 'compiler', comp)
    regconfig.set('regSettings', 'modes', mode)
    regconfig.set('regSettings', 'standalone', standalone)
    regconfig.set('regSettings', 'unittest', deck.get_opt('unittest'))
    regconfig.set('regSettings', 'verification', deck.get_opt('verification'))
    regconfig.set('regSettings', 'dependencies', deck.get_opt('dependencies'))
    regconfig.set('regSettings', 'endtime', deck.get_opt('endtime'))
    npestr = ' '.join(str(e) for e in deck.get_opt('npes'))
    regconfig.set('regSettings', 'npes', npestr)
    regconfig.set('regSettings', 'buildtype', cfg['buildtype'])

    if makesystem == 'makeOld':
        regconfig.set('regSettings', 'repository', cfg['repository'])
    else:
        # Out of source build still pollutes the repository a little bit,
        # specially for nonProduction builds. So, let's make sure we pollute
        # a clone.
        newrepo = os.path.join(cfg['scratchdir'], "scratch", branch, branch)
        regconfig.set('regSettings', 'repository', newrepo)

    regconfig.set('regSettings', 'branch', branch)
    regconfig.set('regSettings', 'basedir', cfg['basedir'])
    regconfig.set('regSettings', 'updatebase', cfg['updatebase'])
    regconfig.set('regSettings', 'makesystem', makesystem)
    regconfig.set('regSettings', 'resultsdir', resultsDir)
    regconfig.set('regSettings', 'scratchdir', scratchDir)
    regconfig.set('regSettings', 'decksdir', decksDir)

    filename = os.path.join(decksDir, deck.name + '.cfg')
    with open(filename, 'w') as configfile:
        regconfig.write(configfile)


def validate_dependencies(runList, config, cfgfile):
    # First create a dictionary of rundeck : dependencies
    # Each item in runList is a member of the Regtest class
    rundeckDeps = {}
    rundeckModes = {}
    rundeckComps = {}
    for regTest in runList:
        rundeckDeps[regTest.name] = regTest.dependencies
        rundeckModes[regTest.name] = regTest.modes
        rundeckComps[regTest.name] = regTest.compilers
        logger.debug(f'rundeckDeps[{regTest.name}] = {regTest.dependencies}')
        logger.debug(f'rundeckModes[{regTest.name}] = {regTest.modes}')
        logger.debug(f'rundeckComps[{regTest.name}] = {regTest.compilers}')

    # Ensure that at least one rundeck has no dependencies
    if 'none' in rundeckDeps.values():
        logger.debug('Successfully found rundecks without dependencies')
    else:
        message = 'Error: All rundecks have dependencies; Cannot proceed!'
        logger.info(message)
        send_errorreport(config, message, cfgfile)
        raise SystemExit

    # Check that all dependencies refer to valid rundecks
    for depsList in rundeckDeps.values():
        logger.debug('depsList: ' + depsList)
        for deck in depsList.split(','):
            if deck != 'none':
                logger.debug('checking for: ' + deck)
                if deck in rundeckDeps.keys():
                    logger.debug('Successfully found dependent rundeck.')
                else:
                    message = 'Error: required dependency, "' + deck + '", not found!'
                    logger.info(message)
                    send_errorreport(config, message, cfgfile)
                    raise SystemExit

                # Also ensure 'deck' is not dependent on another rundeck
                # (this system does not support multilayered/circular dependencies)
                if rundeckDeps[deck] == 'none':
                    logger.debug('Passed multilayer dependency check.')
                else:
                    message = 'Error: found multilayer/circular dependency on rundeck "' + deck + '"'
                    logger.info(message)
                    send_errorreport(config, message, cfgfile)
                    raise SystemExit

    # Also ensure each dependency rundeck has the same modes and compilers as the dependent deck
    for rdeck in rundeckDeps.keys():  # example: rdeck=P4M40
        depsString = rundeckDeps[rdeck]  # example: depsString=PS_Mars
        if depsString != 'none':
            # Iterate thru all dependecies rundecks (there may be more than one)
            for dep in depsString.split(','):  # example: dep=PS_Mars

                # Check for relevent run modes in the dependency rundecks
                for mode in rundeckModes[rdeck].split(','):  # example: mode=serial
                    if mode in rundeckModes[dep]:
                        logger.debug('Passed ' + rdeck + '->' + dep + ' run ' +
                                     mode + ' mode dependency check.')
                    else:
                        message = ('Error: run mode ' + mode + ' not available in ' + rdeck +
                                   ' dependency ' + dep)
                        logger.info(message)
                        send_errorreport(config, message, cfgfile)
                        raise SystemExit

                # Check for relevent compiler types in the dependency rundecks
                for comp in rundeckComps[rdeck].split(','):  # example: comp=intel
                    if comp in rundeckComps[dep]:
                        logger.debug('Passed ' + rdeck + '->' + dep + ' ' + comp +
                                     ' compiler dependency check.')
                    else:
                        message = ('Error: compiler ' + comp + ' not available in ' + rdeck +
                                   ' dependency ' + dep)
                        logger.info(message)
                        send_errorreport(config, message, cfgfile)
                        raise SystemExit

    logger.info('Passed all rundeck dependency error checks.')


def send_errorreport(config, message, cfgfile):
    # Create an error report and notify via email
    userconfig = util.config_section_map(config, 'USERCONFIG')
    mailto = userconfig['mailto']
    branch = userconfig['repobranch']
    resultsDir = os.path.join(userconfig['scratchdir'], 'results', branch)
    html = userconfig['html']

    # Create error file holding abort message
    errorFile = os.path.join(resultsDir, 'abortError.txt')
    fp = open(errorFile, 'w')
    if html == 'yes':
        fp.write('<html><pre>\n')
    fp.write('ModelE regression tests for branch ' + branch + ' aborted! \n')
    fp.write(message + ' \n\n')
    fp.write('Please check dependencies settings in ' + cfgfile + '\n')
    if html == 'yes':
        fp.write('</pre></html>\n')
    fp.close()

    # Send email
    subject = '"[modelE-regression] ' + branch + ' tests aborted " '
    cmd = '/usr/bin/mail -s ' + subject + mailto + ' < ' + errorFile
    if html == 'yes':
        pref = 'mutt -e "set content_type=text/html" -s '
        cmd = pref + subject + mailto + ' < ' + errorFile

    logger.debug('Mail command: \n' + cmd)
    util.sp_call(cmd)


def send_diffreport(config, compconfig, eTime, rundeckDeps):
    # Create a diff report and notify via email
    userconfig = util.config_section_map(config, 'USERCONFIG')
    mailto = userconfig['mailto']
    logger.debug('Creating diffreport for ' + mailto)
    listFile = os.path.join(userconfig['scriptsdir'], 'mailingList')
    branch = userconfig['repobranch']
    if not branch:
        branch = 'detached'
    resultsDir = os.path.join(userconfig['scratchdir'], 'results', branch)
    runDir = os.path.join(userconfig['scratchdir'], 'scratch', branch, 'savedisk')
    buildtype = userconfig['buildtype']
    message = userconfig['message']
    html = userconfig['html']
    sortdiff = userconfig['sortdiff']
    compilers = util.get_compilers(compconfig)

    diffFile = os.path.join(resultsDir, 'diffreport.txt')
    fp = open(diffFile, 'w')
    if html == 'yes':
        fp.write('<html><pre>\n')
    fp.write(message + ' \n')
    fp.write('Repository: ' + userconfig['repository'] + '\n')
    fp.write('-' * 80 + '\n')
    fp.write('Branch: ' + branch)
    fp.write('  --  Build type: ' + buildtype + '\n')
    fp.write('-' * 80 + '\n')
    fp.write('%78s\n' % '    -REPRODUCIBILITY   ')
    fp.write('%20s%10s%8s%8s%8s%8s%8s%8s\n' %
             ('RUNDECK', 'COMPILER', 'MODE', 'RUN', 'UNT', 'BAS', 'RST', 'NPE'))
    fp.write('-' * 80 + '\n')

    if sortdiff == 'yes':
        f1 = os.path.join(resultsDir, 'alldiffs')
        f2 = os.path.join(resultsDir, 'sorteddiffs')
        util.sp_call('find ' + resultsDir + ' -name \*.diff -exec cat {} \; >' + f1)
        util.sp_call('cat ' + f1 + ' | sort -k 1,1 > ' + f2)
        with open(f2, 'r') as inf:
            fp.write(inf.read())
        os.remove(f1)
        os.remove(f2)
    else:
        for comp in compilers:
            diffs = glob.glob(resultsDir + '/' + comp + '/*.diff')
            for f in diffs:
                with open(f, 'r') as inf:
                    fp.write(inf.read())

    # In some cases, if a task terminated unexpectedly then the results will
    # not be recorded to a diff file. However, the system should generate an
    # error file (*.err). If such a file exists then we update the results
    # and notify a system error.
    results = [' ' * 20, ' ' * 10, ' ' * 8,
               '  -  ', '  -  ', '  -  ', '  -  ', '  -  ']
    for comp in compilers:
        errs = glob.glob(resultsDir + '/' + comp + '/*.err')
        for f in errs:
            if os.path.getsize(f) > 0:
                fname = f.split('/')[-1]
                results[0] = re.split(r'\.(?!\d)', fname)[0]
                results[1] = comp
                results[2] = re.split(r'\.(?!\d)', fname)[1]
                results[3] = 'U'
                util.write_diff(results, fp)

    # Write list of rundeck dependencies
    fp.write('-' * 80 + '\n')
    fp.write('             RUNDECK : DEPENDENCIES\n')
    fp.write('-' * 50 + '\n')
    noDependencies = True
    for key in rundeckDeps.keys():
        if rundeckDeps[key] != 'none':
            noDependencies = False
            fp.write('%20s : %-40s\n' % (key, rundeckDeps[key]))

    if noDependencies:
        fp.write(' *** No dependencies were set in these tests ***\n')

    fp.write('-' * 80 + '\n')
    hhmmss = time.strftime('%H:%M:%S', time.gmtime(eTime))
    fp.write('Time taken = %s \n' % hhmmss)
    fp.write('-' * 80 + '\n')
    fp.write('Legend:\n')
    fp.write('-' * 7 + '\n')
    fp.write('+   : success\n')
    fp.write('C   : created baseline\n')
    fp.write('Fb  : build failure\n')
    fp.write('F1  : 1hr run-time failure\n')
    fp.write('Fr  : restart run-time failure\n')
    fp.write('F*  : expected failure\n')
    fp.write('U   : unexpected system failure\n')
    fp.write('NUM : number of reproducibility differences\n')
    fp.write('-   : not available\n')
    fp.write('Notes:\n')
    fp.write('-' * 6 + '\n')
    compconfig = util.config_section_map(compconfig, 'COMPCONFIG')
    compVers = compconfig['compiler_versions'].split(",")
    i = 0
    for comp in compilers:
        fp.write(comp + ' compiler version: ' + compVers[i] + '\n')
        i += 1
    fp.write('Results in: ' + resultsDir + '\n')
    fp.write('Run dirs in: ' + runDir + '\n')
    fp.write('-' * 80 + '\n')
    fp.write('Commits since date of last baseline change:\n')
    #    fp.write('Previous 3 Commits:\n')
    with open(resultsDir + '/gitLog', 'r') as inf:
        fp.write(inf.read())
    fp.write('\n')
    fp.write('-' * 80 + '\n')
    if html == 'yes':
        fp.write('</pre></html>\n')
    fp.close()

    # Set up email list to replace AMLS, which blocked Discover email
    # Read in list of email addresses, one per line
    emailList = ''
    if os.path.isfile(listFile):
        with open(listFile, "r") as mailList:
            for address in mailList:
                emailList = emailList + ' -c "{}" '.format(address.strip())
    logger.debug('Email list: \n' + emailList)

    subject = '"[modelE-regression] ' + branch + ' branch - build: ' + buildtype + '" '
    cmd = '/usr/bin/mail -s ' + subject + mailto + ' < ' + diffFile
    if html == 'yes':
        pref = 'mutt -e "set content_type=text/html" -s '
        cmd = pref + subject + emailList + mailto + ' < ' + diffFile

    logger.debug('Mail command: \n' + cmd)
    util.sp_call(cmd)