import requests
import json
import pandas as pd
from profile_ids import profile_ids, profile_query

url = 'https://api-mumbai.lens.dev/'

profile_data = []
lmt =50
start, end = 0, lmt
while end < len(profile_ids) + lmt:
    current_ids = str(profile_ids[start:end]).replace("'", '"')
    response = requests.post(url, json={'query' : profile_query % (current_ids, lmt)})
    if response.status_code == 200:
        content = json.loads(response.content)
        profile_data.extend(content['data']['profiles']['items'])

        start += lmt
        end += lmt

with open('profile_data.json', 'w') as file:
    file.write(json.dumps(profile_data, indent=4))
