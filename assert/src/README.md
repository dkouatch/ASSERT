[__<< Home__](../doc/README.md)

# ASSERT src module

The `src` module contains all the code needed to run ASSERT
regression tests. It is used by the main.py script.


```
 .
 |______init__.py
 |____config
 |  |____geos_setup.yaml
 |  |____model_e_setup.yaml
 |____lib
 |  |______init__.py
 |  |____utils
 |  |  |______init__.py
 |  |  |____access_repo.py
 |  |  |____config.py
 |  |  |____datatypes.py
 |  |  |____forecasting_metrics.py
 |  |  |____logger.py
 |  |  |____paths.py
 |  |  |____server.py
 |  |  |____time.py
 |  |______init__.py
 |  |____earthsystems_reg.py
 |  |____earthsystems_report.py
 |  |____earthsystems_testcase.py
 |____models
 |  |______init__.py
 |  |____gce
 |  |  |______init__.py
 |  |  |____gce_reg.py
 |  |  |____gce_report.py
 |  |  |____gce_testcase.py
 |  |____geos
 |  |  |______init__.py
 |  |  |____geos_reg.py
 |  |  |____geos_report.py
 |  |  |____geos_testcase.py
 |  |____model_e
 |  |  |______init__.py
 |  |  |____model_e_reg.py
 |  |  |____model_e_report.py
 |  |  |____model_e_testcase.py
 |  |  |____model_e_utils.py
 |  |____nuwrf
 |  |  |______init__.py
 |  |  |____nuwrf_reg.py
 |  |  |____nuwrf_report.py
 |  |  |____nuwrf_testcase.py
```

### Sub-directories

[__assert/src/config >>__](config/README.md)

[__assert/src/lib >>__](lib/README.md)

[__assert/src/models >>__](models/README.md)