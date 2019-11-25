# Developed for the LSST System Integration, Test and Commissioning Team.
# This product includes software developed by the LSST Project
# (http://www.lsst.org).
# See the LICENSE file at the top-level directory of this distribution
# for details of code ownership.
#
# Use of this source code is governed by a 3-clause BSD-style
# license that can be found in the LICENSE file.

import collections
from datetime import datetime, timedelta
import os

import aioinflux

Token = collections.namedtuple("Token", ["uname", "pwd"])

AVAILABLE_EFDS = {"summit": "summit-influxdb-efd.lsst.codes",
                  "tucson": "test-influxdb-efd.lsst.codes"}

QUERY_BASE = "SELECT {columns} FROM \"efd\".\"autogen\".\"lsst.sal.{csc}.{topic}\""
QUERY_TIME_RANGE = "{time_column} >= \'{start}\' AND {time_column} <= \'{end}\'"
QUERY_LAST_TIME = "ORDER BY {time_column} DESC LIMIT {limit}"


def get_client(which_efd, token_file=None):
    efd_url = AVAILABLE_EFDS[which_efd]
    token = get_token(which_efd, token_file)
    return aioinflux.InfluxDBClient(host=efd_url,
                                    port=443,
                                    ssl=True,
                                    username=token.uname,
                                    password=token.pwd,
                                    db='efd',
                                    output="dataframe")


def get_token(which_efd, token_file=None):
    if token_file is None:
        token_file = os.path.join(os.path.expanduser("~/"), f".{which_efd}_efd")
    with open(token_file, 'r') as fd:
        uname = fd.readline().strip()  # Can't hurt to be paranoid
        pwd = fd.readline().strip()
    return Token(uname, pwd)


def get_base_query(columns, csc_name, topic_name, csc_index=0):
    query_columns = ",".join(columns)
    if csc_index and columns[0] != "*":
        query_columns += f",{csc_name}ID"

    query = QUERY_BASE.format(columns=query_columns, csc=csc_name, topic=topic_name)
    if csc_index:
        query += f" WHERE {csc_name}ID={csc_index}"

    return query


def get_time_clause(time_column="time", last=False, limit=1, date_range=None):
    query = ""
    if last:
        query += QUERY_LAST_TIME.format(time_column=time_column, limit=limit)
    else:
        if date_range is None:
            last = datetime.utcnow()
            first = last - timedelta(1, "day")
        else:
            first, last = date_range

        query += QUERY_TIME_RANGE.format(time_column=time_column, start=first, end=last)

    return query


def filter_measurements(measurements, csc_name, topic_name):
    csc_filtered = [measurement.split('.')[-1] for measurement in measurements['name'].values
                    if csc_name in measurement]
    topic_filtered = [topic for topic in csc_filtered if topic_name in topic]
    return topic_filtered
