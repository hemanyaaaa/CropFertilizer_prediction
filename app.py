from flask import Flask, render_template, request, redirect, url_for, session, flash
import joblib
import pandas as pd
import os
import json
import requests

app = Flask(__name__)
app.secret_key = '1234'

# =================================================
# Paths and Model Loading
# =================================================
basedir = os.path.dirname(__file__)
fertilizer_model = joblib.load(os.path.join(basedir, 'fertilizer_model.pkl'))
soil_encoder = joblib.load(os.path.join(basedir, 'soil_encoder.pkl'))
crop_encoder = joblib.load(os.path.join(basedir, 'crop_encoder.pkl'))
crop_model = joblib.load(os.path.join(basedir, 'crop_model.pkl'))

USERS_FILE = os.path.join(basedir, 'users.json')


# =================================================
# User Helpers
# =================================================
def load_users():
    """Load registered users from JSON."""
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}


def save_users(users):
    """Save registered users to JSON."""
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f)


# =================================================
# Weather API
# =================================================
def get_weather(city):
    """Fetch weather data from OpenWeatherMap."""
    api_key = "fbf273f8d5a957163c3acd8f19a6af7f"  # <-- Replace this with your actual key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        condition = data["weather"][0]["description"]
        return temperature, humidity, condition
    else:
        return None, None, None


# =================================================
# Routes
# =================================================
@app.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('home.html')


@app.route('/fertilizer', methods=['GET', 'POST'])
def fertilizer():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        city = request.form['city']
        temperature, humidity, condition = get_weather(city)

        if temperature is None or humidity is None:
            return "❌ Error: Could not fetch weather data for the entered city."

        moisture = float(request.form['moisture'])
        soil_type = request.form['soil_type']
        crop_type = request.form['crop_type']
        nitrogen = float(request.form['nitrogen'])
        phosphorous = float(request.form['phosphorous'])
        potassium = float(request.form['potassium'])

        soil_encoded = soil_encoder.transform([soil_type])[0]
        crop_encoded = crop_encoder.transform([crop_type])[0]

        input_data = pd.DataFrame([[temperature, humidity, moisture, soil_encoded,
                                     crop_encoded, nitrogen, phosphorous, potassium]],
                                   columns=['temperature', 'humidity', 'moisture', 'soil_type',
                                            'crop_type', 'nitrogen', 'phosphorous', 'potassium'])
        prediction = fertilizer_model.predict(input_data)[0]

        return render_template('fertilizer_result.html',
                               fertilizer=prediction,
                               city=city,
                               temperature=temperature,
                               humidity=humidity,
                               condition=condition)

    return render_template('fertilizer.html')


@app.route('/crop', methods=['GET', 'POST'])
def crop():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        N = float(request.form['N'])
        P = float(request.form['P'])
        K = float(request.form['K'])
        city = request.form['city']

        temperature, humidity, condition = get_weather(city)

        if temperature is None or humidity is None:
            return "❌ Error: Could not fetch weather data for the entered city."

        ph = float(request.form['ph'])
        rainfall = float(request.form['rainfall'])

        input_df = pd.DataFrame([[N, P, K, temperature, humidity, ph, rainfall]],
                                 columns=['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall'])
        prediction = crop_model.predict(input_df)[0]

        return render_template('crop_result.html',
                               crop=prediction,
                               city=city,
                               temperature=temperature,
                               humidity=humidity,
                               condition=condition)

    return render_template('crop.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        users = load_users()
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['user'] = username
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.', 'error')
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        users = load_users()
        username = request.form['username']
        password = request.form['password']
        if username in users:
            flash('Username already exists.', 'error')
        else:
            users[username] = password
            save_users(users)
            flash('Signup successful. Please login.', 'success')
            return redirect(url_for('login'))
    return render_template('signup.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


# =================================================
# Main
# =================================================
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)

