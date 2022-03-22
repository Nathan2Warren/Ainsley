import requests
import json
from queries import profile_query, global_protocol_stats_query
from typing import List, Dict

class GraphQLClient:

    def __init__(self):
        self.url = 'https://api-mumbai.lens.dev'

    def __get_number_of_profile_ids(self):
        response = requests.post(self.url, json={'query' : global_protocol_stats_query})
        if response.status_code == 200:
            content = json.loads(response.content)
            return content['data']['globalProtocolStats']['totalProfiles']
        
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
        return profiles_data
    
    def get_existing_profile_ids(self, num=None):
        profile_data = self._get_data_for_all_profiles()
        _ids = [elem['id'] for elem in profile_data]
        return _ids if num is None else _ids[:num]
        

if __name__ == "__main__":
    client = GraphQLClient()
    profiles = client._get_data_for_all_profiles()
    