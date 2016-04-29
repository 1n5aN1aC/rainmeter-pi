#!python
import logging, time

import Stoppable_Thread
import Now

import weather
import settings

#
# This File Handles updating the 'feels-like' display.
# This is the small window in the top-right of the index page
# that show what the weather currently 'feels like.'
class thread_feels_like(Stoppable_Thread.Stoppable_Thread):
    def run(self):
        while self.RUN:
            self.update_feels_like()
            self.update_feels_forecast()
            time.sleep(settings.how_often_to_update_feels_like)
    
    def update_feels_like(self):
        parsed_json = weather.fetchWeather('conditions')
        weather.closeURL()
        
        NOW_URL = "https://icons.wxug.com/i/c/v4/" + parsed_json['current_observation']['icon'] + ".svg"
        NOW_Feel = float(parsed_json['current_observation']['feelslike_f'])
        
        now = Now.get()
        now.Now_URL = NOW_URL
        now.Now_Feel = NOW_Feel
        logging.getLogger("thread-feels").info(" Updated feels like info.")
    
    def update_feels_forecast(self):
        parsed_json = weather.fetchWeather('forecast')
        weather.closeURL()
        
        NOW_Feel_High = float(parsed_json['forecast']['simpleforecast']['forecastday'][0]['high']["fahrenheit"])
        NOW_Feel_Low = float(parsed_json['forecast']['simpleforecast']['forecastday'][0]['low']["fahrenheit"])
        
        now = Now.get()
        
        now.Now_Feel_High = NOW_Feel_High
        now.NOW_Feel_Low = NOW_Feel_Low
        logging.getLogger("thread-feels").info(" Updated high-low data.")