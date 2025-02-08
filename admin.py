from flask import Flask, render_template, request
import pymysql
import time
import matplotlib
matplotlib.use('Agg')  # Use the 'Agg' backend before importing pyplot
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Sumukha_R_Kashyap@8073',
    'database': 'trafficfine',
}

# Function to execute SQL query
def execute_query(query):
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    connection.close()
    return result

# Route for the main page
@app.route('/')
def index():
    return render_template('admin_home.html')

# Route to handle form submission
@app.route('/execute_query', methods=['POST'])
def execute_query_route():
    query = request.form['query']
    result = execute_query(query)
    return render_template('admin_home.html', query=query, result=result)

@app.route('/reducefine',methods=['POST'])
def reduce():
    if request.method=='POST':
        zone=request.form['zone_no']
        percentage=request.form['reduction_factor']
        query="CALL ReduceAmountInZone(%s,%s);"
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute(query,(zone,percentage))
        connection.commit()
        connection.close()
    time.sleep(2)
    return render_template('admin_home.html')

@app.route('/pendingzoneinfo', methods=['POST'])
def zoneinfopending():
    if request.method == 'POST':
        try:
            zone_id = int(request.form['zone_id'])
            query = """
                SELECT zone_name, zonal_officer, calculate_total_amount_pending(%s) as total_amount
                FROM zone
                WHERE zone_id = %s
            """
            connection = pymysql.connect(**db_config)
            cursor = connection.cursor()
            cursor.execute(query, (zone_id, zone_id))
            zone_info = cursor.fetchone()
            print(zone_info,type(zone_info))
            if zone_info:
                # Construct the response
                response=zone_info
                return render_template('admin_home.html', zone_info_pending=response)
            else:
                return render_template('admin_home.html', zone_info_pending=None)

        except Exception as e:
            print(f"Error: {e}")
            return render_template('your_template_name.html', zone_info_pending=None)
@app.route('/paidzoneinfo', methods=['POST'])
def zoneinfopaid():
    if request.method == 'POST':
        try:
            zone_id = int(request.form['zone_id'])
            query = """
                SELECT zone_name, zonal_officer, calculate_total_amount_paid(%s) as total_amount
                FROM zone
                WHERE zone_id = %s
            """
            connection = pymysql.connect(**db_config)
            cursor = connection.cursor()
            cursor.execute(query, (zone_id, zone_id))
            zone_info = cursor.fetchone()
            print(zone_info,type(zone_info))
            if zone_info:
                # Construct the response
                response=zone_info
                return render_template('admin_home.html', zone_info_paid=response)
            else:
                return render_template('admin_home.html', zone_info_paid=None)

        except Exception as e:
            print(f"Error: {e}")
            return render_template('your_template_name.html', zone_info_paid=None)


# Function to get total violations by type for a given zone or all zones
def get_total_violations(zone_id):
    if zone_id == 0:
        query = """
            SELECT viol_type, COUNT(*) as total_count
            FROM violation
            GROUP BY viol_type;
        """
        connection = pymysql.connect(**db_config)
        cursor=connection.cursor()
        result = cursor.execute(query)
    else:
        query = """
            SELECT viol_type, COUNT(*) as total_count
            FROM violation
            WHERE zone_id = %s
            GROUP BY viol_type;
        """
        connection = pymysql.connect(**db_config)
        cursor=connection.cursor()
        result = cursor.execute(query, (zone_id))

    result = cursor.fetchall()
    cursor.close()
    connection.close()
    
    print(result)
    return result

@app.route('/pie_chart', methods=['POST'])
def generate_pie_chart():
    zone_id = int(request.form['zone_id'])
    data = get_total_violations(zone_id)

    # Extract data for plotting
    labels = [row[0] for row in data]
    values = [row[1] for row in data]

    # Plotting the pie chart using the 'Agg' backend
    plt.switch_backend('Agg')
    plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle

    # Convert plot to base64 image for embedding in HTML
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    img_str = base64.b64encode(img_buffer.read()).decode('utf-8')
    plt.close()

    return render_template('admin_home.html', zone_id=zone_id, pie_chart=img_str)


if __name__ == '__main__':
    app.run(debug=True,port=8080)


#SELECT c.aadhaar_id,c.c_name,c.dl_no,c.addr,c.gender,c.phno from rto_vehicle r JOIN citizen c on r.owner_id=c.aadhaar_id where r.vehicle_no in (SELECT vehicle_no from violation) order by vehicle_no;

# SELECT DISTINCT c.dl_no
# FROM citizen c
# JOIN RTO_Vehicle rv ON c.aadhaar_id = rv.owner_id
# JOIN violation v ON rv.vehicle_no = v.vehicle_no
# WHERE v.viol_type = 'Speeding';
