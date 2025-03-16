import requests
import random
import string
from faker import Faker
import time
import json

fake = Faker()
BASE_URL = "https://dycare.astledsa.workers.dev"

def generate_phone():
    # Generate 7-digit numbers that will fit in PostgreSQL integer
    return random.randint(1000000, 9999999)

def generate_location():
    return {
        "latitude": round(random.uniform(-85, 85), 6),
        "longitude": round(random.uniform(-175, 175), 6)
    }

def make_request(endpoint, data, retry_count=3):
    for attempt in range(retry_count):
        try:
            response = requests.post(f"{BASE_URL}/{endpoint}", json=data)
            print(f"Response for {endpoint}: Status {response.status_code}, Body: {response.text}")
            
            if response.status_code == 409:  # Duplicate phone number
                data['phone'] = generate_phone()  # Generate new phone and retry
                continue
                
            return response
            
        except requests.RequestException as e:
            if attempt == retry_count - 1:
                print(f"Failed after {retry_count} attempts for {endpoint}: {str(e)}")
                return None
            time.sleep(1)  # Wait before retry
    return None

def register_users(count=100):
    successful = 0
    for i in range(count):
        data = {
            "name": fake.name(),
            "age": random.randint(18, 80),
            "location": generate_location(),
            "phone": generate_phone()
        }
        
        print(f"\nAttempting to register user {i+1}/{count}")
        response = make_request("register/user", data)
        
        if response and response.status_code == 200:
            successful += 1
        time.sleep(0.5)  # Rate limiting
    
    print(f"\nSuccessfully registered {successful}/{count} users")
    return successful

def register_nurses(count=10):
    specializations = ["Pediatric Nursing", "Critical Care", "Emergency Care", "Surgical Nursing", 
                      "Geriatric Care", "Mental Health", "Oncology", "Cardiac Care"]
    education_levels = ["BSN", "MSN", "DNP", "ADN"]
    successful = 0
    
    for i in range(count):
        data = {
            "name": fake.name(),
            "age": random.randint(25, 60),  # Increased minimum age
            "experience": random.randint(1, 30),
            "education": random.choice(education_levels),
            "profile_picture": "",  # Removed fake profile URL
            "specialization": random.choice(specializations),
            "phone": generate_phone(),
            "loc": generate_location()
        }
        
        print(f"\nAttempting to register nurse {i+1}/{count}")
        response = make_request("register/nurses", data)
        
        if response and response.status_code == 200:
            successful += 1
        time.sleep(0.5)
    
    print(f"\nSuccessfully registered {successful}/{count} nurses")
    return successful

def register_physiotherapists(count=10):
    specializations = ["Sports Physiotherapy", "Neurological Physiotherapy", "Pediatric Physiotherapy",
                      "Geriatric Physiotherapy", "Orthopedic Physiotherapy", "Cardiopulmonary Physiotherapy"]
    education_levels = ["DPT", "MPT", "BPT", "Ph.D"]
    successful = 0
    
    for i in range(count):
        data = {
            "name": fake.name(),
            "age": random.randint(25, 60),
            "experience": random.randint(1, 30),
            "education": random.choice(education_levels),
            "profile_picture": "",
            "specialization": random.choice(specializations),
            "phone": generate_phone(),
            "loc": generate_location()
        }
        
        print(f"\nAttempting to register physiotherapist {i+1}/{count}")
        response = make_request("register/physiotherapists", data)
        
        if response and response.status_code == 200:
            successful += 1
        time.sleep(0.5)
    
    print(f"\nSuccessfully registered {successful}/{count} physiotherapists")
    return successful

def register_counselors(count=10):
    specializations = ["Mental Health", "Family Counseling", "Addiction Counseling", 
                      "Trauma Counseling", "Child Psychology", "Behavioral Therapy"]
    education_levels = ["MSW", "Ph.D", "PsyD", "MA Psychology"]
    successful = 0
    
    for i in range(count):
        data = {
            "name": fake.name(),
            "age": random.randint(25, 60),
            "experience": random.randint(1, 30),
            "education": random.choice(education_levels),
            "profile_picture": "",
            "specialization": random.choice(specializations),
            "phone": generate_phone(),
            "loc": generate_location()
        }
        
        print(f"\nAttempting to register counselor {i+1}/{count}")
        response = make_request("register/counselor", data)
        
        if response and response.status_code == 200:
            successful += 1
        time.sleep(0.5)
    
    print(f"\nSuccessfully registered {successful}/{count} counselors")
    return successful

def register_caretakers(count=10):
    education_levels = ["BSN", "ADN", "CNA", "HHA"]
    successful = 0
    
    for i in range(count):
        data = {
            "name": fake.name(),
            "age": random.randint(25, 60),
            "experience": random.randint(1, 30),
            "education": random.choice(education_levels),
            "profile_picture": "",
            "phone": generate_phone(),
            "loc": generate_location()
        }
        
        print(f"\nAttempting to register caretaker {i+1}/{count}")
        response = make_request("register/caretakers", data)
        
        if response and response.status_code == 200:
            successful += 1
        time.sleep(0.5)
    
    print(f"\nSuccessfully registered {successful}/{count} caretakers")
    return successful

if __name__ == "__main__":
    print("Starting database population...")
    
    total_users = register_users(100)
    total_nurses = register_nurses(10)
    total_physiotherapists = register_physiotherapists(10)
    total_counselors = register_counselors(10)
    total_caretakers = register_caretakers(10)
    
    print("\nFinal Registration Summary:")
    print("-" * 30)
    print(f"Users: {total_users}/100")
    print(f"Nurses: {total_nurses}/10")
    print(f"Physiotherapists: {total_physiotherapists}/10")
    print(f"Counselors: {total_counselors}/10")
    print(f"Caretakers: {total_caretakers}/10")
    print("-" * 30)
    
    if (total_users == 100 and 
        total_nurses == 10 and 
        total_physiotherapists == 10 and 
        total_counselors == 10 and 
        total_caretakers == 10):
        print("Database population completed successfully!")
    else:
        print("Database population completed with some failures.")