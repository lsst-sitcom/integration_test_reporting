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

from .. import utils

__all__ = ('main')


async def run(opts):
    efd = EfdClient(opts.location)
    cscs = utils.CSC.get_from_source(opts.sut)

    summary_state = 5  # STANDBY
    time_window = 10.0  # seconds
    time_format = '%Y-%m-%dT%H:%M:%S.%f'

    print("#############################################################")
    print("#                      STANDBY Report                       #")
    print("#############################################################")
    for csc in cscs:
        ss_df = await efd.select_top_n(csc.efd_topic("logevent_summaryState"),
                                       ["private_sndStamp", "summaryState"],
                                       1, csc.index)

        sv_df = await efd.select_top_n(csc.efd_topic("logevent_settingVersions"),
                                       ["private_sndStamp",
                                        "recommendedSettingsLabels",
                                        "recommendedSettingsVersion"],
                                       1, csc.index)

        sov_df = await efd.select_top_n(csc.efd_topic("logevent_softwareVersions"),
                                        "*",
                                        2, csc.index)

        print("-------------------------------------------------------------")
        print(f"CSC: {csc.full_name}")
        try:
            ss_df = utils.convert_timestamps(ss_df, ["private_sndStamp"])
            if ss_df.summaryState[0] != summary_state:
                print("CSC not in STANDBY State")
            else:
                print("CSC in STANDBY State")
                print(f"Time of Summary State: {ss_df.private_sndStamp[0].strftime(time_format)}")
        except (AttributeError, KeyError):
            print(f"summaryState event not present")
        try:
            sov_df = utils.convert_timestamps(sov_df, ["private_sndStamp"])
            print("softwareVersions present")
        except (AttributeError, KeyError):
            print("softwareVersions event not present")
        if csc.name not in utils.NON_CONFIG_CSCS:
            try:
                sv_df = utils.convert_timestamps(sv_df, ["private_sndStamp"])
                if sv_df.size:
                    delta = utils.time_delta(ss_df.private_sndStamp.values[0],
                                             sv_df.private_sndStamp.values[0])
                    if math.fabs(delta) > time_window:
                        print(f"Large delay in settingVersions publish: {delta:.1f} seconds")
                    rsl = sv_df.recommendedSettingsLabels.values[0]
                    rsv = sv_df.recommendedSettingsVersion.values[0]
                    print(f"Recommended Settings Labels: {rsl}")
                    print(f"Recommended Settings Version: {rsv}")
                else:
                    print(f"settingVersions event not present")
            except (AttributeError, KeyError):
                print(f"settingVersions event not present")


def main():
    parser = utils.create_parser()
    args = parser.parse_args()

    asyncio.run(run(args))
