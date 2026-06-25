from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from ai_service import get_health_prediction
from dotenv import load_dotenv
import os
import re


load_dotenv()


app = Flask(__name__)


# Database Configuration

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///patients.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)



# -----------------------------
# Patient Model
# -----------------------------

class Patient(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    full_name = db.Column(
        db.String(100),
        nullable=False
    )

    dob = db.Column(
        db.Date,
        nullable=False
    )

    email = db.Column(
        db.String(100),
        nullable=False
    )

    glucose = db.Column(
        db.Float,
        nullable=False
    )

    hemoglobin = db.Column(
        db.Float,
        nullable=False
    )

    cholesterol = db.Column(
        db.Float,
        nullable=False
    )

    risk = db.Column(
        db.String(50)
    )

    remarks = db.Column(
        db.Text
    )



# -----------------------------
# Email Validation
# -----------------------------

def validate_email(email):

    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    return re.match(pattern,email)



# -----------------------------
# Extract Risk From Gemini
# -----------------------------

def extract_risk(result):

    result = result.lower()

    if "high risk" in result:
        return "High Risk"

    elif "medium risk" in result:
        return "Medium Risk"

    else:
        return "Low Risk"




# -----------------------------
# Home Page READ
# -----------------------------

@app.route("/")
def index():

    patients = Patient.query.all()

    return render_template(
        "index.html",
        patients=patients
    )




# -----------------------------
# CREATE Patient
# -----------------------------

@app.route("/add", methods=["GET","POST"])
def add_patient():


    if request.method == "POST":


        try:

            dob = datetime.strptime(
                request.form["dob"],
                "%Y-%m-%d"
            ).date()


            if dob > date.today():

                return "DOB cannot be future date"


            email = request.form["email"]


            if not validate_email(email):

                return "Invalid email format"



            glucose=float(
                request.form["glucose"]
            )


            hemoglobin=float(
                request.form["hemoglobin"]
            )


            cholesterol=float(
                request.form["cholesterol"]
            )



        except Exception:

            return "Please enter valid data"



        # Gemini API Call

        try:

            ai_response = get_health_prediction(
                glucose,
                hemoglobin,
                cholesterol
            )


            risk = extract_risk(
                ai_response
            )


        except Exception as e:

            risk="Prediction Failed"

            ai_response=str(e)



        patient = Patient(

            full_name=request.form["full_name"],

            dob=dob,

            email=email,

            glucose=glucose,

            hemoglobin=hemoglobin,

            cholesterol=cholesterol,

            risk=risk,

            remarks=ai_response
        )


        db.session.add(patient)

        db.session.commit()


        return redirect(
            url_for("index")
        )


    return render_template(
        "add.html"
    )




# -----------------------------
# UPDATE Patient
# -----------------------------

@app.route("/edit/<int:id>", methods=["GET","POST"])
def edit_patient(id):


    patient = Patient.query.get_or_404(id)



    if request.method=="POST":


        patient.full_name = request.form["full_name"]

        patient.email = request.form["email"]


        patient.glucose=float(
            request.form["glucose"]
        )


        patient.hemoglobin=float(
            request.form["hemoglobin"]
        )


        patient.cholesterol=float(
            request.form["cholesterol"]
        )



        # Call Gemini again after update

        ai_response = get_health_prediction(

            patient.glucose,

            patient.hemoglobin,

            patient.cholesterol

        )


        patient.risk = extract_risk(
            ai_response
        )


        patient.remarks = ai_response



        db.session.commit()



        return redirect("/")



    return render_template(
        "edit.html",
        patient=patient
    )





# -----------------------------
# DELETE Patient
# -----------------------------

@app.route("/delete/<int:id>")
def delete_patient(id):


    patient = Patient.query.get_or_404(id)


    db.session.delete(patient)

    db.session.commit()


    return redirect("/")





# -----------------------------
# Create Database
# -----------------------------

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True,port=8000)