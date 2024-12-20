from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app and SQLAlchemy
db = SQLAlchemy()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@127.0.0.1:5432/cloud'
db.init_app(app)

# Define the Room model
class Room(db.Model):
    __tablename__ = 'rooms'

    id = db.Column(db.Integer, primary_key=True)  # Primary key is 'id'
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String)
    county = db.Column(db.String)
    postcode = db.Column(db.String)
    furnished = db.Column(db.Boolean)
    amenities = db.Column(db.ARRAY(db.String))
    live_in_landlord = db.Column(db.Boolean)
    shared_with = db.Column(db.Integer)
    bills_included = db.Column(db.Boolean)
    bathroom_shared = db.Column(db.Boolean)
    price_per_month_gbp = db.Column(db.Integer)
    availability_date = db.Column(db.Date)
    spoken_languages = db.Column(db.ARRAY(db.String))
    location = db.Column(db.JSON)  # Changed to db.JSON
    details = db.Column(db.JSON)  # Changed to db.JSON

# Define the ApplicationRoom model
class ApplicationRoom(db.Model):
    __tablename__ = 'applicationroom'

    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, nullable=False)
    roomid = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String, nullable=False)

# Function to check if the application ID exists
def checkid(application_id):
    """
    Checks if the application ID exists in the applicationroom table.
    
    Args:
        application_id (int): The application ID to check.

    Returns:
        bool: True if the application ID exists, False otherwise.
    """
    with app.app_context():
        exists = db.session.query(ApplicationRoom.id).filter_by(id=application_id).first()
        return exists is not None

# Function to check if the room ID exists
def checkroomid(room_id):
    """
    Checks if the room ID exists in the rooms table.
    
    Args:
        room_id (int): The room ID to check.

    Returns:
        bool: True if the room ID exists, False otherwise.
    """
    with app.app_context():
        exists = db.session.query(Room.id).filter_by(id=room_id).first()  # Use 'id' for Room model
        return exists is not None

