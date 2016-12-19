import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
import warnings
import dateutil.parser
import re
import time
import csv
from string import punctuation
from multiprocessing import Pool

warnings.filterwarnings('ignore')

##convert the dates in the emails to a datetime object
def to_date(datestring):
    date = dateutil.parser.parse(datestring)
    return date

root_url = "https://wikileaks.org/podesta-emails/emailid/"
links_to_scrape = []
for i in list(range(1,50888)):
    links_to_scrape.append(root_url+str(i))

#list of all special characters
symbols = punctuation
symbols = symbols.replace("@",'')
symbols = symbols.replace(".",'')

count = 1
for i in links_to_scrape:
    try:
        response = requests.get(i)
        page = response.text
        soup = BeautifulSoup(page)
        header = soup.find("header").text 
        from_person = header[header.find("From:")+5:header.find("To")-6]
        send = header[header.find("To")+18:header.find("Date")-12]
        date = header[header.find("Date")+6:header.find("Subject")-6]
        date = to_date(date)
        subject = header[header.find("Subject")+9:len(header)-11]
        email_content = soup.find("div",attrs = {"class":"email-content"}).text
        email_content = email_content.replace("\n"," ")
        email_content = email_content.replace("\t","")
        email_content = email_content.replace("\xa0",'')
        for i in symbols:
            email_content = email_content.replace(i,' ')
        email_content = email_content.replace('  ', ' ')
        email_content = email_content.replace('  ',' ')
        row = (count, date, from_person, send, subject, email_content)
        with open('45000-50887.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow(row)
        if count % 100 == 0:
            print (count)
        count += 1
        time.sleep(.2)
    except:
        pass


