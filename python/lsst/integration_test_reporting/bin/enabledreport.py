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

from .. import utils

__all__ = ('main')


async def run(opts):
    efd = EfdClient(opts.location)
    cscs = utils.CSC.get_from_source(opts.sut)

    summary_state = 2  # ENABLE
    time_format = '%Y-%m-%dT%H:%M:%S.%f'

    print("###########################################################")
    print("#                     ENABLED Report                      #")
    print("###########################################################")
    for csc in cscs:
        ss_df = await efd.select_top_n(csc.efd_topic("logevent_summaryState"),
                                       ["private_sndStamp", "summaryState"],
                                       1, csc.index)

        print("-----------------------------------------------------------")
        print(f"CSC: {csc.full_name}")
        try:
            ss_df = utils.convert_timestamps(ss_df, ["private_sndStamp"])
            if ss_df.summaryState[0] != summary_state:
                print("CSC not in ENABLED State")
            else:
                print("CSC in ENABLED State")
                print(f"Time of Summary State: {ss_df.private_sndStamp[0].strftime(time_format)}")
        except (AttributeError, KeyError):
            print("summaryState event not present")


def main():
    parser = utils.create_parser()
    args = parser.parse_args()

    asyncio.run(run(args))
