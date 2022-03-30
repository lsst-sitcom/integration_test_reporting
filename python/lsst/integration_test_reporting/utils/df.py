# Developed for the LSST System Integration, Test and Commissioning Team.
# This product includes software developed by the LSST Project
# (http://www.lsst.org).
# See the LICENSE file at the top-level directory of this distribution
# for details of code ownership.
#
# Use of this source code is governed by a 3-clause BSD-style
# license that can be found in the LICENSE file.

from typing import List

import numpy as np
import pandas as pd

__all__ = ("convert_timestamps", "get_now", "time_delta")


def convert_timestamps(df: pd.DataFrame, columns: List):
    for column in columns:
        df[column] = pd.to_datetime(df[column] * 1e9, utc=True)
    return df


def time_delta(t1: pd.Timestamp, t2: np.datetime64):
    if isinstance(t1, np.datetime64):
        t1 = pd.Timestamp(t2).tz_localize("UTC")
    x = t1 - pd.Timestamp(t2).tz_localize("UTC")
    d = x / np.timedelta64(1, "s")
    return d


def get_now() -> pd.Timestamp:
    return pd.Timestamp.now("utc")
