import requests
import json
import re


jsontree="main.temp_max"

splittree=jsontree.split(".")
def download_file(url,filename):
    local_filename = filename
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                #f.flush() commented by recommendation from J.F.Sebastian
    return local_filename


requestURL="http://api.openweathermap.org/data/2.5/weather?id=1275339&appid=15373f8c0b06b6e66e6372db065c4e46"
filename='jsondata.json'

response = download_file(requestURL, filename)
with open(filename) as data_file:    
    data = json.load(data_file)
lastLeafIndex = len(splittree) - 1
#for leaf in splittree:
    #
for i, leaf in enumerate(splittree):
    if i == lastLeafIndex:
        continue
    else:
       leafDataIndex=0
       result =  re.findall(r'\[([^]]*)\]', leaf)
       if result:
          leafDataIndex=result[0]
          leaf=leaf.replace("["+leafDataIndex+"]","")
          leafDataIndex=int(leafDataIndex)
       #print (leafDataIndex)
    try:        
        data=data[leaf][leafDataIndex]
    except(KeyError):
       try: 
           data=data[leaf]
       except (KeyError):
           print ("Error")
           exit()

leaf=splittree[lastLeafIndex]
leafDataIndex=0
result =  re.findall(r'\[([^]]*)\]', leaf)
if result:
    leafDataIndex=result[0]
    leaf=leaf.replace("["+leafDataIndex+"]","")
    leafDataIndex=int(leafDataIndex)
    #print (data[leaf][leafDataIndex])
else:
   print (data[leaf]) 






 
