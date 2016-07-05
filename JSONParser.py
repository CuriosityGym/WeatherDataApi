import requests
import json
import re

import os

from flask import Response, Flask

app = Flask(__name__)

@app.route("/humidity")
def getHumidity():
    return getData("main.humidity")
    
@app.route("/temperature")
def getTemperature():
    return getData("main.temp")

@app.route("/weatherDescription")
def getWeatherDescription():
    return getData("weather.main")
    
    



def getData(jsontree):
    requestURL="http://api.openweathermap.org/data/2.5/weather?id=1275339&appid=15373f8c0b06b6e66e6372db065c4e46"
    filename='jsondata.json'
    response = download_file(requestURL, filename)
    with open(filename) as data_file:    
        data = json.load(data_file)
    splittree=jsontree.split(".")    
    lastLeafIndex = len(splittree) - 1
    #jsontree="main.temp"
    
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
               return "Error"
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
       return str(data[leaf])
   










def download_file(url,filename):
    local_filename = filename
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                #f.flush() commented by recommendation from J.F.Sebastian
    return True



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port,debug=True)


 
