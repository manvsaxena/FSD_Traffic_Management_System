import random
import string
import pymysql

db = pymysql.connect(
    host="localhost", user="root", password="Sumukha_R_Kashyap@8073", database="trafficfine"
)
cursor = db.cursor()

indian_models = ['Hero Honda', 'Bajaj Pulsar', 'Royal Enfield', 'Honda Activa', 'Maruti Suzuki Alto', 'Hyundai Creta', 'Tata Indigo', 'Mahindra Scorpio','RX']

indian_first_names = [
    'Aarav', 'Aishwarya', 'Rahul', 'Priya', 'Sachin', 'Swati', 'Vikram', 'Kiran', 'Anjali', 'Rohit',
    'Neelam', 'Manish', 'Shweta', 'Amit', 'Meera', 'Ganesh', 'Neha', 'Amitabh', 'Madhuri', 'Hrithik'
]

indian_last_names = [
    'Patel', 'Kumar', 'Singh', 'Sharma', 'Gupta', 'Verma', 'Mishra', 'Reddy', 'Jain', 'Mukherjee',
    'Kapoor', 'Yadav', 'Pandey', 'Choudhary', 'Khanna', 'Agarwal', 'Malhotra', 'Mehta', 'Saxena', 'Sinha'
]

street_names = ['Main Street', 'Gandhi Road', 'Shivaji Nagar', 'Rajendra Prasad Avenue', 'Jawaharlal Nehru Lane']
cities =[
    'Bengaluru', 'Mysore', 'Hubli', 'Mangalore', 'Belgaum', 'Davangere', 'Bellary', 'Shimoga', 'Tumkur',
    'Gulbarga', 'Udupi', 'Hassan', 'Bidar', 'Bijapur', 'Raichur', 'Hospet', 'Chitradurga', 'Mandya',
    'Chikkamagaluru', 'Bagalkot', 'Kolar', 'Chamarajanagar', 'Gadag', 'Haveri', 'Karwar', 'Sirsi',
    'Koppal', 'Madikeri', 'Ramanagara'
]

# You can continue to add more cities to the list if needed.

states = ['Karnataka']

genders = ['M', 'F', 'O']

def generate_indian_name():
    first_name = random.choice(indian_first_names)
    last_name = random.choice(indian_last_names)
    full_name = f"{first_name} {last_name}"
    return full_name


def generate_indian_address():
    street = random.choice(street_names)
    city = random.choice(cities)
    state = random.choice(states)
    postal_code = str(random.randint(560000,600000))
    address = f"{street}, {city}, {state} - {postal_code}"
    return address

for _ in range(500):
    reg_year = random.randint(1987, 2023)
    reg_month = random.randint(1, 12)
    reg_day = random.randint(1, 28)
    reg_dt = f'{reg_year}-{reg_month:02d}-{reg_day:02d}'
    vehicle_year = random.randint(1987, 2023)
    vehicle_model = random.choice(indian_models)
    owner_id = random.randint(10**6, 10**7 - 1)
    zone_id = random.randint(1, 6)
    vehicle_no = 'KA' + ''.join(random.choices(string.digits, k=2)) + ''.join(random.choices(string.ascii_uppercase, k=2)) + ''.join(random.choices(string.digits, k=4))

    query = f"INSERT INTO rto_vehicle (reg_dt, vehicle_year, vehicle_model, owner_id, vehicle_no,zone_id) VALUES ('{reg_dt}', {vehicle_year}, '{vehicle_model}', {owner_id},'{vehicle_no}',{zone_id})"
    cursor.execute(query)
    aadhaar_id = owner_id
    c_name = generate_indian_name()
    dl_no = ''.join(random.choices(string.ascii_uppercase, k=3)) + ''.join(random.choices(string.digits, k=7))
    addr = generate_indian_address()
    gender = random.choice(genders)
    phno = str(random.randint(6000000000, 9999999999))

    query = f"INSERT INTO citizen (aadhaar_id, c_name, dl_no, addr, gender, phno) " \
            f"VALUES ({aadhaar_id}, '{c_name}', '{dl_no}', '{addr}', '{gender}', {phno})"
    cursor.execute(query)

db.commit()
db.close()
