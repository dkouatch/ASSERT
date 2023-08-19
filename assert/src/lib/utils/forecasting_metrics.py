#!/usr/bin/env python

"""
  This module contains a collection of functions for
  computing different types of errors using
  Numpy arrays. In most of the functions, it is assumed
  two Numpy arrays are passed as arguments:

   - actual
   - predicted

  This is adaptation of the work presented at:

  https://gist.github.com/bshishov/5dc237f59f019b26145648e2124ca1c9

  References:
    - Theodosiou, M. (2011). Forecasting monthly and quarterly time
      series using STL decomposition. International Journal of
      Forecasting, 27(4), 1178–1195.
      doi:10.1016/j.ijforecast.2010.11.002
    - Shcherbakov, Maxim Vladimirovich, et al. "A survey of forecast
      error measures." World Applied Sciences Journal 24.24
      (2013): 171-176.
    - Blaskowitz and Herwartz (2009, 2011) On economic evaluation
      of directional forecasts.
    - Bergmeir C., Costantini M., Benítez J. M. (2014). On the
      usefulness of cross-validation for directional forecast
      evaluation. Computational Statistics & Data Analysis.
"""

import numpy as np

from typing import Iterable

EPSILON = np.finfo(float).eps  # double precision
# EPSILON = np.finfo(np.float32).eps      # single precision


def _simple_error(actual: np.ndarray,
                  predicted: np.ndarray) -> np.ndarray:
    """
    Compute the simple error.

    Parameters
    ----------
    actual : np.ndarray
        Numpy array
    predicted : np.ndarray
        Numpy array

    Returns
    -------
    np.ndarray
        Simple difference of the actual and the predicted Numpy arrays.

    """
    return actual - predicted


def _percentage_error(actual: np.ndarray,
                      predicted: np.ndarray) -> np.ndarray:
    """
    Compute the percentage error of two Numpy arrays.

    Note: result is NOT multiplied by 100

    Parameters
    ----------
    actual : np.ndarray
        Numpy array
    predicted : np.ndarray
        Numpy array

    Returns
    -------
    np.ndarray
        Percentage error

    """
    return _simple_error(actual, predicted) / (actual + EPSILON)


def _naive_forecasting(actual: np.ndarray, seasonality: int = 1):
    """
    Naive forecasting method which just repeats previous samples

    Parameters
    ----------
    actual : np.ndarray
        Numpy array
    seasonality : int
        The previous samples to consider.

    Returns
    -------
    np.ndarray
        Slice of samples.

    """
    return actual[:-seasonality]


def _relative_error(actual: np.ndarray,
                    predicted: np.ndarray,
                    benchmark: np.ndarray = None) -> np.ndarray:
    """
    Compute the Relative Error of two Numpy arrays against a
    benchmark Numpy array (if provided).

    Parameters
    ----------
    actual : np.ndarray
        Numpy array
    predicted : np.ndarray
        Numpy array
    benchmark : int, np.ndarray
        An integer or a Numpy array. None by default.

    Returns
    -------
    np.ndarray
        The relative error.

    """
    if benchmark is None or isinstance(benchmark, int):
        # If no benchmark prediction provided - use naive forecasting
        if not isinstance(benchmark, int):
            seasonality = 1
        else:
            seasonality = benchmark
        return _simple_error(actual[seasonality:],
                             predicted[seasonality:]) / \
            (_simple_error(
                actual[seasonality:],
                _naive_forecasting(actual, seasonality)
            ) + EPSILON)

    return _simple_error(actual, predicted) / \
        (_simple_error(actual, benchmark) + EPSILON)


def _bounded_relative_error(actual: np.ndarray,
                            predicted: np.ndarray,
                            benchmark: np.ndarray = None) \
        -> np.ndarray:
    """
    Compute the Bounded Relative Error of two Numpy arrays
    against a benchmark Numpy array (if provided).

    Parameters
    ----------
    actual : np.ndarray
        Numpy array
    predicted : np.ndarray
        Numpy array
    benchmark : np.ndarray
        An integer or a Numpy array. None by default.

    Returns
    -------
    np.ndarray
        The bounded relative error.

    """
    if benchmark is None or isinstance(benchmark, int):
        # If no benchmark prediction provided - use naive forecasting
        if not isinstance(benchmark, int):
            seasonality = 1
        else:
            seasonality = benchmark

        abs_err = np.abs(_simple_error(actual[seasonality:],
                                       predicted[seasonality:]))
        abs_err_bench = np.abs(
            _simple_error(actual[seasonality:],
                          _naive_forecasting(actual, seasonality)))
    else:
        abs_err = np.abs(_simple_error(actual, predicted))
        abs_err_bench = np.abs(_simple_error(actual, benchmark))

    return abs_err / (abs_err + abs_err_bench + EPSILON)


def _geometric_mean(a: Iterable,
                    axis: int = 0,
                    dtype=None) -> np.ndarray:
    """
    Compute the geometric mean along an axis.

    Parameters
    ----------
    a : Iterable (list, ndarray, etc.)
        A collection of numbers.
    axis : int
        The axis index.
    dtype :
        The data type of the collection a.
    Returns
    -------
    np.ndarray
        The geometric mean along the axis.

    """
    if not isinstance(a, np.ndarray):
        # if not an ndarray object attempt to convert it
        log_a = np.log(np.array(a, dtype=dtype))
    elif dtype:
        # Must change the default dtype allowing array type
        if isinstance(a, np.ma.MaskedArray):
            log_a = np.log(np.ma.asarray(a, dtype=dtype))
        else:
            log_a = np.log(np.asarray(a, dtype=dtype))
    else:
        log_a = np.log(a)
    return np.exp(log_a.mean(axis=axis))


def compute_mse(actual: np.ndarray, predicted: np.ndarray) -> float:
    """
    Compute the Mean Squared Error

    Parameters
    ----------
    actual : np.ndarray
        Numpy array
    predicted : np.ndarray
        Numpy array

    Returns
    -------
    float
        A floating point number for the MSE.

    """
    return np.mean(np.square(_simple_error(actual, predicted)))


def compute_rmse(actual: np.ndarray, predicted: np.ndarray) -> float:
    """
    Compute the Root Mean Squared Error.

    Parameters
    ----------
    actual : np.ndarray
        Numpy array
    predicted : np.ndarray
        Numpy array

    Returns
    -------
    float
        A floating point number for the RMSE.

    """
    return np.sqrt(compute_mse(actual, predicted))


def compute_nrmse(actual: np.ndarray, predicted: np.ndarray) -> float:
    """
    Compute the Normalized Root Mean Squared Error.

    Parameters
    ----------
    actual : np.ndarray
        Numpy array
    predicted : np.ndarray
        Numpy array

    Returns
    -------
    float
        A floating point number for the NRMSE.

    """
    return compute_rmse(actual, predicted) / (actual.max() - actual.min())


def compute_me(actual: np.ndarray, predicted: np.ndarray) -> float:
    """
    Compute the Mean Error.

    Parameters
    ----------
    actual : np.ndarray
        Numpy array
    predicted : np.ndarray
        Numpy array

    Returns
    -------
    float
        A floating point number for the mean error.

    """
    return np.mean(_simple_error(actual, predicted))


# ---------------------------------------------------------------------
# --> compute_mae
# ---------------------------------------------------------------------
def compute_mae(actual: np.ndarray, predicted: np.ndarray) -> float:
    """
    Compute the Mean Absolute Error.

    Parameters
    ----------
    actual : np.ndarray
        Numpy array
    predicted : np.ndarray
        Numpy array

    Returns
    -------
    float
        A floating point number for the mean absolute error.

    """
    return np.mean(np.abs(_simple_error(actual, predicted)))


compute_mad = compute_mae  # Mean Absolute Deviation (it is the same as MAE)


def compute_gmae(actual: np.ndarray, predicted: np.ndarray) -> float:
    """
    Compute the Geometric Mean Absolute Error.

    Parameters
    ----------
    actual : np.ndarray
        Numpy array
    predicted : np.ndarray
        Numpy array

    Returns
    -------
    float
        A floating point number for the mean absolute error.

    """
    return _geometric_mean(np.abs(_simple_error(actual, predicted)))


def compute_mdae(actual: np.ndarray, predicted: np.ndarray) -> float:
    """
    Compute the Median Absolute Error.

    Parameters
    ----------
    actual : np.ndarray
        Numpy array
    predicted : np.ndarray
        Numpy array

    Returns
    -------
    float
        A floating point number for the median absolute error.

    """
    return np.median(np.abs(_simple_error(actual, predicted)))


def compute_mpe(actual: np.ndarray, predicted: np.ndarray) -> float:
    """
    Compute the Mean Percentage Error.

    Parameters
    ----------
    actual : np.ndarray
        Numpy array
    predicted : np.ndarray
        Numpy array

    Returns
    -------
    float
        A floating point number for the mean percentage error.

    """
    return np.mean(_percentage_error(actual, predicted))


def compute_maxape(actual: np.ndarray,
                   predicted: np.ndarray) -> float:
    """
    Compute the Max Absolute Percentage Error.

    Parameters
    ----------
    actual : np.ndarray
        Numpy array
    predicted : np.ndarray
        Numpy array

    Returns
    -------
    float
        A floating point number for the max absolute percentage error.

    """
    return np.max(np.abs(_percentage_error(actual, predicted)))


def compute_mape(actual: np.ndarray, predicted: np.ndarray) -> float:
    """
    Compute the Mean Absolute Percentage Error.
    The function has the following properties:
        + Easy to interpret
        + Scale independent
        - Biased, not symmetric
        - Undefined when actual[t] == 0

    Note: result is NOT multiplied by 100

    Parameters
    ----------
    actual : np.ndarray
        Numpy array
    predicted : np.ndarray
        Numpy array

    Returns
    -------
    float
        A floating point number for the mean
        absolute percentage error.

    """
    return np.mean(np.abs(_percentage_error(actual, predicted)))


def compute_mdape(actual: np.ndarray, predicted: np.ndarray) -> float:
    """
    Compute the Median Absolute Percentage Error.

    Note: result is NOT multiplied by 100

    Parameters
    ----------
    actual : np.ndarray
        Numpy array
    predicted : np.ndarray
        Numpy array

    Returns
    -------
    float
        A floating point number for the median
        absolute percentage error.

    """
    return np.median(np.abs(_percentage_error(actual, predicted)))


def compute_smape(actual: np.ndarray, predicted: np.ndarray) -> float:
    """
    Compute the Symmetric Mean Absolute Percentage Error.

    Note: result is NOT multiplied by 100

    Parameters
    ----------
    actual : np.ndarray
        Numpy array
    predicted : np.ndarray
        Numpy array

    Returns
    -------
    float
        A floating point number for the symmetric
        mean absolute percentage error.

    """
    return np.mean(
        2.0 * np.abs(actual - predicted) /
        ((np.abs(actual) + np.abs(predicted)) + EPSILON)
    )


def compute_smdape(actual: np.ndarray,
                   predicted: np.ndarray) -> float:
    """
    Compute the Symmetric Median Absolute Percentage Error.

    Note: result is NOT multiplied by 100

    Parameters
    ----------
    actual : np.ndarray
        Numpy array
    predicted : np.ndarray
        Numpy array

    Returns
    -------
    float
        A floating point number for the symmetric
        median absolute percentage error.

    """
    return np.median(
        2.0 * np.abs(actual - predicted) /
        ((np.abs(actual) + np.abs(predicted)) + EPSILON)
    )


def compute_maape(actual: np.ndarray, predicted: np.ndarray) -> float:
    """
    Compute the Mean Arctangent Absolute Percentage Error.

    Note: result is NOT multiplied by 100

    Parameters
    ----------
    actual : np.ndarray
        Numpy array
    predicted : np.ndarray
        Numpy array

    Returns
    -------
    float
        A floating point number for the mean arctangent
        absolute percentage error.

    """
    return np.mean(
        np.arctan(
            np.abs((actual - predicted) / (actual + EPSILON))
        )
    )


def compute_mase(actual: np.ndarray,
                 predicted: np.ndarray,
                 seasonality: int = 1) -> float:
    """
    Compute the Mean Absolute Scaled Error.
    The baseline (benchmark) is computed with naive
    forecasting (shifted by @seasonality).

    Parameters
    ----------
    actual : np.ndarray
        Numpy array
    predicted : np.ndarray
        Numpy array
    seasonality: int
        An integer

    Returns
    -------
    float
        A floating point number for the mean absolute scaled error.

    """
    return compute_mae(actual, predicted) / \
        compute_mae(actual[seasonality:],
                    _naive_forecasting(actual, seasonality)
                    )


def compute_std_ae(actual: np.ndarray,
                   predicted: np.ndarray) -> float:
    """
    Compute the  Normalized Absolute Error.

    Parameters
    ----------
    actual : np.ndarray
        Numpy array
    predicted : np.ndarray
        Numpy array

    Returns
    -------
    float
        A floating point number for the normalized absolute error.

    """
    __mae = compute_mae(actual, predicted)
    return np.sqrt(
        np.sum(np.square(_simple_error(actual, predicted) - __mae))
        /
        (len(actual) - 1)
    )


def compute_std_ape(actual: np.ndarray,
                    predicted: np.ndarray) -> float:
    """
    Compute the Normalized Absolute Percentage Error.

    Parameters
    ----------
    actual : np.ndarray
        Numpy array
    predicted : np.ndarray
        Numpy array

    Returns
    -------
    float
        A floating point number for the normalized
        absolute percentage error.

    """
    __mape = compute_mape(actual, predicted)
    return np.sqrt(
        np.sum(
            np.square(_percentage_error(actual, predicted) - __mape)
        ) /
        (len(actual) - 1)
    )


def compute_rmspe(actual: np.ndarray, predicted: np.ndarray) -> float:
    """
    Compute the Root Mean Squared Percentage Error.

    Note: result is NOT multiplied by 100

    Parameters
    ----------
    actual : np.ndarray
        Numpy array
    predicted : np.ndarray
        Numpy array

    Returns
    -------
    float
        A floating point number for the root mean
        squared percentage error.

    """
    return np.sqrt(
        np.mean(np.square(_percentage_error(actual, predicted)))
    )


def compute_rmdspe(actual: np.ndarray,
                   predicted: np.ndarray) -> float:
    """
    Compute the Root Median Squared Percentage Error.

    Note: result is NOT multiplied by 100

    Parameters
    ----------
    actual : np.ndarray
        Numpy array
    predicted : np.ndarray
        Numpy array

    Returns
    -------
    float
        A floating point number for the root median
        squared percentage error.

    """
    return np.sqrt(
        np.median(np.square(_percentage_error(actual, predicted)))
    )


def compute_rmsse(actual: np.ndarray,
                  predicted: np.ndarray,
                  seasonality: int = 1) -> float:
    """
    Compute the Root Mean Squared Scaled Error.

    Parameters
    ----------
    actual : np.ndarray
        Numpy array
    predicted : np.ndarray
        Numpy array
    seasonality: int
        An integer

    Returns
    -------
    float
        A floating point number for the root mean squared scaled error.
    """
    q = (np.abs(_simple_error(actual, predicted))
         /
         compute_mae(actual[seasonality:],
                     _naive_forecasting(actual, seasonality))
         )
    return np.sqrt(np.mean(np.square(q)))


def compute_inrse(actual: np.ndarray, predicted: np.ndarray) -> float:
    """
    Compute the Integral Normalized Root Squared Error.

    Parameters
    ----------
    actual : np.ndarray
        Numpy array
    predicted : np.ndarray
        Numpy array

    Returns
    -------
    float
        A floating point number for the integral normalized root squared error.

    """
    return np.sqrt(
        np.sum(np.square(_simple_error(actual, predicted)))
        /
        np.sum(np.square(actual - np.mean(actual)))
    )


def compute_rrse(actual: np.ndarray, predicted: np.ndarray) -> float:
    """
    Compute the Root Relative Squared Error.

    Parameters
    ----------
    actual : np.ndarray
        Numpy array
    predicted : np.ndarray
        Numpy array

    Returns
    -------
    float
        A floating point number for the root relative squared error.

    """
    return np.sqrt(
        np.sum(np.square(actual - predicted))
        /
        np.sum(np.square(actual - np.mean(actual)))
    )


def compute_mre(actual: np.ndarray,
                predicted: np.ndarray,
                benchmark: np.ndarray = None) -> float:
    """
    Compute the Mean Relative Error.

    Parameters
    ----------
    actual : np.ndarray
        Numpy array
    predicted : np.ndarray
        Numpy array
    benchmark : int, np.ndarray
        An integer or a Numpy array. None by default.

    Returns
    -------
    float
        A floating point number for the mean relative error.

    """
    return np.mean(_relative_error(actual, predicted, benchmark))


def compute_rae(actual: np.ndarray, predicted: np.ndarray) -> float:
    """
    Compute the Relative Absolute Error (aka Approximation Error).

    Parameters
    ----------
    actual : np.ndarray
        Numpy array
    predicted : np.ndarray
        Numpy array

    Returns
    -------
    float
        A floating point number for the relative absolute error.
    """
    return np.sum(np.abs(actual - predicted)) / \
        (np.sum(np.abs(actual - np.mean(actual))) + EPSILON)


def compute_mrae(actual: np.ndarray,
                 predicted: np.ndarray,
                 benchmark: np.ndarray = None) -> float:
    """
    Compute the Mean Relative Absolute Error.

    Parameters
    ----------
    actual : np.ndarray
        Numpy array
    predicted : np.ndarray
        Numpy array
    benchmark : int, np.ndarray
        An integer or a Numpy array. None by default.

    Returns
    -------
    float
        A floating point number for the mean relative absolute error.
    """
    return np.mean(
        np.abs(_relative_error(actual, predicted, benchmark))
    )


def compute_mdrae(actual: np.ndarray,
                  predicted: np.ndarray,
                  benchmark: np.ndarray = None) -> float:
    """
    Compute the Median Relative Absolute Error.

    Parameters
    ----------
    actual : np.ndarray
        Numpy array
    predicted : np.ndarray
        Numpy array
    benchmark : int, np.ndarray
        An integer or a Numpy array. None by default.

    Returns
    -------
    float
        A floating point number for the median
        relative absolute error.

    """
    return np.median(np.abs(_relative_error(actual, predicted, benchmark)))


def compute_gmrae(actual: np.ndarray,
                  predicted: np.ndarray,
                  benchmark: np.ndarray = None) -> float:
    """
    Compute the Geometric Mean Relative Absolute Error.

    Parameters
    ----------
    actual : np.ndarray
        Numpy array
    predicted : np.ndarray
        Numpy array
    benchmark : int, np.ndarray
        An integer or a Numpy array. None by default.

    Returns
    -------
    float
        A floating point number for the geometric
        mean relative absolute error.

    """
    return _geometric_mean(
        np.abs(_relative_error(actual, predicted, benchmark))
    )


def compute_mbrae(actual: np.ndarray,
                  predicted: np.ndarray,
                  benchmark: np.ndarray = None) -> float:
    """
    Compute the Mean Bounded Relative Absolute Error.

    Parameters
    ----------
    actual : np.ndarray
        Numpy array
    predicted : np.ndarray
        Numpy array
    benchmark : int, np.ndarray
        An integer or a Numpy array. None by default.

    Returns
    -------
    float
        A floating point number for the mean
        bounded relative absolute error.

    """
    return np.mean(
        _bounded_relative_error(actual, predicted, benchmark)
    )


def compute_umbrae(actual: np.ndarray,
                   predicted: np.ndarray,
                   benchmark: np.ndarray = None) -> float:
    """
    Compute the Unscaled Mean Bounded Relative Absolute Error.

    Parameters
    ----------
    actual : np.ndarray
        Numpy array
    predicted : np.ndarray
        Numpy array
    benchmark : int, np.ndarray
        An integer or a Numpy array. None by default.

    Returns
    -------
    float
        A floating point number for the unscaled mean bounded relative absolute error.

    """
    __mbrae = compute_mbrae(actual, predicted, benchmark)
    return __mbrae / (1 - __mbrae)


def compute_mda(actual: np.ndarray, predicted: np.ndarray) -> float:
    """
    Compute the Mean Directional Accuracy.

    Parameters
    ----------
    actual : np.ndarray
        Numpy array
    predicted : np.ndarray
        Numpy array

    Returns
    -------
    float
        A floating point number for the mean directional accuracy.
    """
    return np.mean(
        (np.sign(actual[1:] - actual[:-1])
         ==
         np.sign(predicted[1:] - predicted[:-1])).astype(int)
    )


METRICS = {'mse': compute_mse,
           'rmse': compute_rmse,
           'nrmse': compute_nrmse,
           'me': compute_me,
           'mae': compute_mae,
           'mad': compute_mad,
           'gmae': compute_gmae,
           'mdae': compute_mdae,
           'mpe': compute_mpe,
           'mape': compute_mape,
           'mdape': compute_mdape,
           'smape': compute_smape,
           'smdape': compute_smdape,
           'maape': compute_maape,
           'mase': compute_mase,
           'std_ae': compute_std_ae,
           'std_ape': compute_std_ape,
           'rmspe': compute_rmspe,
           'rmdspe': compute_rmdspe,
           'rmsse': compute_rmsse,
           'inrse': compute_inrse,
           'rrse': compute_rrse,
           'mre': compute_mre,
           'rae': compute_rae,
           'mrae': compute_mrae,
           'mdrae': compute_mdrae,
           'gmrae': compute_gmrae,
           'mbrae': compute_mbrae,
           'umbrae': compute_umbrae,
           'mda': compute_mda,
           }


def evaluate(actual: np.ndarray,
             predicted: np.ndarray,
             metrics: set = ('mae', 'mse', 'smape', 'umbrae')) \
        -> dict:
    """
    Evaluates certain metrics

    Parameters
    ----------
    actual : np.ndarray
        Numpy array
    predicted : np.ndarray
        Numpy array
    metrics : set
        Metric to evaluate stored as strings in a tuple

    Returns
    -------
    dict
        Evaluation results

    """
    results = dict()
    for name in metrics:
        try:
            results[name] = METRICS[name](actual, predicted)
        except Exception as err:
            results[name] = np.nan
            print('Unable to compute metric {0}: {1}'.format(name, err))
    return results


def evaluate_all_metrics(actual: np.ndarray,
                         predicted: np.ndarray) -> dict:
    """
    Evaluates all metrics

    Parameters
    ----------
    actual : np.ndarray
        Numpy array
    predicted : np.ndarray
        Numpy array

    Returns
    -------
    dict
        Evaluation results

    """
    return evaluate(actual, predicted, metrics=set(METRICS.keys()))


if __name__ == "__main__":
    """import random

    actual = np.random.uniform(-1.5, 2.0, size=(144, 91))
    predicted = actual + random.gauss(0.0, 0.095)

    actual = np.array([[0, 1], [1, 1]])
    predicted = np.array([[0.1, 1], [1, 1]])

    # results = evaluate(actual, predicted)
    # for key in results:
    #    print("{:>10}: {}".format(key, results[key]))

    results = evaluate_all_metrics(actual, predicted)
    for key in results:
        print("{:>10}: {}".format(key, results[key]))"""
