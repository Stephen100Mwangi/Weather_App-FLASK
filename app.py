from flask import Flask, request, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
import requests


# Create app
app = Flask(__name__)
CORS(app)

# Configuration
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/weather_db'

class Base(DeclarativeBase):
    pass

# Create database
db = SQLAlchemy(app)

class City (db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50),nullable=False)

# Create routes
@app.route('/',methods=["GET","POST"])
def index():
    if request.method == "POST":
        new_city = request.form.get("city")
        if new_city:
            new_city = City(name=new_city)
            db.session.add(new_city)
            db.session.commit()

    cities = City.query.all()
    apiURL = 'https://api.openweathermap.org/data/2.5/weather?units=imperial&q={}&appid=551e24112fa184689a71b359a4cd7c9e'

    weather_data = []

    try:
        for city in cities:
            response = requests.get(apiURL.format(city.name)).json()
            # print(response)

            weather = {
                'city':response['name'],
                'temperature':response['main']['temp'],
                'description':response['weather'][0]['description'],
                'icon':response['weather'][0]['icon'],
            }

            weather_data.append(weather)

        return render_template('index.html',weather_data=weather_data)
    except requests.exceptions.RequestException as e:
        print(f"Error making API request {e}")
        return "Error weather data",500
    
@app.cli.command('init-db')
def init_db():
    db.create_all()
    print("Initialized the database successfully") 

# @app.cli.command('add-city')
# def add_city():
#     seattle = City(name="Seattle")
#     nairobi = City(name="Nairobi")
#     new_york = City(name="New York")
#     beijing = City(name="Beijing")
#     tokyo = City(name="Tokyo")
#     sydney = City(name="Sydney")
#     brussels = City(name="Brussels")
#     mumbai = City(name="Mumbai")
#     dubai = City(name="Dubai")

#     db.create_all()
#     print("Created new cities successfully")

# Run app
if __name__ == "__main__":
    app.run(debug=True)


# {
#     'coord': {'lon': -115.1372, 'lat': 36.175},
#     'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}],
#     'base': 'stations', 
#     'main': 
#     {   
#         'temp': 7.69, 'feels_like': 6.45, 'temp_min': 7.09, 'temp_max': 9.25, 'pressure': 1023, 
#         'humidity': 28, 'sea_level': 1023, 'grnd_level': 954
#     }, 
#     'visibility': 10000,
#     'wind': {'speed': 2.06, 'deg': 320}, 
#     'clouds': {'all': 0}, 'dt': 1733063907,
#     'sys': {'type': 1, 'id': 6171, 'country': 'US', 'sunrise': 1733063630, 'sunset': 1733099173},
#     'timezone': -28800,
#     'id': 5506956,
#     'name': 'Las Vegas',
#     'cod': 200
# }    