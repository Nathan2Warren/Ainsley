import json
import requests

from .queries import (
    global_protocol_stats_query,
    profile_query,
    publications_query,
    profile_revenue_query
)
class GraphQLClient:

    url = 'https://api-mumbai.lens.dev'

    @classmethod
    def __get_number_of_profile_ids(cls):
        response = requests.post(
            cls.url, json={'query' : global_protocol_stats_query}
        )
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
    def _get_data_for_all_profiles(cls, limit: int=50):
        profiles_data = []
        prev, _next = None, "0"
        profile_ids = cls.__get_valid_profile_ids()
        while prev != _next:
            variables = json.dumps({
                        "request": {
                            "profileIds": profile_ids,
                            "limit": limit,
                            "cursor": _next
                        }
                    })
            response = requests.post(cls.url, json={'query' : profile_query, 'variables' : variables})
            if response.status_code == 200:
                content = json.loads(response.content)
                profiles = content["data"]["profiles"]
                profiles_data.extend(profiles["items"])

                prev = profiles["pageInfo"]["prev"]
                _next = profiles["pageInfo"]["next"]
            else:
                raise Exception(response.content.decode())
        return profiles_data
    
    @classmethod
    def get_existing_profile_ids(cls, num=None):
        profile_data = cls._get_data_for_all_profiles()
        _ids = [elem['id'] for elem in profile_data]
        return _ids if num is None else _ids[:num]

    @classmethod
    def get_profile_revenues(cls, profile_ids):
        if isinstance(profile_ids, str):
            profile_ids = [profile_ids]
        query_payload = ",".join([profile_revenue_query.format(f'prorev_{pid}', pid) for pid in profile_ids])
        query_string = f'query Items {{{query_payload}}}'
        response = requests.post(cls.url, json={'query' : query_string}) # , 'variables' : variables
        if response.status_code == 200:
            content = json.loads(response.content)
            profile_revenues = content['data']
            profile_revs = [v['items'] for k, v in profile_revenues.items() if len(v['items']) > 0]
            return profile_revs
        else:
            raise Exception(response.content.decode())
    
    @classmethod
    def get_publication_revenue(cls, publication_id: str):
        return {
                "data": {
                    "publicationRevenue": {
                    "publication": {
                        "id": "0x12-0x05"
                    },
                    "earnings": {
                        "asset": {
                            "name": "Wrapped Matic",
                            "symbol": "WMATIC",
                            "decimals": 18,
                            "address": "0x9c3C9283D3e44854697Cd22D3Faa240Cfb032889"
                        },
                        "value": "0.0001"
                    },
                    "protocolFee": 0
                    }
                }
            }

    @classmethod
    def get_publications(cls, profile_id: str, limit: int=50):
        publications = []
        prev, _next = None, "0"
        while prev != _next:
            variables = json.dumps({
                        "request": {
                            "profileId": profile_id,
                            "publicationTypes": ["POST", "COMMENT", "MIRROR"],
                            "limit": limit,
                            "cursor" : _next
                        }
                    })
            response = requests.post(cls.url, json={'query' : publications_query, 'variables' : variables})
            if response.status_code == 200:
                content = json.loads(response.content)
                publications.extend(content['data']['publications']['items'])
                
                page_info = content['data']['publications']["pageInfo"]
                prev, _next = page_info['prev'], page_info['next']
            else:
                raise Exception(response.content.decode())
        return publications

    
if __name__ == "__main__":
    profile_ids = GraphQLClient.get_existing_profile_ids()
    profile_revenues = GraphQLClient.get_profile_revenues(profile_ids)
