import asyncio
import math

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
            print(f"First Offline Detailed State: {ods_df.substate.values[1]}")
            print(f"Second Offline Detailed State: {ods_df.substate.values[0]}")
        except (AttributeError, KeyError):
            print(f"offlineDetailedState event not present")


def main():
    parser = utils.create_parser()
    args = parser.parse_args()

    asyncio.run(run(args))
