from bs4 import BeautifulSoup
import requests
import pandas as pd
import sys
import time

texas_df = pd.read_csv('texas-deathrow-executions.csv', index_col='Execution_id')

base = 'https://www.tdcj.texas.gov/death_row/'

for i in range(len(texas_df)):
	last_url = texas_df.iloc[i][8]
	last_statement = base_url + last_url

	last_resp = requests.get(last_statement)
	soup = BeautifulSoup(last_resp.text, 'html.parser')

	p_tags = soup.find_all('p')

	ex_id = texas_df.index[i]
	last_name = texas_df.iloc[i][0]
	first_name = texas_df.iloc[i][1]

	filename = f'{ex_id}-{last_name}-{first_name}-last-statement.txt'

	with open(filename, 'w') as f:
		for p in p_tags:
			f.write(p.text)
	f.close()

	print(f'offender {exid} statement gathered')

	time.sleep(2)