# app.py
from flask import Flask, render_template, request, redirect, url_for, session
import subprocess
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong, random secret key

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/show_map', methods=['POST'])
def show_map():
    bus_service_numbers = request.form.get('bus_service_numbers')
    if not bus_service_numbers:
        return redirect(url_for('home'))

    # Store bus service numbers in session
    session['bus_service_numbers'] = bus_service_numbers

    # Generate the map using map.py with the bus service numbers
    bus_service_list = [num.strip() for num in bus_service_numbers.split(',') if num.strip()]
    subprocess.run(['python', 'map.py'] + bus_service_list, check=True)

    return render_template('map.html')

@app.route('/find_best_route', methods=['POST'])
def find_best_route():
    current_location = request.form.get('current_location')
    destination = request.form.get('destination')
    
    # Retrieve bus service numbers from session
    bus_service_numbers = session.get('bus_service_numbers', None)
    
    if not current_location or not destination or not bus_service_numbers:
        return redirect(url_for('home'))

    # Process bus service numbers for RL
    bus_service_list = ','.join([num.strip() for num in bus_service_numbers.split(',') if num.strip()])

    # Run rl.py with the inputs
    result = subprocess.run(
        ['python', 'rl.py', bus_service_list, current_location, destination],
        capture_output=True, text=True
    )

    best_route_info = result.stdout.strip()
    return render_template('results.html', best_route=best_route_info)

if __name__ == '__main__':
    app.run(debug=True)
