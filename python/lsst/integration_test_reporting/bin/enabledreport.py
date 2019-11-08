import asyncio

from .. import efd
from .. import utils

__all__ = ('main')


async def run(opts):
    client = efd.get_client(opts.location)
    cscs = utils.CSC.get_from_file(opts.sut)

    summary_state = 2  # ENABLE
    time_format = '%Y-%m-%dT%H:%M:%S.%f'

    print("###########################################################")
    print("#                     ENABLED Report                      #")
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

        print("-----------------------------------------------------------")
        print(f"CSC: {csc.full_name}")
        try:
            print(f"Time of Summary State: {ss_df.private_sndStamp[0].strftime(time_format)}")
        except AttributeError:
            print(f"summaryState event not present for {csc.full_name}")


def main():
    parser = utils.create_parser()
    args = parser.parse_args()

    asyncio.run(run(args))
