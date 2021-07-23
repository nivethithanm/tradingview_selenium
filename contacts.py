from bs4 import BeautifulSoup
import mechanize
import csv

users = []
contacts = []
members_input_file = 'members.csv'
with open(members_input_file, 'r+', encoding='UTF-8') as f:
        rows = csv.reader(f,delimiter=",",lineterminator="\n")
        next(rows, None)
        for row in rows:
            user = {}
            user['username'] = row[0]
            user['id'] = int(row[1])
            user['access_hash'] = int(row[2])
            user['name'] = row[3]
            users.append(user)    
for user in users:
        mc = mechanize.Browser()
        mc.set_handle_robots(False) 
        url = 'https://www.findandtrace.com/trace-mobile-number-location'
        mc.open(url) 
        mc.select_form(name='trace')
        try:
            mc['mobilenumber'] = user['id'] # Enter a mobile number
            res = mc.submit().read()
        except:
            continue
        soup = BeautifulSoup(res,'html.parser')
        tbl = soup.find_all('table',class_='shop_table')
        #print(tbl)        
        contact['phone'] = user['id']
        data = tbl[0].find('tfoot')
        c=0
        for i in data:
            c+=1
            if c in (1,4,6,8):
                continue
            if (c == 3):
                contact['Circle'] = i.find('td').text
            if (c == 5):
                contact['Network'] = i.find('td').text
            if (c > 8):
                contact['Connection'] = i.find('td').text
            #th = i.find('th')
            #td = i.find('td')
            #print(th.text,td.text) 
        data = tbl[1].find('tfoot')
        c=0
        for i in data:
            c+=1
            if(c==22):
                contact['main_languange'] = i.find('td').text
                #th = i.find('th')
                #td = i.find('td')
                #print(th.text,td.text)
        contacts.append(contact)        
input_file = 'contacts.csv'
with open(input_file,'w+',encoding='UTF-8') as f:
            writer = csv.writer(f,delimiter=",",lineterminator="\n")
            csv_dict = [row for row in csv.DictReader(f)]
            if len(csv_dict) == 0:
                writer.writerow(['Name','Phone Number', 'Telecom Circle', 'Network', 'Main Language'])
            for user in contacts:
                writer.writerow([user['name'],user['phone'],user['Circle'], user['Connection'],user['network'],user['main_language']]) 

