# Developed for the LSST System Integration, Test and Commissioning Team.
# This product includes software developed by the LSST Project
# (http://www.lsst.org).
# See the LICENSE file at the top-level directory of this distribution
# for details of code ownership.
#
# Use of this source code is governed by a 3-clause BSD-style
# license that can be found in the LICENSE file.

import asyncio
import math

import numpy as np

from .. import efd
from .. import utils

__all__ = ('main')


async def run(opts):
    client = efd.get_client(opts.location)
    cscs = utils.CSC.get_from_file(opts.sut)

    summary_state = 4  # OFFLINE
    time_window = 120.0  # seconds
    time_format = '%Y-%m-%dT%H:%M:%S.%f'

    print("#########################################################")
    print("#                    OFFLINE Report                     #")
    print("#########################################################")
    for csc in cscs:
        if "Camera" not in csc.name or "Generic" in csc.name:
            continue
        query = efd.get_base_query(columns=["private_sndStamp",
                                            "summaryState"],
                                   csc_name=csc.name,
                                   csc_index=csc.index,
                                   topic_name="logevent_summaryState")

        query += " " + efd.get_time_clause(last=True)

        ss_df = await client.query(query)

        query = efd.get_base_query(columns=["private_sndStamp",
                                            "substate"],
                                   csc_name=csc.name,
                                   csc_index=csc.index,
                                   topic_name="logevent_offlineDetailedState")

        query += efd.get_time_clause(last=True, limit=2)

        ods_df = await client.query(query)

        query = efd.get_base_query(columns=["*"],
                                   csc_name=csc.name,
                                   csc_index=csc.index,
                                   topic_name="logevent_softwareVersions")

        query += efd.get_time_clause(last=True, limit=2)

        sv_df = await client.query(query)

        print("---------------------------------------------------------")
        print(f"CSC: {csc.full_name}")
        try:
            ss_df = utils.convert_timestamps(ss_df, ["private_sndStamp"])
            if ss_df.summaryState[0] != summary_state:
                print("CSC not in OFFLINE State")
            else:
                print("CSC in OFFLINE State")
                print(f"Time of Summary State: {ss_df.private_sndStamp[0].strftime(time_format)}")
        except (AttributeError, KeyError):
            print(f"summaryState event not present")
        try:
            ods_df = utils.convert_timestamps(ods_df, ["private_sndStamp"])
            delta = utils.time_delta(ss_df.private_sndStamp.values[0],
                                     ods_df.private_sndStamp.values[0])
            if math.fabs(delta) > time_window:
                print(f"Large delay in offlineDetailedState publish: {delta:.1f} seconds")

            substate_order = np.array([1, 2])
            ss_order = ods_df.substate.values
            does_transition = np.all(ss_order == substate_order)
            if does_transition:
                print("Offline Detailed States Order Correct!")
            else:
                print(f"Incorrect Offline Detailed States Order: {ss_order}")
        except (AttributeError, KeyError):
            print(f"offlineDetailedState event not present")
        try:
            sv_df = utils.convert_timestamps(sv_df, ["private_sndStamp"])
            print("softwareVersions present")
        except (AttributeError, KeyError):
            print("softwareVersions event not present")


def main():
    parser = utils.create_parser()
    args = parser.parse_args()

    asyncio.run(run(args))
