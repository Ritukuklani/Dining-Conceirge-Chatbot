import requests
import json
from decimal import Decimal
import datetime

# Define the API key, Define the endpoint, and define the header
API_KEY = 'PUT YOUR KEY HERE'
ENDPOINT = 'https://api.yelp.com/v3/businesses/search'
HEADERS = {'Authorization': 'bearer %s' % API_KEY}

json_list = []

cuisine_types = ['korean'] # put cuisine types here

for cuisine_type in cuisine_types:
    offset = 0
    for i in range(0, 19):
        offset += 50
        PARAMETERS = {
            'term': 'restaurant',
            'location': 'New York',
            'radius': 40000,
            'categories': cuisine_type,
            'limit': 50,
            'offset': offset,
            'sort_by': 'best_match'
        }
        response = requests.get(url=ENDPOINT, params=PARAMETERS, headers=HEADERS)
        business_data = response.json()

        for biz in business_data['businesses']:
            if biz['id'] not in json_list:
                dictionary = "{\"businessId\": " + '"'+biz['id']+'"' + ", \"category\": " + '"'+biz['categories'][0]['alias']+'"' + "}"
                json_list.append(dictionary)


base_str = "curl -XPUT YOUR_END_POINT_URL_OF_ELASTICSEARCH/restaurants/Restaurant/"

count = 0
for res in json_list:
    count += 1
    new_str = base_str + str(count) + " -d '" + str(res) + "' -H 'Content-Type: application/json' ; "
    print(new_str)