# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2022 Valory AG
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

"""Machine learning tools for agent behaviours of the PriceProphetABCIApp"""

import time
from typing import Tuple
import logging

import numpy as np
import pandas as pd

from sklearn.metrics import mean_squared_error, make_scorer
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, cross_validate, cross_val_score

from skforecast.ForecasterAutoreg import ForecasterAutoreg
from skforecast.ForecasterAutoregCustom import ForecasterAutoregCustom
from skforecast.ForecasterAutoregDirect import ForecasterAutoregDirect
from skforecast.model_selection import grid_search_forecaster
from skforecast.model_selection import backtesting_forecaster
from skforecast.utils import save_forecaster
from skforecast.utils import load_forecaster

import matplotlib.pyplot as plt

try:
    import talib
    from talib import abstract
except ImportError:
    raise ImportError("install TA-Lib using the instruction here: https://cloudstrata.io/install-ta-lib-on-ubuntu-server/")


RANDOM_STATE = 123

Y_TARGET = "close"
STEPS_INTO_THE_FUTURE = 5  # 5 minutes
N_BACKTESTING = STEPS_INTO_THE_FUTURE * 3
DEFAULT_LAGS = 5

# hyperparameter optimization
LAGS_GRID = [1, 1]
PARAM_GRID = dict(
    n_estimators=[10, 50],
)

RMSE = make_scorer(mean_squared_error, squared=True, greater_is_better=False)

# __repr__ display them as dicts, all are in fact classes
TA_INDICATORS = list(map(abstract.Function, talib.get_functions()))
COLUMNS = ["timestamp", "open", "high", "low", "close", "volume"]


regressor = RandomForestRegressor(random_state=RANDOM_STATE)
forecaster = ForecasterAutoreg(regressor=regressor, lags=DEFAULT_LAGS)


def compute_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Compute TA indicators"""
    # tested as: data = ccxt.kraken().fetch_ohlcv("BTC/USDT")
    #            df = pd.DataFrame(data, columns=COLUMNS)
    data = [df]
    for f in TA_INDICATORS:
        name = f._Function__name.decode('utf-8')
        try:
            transformed = f(df)
            if len(transformed.shape) == 1:
                transformed = transformed.to_frame(name=name)
            data.append(transformed)
        except Exception:
            logging.warning(f"could not apply {name}")
    # expected shape: time x feature = 720 x 180
    return pd.concat(data, axis=1)


def impute(x: pd.DataFrame) -> pd.DataFrame:
    """Impute and discard features with NaNs"""

    # we do not train an imputer and opt to simply
    # interpolate or drop otherwise
    shape_in = x.shape
    total_data_points = int.__mul__(*shape_in)
    x = x.replace([np.inf, -np.inf], np.nan)

    number_of_nans = x.isna().sum().sum()
    logging.info(f"NaN fraction: {number_of_nans / total_data_points}")

    # time series interpolation: linear, time, splines, etc.
    datetime_index = x["timestamp"].values.astype(dtype='datetime64[ms]')
    x = x.set_index(datetime_index)
    x = x.interpolate(method="time")
    logging.info(f"NaN fraction: {number_of_nans / total_data_points}")

    # here we could impute; e.g. mean, median.

    # drop remaining NaNs
    x = x.dropna(axis=1)
    remaining_ratio = int.__mul__(*x.shape) / total_data_points
    logging.info(f"Remaining data: {shape_in} -> {x.shape} ({remaining_ratio})")
    return x.reset_index(drop=True)


def split_train_test(x: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Split the data in train and test set"""

    x_train, x_test = x[:-STEPS_INTO_THE_FUTURE], x[-STEPS_INTO_THE_FUTURE:]
    return x_train, x_test


def train_model(x: pd.DataFrame, random_state: int):
    """Train model"""

    # currently we interpolate and discard features with NaN
    x_imputed = x.dropna(axis=1, how="all").dropna()
    x_imputed.reset_index(drop=True, inplace=True)  # for forecaster
    x_train, x_test = split_train_test(x_imputed)
    forecaster.regressor.random_state = random_state

    # this runs the grid search
    # currently still univariate (without exogenous variables)
    results_grid = grid_search_forecaster(
        forecaster=forecaster,
        y=x_train[Y_TARGET],
        param_grid=PARAM_GRID,
        lags_grid=LAGS_GRID,
        steps=STEPS_INTO_THE_FUTURE,
        refit=True,  # set False to speed up
        metric="mean_squared_error",
        initial_train_size=x_train.shape[0] // 2,
        fixed_train_size=False,
        return_best=True,
        verbose=False,
    )

    # ['lags', 'params', 'mean_squared_error', 'max_depth', 'n_estimators']
    return results_grid


def test_dev():
    """"""

    import ccxt
    data = ccxt.kraken().fetch_ohlcv("BTC/USDT")
    df = pd.DataFrame(data, columns=COLUMNS)
    transformed_data = compute_indicators(df)

    # X = impute(transformed_data)
    X = transformed_data.dropna(axis=1, how="all").dropna()
    X = X.reset_index(drop=True)

    X_train, X_test = split_train_test(X)

    # plot the data
    fig, ax = plt.subplots(figsize=(10, 6))
    X_train[Y_TARGET].plot(ax=ax, label='train')
    X_test[Y_TARGET].plot(ax=ax, label='test')
    ax.legend()
    plt.show()

    forecaster.fit(y=X_train[Y_TARGET])
    predictions = forecaster.predict(steps=STEPS_INTO_THE_FUTURE)

    fig, ax = plt.subplots(figsize=(10, 6))
    X_train[Y_TARGET].plot(ax=ax, label='train')
    X_test[Y_TARGET].plot(ax=ax, label='test')
    predictions.plot(ax=ax, label='predictions')
    ax.legend()
    plt.show()

    score = mean_squared_error(y_true=X_test[Y_TARGET], y_pred=predictions)
    logging.error(f"MSE: {score}")

    t0 = time.time()
    results_grid = grid_search_forecaster(
        forecaster=forecaster,
        y=X_train[Y_TARGET],
        param_grid=PARAM_GRID,
        lags_grid=LAGS_GRID,
        steps=STEPS_INTO_THE_FUTURE,
        refit=True,
        metric="mean_squared_error",
        initial_train_size=X_train.shape[0] // 2,
        fixed_train_size=False,
        return_best=True,
        verbose=False,
    )
    logging.error(f"Time to search: {time.time() - t0}")

    predictions = forecaster.predict(steps=STEPS_INTO_THE_FUTURE)
    feature_importance = forecaster.get_feature_importance()
    score = mean_squared_error(y_true=X_test[Y_TARGET], y_pred=predictions)
    logging.error(f"MSE: {score}")

    # Backtesting

    # https://joaquinamatrodrigo.github.io/skforecast/0.5.1/user_guides/backtesting.html#backtesting
    metric, predictions_backtest = backtesting_forecaster(
        forecaster=forecaster,
        y=X_train[Y_TARGET],
        initial_train_size=len(X) - N_BACKTESTING,
        fixed_train_size=False,
        steps=STEPS_INTO_THE_FUTURE,
        metric='mean_squared_error',
        refit=True,
        verbose=True
    )

    logging.error(f"Backtest error: {metric}")

    fig, ax = plt.subplots(figsize=(10, 6))
    X.loc[predictions_backtest.index, Y_TARGET].plot(ax=ax, label='test')
    predictions_backtest.plot(ax=ax, label='predictions')
    ax.legend()

