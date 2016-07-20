# WeatherDataApi

Heroku Deployment Application that reduces data downloaded for OpenWeatherMap Api

We are using esp-link firmware on an ESP8266-01 with an Arduino. The firmware is put onto a ESP8266-01 and accesses openweathermaps api for weather.

Owing to a limitation in the firmware, where it cannot download a response from a website which exceeds 100 characters, data has to be routed through a server which only provides the ESP with the relevant data, and not the whole response. 

In simple terms, this is a data filtering service which only gives specific parts of the response, which a remote device can access.

This service uses the free servers on Heroku which have a generous 550hrs/month limit for any web application that wants to be hosted with them.

The code allows you to have three services
The first parameter is the cityid found from openweathermapsapi. 1275339 corresponds to Mumbai, India
The second parameter is a appid which you have to get as an api key from openweathermaps. The appid 15373f8c0b06b6e66e6372db065c4e46 belongs to us and has been kept here for demo, please do not use it in your application.(We may discontinue its use anytime we see usage abuse)

#Manual City Configuration

**Humidty**

http://idiotware.herokuapp.com/humidity?id=1275339&appid=15373f8c0b06b6e66e6372db065c4e46

**Temperature**

http://idiotware.herokuapp.com/temperature?id=1275339&appid=15373f8c0b06b6e66e6372db065c4e46

**Weather Description**

http://idiotware.herokuapp.com/weatherDescription?id=1275339&appid=15373f8c0b06b6e66e6372db065c4e46

**City and Country**

http://idiotware.herokuapp.com/getCityCountry?id=1275339&appid=15373f8c0b06b6e66e6372db065c4e46




#Automatic Location Detection by IP

We have been able to add automatic detection of city which the device is asking data for, based on IP address. If you would like to use automatic detection, please do not add the id parameter in the above URL's

**Humidty**

http://idiotware.herokuapp.com/humidity?appid=15373f8c0b06b6e66e6372db065c4e46

**Temperature**

http://idiotware.herokuapp.com/temperature?appid=15373f8c0b06b6e66e6372db065c4e46

**Weather Description**

http://idiotware.herokuapp.com/weatherDescription?appid=15373f8c0b06b6e66e6372db065c4e46

**City and Country**

http://idiotware.herokuapp.com/getCityCountryByIP





