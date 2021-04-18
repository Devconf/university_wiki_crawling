import wikipediaapi
from mediawiki import MediaWiki
import requests
import pypandoc
import json
import datetime
import os
import glob
import re


def GetUniversity():
    f=open("./assets/university.txt",'r')
    return f.readlines()

def BuildUniversitySkeleton(university_list):
    univ_list={"university" : []}
    f= open("./Data/university/UniversitySkeleton.json",'w')

    for university in university_list:
        univ = university[:-1] if university[-1:] =='\n'else university 
    
        content ={
                "pip": "Public",
                "type": "university",
                "parentId": "",
                "ownerId": "",
                "createdAt": datetime.datetime.utcnow().isoformat(),
                "modifiedAt": datetime.datetime.utcnow().isoformat(),
                "deletedAt": "",
                "title":univ,
                "description":"",
                "emblemImgURL": "https://en.wikipedia.org/wiki/",
                "location": [],
                "address": "",
            }
        univ_list["university"].append(content)
    
    f.write(json.dumps(univ_list,indent=4))

def ConvertWikiToMarkdown(university_list):
    wikipedia = MediaWiki()

    for university in university_list:
        univ = university[:-1] if university[-1:] =='\n'else university
        if not(os.path.isdir("./Data/markdown/"+univ)):
            os.makedirs(os.path.join("./markdown/"+univ))            
        
        if not(os.path.isfile("./Data/markdown/"+univ+"/Summary.md")):
            pypandoc.convert_text("== "+wikipedia.page(univ).title+"==\n"+wikipedia.page(univ).summary +"\n\nfrom [wikipedia]("+wikipedia.page(univ).url+")"
                ,'md',format='mediawiki',outputfile="./Data/markdown/"+univ+"/Summary.md",encoding='utf-8')

        section_list =wikipedia.page(univ).sections
        
        for section in section_list:
            file_name =str(section).replace("/","_")
            characters= '"'
            file_name = ''.join( x for x in file_name if x not in characters)
            if os.path.isfile("./Data/markdown/"+univ+"/"+file_name+".md"):
                continue
            else:
                pypandoc.convert_text("== "+section+"==\n"+wikipedia.page(univ).section(section) +"\n\nfrom [wikipedia]("+wikipedia.page(univ).url+")"
                ,'md',format='mediawiki',outputfile="./Data/markdown/"+univ+"/"+file_name+".md",encoding='utf-8')
            
            
def format_wikies():
    wikies = glob.glob("./data/markdown/**/*")

    #print(wikies)
    result = {}
    for i in wikies:
        univ_name = i.split("\\")[1]
        menu_name = i.split("\\")[2].replace(".md","")
        f = open(i,"r", encoding="utf8")
        d = f.read()
        f.close()
        d = re.sub('(\{#\w+\})','',d)
        if univ_name not in result:
            result[univ_name] = {}
            #print(re.sub('({#\w+})','',d))
            result[univ_name][menu_name] = d
        else:
            result[univ_name][menu_name] = d
    f = open("./Data/wikies.json","w")
    f.write(json.dumps(result, indent=2))          
            

if __name__ == "__main__":
    wiki = wikipediaapi.Wikipedia( language='en', extract_format=wikipediaapi.ExtractFormat.WIKI)
    university_list =GetUniversity()
    #BuildUniversitySkeleton(university_list)
    #ConvertWikiToMarkdown(university_list)
    format_wikies()
    


   