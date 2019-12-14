from bs4 import BeautifulSoup
import requests
import json
import sys

url = sys.argv[1]

response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

p_tags = soup.find_all('p')

p_tag_list = list()
headers = list()
values = list()

for p in p_tags:
    p_tag_list.append(p.text)
    
    
name_num = p_tag_list[3].split('#')

headers = [p_tag_list[0].strip()] + [p_tag_list[2].strip()] + ['TDCJ_num:'] + [p_tag_list[4]]

values = [p_tag_list[1]] + [name_num[0].strip()] + [name_num[1]] + p_tag_list[5:]


offender_dict = dict(zip(headers, values))

with open('offender-2.txt', 'w') as outfile:
    json.dump(offender_dict, outfile, indent=4)






