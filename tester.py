import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import numpy as np

import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup


LEN = 10

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

creds = ServiceAccountCredentials.from_json_keyfile_name('secret.json', scope)
client = gspread.authorize(creds)
sheet = client.open('Words').sheet1

lol = sheet.get_all_values()
words = []

for row in lol:
    words = words + [x for x in row if x.strip()]

#print(words)

z = np.random.choice(words, size=LEN, replace=False)
#print(z)

clear = lambda: os.system('clear')
count = 0

for i in range(LEN):
    clear()
    print("------ LIST LENGTH = "+str(len(words))+" -------")
    print('Word #' +str(i+1)+' : ' +z[i])
    print("Press (f) for next word")
    print('Press (g) to verify')
    print('Press (h) for definition')
    inp = input("")
    #print(inp)
    if inp == 'f':
        count += 1
    else:
        print(" Showing Definitions - ")
        my_url='https://www.wordnik.com/words/'+str(z[i])

        uClient = uReq(my_url)

        page_html = uClient.read()
        uClient.close()

        page_soup = soup(page_html,"html.parser")
        x = page_soup.findAll("div",{"class":"word-module module-definitions"})
        x = x[0]
        
        t = x.findAll("li")
        for u in t:
            print(u.text.strip())
        
        print("________")

        if inp=='g':
            print("Did you get it right? (y/n)")
            nex = input('')
            if nex == 'y':
                count += 1
        
        else: 
            nex = input('')
        
    
print("Your score = "+str(count)+"/10")
