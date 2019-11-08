import asyncio
import math

from .. import utils
from .. import efd

__all__ = ('main')


async def run(opts):
    client = efd.get_client(opts.location)
    cscs = utils.CSC.get_from_file(opts.sut)

    summary_state = 1  # DISABLE
    time_window = 10.0  # seconds
    time_format = '%Y-%m-%dT%H:%M:%S.%f'

    print("###########################################################")
    print("#                     DISABLED Report                     #")
    print("###########################################################")
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

        query = efd.get_base_query(columns=["*"],
                                   csc_name=csc.name,
                                   csc_index=csc.index,
                                   topic_name="logevent_settingsApplied")

        query += " " + efd.get_time_clause(last=True)

        sa_df = await client.query(query)
        try:
            sa_df = utils.convert_timestamps(sa_df, ["private_sndStamp"])
        except KeyError:
            pass

        measurements_df = await client.query("SHOW MEASUREMENTS")
        csc_sa_list = efd.filter_measurements(measurements_df, csc.name, "settingsApplied")
        csc_sa = [x for x in csc_sa_list if x != "logevent_settingsApplied"]

        query = efd.get_base_query(columns=["private_sndStamp",
                                            "appliedSettingsMatchStartIsTrue"],
                                   csc_name=csc.name,
                                   csc_index=csc.index,
                                   topic_name="logevent_appliedSettingsMatchStart")

        query += " " + efd.get_time_clause(last=True)

        asms_df = await client.query(query)
        try:
            asms_df = utils.convert_timestamps(asms_df, ["private_sndStamp"])
        except KeyError:
            pass

        print("-----------------------------------------------------------")
        print(f"CSC: {csc.full_name}")
        try:
            print(f"Time of Summary State: {ss_df.private_sndStamp[0].strftime(time_format)}")
        except AttributeError:
            print(f"summaryState event not present for {csc.full_name}")
        try:
            if sa_df.size:
                delta = utils.time_delta(ss_df.private_sndStamp.values[0],
                                         sa_df.private_sndStamp.values[0])
                if math.fabs(delta) > time_window:
                    print(f"Large delay in settingsApplied publish: {delta:.1f} seconds")
            else:
                print(f"settingsApplied event not present for {csc.full_name}")
        except AttributeError:
            print(f"settingsApplied event not present for {csc.full_name}")
        print(f"Number of CSC specific settingsApplied event: {len(csc_sa)}")
        try:
            if asms_df.size:
                delta = utils.time_delta(ss_df.private_sndStamp.values[0],
                                         asms_df.private_sndStamp.values[0])
                if math.fabs(delta) > time_window:
                    print(f"Large delay in appliedSettingsMatchStart publish: {delta:.1f} seconds")
                asmsit = asms_df.appliedSettingsMatchStartIsTrue.values[0]
                print(f"Applied Settings Match Start Is True: {asmsit}")
            else:
                print(f"appliedSettingsMatchStart event not present for {csc.full_name}")
        except AttributeError:
            print(f"appliedSettingsMatchStart event not present for {csc.full_name}")


def main():
    parser = utils.create_parser()
    args = parser.parse_args()

    asyncio.run(run(args))
