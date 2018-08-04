
import requests
from bs4 import BeautifulSoup
import re
import time

#Receive Wiki link as input
print('Please input a Wikipedia link')
input_link = input()

response = requests.get(input_link)

#Checking if it is a valid link
if(response.status_code != 200):
    print('Link not found. Please input another link')
    input_link = input()
response = requests.get(input_link)

soup = BeautifulSoup(response.content,"html.parser")


#print(soup.prettify())

#print(soup.find("h1",attrs={"class":"firstHeading"}).text)


all_links = []
all_links.append(input_link)
while soup.find("h1",attrs={"class":"firstHeading"}).text != 'Philosophy':
    paragraph = soup.find('p')
    
    # remove pronounciation, tables, italics and content within paranthesis
    for s in paragraph.find_all(['i', 'small', 'sup,', 'span', 'table']): 
        s.replace_with("")
    para_text = str(paragraph)
    para_text = re.sub(r' \(.*?\)', '', para_text)
    
    soup_para = BeautifulSoup(para_text,"html.parser")
    
    first_link = soup_para.find(href = re.compile('^/wiki/'))
    
    while first_link == None:
        paragraph = paragraph.find_next_sibling("p")
        # remove pronounciation, tables, italics and content within paranthesis
        for s in paragraph.find_all(['i', 'small', 'sup,', 'span', 'table']): 
            s.replace_with("")
        para_text = str(paragraph)
        para_text = re.sub(r' \(.*?\)', '', para_text)
        soup_para = BeautifulSoup(para_text,"html.parser")
        first_link = soup_para.find(href = re.compile('^/wiki/'))
        
    url = 'http://en.wikipedia.org' + first_link.get('href')
    print(url)
    
    #Time out between queries
    time.sleep(0.5)
    
    r = requests.get(url) # Make new request
    soup = BeautifulSoup(r.text,"lxml")
    
    #Checking loops
    if url not in all_links:
        continue 
    else:
        print('Stuck in loop')
        break
    
    all_links.append(url)

