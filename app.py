from flask import Flask, render_template, request
from apply import fetch_room_details, send_application_data
from cancel import cancel_application_request
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
@app.route('/cancel')
def cancel():
    # No room data here, just rendering the template
    return render_template('cancel.html')
@app.route('/apply')
def apply():
    # Check if the user is logged in by checking if session contains user data
    logged_in = 'user_data' in session
    
    # If the user is logged in, retrieve the user ID from the session
    user_id = None
    if logged_in:
        user_id = session['user_data']['id']  # Retrieve the user ID from session
    
    # Pass the login status and user_id to the template
    return render_template('apply.html', logged_in=logged_in, user_id=user_id)


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
@app.route('/history')
def history():
    # Retrieve all application records from the database
    applications = Application.query.all()
    
    # Pass the applications to the template for display
    return render_template('history.html', applications=applications)

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
@app.route('/book_room', methods=['POST'])
def book_room():
    # Get room_id from the form
    room_id = request.form['room_id']

    # Retrieve user_id from session
    user_id = session['user_data']['id']  # Get the logged-in user's ID from the session

    print(f"Booking room for User ID: {user_id} with Room ID {room_id}")

    try:
        # Fetch room details using the provided room ID
        room_details = fetch_room_details(room_id)
        print(f"Room details: {room_details}")

        # Retrieve user details from the session
        user = session['user_data']  # User data from session

        # Step 1: Create a new application entry in the database
        application = Application(
            user_id=user_id,
            firstname=user['firstname'],
            familyname=user['familyname'],
            email=user['email'],
            phone_number=user['phone_number'],
            room_id=room_id
        )
        db.session.add(application)
        db.session.commit()  # Commit the transaction to save the new application

        # Step 2: Fetch the last application_id from the Application table and increment it
        last_application = Application.query.order_by(Application.application_id.desc()).first()
        new_application_id = last_application.application_id + 1 if last_application else 1

        # Step 3: Send application data to the server, passing the new application_id and user_id
        send_application_data(user_id, room_id, room_details, new_application_id)

        return f"Room booked successfully for User ID {user_id} in room {room_id}. Application ID: {new_application_id}"

    except Exception as e:
        print(f"Error: {str(e)}")
        return f"An error occurred: {str(e)}"


@app.route('/cancel_application', methods=['POST'])
def cancel_application():
    application_id = request.form['application_id']

    print(f"Cancelling application with ID: {application_id}")

    try:
        # Cancel the application request using the external service or any logic you need
        cancel_application_request(application_id)
        
        # Now, remove the application from the Application table in the database
        application_to_delete = Application.query.filter_by(application_id=application_id).first()
        
        if application_to_delete:
            db.session.delete(application_to_delete)  # Delete the application record
            db.session.commit()  # Commit the transaction

            return f"Application {application_id} has been cancelled and removed from the database."
        else:
            return f"Application with ID {application_id} not found."

    except Exception as e:
        print(f"Error: {str(e)}")
        return f"An error occurred while cancelling the application: {str(e)}"

    
    

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



