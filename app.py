import csv
import hashlib
import logging
import subprocess
import ssl
import certifi
import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from pymongo import MongoClient
from bson import ObjectId
app = Flask(__name__)

# MongoDB Setup
client = MongoClient( HERE REPLACE WITH YOUR MONGODB URI, ssl_cert_reqs=ssl.CERT_NONE)
mongoDB = client['Bulk_Database']
collection = mongoDB['User_info']
collection2 = mongoDB['Detailed']
collection3 = mongoDB['Templates']
users_collection = mongoDB['users_credentials']

app.config['UPLOAD_FOLDER'] = 'uploads'
# CSV File Handling Function
def read_csv_and_save(file_path):
    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            mongo_user = {"name": row['first_name'], "surname": row['last_name'], "phone": row['phone']}
            collection.insert_one(mongo_user)

@app.route("/")
def index():
    mongoDB_users = list(collection.find())
    mongoDB_users1 = [{**user, '_id': str(user['_id'])} for user in mongoDB_users]

    mongoDB_users2 = list(collection2.find())
    mongoDB_users2 = [{**user, '_id': str(user['_id'])} for user in mongoDB_users2]

    mongoDB_users3 = list(collection3.find())
    mongoDB_users3 = [{**user, '_id': str(user['_id'])} for user in mongoDB_users3]
    return render_template('login.html', userInfo=mongoDB_users1, userDetails=mongoDB_users2, templates=mongoDB_users3)


# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Basic validation
        if password != confirm_password:
            return "Passwords do not match!", 400

        # Hash the password for security
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Insert user into MongoDB
        users_collection.insert_one({
            'name': name,
            'email': email,
            'hash_password': hashed_password,
            'password': password
        })
        return render_template('login.html')

    return render_template('signup.html')

# Login route placeholder (replace with your login logic)
# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email =  request.form.get('email')
        password = request.form.get('password')

        # Hash the password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Check if the user exists in MongoDB
        user = users_collection.find_one({"email": email, "password": hashed_password})
        if user:
            session['user_id'] = str(user['_id'])  # Store user ID in session
            return redirect(url_for('dashboard'))
        else:
            return "Invalid email or password!", 401

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        mongoDB_users1 = list(collection.find())
        mongoDB_users1 = [{**user, '_id': str(user['_id'])} for user in mongoDB_users1]

        mongoDB_users2 = list(collection2.find())
        mongoDB_users2 = [{**user, '_id': str(user['_id'])} for user in mongoDB_users2]

        mongoDB_users3 = list(collection3.find())
        mongoDB_users3 = [{**user, '_id': str(user['_id'])} for user in mongoDB_users3]
        return render_template('dashboard.html', userInfo=mongoDB_users1, userDetails=mongoDB_users2, templates=mongoDB_users3)
    else:
        return redirect(url_for('login'))

@app.route('/details', methods=['GET', 'POST'])
def details():
    if request.method == 'POST':
        first_name = request.form.get('name')
        last_name = request.form.get('surname')
        phone = request.form.get('phone')

        if 'file' in request.files:
            uploaded_file = request.files['file']
            if uploaded_file.filename != '':
                if not os.path.exists(app.config['UPLOAD_FOLDER']):
                    os.makedirs(app.config['UPLOAD_FOLDER'])
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
                uploaded_file.save(file_path)
                read_csv_and_save(file_path)

        elif first_name and last_name and phone:
            mongo_user = {"name": first_name, "surname": last_name, "phone": phone}
            collection.insert_one(mongo_user)

        return redirect(url_for('details'))

    mongoDB_users = list(collection.find())
    mongoDBuser = [{**user, '_id': str(user['_id'])} for user in mongoDB_users]
    return render_template('details.html', mongoDBuser=mongoDBuser)

@app.route('/delete_info2/<string:user_id>', methods=['POST'])
def delete_info2(user_id):
    collection2.delete_one({"_id": ObjectId(user_id)})
    return redirect(url_for('dashboard'))

@app.route('/delete_info/<string:user_id>', methods=['POST'])
def delete_info(user_id):
    collection.delete_one({"_id": ObjectId(user_id)})
    return redirect(url_for('details'))

@app.route('/delete_template/<string:template_id>', methods=['POST'])
def delete_template(template_id):
    collection3.delete_one({"_id": ObjectId(template_id)})
    return redirect(url_for('templates'))

@app.route('/update_info', methods=['POST'])
def update_info():
    user_id = request.form['user_id']
    name = request.form['name']
    surname = request.form['surname']
    phone = request.form['phone']

    collection.update_one(
            {"_id": ObjectId(user_id)},
            {
                "$set": {
                    "name": name,
                    "surname": surname,
                    "phone": phone,
                }
            }
        )
    return redirect(url_for('details'))

@app.route('/add_dashboard_user_data', methods=['POST'])
def add_dashboard_user_data():
    if request.method == 'POST':
        message_template = request.form['message']
        if not message_template:
            return redirect(url_for('run_script'))

        mongoDB_users = list(collection.find())
        for user in mongoDB_users:
            message = (
                message_template
                       .replace("[Name]", user['name'])
                       .replace("[Surname]", user['surname'])
                       .replace("[Phone]", user['phone'])
            )
            detailed = {
                "firstName": user['name'],
                "lastName": user['surname'],
                "phoneNumber": user['phone'],
                "Send_message": message,
                "status": "Pending",
                "sent_timestamp": "00-00-00"
            }
            collection2.insert_one(detailed)

        return redirect(url_for('run_script'))

@app.route('/run_script')
def run_script():
    subprocess.Popen(['python', 'process.py'])
    return redirect(url_for('dashboard'))


@app.route('/templates', methods=['GET', 'POST'])
def templates():
    if request.method == 'POST':
        print(request.form)
        new_template = request.form.get('templateText')

        if new_template:
            template_type = request.form.get('template_type', 'user_design')
            collection3.insert_one({"template": new_template, "templateTypes": template_type})

        return redirect(url_for('templates'))

    mongoDB = list(collection3.find())
    templatesDB = [{**user, '_id': str(user['_id'])} for user in mongoDB]
    return render_template('templates.html', templatesDB=templatesDB)


@app.route('/sending')
def sending():
    return render_template('sending.html')


if __name__ == "__main__":
    app.run(debug=True, port=8080)
