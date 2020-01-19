from bs4 import BeautifulSoup
import argparse
import pandas as pd
import requests
import json
import sys
import time

parser = argparse.ArgumentParser()

group = parser.add_mutually_exclusive_group(required=True)

group.add_argument('--name', type=str, default='index_given', help='Enter the first name of the offender followed by last name, separating with a space')
group.add_argument('--execution_id', type=int, default=0, help='Enter the Execution id as an integer. See Texas-Deathrow-Executions.csv')

args = parser.parse_args()

offender_input_name = args.name
ex_id = args.execution_id


def offenders_table():

	df = pd.read_csv('texas-deathrow-executions.csv', index_col='Execution_id')

	return df


def get_last_statement(offender_url):
	'''
	Function for retrieving a single last statement record from the Texas Dept Criminal Justice Website.
	This function assumes the "texas-deathrow-executions.csv" has been created and filled.
	''' 
	offender_name_url = offender_url.split('/')[5].split('.')[0]

	if offender_name_url == 'no_last_statement':
		offender_name = 'None'
	else:
		offender_name = offender_name_url[:-4]

	last_statement_dict = {	'Date of Execution:': '#####', 
							'Offender:': offender_name,
							'TDCJ_num': 'None',
							'Last Statement': 'None' }

	offender_response = requests.get(offender_url)

	soup = BeautifulSoup(offender_response.text, 'html.parser')

	p_tags = soup.find_all('p')

	p_tag_list = list()
	headers = list()
	values = list()

	for p in p_tags:
		if len(p.text) > 1:
			p_tag_list.append(p.text)

	if len(p_tag_list) > 2:

		statement_body = p_tag_list[5:]
		clean_statement = []

		for line in statement_body:
			line = line.replace(u'\u2019',"'")
			line = line.replace(u'\u00a0','')
			clean_statement.append(line)

			# need to adjust dictionary, ID number
		headers = [p_tag_list[0].strip(), p_tag_list[2].strip(), 'TDCJ_num', p_tag_list[4].strip()]
		values = [p_tag_list[1].strip()] + [p_tag_list[3].split('#')[0]] + [p_tag_list[3].split('#')[1]] + clean_statement

		final_statement_dict = dict(zip(headers, values))

	else:
		final_statement_dict = last_statement_dict

	return final_statement_dict


def get_url_by_name(first_name, last_name):

	base_url = 'https://www.tdcj.texas.gov/death_row/dr_info/'

	offender_url = base_url + last_name + first_name + 'last.html'

	return offender_url


def retrieve_record_by_index(execution_id):

	texas_df = offenders_table()
	
	offender_row = texas_df.loc[execution_id]

	first_name = offender_row.loc['First_Name']
	last_name = offender_row.loc['Last_Name']
	tdcj_no = offender_row.loc['TDCJ_Number']

	last_statement_url = get_url_by_name(first_name, last_name)
	last_statement_dict = get_last_statement(last_statement_url)

	last_statement_dict['Date of Execution:'] = offender_row.loc['Date']
	last_statement_dict['Offender:'] = first_name + ' ' + last_name
	last_statement_dict['TDCJ_num'] = tdcj_no

	return last_statement_dict


def retrieve_record_by_name(name_string):

	texas_df = offenders_table()

	first_last_input = offender_input_name.split()

	first_name_input = first_last_input[0]
	last_name_input = first_last_input[1]

	last_statement_url = get_url_by_name(first_name_input, last_name_input)
	last_statement_dict = get_last_statement(last_statement_url)

	return last_statement_dict


def retrieve_record_series(index_start, index_end):

	texas_df = offenders_table()

	for index in range(index_start,index_end):

		offender_dict = retrieve_record_by_index(index)

		offender_dict['TDCJ_num'] = int(offender_dict['TDCJ_num'])

		name = offender_dict['Offender:']
		tdcj_no = offender_dict['TDCJ_num']

		with open(f'No.{ex_id}-{name}-{tdcj_no}-last-statement.txt', 'w') as outfile:
			json.dump(offender_dict, outfile, indent=4)

		time.sleep(2)

print('Record retrieved')

if offender_input_name == 'index_given':

	offender_dict = retrieve_record_by_index(ex_id)

	offender_dict['TDCJ_num'] = int(offender_dict['TDCJ_num'])

	name = offender_dict['Offender:']
	tdcj_no = offender_dict['TDCJ_num']


else:

	offender_dict = retrieve_record_by_name(offender_input_name)

	offender_dict['TDCJ_num'] = int(offender_dict['TDCJ_num'])

	name = offender_dict['Offender:']
	tdcj_no = offender_dict['TDCJ_num']


with open(f'No.{ex_id}-{name}-{tdcj_no}-last-statement.txt', 'w') as outfile:
	json.dump(offender_dict, outfile, indent=4)

print('File Done')







