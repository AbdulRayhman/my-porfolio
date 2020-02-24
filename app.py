import csv
from flask import render_template, request, url_for, redirect, Blueprint, Flask
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail
import os

app = Flask(__name__, template_folder='templates')
ENV = 'pro'
if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/portfolio'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://rlpszxythocamh:76086121639d63ff015b7f3f14b6a6cd55e5ebc03292984694c32bbf31253fe5@ec2-52-23-14-156.compute-1.amazonaws.com:5432/d4264cjl2tikd3'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Contact(db.Model):
    __tablename__ = 'contact_data'
    id = db.Column(db.Integer,  primary_key=True)
    email = db.Column(db.String(200), unique=True)
    subject = db.Column(db.String(300))
    message = db.Column(db.String(500))

    def __init__(self, email, subject, message):
        super().__init__()
        self.email = email
        self.subject = subject
        self.message = message


@app.route('/')
def home_page():
    return render_template('index.html')


@app.route('/<string:page_name>')
def html_pages(page_name: None):
    return render_template(page_name)


def write_data_to_database(data):
    try:
        if data['email'] == '' or data['subject'] == '' or data['message'] == '':
            return render_template('contact.html', errorMessage='Please enter the required fields!')
        else:
            if db.session.query(Contact).filter(Contact.email == data['email']).count() == 0:
                dbData = Contact(
                    data['email'], data['subject'], data['message'])
                db.session.add(dbData)
                db.session.commit()
                send_mail(
                    data['email'], data['subject'], data['message'])
                return redirect('thank-you.html')
            else:
                return render_template('contact.html', errorMessage='Email already exist!')

    except:
        return redirect('index.html')


@app.route('/submit_form', methods=['POST', 'GET'])
def form_submit():
    data = request.form.to_dict()
    try:
        return write_data_to_database(data)
    except:
        return redirect('index.html')


if __name__ == '__main__':
    app.run()
