# Developed for the LSST System Integration, Test and Commissioning Team.
# This product includes software developed by the LSST Project
# (http://www.lsst.org).
# See the LICENSE file at the top-level directory of this distribution
# for details of code ownership.
#
# Use of this source code is governed by a 3-clause BSD-style
# license that can be found in the LICENSE file.

import asyncio

from lsst_efd_client import EfdClient
import numpy as np

from .. import utils

__all__ = ('main')


async def run(opts):
    efd = EfdClient(opts.location)
    cscs = utils.CSC.get_from_source(opts.sut)

    # Full shutdown goes to OFFLINE state. Normal is to STANDBY state.
    if opts.full_shutdown:
        ss_limit = 4
        if opts.handle_restart:
            ss_limit += 1
        shutdown_start = 0
    else:
        ss_limit = 3
        shutdown_start = 1
    ss_shutdown_order = np.array([4, 5, 1, 2])
    # Give CSCs ten minutes to shutdown
    shutdown_wait_time = 600  # seconds

    print("######################################")
    print("#          Shutdown Report           #")
    print("######################################")
    for csc in cscs:
        ss_df = await efd.select_top_n(csc.efd_topic("logevent_summaryState"),
                                       ["private_sndStamp", "summaryState"],
                                       ss_limit, csc.index)

        ss_df = utils.convert_timestamps(ss_df, ["private_sndStamp"])

        dc_df = await efd.select_top_n(csc.efd_topic("command_disable"),
                                       ["private_sndStamp"],
                                       1, csc.index)

        dc_df = utils.convert_timestamps(dc_df, ["private_sndStamp"])

        print("--------------------------------------")
        print(f"CSC: {csc.full_name}")

        ss_shutdown = ss_df.summaryState.values
        if opts.handle_restart:
            ss_shutdown = ss_shutdown[1:]
        does_shutdown = np.all(ss_shutdown == ss_shutdown_order[shutdown_start:])
        if not does_shutdown:
            print(f"Incorrect Shutdown Order: {ss_shutdown}")
        else:
            print("Shutdown Order Correct!")
            shutdown_time = utils.time_delta(ss_df.private_sndStamp.values[0],
                                             dc_df.private_sndStamp.values[0])
            print(f"Total Shutdown Time: {shutdown_time:.4f} s")
            if shutdown_time > shutdown_wait_time:
                print("Timestamps:")
                for timestamp in ss_df.private_sndStamp.values:
                    print(f"\t{timestamp}")


def main():
    parser = utils.create_parser()

    parser.add_argument('--full-shutdown', dest='full_shutdown', action='store_true',
                        help='Check a full shutdown to OFFLINE, otherwise to STANDBY.')
    parser.add_argument('--handle-restart', dest='handle_restart', action='store_true',
                        help='Shift window due to component automatic restart. Only effects full shutdown')

    args = parser.parse_args()

    asyncio.run(run(args))
