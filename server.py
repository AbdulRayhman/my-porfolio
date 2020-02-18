import csv
from flask import render_template, request, url_for, redirect, Blueprint, Flask
from flask_pymongo import PyMongo
import  os

app = Flask(__name__, template_folder='templates')
app.config['APP'] = 'server'
app.config['DEBUG'] = True
# MONGO_URI = os.environ.get('MONGO_URI')
# print(MONGO_URI)
# app.config.from_object('some string')
app.config["MONGO_URI"] = 'mongodb+srv://abdulrehmanFrt:abdulrehmanFrt@userdb-tywac.mongodb.net/portfolio?retryWrites=true&w=majority'
mongo = PyMongo(app)

@app.route('/')
def home_page():
    return render_template('index.html')


@app.route('/<string:page_name>')
def html_pages(page_name: None):
    return render_template(page_name)

def write_data_to_database(data):
    try:
        portfolio_collection = mongo.db.contacts
        portfolio_collection.insert({
            'email ': data['email'],
            'subject ': data['subject'],
            'message ': data['message'],
        })
        return redirect('thank-you.html')
    except:
        return redirect('index.html')


@app.route('/submit_form', methods=['POST', 'GET'])
def form_submit():
    data = request.form.to_dict()
    print(data)
    try:
        return write_data_to_database(data)
    except:
        return redirect('index.html')



if __name__ == '__main__':
    app.run(debug=True)