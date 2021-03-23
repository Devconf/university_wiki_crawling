import json
import requests
from markdownify import markdownify

url_head ="https://api.concept3d.com/locations/"
url_last = "?map=82&key=0001085cc708b9cef47080f064612ca5"

services={1:'Library',2:'Restaurant',4:'Parking',8:'Medical',16:'Custom'}

with open('./assets/georgia_tech_map.json',encoding='utf-8') as buildings:
    building_list= json.load(buildings)


def BuildingExtractByCategory():
    place_list =[{"Covid-19 Testing Locations":8}, {"Parking":4}, {"Dining":2}, {"Buildings By Category":16}, {"Greenspaces":16}, {"Restrooms":16},
    {"Student Disposable Face Covering Pickup Locations":8}, {"Social Distance Tents":8}]
    real_custom={'Library':[],'Restaurant':[],'Parking':[],'Medical':[],'Custom':[]}
    for place in place_list:
        real_building=[]
        
        service =(key for key in place.values())
        service =(next(service,False))
        print(service)
        
        where = (key for key in place.keys())
        where = (next(where,False))
        
        building = (item for item in building_list if item['name'] == where)
        building_info = next(building,False)
        
        if 'categories' in building_info['children']:
            match=[]
            building_cate=building_info['children']['categories']
            for b in building_cate:
                match =(item for item in building_list if item['name'] == b['name'])
                for m in match:
                    real_building += m['children']['locations']
            
            if len(building_info['children']['locations']) != 0:
                real_building += building_info['children']['locations']
        else:
            real_building += building_info['children']['locations']
        real_custom[services[service]]+=real_building

    for service, building in real_custom.items():
        building_extract =[]
        for b in building:
            print(b['id'])
            res =requests.get(url_head+str(b['id'])+url_last)
            data=res.json()
           
            description= markdownify(data["description"])
            

            content ={
                "pip": "Public",
                "parentId": "",
                "ownerId": "",
                "title": data["name"],
                "description": description,
                "location": [data["lat"],data["lng"]],
                "serviceCheckBits": service,
                "likes": "",
                "bookmarks": "",
            }
            building_extract.append(content)

        ToJson(service,building_extract)

def ToJson(category,data):
    f= open("./Data/Buildings/"+category+".json",'w',encoding='utf-8')
    f.write(json.dumps(data,indent=4))
    f.close()
    


if __name__ =="__main__":
    BuildingExtractByCategory()