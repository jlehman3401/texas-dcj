from bs4 import BeautifulSoup
import requests
import pandas as pd
import sys
import time

texas_df = pd.read_csv('texas-deathrow-executions.csv', index_col='Execution_id')

base_url = 'https://www.tdcj.texas.gov/death_row/'

for i in range(len(texas_df)):
	last_url = texas_df.iloc[i][8]
	last_statement = base_url + last_url

	last_resp = requests.get(last_statement)
	soup = BeautifulSoup(last_resp.text, 'html.parser')

	p_tags = soup.find_all('p')


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

    offender_df = pd.DataFrame(offender_dict)

	ex_id = texas_df.index[i]
	last_name = texas_df.iloc[i][0]
	first_name = texas_df.iloc[i][1]

	offender_df.to_csv(f'{ex_id}-{last_name}-{first_name}-last-statement.csv', header=True, index=False)

	print(f'offender {ex_id} statement gathered')

	time.sleep(2)