import json
import requests
from bs4 import BeautifulSoup

def GetUniversity():
    f = open("./assets/university.txt",'r')
    university= f.readlines()
    search = "\n"
    for i, word in enumerate(university):
        if search in word: 
            university[i] = word.strip(search)
    #print(university)
    return university

def ExtractDomain():
    university_list=GetUniversity()
    for university in university_list:
        res =requests.get("http://en.wikipedia.org/wiki/"+university)
        soup = BeautifulSoup(res.text, 'html.parser')
        title_list = soup.find_all('span',class_='url')
        for temp in title_list:
            for a in temp.select('a[class="external text"]'):
                print(a['href'])
                break
            break
        #break

if __name__ == "__main__":
    ExtractDomain()