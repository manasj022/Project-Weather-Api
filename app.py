import requests
import configparser
from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///city.db'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

@app.route('/weather',methods=['POST'])
def weather():
    city_name=request.form['cityName']
    api_key=get_api_key()
    data=get_weather_results(city_name, api_key)
    main_weather=data["weather"][0]["main"]
    main_weather_description=data["weather"][0]["description"]
    temp="{0:.2f}".format(data["main"]["temp"])
    temp_feels_like="{0:.2f}".format(data["main"]["feels_like"])
    humidity="{0:.2f}".format(data["main"]["humidity"])
    wind_speed="{0:.2f}".format(data["wind"]["speed"])
    country=data["sys"]["country"]
    name=data["name"]
    return render_template('results.html', city_name=city_name, main_weather=main_weather, main_weather_description=main_weather_description, temp=temp, temp_feels_like=temp_feels_like, humidity=humidity, wind_speed=wind_speed, country=country, name=name)


def get_api_key():
    config=configparser.ConfigParser()
    config.read('config.ini')
    return config['openweatherapp']['api']   

def get_weather_results(city_name,api_key):
    api_url="https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}".format(city_name,api_key)
    r=requests.get(api_url)
    return r.json()


if __name__=='__main__':
    app.run(debug=True)



