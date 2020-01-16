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
    
# ===== headers =====
    
date_header = [p_tag_list[0].strip()]
offender_header = [p_tag_list[2].strip()]
statement_header = [p_tag_list[4]]

headers = date_header + offender_header + ['TDCJ_num:'] + statement_header

# ===== values =====

name_num = p_tag_list[3].split('#')

statement_body = p_tag_list[5:]
clean_statement = []

for line in statement_body:
	line = line.replace(u'\u2019',"'")
	clean_statement.append(line)


date_value = [p_tag_list[1]]
offender_value = [name_num[0].strip()]
id_value = [name_num[1]]

values = date_value + offender_value + id_value + clean_statement


offender_dict = dict(zip(headers, values))

with open(f'{id_value}-{offender_value}-last-statement.txt', 'w') as outfile:
    json.dump(offender_dict, outfile, indent=4)

