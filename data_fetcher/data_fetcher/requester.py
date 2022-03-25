import json
import time
from datetime import datetime
from typing import Union

import requests
from pandas import json_normalize

from .queries import (
    global_protocol_stats_query,
    profile_query,
    profile_revenue_query,
    profile_timeseries,
    publication_revenue_query,
    publications_query,
)


class GraphQLClient:

    url = "https://api-mumbai.lens.dev"

    @classmethod
    def __get_number_of_profile_ids(cls):
        response = requests.post(cls.url, json={"query": global_protocol_stats_query})
        if response.status_code == 200:
            content = json.loads(response.content)
            return content["data"]["globalProtocolStats"]["totalProfiles"]
        else:
            raise Exception(response.content.decode())

    @classmethod
    def __get_valid_profile_ids(cls):
        profile_count = cls.__get_number_of_profile_ids()
        profile_ids = ["{0:02x}".format(i) for i in range(profile_count + 1)]
        profile_ids = map(
            lambda x: x.zfill(len(x) + 1) if len(x) % 2 != 0 else x,
            profile_ids,
        )
        profile_ids = [f"0x{n}" for n in profile_ids]
        return profile_ids

    @classmethod
    def _get_data_for_all_profiles(cls, limit: int = 50, normalize: bool = False):
        profiles_data = []
        prev, _next = None, "0"
        profile_ids = cls.__get_valid_profile_ids()
        while prev != _next:
            variables = json.dumps({"request": {"profileIds": profile_ids, "limit": limit, "cursor": _next}})
            response = requests.post(cls.url, json={"query": profile_query, "variables": variables})
            if response.status_code == 200:
                content = json.loads(response.content)
                profiles = content["data"]["profiles"]
                profiles_data.extend(profiles["items"])

                prev = profiles["pageInfo"]["prev"]
                _next = profiles["pageInfo"]["next"]
            else:
                raise Exception(response.content.decode())
        return json_normalize(profiles_data) if normalize else profiles_data

    @classmethod
    def get_existing_profile_ids(cls, num=None):
        profile_data = cls._get_data_for_all_profiles()
        _ids = [elem["id"] for elem in profile_data]
        return _ids if num is None else _ids[:num]

    @classmethod
    def get_profile_revenues(cls, profile_ids: Union[list, str]):
        if isinstance(profile_ids, str):
            profile_ids = [profile_ids]
        query_payload = ",".join([profile_revenue_query.format(f"prorev_{pid}", pid) for pid in profile_ids])
        query_string = f"query Items {{{query_payload}}}"
        response = requests.post(cls.url, json={"query": query_string})
        if response.status_code == 200:
            content = json.loads(response.content)
            profile_revenues = content["data"]

            data = []
            for k, v in profile_revenues.items():
                if len(v["items"]) > 0:
                    data.extend(v["items"])
            df = json_normalize(data)
            df["profile_id"] = df["publication.id"].apply(lambda x: x.split("-")[0])
            return df
        else:
            raise Exception(response.content.decode())

    @classmethod
    def get_timeseries(cls, start, end):
        start_unix = convert_datetime_to_unix(start)
        end_unix = convert_datetime_to_unix(end)
        query = profile_timeseries.format(start_unix, end_unix)
        # query = ",".join([profile_timeseries.format(start_unix, end_unix) for start_unix, end_unix in zip(start_unix, end_unix)])
        response = requests.post(cls.url, json={"query": query})
        if response.status_code == 200:
            content = json.loads(response.content)
            df = json_normalize(content)
            df["start"] = start
            df["end"] = end
            return df
        else:
            raise Exception(response.content.decode())

    @classmethod
    def get_publication_revenue(cls, publication_id: str):
        variables = json.dumps({"request": {"publicationId": publication_id}})
        response = requests.post(cls.url, json={"query": publication_revenue_query, "variables": variables})
        if response.status_code == 200:
            content = json.loads(response.content)
            revenue_data = content["data"]["publicationRevenue"]
            return json_normalize(revenue_data)
        else:
            raise Exception(response.content.decode())

    @classmethod
    def get_publications_by_profile(cls, profile_id: str, limit: int = 50):
        publications = []
        prev, _next = None, "0"
        while prev != _next:
            variables = json.dumps(
                {
                    "request": {
                        "profileId": profile_id,
                        "publicationTypes": ["POST", "COMMENT", "MIRROR"],
                        "limit": limit,
                        "cursor": _next,
                    }
                }
            )
            response = requests.post(cls.url, json={"query": publications_query, "variables": variables})
            if response.status_code == 200:
                content = json.loads(response.content)
                publications.extend(content["data"]["publications"]["items"])

                page_info = content["data"]["publications"]["pageInfo"]
                prev, _next = page_info["prev"], page_info["next"]
            else:
                raise Exception(response.content.decode())
        return json_normalize(publications)


def convert_datetime_to_unix(d: str):
    unix_timestamp = int(time.mktime(datetime.fromisoformat(d).timetuple()))
    # unix_timestamp_list =[int(time.mktime(datetime.fromisoformat(x).timetuple())) for x in d]
    return unix_timestamp
