import wikipediaapi

def PrintTextFile(university, p_wiki):
    f= open("data/"+university+".txt",'w',encoding='utf-8')
    f.write(p_wiki.text)
    f.close()

def GetUniversity():
    f=open("./university.txt",'r')
    return f.readlines()


if __name__ == "__main__":
    wiki = wikipediaapi.Wikipedia( language='en', extract_format=wikipediaapi.ExtractFormat.WIKI)
    university_list =GetUniversity()

    for university in university_list:
        univ = university[:-1] if university[-1:] =='\n'else university 
        p_wiki= wiki.page(univ)
        if p_wiki.exists():
            print("OK "+ univ) 
            PrintTextFile(univ,p_wiki)
        else:
            print("Fail "+ univ) 


   