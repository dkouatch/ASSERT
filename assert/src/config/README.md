[__<< src__](../README.md)

# ASSERT config module

### Basic example YAML configuration file

```
modelconfig:
  repository: <enter repo URL here>
  repobranch: <enter repo branch name here>
  ...
systemconfig:
  scratchdir: <enter scratch directory here>
  cleanscratch: yes
  ...
reportconfig:
  mailto: <enter email addresses here>
  message: <enter email subject message here>
  html: no
  ...
testcases:
  test1:
    run: yes
    ...
  ...
```

Each configuration file should contain four main categories:
`modelconfig`, `systemconfig`, `reportconfig`, and `testcases`.

### `Modelconfig`

Contains all the information related to repositories and
the model itself.

At the very least, it should contain:

- The remote repository URL
- The branch name of the remote repository

### `Systemconfig`

Contains all system-related information for running the test
including key directory locations and compiler types and versions.

At the very least, it should contain:

- A scratch directory to run the model regression test in
- A flag for whether to clear the scratch directory after running
  tests

### `Reportconfig`

Contains all the information related to generating reports from
the regression test such as mailing addresses and
formatting options.

At the very least, it should contain:

- A list of email addresses to send reports to
- The email subject message
- An _HTML_ formatting flag

### `Testcases`

Contains information about all the tests for the model including
compiler specs and build type.