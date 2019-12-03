from bs4 import BeautifulSoup
import requests
import pandas as pd
import sys
import time

first_name = input('First Name: ').lower()
last_name = input('Last Name: ').lower()
ex_id = input('Execution Id: ')

print(f'{ex_id}-{last_name}-{first_name}')

texas_df = pd.read_csv('texas-deathrow-executions.csv', index_col='Execution_id')

base_url = 'https://www.tdcj.texas.gov/death_row/'
last_url = f'dr_info/{last_name}{first_name}last.html'

last_statement = base_url + last_url

last_resp = requests.get(last_statement)
soup = BeautifulSoup(last_resp.text, 'html.parser')

p_tags = soup.find_all('p')


filename = f'{ex_id}-{last_name}-{first_name}-last-statement.txt'

# https://stackoverflow.com/questions/44391671/python3-unicodeencodeerror-charmap-codec-cant-encode-characters-in-position
with open(filename, 'w', encoding='utf-8') as f:
	for p in p_tags:
		f.write(p.text)
		f.write('\n')
		f.write('\n')
f.close()
