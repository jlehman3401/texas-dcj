from bs4 import BeautifulSoup
import requests
import json
import sys

url = sys.argv[1]

response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

# parsing html for p-tags and establishing dictionary
# need to create handling for unicode / ascii characters
p_tag_list = list()
headers = list()
values = list()

for p in p_tags:
    p_tag_list.append(p.text)
    
for item in p_tag_list:
    if p_tag_list.index(item) % 2 == 0:
        headers.append(item)
    if p_tag_list.index(item) % 2 == 1:
            values.append(item)

offender_dict = dict(zip(headers, values))

with open('offender.txt', 'w') as outfile:
    json.dump(offender_dict, outfile)






