from bs4 import BeautifulSoup
import requests

url = 'https://www.tdcj.texas.gov/death_row/dr_executed_offenders.html'

response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')



td_tags = soup.find_all('td')



headers = [ 'Execution_id',
            'Offender_Link',
            'Last_Statement',
            'Last_Name',
            'First_Name',
            'TDCJ_Number',
            'Age',
            'Date',
            'Race',
            'County']

offenders = dict()

# getting table values with offender and 
td_tags = soup.find_all('td')

td_items = list()

for element in td_tags:
    td_items.append(element.text)

offenders['Execution_id'] = td_items[0:len(td_items):10]

offenders['Last_Name'] = td_items[3:len(td_items):10]
offenders['First_Name'] = td_items[4:len(td_items):10]
offenders['TDCJ_Number'] = td_items[5:len(td_items):10]
offenders['Age'] = td_items[6:len(td_items):10]
offenders['Date'] = td_items[7:len(td_items):10]
offenders['Race'] = td_items[8:len(td_items):10]
offenders['County'] = td_items[9:len(td_items):10]


# get links from a tags
a_tags = soup.find_all('a')

links = list()
for a in a_tags:
    links.append(a.get('href'))

links = all_links[26:1156]

offenders['Offender_Link'] = links[:len(links):2]
offenders['Last_Statement'] = links[1:len(links):2]





