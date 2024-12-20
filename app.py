from flask import Flask, render_template, request
from flask import Flask, request, render_template, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
import logging
from werkzeug.security import check_password_hash, generate_password_hash
from search import search_room
import search 
import requests
from flask import  json
from crime import crime_client 
from weather import get_weather_data, parse_weather_data
from distance import calculate_distance 
from apply import apply_room
from cancel import cancel_application
from history import post_user_id, get_history,  deserialize
from check import checkid, checkroomid


app = Flask(__name__)
app.secret_key = 'your_secret_key'
# In-memory counter for application IDs (just for demonstration purposes)
application_id_counter = 1
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@127.0.0.1:5432/cloud'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
logging.basicConfig(level=logging.INFO)
class Contact(db.Model):
    __tablename__ = 'contact'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(50), nullable=False)
    familyname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
class Userdetails(db.Model):
    __tablename__ = 'userdetails'
    
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    familyname = db.Column(db.String(100), nullable=False)
    dateofbirth = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)

class Application(db.Model):
    __tablename__ = 'application'
    
    application_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('userdetails.id'), nullable=False)
    firstname = db.Column(db.String(100), nullable=False)
    familyname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    room_id = db.Column(db.Integer, nullable=False)

    user = db.relationship('Userdetails', backref=db.backref('applications', lazy=True))
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/rooms')
def room():
    # No room data here, just rendering the template
    return render_template('rooms.html')
@app.route('/Search')
def Search():
    # No room data here, just rendering the template
    return render_template('Search.html')
@app.route('/cancel', methods=['GET', 'POST'])
def cancel():
    logged_in = 'user_data' in session
    user_id = None
    response = None  # Initialize response variable

    if logged_in:
        user_id = session['user_data']['id']
    
    if request.method == 'POST':
        try:
            application_id = request.form['application_id']
            if not checkid(application_id):
                response = {"error": "Application ID does not exist."}
            elif logged_in:
                cancel_result = cancel_application(application_id, user_id)
                if cancel_result:  # Assuming cancel_application returns True on success
                    response = {"success": "Failed to cancel the application."}
                else:
                    response = {"error":
                                "Your application has been successfully cancelled." }
            else:
                response = {"error": "User is not logged in."}
        except ValueError:  # Catch invalid value for application_id
            response = {"error": "Invalid Application ID. Please enter a valid ID."}
        except Exception as e:
            response = {"error": str(e)}

    return render_template('cancel.html', response=response)



@app.route('/apply', methods=['GET', 'POST'])
def apply():
    # Check if the user is logged in by checking if session contains user data
    logged_in = 'user_data' in session
    
    # If the user is logged in, retrieve the user ID from the session
    user_id = None
    room_application_status = None
    if logged_in:
        user_id = session['user_data']['id']
    
    # If the request method is POST (when the form is submitted)
    if request.method == 'POST':
        try:
            # Get room_id from the form
            room_id = request.form['room_id']
            
            # Check if the room ID exists in the database
            if not checkroomid(room_id):
                room_application_status = "Room ID does not exist."  # If room does not exist, show error
            else:
                # If user is logged in, call apply_room function with user_id and room_id
                if logged_in:
                    response = apply_room(user_id, room_id)
                    room_application_status = response  # Set the response to be shown on the page
                else:
                    room_application_status = "User not logged in."  # Show error if user isn't logged in
        except Exception as e:
            room_application_status = f"An error occurred: {str(e)}"  # Handle unexpected errors
    
    # Render the apply page with the room_application_status message
    return render_template('apply.html', logged_in=logged_in, user_id=user_id, room_application_status=room_application_status)



@app.route('/distance')
def distance():
    # No room data here, just rendering the template
    return render_template('distance.html')
@app.route('/crime')
def crime():
    # No room data here, just rendering the template
    return render_template('crime.html')
@app.route('/weather')
def weather():
    # No room data here, just rendering the template
    return render_template('weather.html')
@app.route('/history', methods=['GET', 'POST'])
def history():
    if request.method == 'POST':
        user_id = request.form['userId']
        
        try:
            # Post the userId to set it on the server
            post_response = post_user_id(user_id)
            get_response = get_history()

            # Deserialize and parse the history response
            parsed_history = deserialize(get_response)  # Call deserialize here

            # Render the response on the history page
            return render_template('history.html', post_response=post_response, 
                                   get_response=get_response, parsed_history=parsed_history)

        except Exception as e:
            return f"Error occurred: {e}"

    return render_template('history.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Get form data
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        message = request.form.get('message')

        # Log received form data for debugging
        logging.info("Received contact form submission: %s, %s, %s", first_name, last_name, email)

        # Save the data to the database
        new_contact = Contact(
            firstname=first_name,
            familyname=last_name,
            email=email,
            message=message
        )
        db.session.add(new_contact)
        db.session.commit()
        
        # Redirect or render a success message
        return redirect(url_for('contact'))

    return render_template('contact.html')


@app.route('/home')
def home():
    # No room data here, just rendering the template
    return render_template('home.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get form data
        firstname = request.form.get('first_name')
        familyname = request.form.get('family_name')
        dateofbirth = request.form.get('dob')
        phone_number = request.form.get('phone')
        email = request.form.get('email')
        password = request.form.get('password')

        # Log received form data for debugging
        logging.info("Received signup form submission: %s, %s, %s, %s, %s, %s", 
                     firstname, familyname, dateofbirth, phone_number, email, password)

        # Hash the password before saving
        hashed_password = generate_password_hash(password)

        # Save the data to the database
        new_user = Userdetails(
            firstname=firstname,
            familyname=familyname,
            dateofbirth=dateofbirth,
            phone_number=phone_number,
            email=email,
            password=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()
        
        # Redirect to the login page or another page after successful sign-up
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/check_credentials', methods=['POST'])
def check_credentials():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = Userdetails.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):  # Use `check_password_hash` for comparison
            # Store user data in session
            session['user_data'] = {
                "id": user.id,
                "firstname": user.firstname,
                "familyname": user.familyname,
                "dateofbirth": user.dateofbirth.strftime('%Y-%m-%d'),
                "email": user.email,
                "phone_number": user.phone_number
            }

            logging.info("User %s successfully logged in.", email)
            return jsonify({"success": True})  # Return success response to trigger front-end action
        else:
            logging.warning("Login attempt failed for user: %s", email)
            return jsonify({"success": False})  # Return failure response if credentials don't match


@app.route('/logout')
def logout():
    session.pop('user_data', None)  # Remove the user data from session
    return redirect(url_for('index'))  # Redirect to home page or login page

    
@app.route('/Search', methods=['GET', 'POST'])
def search_room():
    if request.method == 'POST':
        # Get input from form
        price_max = request.form['priceMax']
        city = request.form['city']
        county = request.form['county']

        # Construct the external API URL
        external_url = f'http://localhost:8080/RestfulService/webresources/WeatherApp/searchRoom?priceMax={price_max}&city={city}&county={county}'

        
        # Fetch the data from the external API
        response = requests.get(external_url)
        
        # Check if the response is successful
        if response.status_code == 200:
            rooms_data = response.json()  # Parse the JSON data
            
            # Process the room data
            rooms = rooms_data.get('rooms', [])
            room_details = []

            for room in rooms:
                room_info = {
                    'name': room.get('name', 'N/A'),
                    'city': room.get('location', {}).get('city', 'N/A'),
                    'county': room.get('location', {}).get('county', 'N/A'),
                    'postcode': room.get('location', {}).get('postcode', 'N/A'),
                    'price': room.get('details', {}).get('price_per_month_gbp', 'N/A'),
                    'amenities': ', '.join(room.get('details', {}).get('amenities', [])),
                    'availability_date': room.get('details', {}).get('availability_date', 'N/A'),
                    'shared_with': room.get('details', {}).get('shared_with', 'N/A'),
                    'live_in_landlord': 'Yes' if room.get('details', {}).get('live_in_landlord', False) else 'No',
                    'furnished': 'Yes' if room.get('details', {}).get('furnished', False) else 'No',
                }
                room_details.append(room_info)
            
            return render_template('Search.html', room_details=room_details)
        else:
            return render_template('Search.html', message="No rooms found matching your criteria.")
    return render_template('Search.html')

@app.route('/fetch_crime_data', methods=['POST'])
def fetch_crime_data():
    data = request.json
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    result = crime_client(latitude, longitude)  # Get crime data from crime_client function
    return jsonify(result)  # Return as JSON


@app.route('/get_weather', methods=['POST'])
def get_weather():
    # Retrieve latitude and longitude from the form
    latitude = float(request.form['latitude'])
    longitude = float(request.form['longitude'])
    
    # Call the get_weather_data function from weather.py
    raw_weather_data = get_weather_data(latitude, longitude)
    
    # Check if the response contains an error
    if "Error" not in raw_weather_data:
        # Parse the weather data
        parsed_weather_data = parse_weather_data(raw_weather_data)
        # Return the parsed weather data as JSON
        return jsonify(parsed_weather_data)
    else:
        return jsonify({'error': raw_weather_data})
    
@app.route('/distance', methods=['GET', 'POST'], endpoint='distance_calculation')
def distance():
    if request.method == 'POST':
        # Get form data
        lat1 = float(request.form['lat1'])
        lon1 = float(request.form['lon1'])
        lat2 = float(request.form['lat2'])
        lon2 = float(request.form['lon2'])
        unit = request.form['unit']

        # Call the calculate_distance function
        json_response, _ = calculate_distance(lat1, lon1, lat2, lon2, unit)

        # Parse the JSON response to extract the distance and unit
        response_data = json.loads(json_response)
        formatted_distance = f"{response_data['distance']:.2f} {response_data['unit']}"

        # Display the results
        return render_template('distance.html', formatted_distance=formatted_distance)

    return render_template('distance.html', formatted_distance=None)


    
if __name__ == '__main__':
    app.run(debug=True)



