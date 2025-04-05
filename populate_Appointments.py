import requests
import json
import random
import uuid
from datetime import datetime, timedelta
import faker

# Initialize Faker to generate realistic user data with Indian locale
fake = faker.Faker(['en_IN'])

# API base URL
API_BASE_URL = 'http://localhost:3001/'

# Specified nurse ID
NURSE_ID = "7d03280e-5c88-4fb5-8575-59c3d0faccea"

# Define shifts
SHIFTS = ["MORNING", "AFTERNOON", "EVENING"]

# Mumbai localities
MUMBAI_LOCALITIES = [
    "Andheri", "Bandra", "Colaba", "Dadar", "Juhu", "Malad", "Worli", 
    "Powai", "Borivali", "Thane", "Navi Mumbai", "Chembur", "Santacruz",
    "Goregaon", "Kandivali", "Khar", "Mira Road", "Mulund", "Sion", "Vikhroli"
]

# Worker types available
WORKER_TYPES = ["NURSE", "PHYSIOTHERAPIST", "CARETAKER", "COUNSELOR"]

# Function to generate location data in Mumbai
def generate_location():
    # Mumbai area locations with their approximate coordinates
    mumbai_locations = [
        {"name": "Thane", "lat": 19.2183, "lng": 72.9781},
        {"name": "Dadar", "lat": 19.0178, "lng": 72.8478},
        {"name": "Churchgate", "lat": 18.9322, "lng": 72.8264},
        {"name": "Chembur", "lat": 19.0522, "lng": 72.8994},
        {"name": "Andheri", "lat": 19.1136, "lng": 72.8697},
        {"name": "Bandra", "lat": 19.0596, "lng": 72.8295},
        {"name": "Powai", "lat": 19.1176, "lng": 72.9060},
        {"name": "Mulund", "lat": 19.1662, "lng": 72.9538}
    ]
    
    # Select a random location and add slight variation
    base_location = random.choice(mumbai_locations)
    return {
        "latitude": round(base_location["lat"] + random.uniform(-0.01, 0.01), 6),
        "longitude": round(base_location["lng"] + random.uniform(-0.01, 0.01), 6)
    }

# Function to generate phone number
def generate_phone():
    # Generate 10-digit phone numbers as strings
    return str(random.randint(1111111111, 9999999999))

# Function to create a user
def create_user():
    gender = random.choice(["Male", "Female"])
    
    # Generate user data matching the schema
    user_data = {
        "id": str(uuid.uuid4()),
        "name": fake.name(),
        "age": random.randint(25, 80),
        "location": generate_location(),
        "phone": generate_phone(),
        "backup_phone": generate_phone(),
        "gender": gender,
        "prefered_type": random.choice(WORKER_TYPES).lower()
    }
    
    return user_data

# Function to create an appointment
def create_appointment(user_id, worker_id):
    # Generate a future date within next 30 days
    future_date = datetime.now() + timedelta(days=random.randint(1, 30))
    future_date = future_date.replace(hour=random.randint(8, 17), minute=0, second=0, microsecond=0)
    
    appointment_data = {
        "date": future_date.isoformat(),
        "userID": user_id,
        "workerID": worker_id,
        "shift": random.choice(SHIFTS),
        "status": False,
        "notified": False
    }
    
    return appointment_data

# Function to insert a user directly to the database
def insert_user(user_data):
    try:
        url = f"{API_BASE_URL}/register/user"
        headers = {
            "Content-Type": "application/json"
        }
        response = requests.post(url, json=user_data, headers=headers)
        
        print(f"User creation response: {response.status_code}")
        if response.text:
            print(response.text[:200])  # Print just the beginning to keep output manageable
            
        if response.status_code == 200 or response.status_code == 201:
            print(f"User created successfully: {user_data['name']}")
            return user_data["id"]
        else:
            print(f"Failed to create user: {response.status_code}")
            try:
                print(response.json())
            except:
                print(response.text)
            return None
    except Exception as e:
        print(f"Error creating user: {str(e)}")
        return None

# Function to book an appointment
def book_appointment(user_id, appointment_data):
    try:
        # First schedule the appointment time with the worker
        schedule_url = f"{API_BASE_URL}/appointments/schedule"
        schedule_data = {
            "date": appointment_data["date"],
            "shift": appointment_data["shift"]
        }
        
        # Using worker ID in header for session
        headers = {
            "sessionID": appointment_data["workerID"],
            "Content-Type": "application/json"
        }
        
        print(f"Scheduling appointment with headers: {headers}")
        print(f"And data: {schedule_data}")
        
        schedule_response = requests.post(schedule_url, json=schedule_data, headers=headers)
        
        print(f"Schedule response: {schedule_response.status_code}")
        if schedule_response.text:
            print(schedule_response.text[:200])  # Print just the beginning
        
        if schedule_response.status_code != 200:
            print(f"Failed to schedule appointment: {schedule_response.status_code}")
            print(schedule_response.text)
            return False
        
        # Now book the appointment for the user
        book_url = f"{API_BASE_URL}/appointments/book"
        
        # Headers for booking
        book_headers = {
            "workerID": appointment_data["workerID"],
            "userID": user_id,
            "Content-Type": "application/json"
        }
        
        print(f"Booking appointment with headers: {book_headers}")
        
        book_response = requests.post(book_url, json=schedule_data, headers=book_headers)
        
        print(f"Book response: {book_response.status_code}")
        if book_response.text:
            print(book_response.text[:200])  # Print just the beginning
        
        if book_response.status_code == 200:
            print(f"Appointment booked successfully for user {user_id}")
            return True
        else:
            print(f"Failed to book appointment: {book_response.status_code}")
            print(book_response.text)
            return False
    except Exception as e:
        print(f"Error booking appointment: {str(e)}")
        return False

def main():
    print("Starting to populate users and appointments...")
    
    # Create 10 users with appointments
    successful_users = 0
    for i in range(10):
        print(f"\nCreating user {i+1}/10")
        
        # Create user
        user_data = create_user()
        user_id = insert_user(user_data)
        
        if user_id:
            # Create appointment for this user
            appointment_data = create_appointment(user_id, NURSE_ID)
            success = book_appointment(user_id, appointment_data)
            
            if success:
                successful_users += 1
            
            # Small delay to avoid overwhelming the API
            import time
            time.sleep(1)
    
    print(f"\nPopulation complete! Created {successful_users} users with appointments.")

if __name__ == "__main__":
    main()