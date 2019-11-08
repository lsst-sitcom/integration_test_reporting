import asyncio
import math

from .. import efd
from .. import utils

__all__ = ('main')


async def run(opts):
    client = efd.get_client(opts.location)
    cscs = utils.CSC.get_from_file(opts.sut)

    summary_state = 4  # OFFLINE
    time_window = 10.0  # seconds
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

        query += f" WHERE summaryState={summary_state}"
        query += " " + efd.get_time_clause(last=True)

        ss_df = await client.query(query)
        try:
            ss_df = utils.convert_timestamps(ss_df, ["private_sndStamp"])
        except KeyError:
            pass

        query = efd.get_base_query(columns=["private_sndStamp",
                                            "substate"],
                                   csc_name=csc.name,
                                   csc_index=csc.index,
                                   topic_name="logevent_offlineDetailedState")

        query += efd.get_time_clause(last=True, limit=2)

        ods_df = await client.query(query)
        try:
            ods_df = utils.convert_timestamps(ods_df, ["private_sndStamp"])
        except KeyError:
            pass

        print("---------------------------------------------------------")
        print(f"CSC: {csc.full_name}")
        try:
            print(f"Time of Summary State: {ss_df.private_sndStamp[0].strftime(time_format)}")
        except AttributeError:
            print(f"summaryState event not present for {csc.full_name}")
        try:
            delta = utils.time_delta(ss_df.private_sndStamp.values[0],
                                     ods_df.private_sndStamp.values[0])
            if math.fabs(delta) > time_window:
                print(f"Large delay in offlineDetailedState publish: {delta:.1f} seconds")
        except AttributeError:
            pass
        try:
            print(f"First Offline Detailed State: {ods_df.substate.values[1]}")
            print(f"Second Offline Detailed State: {ods_df.substate.values[0]}")
        except AttributeError:
            print(f"offlineDetailedState event not present for {csc.full_name}")


def main():
    parser = utils.create_parser()
    args = parser.parse_args()

    asyncio.run(run(args))
