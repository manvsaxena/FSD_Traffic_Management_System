from flask import Flask, render_template, request, redirect, url_for,Response
import pymysql 
from pymysql import cursors
import random
import time
import base64

app = Flask(__name__)
violist=[]
login_id=[]
login_id.append(0)
paymentlist=[]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login_info')
def login_info():
    return render_template('login.html')

@app.route('/login',methods=['POST'])
def login():
    db = pymysql.connect(host="localhost", user="root", password="Sumukha_R_Kashyap@8073", database="trafficfine")
    cursor = db.cursor()
    if request.method=='POST':
        user_n=str(request.form['u_name'])
        passwd=str(request.form['passwd'])

        query='SELECT * from login where un=%s and pass=%s'
        cursor.execute(query,(user_n,passwd))
        user=cursor.fetchall()
        if(len(user) !=0):
            login_id[0]=1
            time.sleep(1.5)
            return redirect('/')
        else :
            return render_template('wrong_login.html')
    db.commit()
    cursor.close()
    db.close()

@app.route('/add_data', methods=['POST'])
def add_data():
    
    db = pymysql.connect(host="localhost", user="root", password="Sumukha_R_Kashyap@8073", database="trafficfine")
    cursor = db.cursor()
    if request.method == 'POST':
        # Get data from the form
        viol_type=request.form['type']
        print(viol_type,type(viol_type))
        location=request.form['location']
        zone_id=int(request.form['zone_id'][0])
        vehicle_no = request.form['vehicle_no']
        if 'viol_img' in request.files:
            image=request.files['viol_img']
            if image.filename != '':
                image_data = image.read()
        fines = {}
        fines['Signal Jump']=500
        fines['Wrong Parking']=750
        fines['Wrong way driving']=1000
        fines['No helmet']=500
        fines['Triple riding']=1750
        fines['Using Mobile']=750
        fines['Reckless Driving'] = 2000
        a=random.randint(1000,10000)
        while(a in violist):
            a=random.randint(1000,10000)
    if login_id[0]==1:
        try:
            insert_query = "INSERT INTO violation (violation_id,viol_type,dt_time,amount,loc,zone_id,vehicle_no,viol_img) VALUES (%s,%s,NOW(),%s,%s, %s,%s,%s)"
            cursor.execute(insert_query, (a,viol_type,fines[viol_type], location,zone_id,vehicle_no,image_data))
            db.commit()
            cursor.close()
            db.close()
            time.sleep(1.5)
            return redirect('/')
        except Exception as e:
            return render_template("vehicle_not_found.html")
        
    else:
        db.commit()
        cursor.close()
        db.close()
        return redirect('/login_info')


@app.route("/search_violations", methods=["POST"])
def search_violations():
    import base64
    from PIL import Image
    from io import BytesIO

    db = pymysql.connect(
        host="localhost",
        user="root",
        password="Sumukha_R_Kashyap@8073",
        database="trafficfine",
        cursorclass=pymysql.cursors.DictCursor
    )


    vehicle_number = request.form["vehi_no"]
    with db.cursor() as cursor:
        query = "SELECT * FROM violation WHERE vehicle_no = %s"
        cursor.execute(query, (vehicle_number,))
        violations = cursor.fetchall()

        for violation in violations:
            image_data = violation.get("viol_img")

            if image_data:
                encoded_image = base64.b64encode(image_data).decode("utf-8")
                violation["encoded_image"] = encoded_image

    violations_list = list(violations)

    if len(violations_list)>0:
        return render_template("violations.html", violations=violations_list)
    else:
        return render_template("no_viol.html")
    
@app.route("/add_payment", methods=['POST'])
def add_payment():
    db = pymysql.connect(host="localhost", user="root", password="Sumukha_R_Kashyap@8073", database="trafficfine")
    cursor = db.cursor()
    if request.method=='POST':
        violation_id=int(request.form["violation_id"])
        amount=int(request.form["amount"])
        vehi_no=request.form['vehi_no']
        a=random.randint(1000,10000)
        while(a in paymentlist):
            a=random.randint(1000,10000)
        print(vehi_no,type(vehi_no))
        print(a,type(a))
        print(violation_id,type(violation_id))
        print(amount,type(amount))
        query="INSERT INTO payment (payment_id,violation_id,amount,dt_time,stat) VALUES (%s,%s,%s,NOW(),'success')"
        cursor.execute(query,(a,violation_id,amount))
        db.commit()
        time.sleep(1.5)
        cursor.close()
        db.close()
        html="<h1 style='color: green;'>Successful</h1><p style='color: blue;'>Payment of rupees "+str(amount)+" is received</p><form id='redirect_form' method='POST' action='/search_violations'><input type='hidden' name='vehi_no' value='"+str(vehi_no)+"'><input type='submit' value='View Remaining Violation'></form>"
    return (html)


@app.route('/show_image', methods=['POST'])
def show_image():
    # Get the violation_id from the form
    violation_id = request.form['violation_id']
    print(violation_id)
    # Query the database to get the image data
    connection = pymysql.connect(host="localhost", user="root", password="Sumukha_R_Kashyap@8073", database="trafficfine")
    try:
        with connection.cursor() as cursor:
            # Assuming your table is named 'violations' and has columns 'violation_id' and 'violation_img'
            query = f"SELECT viol_img FROM violation WHERE violation_id = {violation_id}"
            cursor.execute(query)
            result = cursor.fetchone()
            if result:
                # Extract image data from the result
                image_data = result

                # Convert binary image data to base64 for rendering in HTML
                image_base64 = base64.b64encode(image_data[0]).decode('utf-8')

                # Render the HTML page with the image
                return render_template('show_image.html', image_base64=image_base64)
            else:
                return render_template('error.html', message='Violation ID not found')

    except Exception as e:
        return render_template('error.html', message=f'Error: {str(e)}')
    finally:
        connection.close()

if __name__ == "__main__":
    app.run(debug=True)
