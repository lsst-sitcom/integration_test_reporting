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

    summary_state = 1  # DISABLE
    time_window = 10.0  # seconds
    time_format = '%Y-%m-%dT%H:%M:%S.%f'

    print("###########################################################")
    print("#                     DISABLED Report                     #")
    print("###########################################################")

    if opts.index_auto:
        top_n = 3
    else:
        top_n = 1

    for csc in cscs:
        ss_df = await efd.select_top_n(csc.efd_topic("logevent_summaryState"),
                                       ["private_sndStamp", "summaryState"],
                                       top_n, csc.index)

        if opts.index_auto:
            ss_df = ss_df.iloc[[1]]

        sa_df = await efd.select_top_n(csc.efd_topic("logevent_settingsApplied"),
                                       "*",
                                       1, csc.index)

        if not opts.index_auto:
            sc_df = await efd.select_top_n(csc.efd_topic("command_start"),
                                           "private_sndStamp",
                                           1, csc.index)
            sc_df = utils.convert_timestamps(sc_df, ["private_sndStamp"])
        else:
            sc_df = None

        measurements = await efd.get_topics()
        csc_sa_list = utils.filter_measurements(measurements, csc.name,
                                                csc.efd_topic("settingsApplied"))
        csc_sa = [x for x in csc_sa_list if x != "logevent_settingsApplied"]

        csc_sa_dict = {}
        for event in csc_sa:
            csc_sa_dict[event] = await efd.select_top_n(csc.efd_topic(event),
                                                        "*",
                                                        1, csc.index)

        asms_df = await efd.select_top_n(csc.efd_topic("logevent_appliedSettingsMatchStart"),
                                         ["private_sndStamp",
                                          "appliedSettingsMatchStartIsTrue"],
                                         1, csc.index)

        print("-----------------------------------------------------------")
        print(f"CSC: {csc.full_name}")
        try:
            ss_df = utils.convert_timestamps(ss_df, ["private_sndStamp"])
            if ss_df.summaryState[0] != summary_state:
                print("CSC not in DISABLED State")
            else:
                print("CSC in DISABLED State")
                print(f"Time of Summary State: {ss_df.private_sndStamp[0].strftime(time_format)}")
        except (AttributeError, KeyError):
            print("summaryState event not present")
        if csc.name not in utils.NON_CONFIG_CSCS:
            try:
                sa_df = utils.convert_timestamps(sa_df, ["private_sndStamp"])
                if sa_df.size:
                    delta = utils.time_delta(ss_df.private_sndStamp.values[0],
                                             sa_df.private_sndStamp.values[0])
                    if math.fabs(delta) > time_window:
                        print(f"Large delay in settingsApplied publish: {delta:.1f} seconds")
                        print(f"summaryState Time:    {ss_df.private_sndStamp.values[0]}")
                        print(f"settingsApplied Time: {sa_df.private_sndStamp.values[0]}")
                else:
                    print("settingsApplied event not present")
            except (AttributeError, KeyError):
                print("settingsApplied event not present")
            print(f"Number of CSC specific settingsApplied events: {len(csc_sa)}")
            for key, value in csc_sa_dict.items():
                try:
                    if value.shape[0] == 1:
                        print(f"{key} present")
                        value = utils.convert_timestamps(value, ["private_sndStamp"])
                        delta = utils.time_delta(ss_df.private_sndStamp.values[0],
                                                 value.private_sndStamp.values[0])
                    if math.fabs(delta) > time_window:
                        print(f"Large delay in {key} publish: {delta:.1f} seconds")
                        print(f"summaryState Time:\t{ss_df.private_sndStamp.values[0]}")
                        print(f"{key} Time:\t{value.private_sndStamp.values[0]}")
                except (AttributeError, KeyError):
                    print(f"{key} not present")
            try:
                asms_df = utils.convert_timestamps(asms_df, ["private_sndStamp"])
                if asms_df.size:
                    delta = utils.time_delta(ss_df.private_sndStamp.values[0],
                                             asms_df.private_sndStamp.values[0])
                    if math.fabs(delta) > time_window:
                        print(f"Large delay in appliedSettingsMatchStart publish: {delta:.1f} seconds")
                        print(f"summaryState Time:              {ss_df.private_sndStamp.values[0]}")
                        print(f"appliedSettingsMatchStart Time: {asms_df.private_sndStamp.values[0]}")
                    asmsit = asms_df.appliedSettingsMatchStartIsTrue.values[0]
                    print(f"Applied Settings Match Start Is True: {asmsit}")
                else:
                    print("appliedSettingsMatchStart event not present")
            except (AttributeError, KeyError):
                print("appliedSettingsMatchStart event not present")


def main():
    parser = utils.create_parser()
    args = parser.parse_args()

    asyncio.run(run(args))
