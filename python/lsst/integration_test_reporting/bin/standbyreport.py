import asyncio
import math

from .. import utils
from .. import efd

__all__ = ('main')


async def run(opts):
    client = efd.get_client(opts.location)
    cscs = utils.CSC.get_from_file(opts.sut)

    summary_state = 5  # STANDBY
    time_window = 10.0  # seconds
    time_format = '%Y-%m-%dT%H:%M:%S.%f'

    print("#############################################################")
    print("#                      STANDBY Report                       #")
    print("#############################################################")
    for csc in cscs:
        query = efd.get_base_query(columns=["private_sndStamp",
                                            "summaryState"],
                                   csc_name=csc.name,
                                   csc_index=csc.index,
                                   topic_name="logevent_summaryState")

        # Handle indexed components from base query
        if "WHERE" not in query:
            query += " WHERE"
        else:
            query += " AND"
        query += f" summaryState={summary_state}"
        query += " " + efd.get_time_clause(last=True)

        ss_df = await client.query(query)
        ss_df = utils.convert_timestamps(ss_df, ["private_sndStamp"])

        query = efd.get_base_query(columns=["private_sndStamp",
                                            "recommendedSettingsLabels",
                                            "recommendedSettingsVersion"],
                                   csc_name=csc.name,
                                   csc_index=csc.index,
                                   topic_name="logevent_settingVersions")

        query += " " + efd.get_time_clause(last=True)

        sv_df = await client.query(query)
        try:
            sv_df = utils.convert_timestamps(sv_df, ["private_sndStamp"])
        except KeyError:
            # CSC not publishing settingsVersion topic
            pass

        print("-------------------------------------------------------------")
        print(f"CSC: {csc.full_name}")
        try:
            print(f"Time of Summary State: {ss_df.private_sndStamp[0].strftime(time_format)}")
        except AttributeError:
            print(f"summaryState event not present for {csc.full_name}")
        try:
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
                print(f"settingVersions event not present for {csc.full_name}")
        except AttributeError:
            print(f"settingVersions event not present for {csc.full_name}")


def main():
    parser = utils.create_parser()
    args = parser.parse_args()

    asyncio.run(run(args))
