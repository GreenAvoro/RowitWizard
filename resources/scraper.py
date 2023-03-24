from bs4 import BeautifulSoup
import requests
import mysql.connector


event_no = 1
data = []
regattas = [
    'niss2023',
    'kric2023r3'
]
for regatta in regattas:
    for event_no in range(1,5):
        url = "https://rowit.nz/"+regatta+"/results?en="+str(event_no)
        page = requests.get(url)
        page = page.content
        soup = BeautifulSoup(page, 'html.parser')


        #get all the result data
        tables = soup.find_all("table", class_="result-table")
        for table in tables:
            div = table.thead.a.get_text()
            results = table.find_all("tr", class_="result-details")
            
            for r in results:
                result = {"div": div}
                result['regatta'] = regatta
                result['name'] = soup.find_all("a", class_="cardEventName")[0].get_text()
                result['no'] = event_no
                names = r.find_all("div", class_="cardCrewMembers")[0].find_all("a")
                result['names'] = []
                for name in names:
                    result['names'].append(name.get_text())
                result['time'] = r.find_all("a", class_="resultTimeLink")[0].find_all("span")[1].get_text()
                data.append(result)


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="gdcCoach12",
    database="rowit_wizard"
)

cursor = mydb.cursor()

for race in data:
    names = ''
    for name in race['names']:
        names = names + str(name) + ', '
    cursor.execute("INSERT INTO `races` (`time`, `event_no`,`event_name`, `regatta`, `div`, `names`) VALUES (%s, %s, %s, %s, %s, %s)", (race['time'], race['no'],race['name'], race['regatta'], race['div'], names))
mydb.commit()
