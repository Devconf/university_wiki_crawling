from bs4 import BeautifulSoup
import os
import json

days={'M':'Mon','T':'Tue', 'W':'Wed', 'R':'Thu', 'F':'Fri', 'S':'Sat'}

def TransportTime(day, time):
    schedule = []

    time=time.split(" ")
    for i in range(0,len(day.strip())):
        d=days.get(day[i],'')
        if d =='' or time[0] =='TBA':
            return schedule
        else:
            if time[1] =="am" or int(time[0].split(':')[0]) == 12:
                if time[4] =="am" or int(time[3].split(':')[0]) == 12:
                    schedule.append(d+" | "+time[0]+" ~ "+time[3])
                else:
                    schedule.append(d+" | "+time[0]+" ~ "+str(int(time[3].split(':')[0])+12)+":"+time[3].split(':')[1])      
            else:
                schedule.append(d+" | "+str(int(time[0].split(':')[0])+12)+":"+time[0].split(':')[1]+" ~ "+str(int(time[3].split(':')[0])+12)+":"+time[3].split(':')[1])

    return schedule

def TransportGrade(grade):
    result=""
    for idx in range(len(grade)):
        if idx !=len(grade):
            if grade[idx] =='A':
                result+=  'Audit'
            elif grade[idx] =='L':
                result+= 'Letter Grade'
            elif grade[idx] =='P':
                result+= 'Pass/Fail'
            result+=","
    return result[:-1]

def MakeFile():
    path_dir = './assets/GatechClass/'
    file_list = os.listdir(path_dir)
    for file in file_list:
        f= open("./Data/GatechClass/"+file[:-5]+".json",'w',encoding='utf-8')
        f.write(json.dumps(Extract(path_dir+file),indent=4))
        f.close()


def Extract(path):
    lectures=[]

    lecture = open(path,encoding='utf-8')
    soup = BeautifulSoup(lecture, 'html.parser') 
    title_list = soup.find_all('th', class_= 'ddtitle')
    lecture_list = soup.find_all('td',class_='dddefault')
    
    cnt=0
    for lecture in lecture_list:
        if lecture.text.find("Associated Term") != -1:
            title = title_list[cnt].text.split(" - ")

            datas =lecture.text.split("\n")
            new_datas= {i : datas[i] for i in range(len(datas))}

            grade =""
            times=[]
            professor=""
            room=""
            
            
            for idx,data in new_datas.items():
                if data.find('Grade Basis')!=-1:
                    grade =data[13:-1]
                    continue
                if data == "Class":
                    if new_datas[idx+2] == str('\xa0'):
                        times += TransportTime('',new_datas[idx+1])
                    else:
                        times += TransportTime(new_datas[idx+2],new_datas[idx+1])
                    professor = new_datas[idx+6]
                    room = new_datas[idx+3]
                    continue
                    
            content ={
                "pip": "Internal",
                "parentId": "",
                "ownerId": "",
                "title": title[0],
                "description": title[0]+" - "+title[2]+" - "+title[3],
                "times": times,
                "alerts": "",
                "professor": professor,
                "room": room,
                "grade": TransportGrade(grade),
                "exam": "",
                "attendance": "",
                "book": "",
            }
            lectures.append(content)
            cnt+=1       
        else:
            continue
    return lectures


if __name__ == "__main__":
    MakeFile()

    
