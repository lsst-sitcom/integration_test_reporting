from typing import List

import numpy as np
import pandas as pd

__all__ = ('convert_timestamps', 'time_delta')


def convert_timestamps(df: pd.DataFrame, columns: List):
    for column in columns:
        df[column] = pd.to_datetime(df[column] * 1e9, utc=True)
    return df


def time_delta(t1: pd.Timestamp, t2: pd.Timestamp):
    return (t1 - t2) / np.timedelta64(1, 's')
