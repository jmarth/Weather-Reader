import requests
import pyttsx
import time

def get_current_weather():
    conditions = requests.get("http://api.wunderground.com/api/0def10027afaebb7/conditions/q/78256.json")
    weather = conditions.json()
    
    currentWeather = {}
    currentWeather['weather'] = weather['current_observation']['weather']
    currentWeather['temp'] = float(weather['current_observation']['temp_f'])
    currentWeather['feelsLikeTemp'] = float(weather['current_observation']['feelslike_f'])
    
    return currentWeather

def get_current_weather_text():
    currentWeather = get_current_weather()
    feelsLike = ""
    if currentWeather['feelsLikeTemp'] < currentWeather['temp']:
         feelsLike = ", but if feels like %s" % currentWeather['feelsLikeTemp']
         
    text = "The weather is currently %s and %s degrees%s." % (currentWeather['weather'], currentWeather['temp'], feelsLike)
    return text
    
def get_todays_weather():
    forecast = requests.get("http://api.wunderground.com/api/0def10027afaebb7/forecast/q/78256.json")
    weather = forecast.json()
    
    todaysWeather = {}
    todaysWeather['todaysHigh'] =  weather['forecast']['simpleforecast']['forecastday'][0]['high']['fahrenheit']
    todaysWeather['todaysLow'] =  weather['forecast']['simpleforecast']['forecastday'][0]['low']['fahrenheit']
    todaysWeather['todaysWeather'] = weather['forecast']['simpleforecast']['forecastday'][0]['conditions']
    
    return todaysWeather

def get_todays_weather_text():
    todaysWeather = get_todays_weather()
    text = "Todays weather forecast will be %s with a high of %s and a low of %s" % (todaysWeather['todaysWeather'], todaysWeather['todaysHigh'], todaysWeather['todaysLow'])
    return text

def get_gretting():
    hour = int(time.strftime('%H:%M:%S')[:2])
    if hour == 24 or hour < 12:
        return "Good morning Joseph!"
    return "Good afternoon Joseph!"

def get_reminders():
    todaysWeather = get_todays_weather()
    reminder = ""
    if "rain" in todaysWeather['todaysWeather']:
        reminder = "Remember to bring an umbrella"
    if float(todaysWeather['todaysLow']) < 70:
        if reminder == "":
            reminder = "Remember to bring a jacket"
        else:
            reminder += " and a jacket"
    return reminder

def main():
    engine = pyttsx.init()
    engine.setProperty('rate', 175)
    engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-GB_HAZEL_11.0')
    #added , between text so there will be a small pause before it speaks the next text
    engine.say('%s , %s , %s because %s' % (get_gretting(), get_current_weather_text(), get_reminders(), get_todays_weather_text() ))
    engine.runAndWait()

def list_voices():
    engine = pyttsx.init()
    voices = engine.getProperty('voices')
    for voice in voices:
       engine.setProperty('voice', voice.id)
       print "voice id = %s" % voice.id
       engine.say('The quick brown fox jumped over the lazy dog.')
    engine.runAndWait()

#you can see the available voice id's on your system by running list_voices()
main()
#list_voices()




