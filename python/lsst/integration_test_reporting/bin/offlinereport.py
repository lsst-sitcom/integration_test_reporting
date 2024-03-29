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

from lsst_efd_client import EfdClient
import numpy as np

from .. import utils

__all__ = ('main')


async def run(opts):
    efd = EfdClient(opts.location)
    cscs = utils.CSC.get_from_list(",".join(utils.OFFLINE_CSCS))

    summary_state = 4  # OFFLINE
    time_window = 120.0  # seconds
    time_format = '%Y-%m-%dT%H:%M:%S.%f'

    print("#########################################################")
    print("#                    OFFLINE Report                     #")
    print("#########################################################")
    for csc in cscs:
        ss_df = await efd.select_top_n(csc.efd_topic("logevent_summaryState"),
                                       ["private_sndStamp", "summaryState"],
                                       1, csc.index)
        is_camera = False
        ods_topic = None
        if "Camera" in csc.name:
            ods_topic = "offlineDetailedState"
            ods_df = await efd.select_top_n(csc.efd_topic(f"logevent_{ods_topic}"),
                                            ["private_sndStamp", "substate"],
                                            2, csc.index)
            is_camera = True
        else:
            ods_topic = "commandableByDDS"
            ods_df = await efd.select_top_n(csc.efd_topic(f"logevent_{ods_topic}"),
                                            ["private_sndStamp", "state"],
                                            1, csc.index)

        sv_df = await efd.select_top_n(csc.efd_topic("logevent_softwareVersions"),
                                       "*",
                                       1, csc.index)

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
            print("summaryState event not present")
        try:
            ods_df = utils.convert_timestamps(ods_df, ["private_sndStamp"])
            delta = utils.time_delta(ods_df.private_sndStamp.values[0],
                                     ss_df.private_sndStamp.values[0])
            if math.fabs(delta) > time_window:
                print(f"Large delay in {ods_topic} publish: {delta:.1f} seconds")

            if is_camera:
                substate_order = np.array([1, 2])
                ss_order = ods_df.substate.values
                does_transition = np.all(ss_order == substate_order)
                if does_transition:
                    print("Offline Detailed States Order Correct!")
                else:
                    print(f"Incorrect Offline Detailed States Order: {ss_order}")
            else:
                if bool(ods_df.state.values[0]):
                    print("CSC Ready for DDS Commands!")
                else:
                    print("CSC NOT Ready for DDS Commands!")
        except (AttributeError, KeyError):
            print(f"{ods_topic} event not present")
        try:
            sv_df = utils.convert_timestamps(sv_df, ["private_sndStamp"])
            delta = utils.time_delta(utils.get_now(), sv_df.private_sndStamp.values[0])
            print("softwareVersions present")
            print(f"Publication time gap: {delta:.1f} seconds")
            utils.check_correct_value(opts.xml, sv_df["xmlVersion"][0], "XML version")
            utils.check_correct_value(opts.sal, sv_df["salVersion"][0], "SAL version")
        except (AttributeError, KeyError):
            print("softwareVersions event not present")


def main():
    parser = utils.create_parser()
    args = parser.parse_args()

    asyncio.run(run(args))
