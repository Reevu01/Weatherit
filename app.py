from flask import Flask, render_template, request
import requests
from flask_sqlalchemy import SQLAlchemy
from weather2 import main as getWeather

app = Flask(__name__)
app.config['DeBUG'] = True

@app.route('/', methods=['GET','POST'])
def index():
    temp = None
    day = None
    country = ''
    state = ''
    city = ''
    if request.method == 'POST':
        country = request.form['country']
        state = request.form['state']
        city = request.form['city']
        temp, day = getWeather(country, state, city)
    return render_template('weather.html',temp=temp, day=day, country = country, state = state, city = city)
    
if __name__ == '__main__':
    app.run(debug=True)
