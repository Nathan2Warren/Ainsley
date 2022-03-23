import requests
import json
from queries import profile_query, global_protocol_stats_query, publications_query

class GraphQLClient:

    def __init__(self):
        self.url = 'https://api-mumbai.lens.dev'

    def __get_number_of_profile_ids(self):
        response = requests.post(self.url, json={'query' : global_protocol_stats_query})
        if response.status_code == 200:
            content = json.loads(response.content)
            return content['data']['globalProtocolStats']['totalProfiles']
        else:
            raise Exception(response.content)
        
    def __get_valid_profile_ids(self):
        profile_count = self.__get_number_of_profile_ids()
        profile_ids = ["{0:02x}".format(i) for i in range(profile_count + 1)]
        profile_ids = map(lambda x: x.zfill(len(x)+1) if len(x)  % 2 != 0 else x, profile_ids)
        profile_ids = [f'0x{n}' for n in profile_ids]
        return profile_ids
        
    def _get_data_for_all_profiles(self, limit: int=50):
        profiles_data = []
        prev, _next = None, "0"
        profile_ids = self.__get_valid_profile_ids()
        while prev != _next:
            variables = json.dumps({
                        "request": {
                            "profileIds": profile_ids,
                            "limit": limit,
                            "cursor": _next
                        }
                    })
            response = requests.post(self.url, json={'query' : profile_query, 'variables' : variables})
            if response.status_code == 200:
                content = json.loads(response.content)
                profiles = content['data']['profiles']
                profiles_data.extend(profiles['items'])
                
                prev = profiles['pageInfo']['prev']
                _next = profiles['pageInfo']['next']
            else:
                raise Exception(response.content)
        return profiles_data
    
    def get_existing_profile_ids(self, num=None):
        profile_data = self._get_data_for_all_profiles()
        _ids = [elem['id'] for elem in profile_data]
        return _ids if num is None else _ids[:num]

    def get_profile_revenue(self, profile_id: str):
        return {
                "data": {
                    "profileRevenue": {
                    "items": [
                        {
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
                    ],
                    "pageInfo": {
                        "next": "{\"entityIdentifier\":\"0x12-0x05\",\"timestamp\":1647701744,\"cursorDirection\":\"AFTER\"}",
                        "prev": "{\"entityIdentifier\":\"0x12-0x05\",\"timestamp\":1647701744,\"cursorDirection\":\"BEFORE\"}",
                        "totalCount": 1
                        }
                    }
                }
            }
    
    def get_publication_revenue(self, publication_id: str):
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

    def get_publications(self, profile_id: str, limit: int=50):
        variables = json.dumps({
                    "request": {
                        "profileId": profile_id,
                        "publicationTypes": ["POST", "COMMENT", "MIRROR"],
                        "limit": limit
                    }
                })
        response = requests.post(self.url, json={'query' : publications_query, 'variables' : variables})
        if response.status_code == 200:
            content = json.loads(response.content)
            publications = content['data']['publications']['items']
            return publications
        else:
            raise Exception(response.content)
        
    
if __name__ == "__main__":
    client = GraphQLClient()
    # profiles = client._get_data_for_all_profiles()
    publications = client.get_publications(profile_id='0x3b')
    
