import pytest
import math
# import numpy as np

from src.lib.utils.forecasting_metrics import *


@pytest.mark.parametrize("actual, predicted, mse",
                         [(np.array([[1, 2], [3, 4]]),
                           np.array([[1, 2], [3, 4]]),
                           0.0),
                          (np.array([[1, 2], [3, 4]]),
                           np.array([[1, 2], [4, 4]]),
                           0.25),
                          (np.array([[0, 0], [0, 0]]),
                           np.array([[2, 2], [2, 2]]),
                           4.0),
                          (np.array([[1, 7], [0, 4]]),
                           np.array([[5, 2], [3, 4]]),
                           12.5)
                          ])
def test_compute_mse(actual, predicted, mse):
    assert mse - EPSILON <= compute_mse(actual, predicted) <= \
           mse + EPSILON


@pytest.mark.parametrize("actual, predicted, me",
                         [(np.array([[1, 2], [3, 4]]),
                           np.array([[1, 2], [3, 4]]),
                           0.0),
                          (np.array([[1, 2], [3, 4]]),
                           np.array([[1, 2], [4, 4]]),
                           -0.25),
                          (np.array([[0, 0], [0, 0]]),
                           np.array([[2, 2], [2, 2]]),
                           -2.0),
                          (np.array([[1, 7], [0, 4]]),
                           np.array([[5, 2], [3, 4]]),
                           -0.5)
                          ])
def test_compute_me(actual, predicted, me):
    assert me - EPSILON <= compute_me(actual, predicted) <= \
           me + EPSILON


@pytest.mark.parametrize("actual, predicted, mae",
                         [(np.array([[1, 2], [3, 4]]),
                           np.array([[1, 2], [3, 4]]),
                           0.0),
                          (np.array([[1, 2], [3, 4]]),
                           np.array([[1, 2], [4, 4]]),
                           0.25),
                          (np.array([[0, 0], [0, 0]]),
                           np.array([[2, 2], [2, 2]]),
                           2.0),
                          (np.array([[1, 7], [0, 4]]),
                           np.array([[5, 2], [3, 4]]),
                           3.0)
                          ])
def test_compute_mae(actual, predicted, mae):
    assert mae - EPSILON <= compute_mae(actual, predicted) <= \
           mae + EPSILON


@pytest.mark.parametrize("actual, predicted, rmse",
                         [(np.array([[1, 2], [3, 4]]),
                           np.array([[1, 2], [3, 4]]),
                           0.0),
                          (np.array([[1, 2], [3, 4]]),
                           np.array([[1, 2], [4, 4]]),
                           math.sqrt(0.25)),
                          (np.array([[0, 0], [0, 0]]),
                           np.array([[2, 2], [2, 2]]),
                           2.0),
                          (np.array([[1, 7], [0, 4]]),
                           np.array([[5, 2], [3, 4]]),
                           math.sqrt(12.5))
                          ])
def test_compute_rmse(actual, predicted, rmse):
    assert rmse - EPSILON <= compute_rmse(actual, predicted) <= \
           rmse + EPSILON


@pytest.mark.parametrize("actual, predicted, mpe",
                         [(np.array([[1, 2], [3, 4]]),
                           np.array([[1, 2], [3, 4]]),
                           0.0),
                          (np.array([[1, 2], [3, 4]]),
                           np.array([[1, 2], [4, 4]]),
                           0.25 * (-1.0 / 3.0)),
                          (np.array([[1, 1], [1, 1]]),
                           np.array([[2, 2], [2, 2]]),
                           0.25 * -4),
                          (np.array([[1, 4], [3, 4]]),
                           np.array([[3, 2], [6, 4]]),
                           0.25 * (-2.0 + 0.5 + -1.0))
                          ])
def test_compute_mpe(actual, predicted, mpe):
    assert mpe - EPSILON <= compute_mpe(actual, predicted) <= \
           mpe + EPSILON
