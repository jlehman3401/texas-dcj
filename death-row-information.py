from bs4 import BeautifulSoup
import requests

url = 'https://www.tdcj.texas.gov/death_row/dr_executed_texas.html'

response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')


texas = dict()

# getting table values with offender and 
td_tags = soup.find_all('td')

td_items = list()

for element in td_tags:
    td_items.append(element.text)

texas['Execution_id'] = td_items[0:len(td_items):10]

texas['Last_Name'] = td_items[3:len(td_items):10]
texas['First_Name'] = td_items[4:len(td_items):10]
texas['TDCJ_Number'] = td_items[5:len(td_items):10]
texas['Age'] = td_items[6:len(td_items):10]
texas['Date'] = td_items[7:len(td_items):10]
texas['Race'] = td_items[8:len(td_items):10]
texas['County'] = td_items[9:len(td_items):10]


# get links from a tags
a_tags = soup.find_all('a')

links = list()
for a in a_tags:
    links.append(a.get('href'))

links = all_links[26:1156]

texas['Offender_Link'] = links[:len(links):2]
texas['Last_Statement'] = links[1:len(links):2]
texas_len = len(texas['Offender_Link'])


filename = 'texas-dcj-offender-info.txt'

with open(filename, "w") as f:
    for i in range(len(texas_len)):
        f.write(texas['Execution_id'][i] + ',' + texas['Last_Statement']+ '\n')

