import requests
import json
import re

import os

from flask import Response, Flask, request
errorText="Error"
app = Flask(__name__)
gCityID="1275339"
gAppID="15373f8c0b06b6e66e6372db065c4e46"
filename='temp.json'

	

@app.route("/humidity")
def getHumidity():
       
        gCityID = request.args.get('id')
        gAppID = request.args.get('appid')

        if (gCityID is None):
                latitude,longitude=getLatLongFromIP()
                #return longitude
                requestURL="http://api.openweathermap.org/data/2.5/weather?lat="+latitude+"&lon="+longitude+"&appid="+gAppID  
        else:
                requestURL="http://api.openweathermap.org/data/2.5/weather?id="+gCityID+"&appid="+gAppID        
        return requestURL
       
        #try:        
        response = download_file(requestURL, filename)
        return getData("main.humidity")
        #except:
        #       return errorText
    
@app.route("/temperature")
def getTemperature():
        gCityID = request.args.get('id')
        gAppID = request.args.get('appid')

        if (gCityID is None):
                latitude,longitude=getLatLongFromIP()
                requestURL="http://api.openweathermap.org/data/2.5/weather?lat="+latitude+"&lon="+longitude+"&appid="+gAppID  
        else:
                requestURL="http://api.openweathermap.org/data/2.5/weather?id="+gCityID+"&appid="+gAppID        

       
        try:        
                response = download_file(requestURL, filename)
                return getData("main.temp")
        except:
                return errorText

@app.route("/weatherDescription")
def getWeatherDescription():
        gCityID = request.args.get('id')
        gAppID = request.args.get('appid')

        if (gCityID is None):
                latitude,longitude=getLatLongFromIP()
                requestURL="http://api.openweathermap.org/data/2.5/weather?lat="+latitude+"&lon="+longitude+"&appid="+gAppID  
        else:
                requestURL="http://api.openweathermap.org/data/2.5/weather?id="+gCityID+"&appid="+gAppID        

       
        try:        
                response = download_file(requestURL, filename)
                return getData("weather.main")
        except:
                return errorText
				
@app.route("/getCityCountryByIP")
def getLocationbyIP():
        try:
                if "X-Forwarded-For" in request.headers:
                        IPAddress=request.headers['X-Forwarded-For']
                else:
                        IPAddress=request.environ['REMOTE_ADDR']
                
                requestURL="http://ip-api.com/json/"+IPAddress
                #requestURL="http://ip-api.com/json/182.56.200.95"
                response = download_file(requestURL, filename)
                cityName=getData("city")
                countryName=getData("countryCode")
                return cityName+ ", "+countryName # Mumbai, IN, for example
                
        except:
                return errorText
				
@app.route("/getCityCountry")
def getLocation():
        gCityID = request.args.get('id')
        gAppID = request.args.get('appid')
        try:
                requestURL="http://api.openweathermap.org/data/2.5/weather?id="+gCityID+"&appid="+gAppID
                response = download_file(requestURL, filename)        
                cityName=getData("name")
                countryName=getData("sys.country")
                return cityName+ ", "+countryName # Mumbai, IN, for example

        except:
                return errorText				
    
def getLatLongFromIP():
        try:
                if "X-Forwarded-For" in request.headers:
                        IPAddress=request.headers['X-Forwarded-For']
                else:
                        IPAddress=request.environ['REMOTE_ADDR']

                requestURL="http://ip-api.com/json/"+IPAddress
                #requestURL="http://ip-api.com/json/182.56.200.95"
                response = download_file(requestURL, filename)
                latitude=getData("lat")
                longitude=getData("lon")
                return (latitude, longitude) 

        except:
                return (0,0)  


def getData(jsontree):    
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
    return True



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port,debug=True)


 
