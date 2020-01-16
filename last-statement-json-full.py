from bs4 import BeautifulSoup
import json
import requests
import pandas as pd
import sys
import time


texas_df = pd.read_csv('texas-deathrow-executions.csv', index_col='Execution_id')

base_url = 'https://www.tdcj.texas.gov/death_row/'

#for i in range(len(texas_df)):
#for i in range(31, len(texas_df)):
for i in range(70,80):
	tdcj_id = texas_df.index[i]
	tdcj_name = texas_df.iloc[i][2]
	tdcj_no = texas_df.iloc[i][4]
	last_url = texas_df.iloc[i][8]
	last_statement = base_url + last_url

	last_resp = requests.get(last_statement)


	soup = BeautifulSoup(last_resp.text, 'html.parser')

	p_tags = soup.find_all('p')


	p_tag_list = list()
	headers = list()
	values = list()

	for p in p_tags:
		if len(p.text) > 1:
			p_tag_list.append(p.text)

	# if no last statement
	if len(p_tag_list) <= 2:
		with open(f'No.{tdcj_id}-{tdcj_name}-{tdcj_no}-last-statement.txt', 'w') as outfile:
			outfile.write("No last statement")
	else:

	    # ===== headers =====
  
		date_header = [p_tag_list[0].strip()]
		offender_header = [p_tag_list[2].strip()]
		statement_header = [p_tag_list[4].strip()]

		headers = date_header + offender_header + ['TDCJ_num:'] + statement_header

		# ===== values =====

		name_num = p_tag_list[3].split('#')

		if "-" in name_num:
			name_num = name_num.split('-')[0].strip()

		statement_body = p_tag_list[5:]
		clean_statement = []

		for line in statement_body:
			line = line.replace(u'\u2019',"'")
			clean_statement.append(line)


		date_value = [p_tag_list[1].strip()]

		if len(name_num) > 1:
			offender_value = [name_num[0].strip()]
			id_value = [name_num[1].strip()]
		else:
			offender_value = [name_num[0].strip()]
			id_value = ["NA"]

		values = date_value + offender_value + id_value + clean_statement

		offender_dict = dict(zip(headers, values))

		# ========== 	writing to file	 ==========
		with open(f'No.{tdcj_id}-{id_value[0]}-{offender_value[0]}-last-statement.txt', 'w') as outfile:
		    json.dump(offender_dict, outfile, indent=4)

		print(f'offender {tdcj_id} {id_value[0]} statement gathered')

		time.sleep(2)
