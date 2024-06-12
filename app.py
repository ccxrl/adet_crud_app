from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL



app = Flask(__name__)
app.secret_key = 'secret'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask_crud'

mysql = MySQL(app)


@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM patients")
    data = cur.fetchall()
    cur.close()
    
    return render_template('index2.html', patients=data)


# add a patient (ADD API)
@app.route('/insert', methods = ['POST'])
def insert():

    if request.method == "POST":
        flash("Data Inserted Successfully")
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO patients (name, email, phone) VALUES (%s, %s, %s)", (name, email, phone))
        mysql.connection.commit()
        return redirect(url_for('Index'))
    

# delete a patient (DELETE API)
@app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM patients WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('Index'))


# edit patient details (UPDATE API)
@app.route('/update',methods=['POST','GET'])
def update():

    if request.method == 'POST':
        id_data = request.form['id']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        cur = mysql.connection.cursor()
        cur.execute("""
               UPDATE patients
               SET name=%s, email=%s, phone=%s
               WHERE id=%s
            """, (name, email, phone, id_data))
        flash("Data Updated Successfully")
        mysql.connection.commit()
        return redirect(url_for('Index'))
    
    
# view patient (GET API)
@app.route('/view/<int:patient_id>')
def view_patient(patient_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM records WHERE patient_id = %s", (patient_id,))
    records = cur.fetchall()
    cur.close()
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM patients WHERE id = %s", (patient_id,))
    patient = cur.fetchone()
    cur.close()
    if patient:
        return render_template('view_patient.html', patient=patient, records=records)
    else:
        flash("Patient not found")
        return redirect(url_for('Index'))


if __name__ == "__main__":
    app.run(debug=True)