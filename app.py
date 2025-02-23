from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import requests
import joblib

app = Flask(__name__)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://<your-database-url>'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define a simple User model (for demonstration purposes)
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api-data')
def api_data():
    response = requests.get('https://jsonplaceholder.typicode.com/posts')
    posts = response.json()
    return render_template('api_data.html', posts=posts)

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    model = joblib.load('model.pkl')
    if request.method == 'POST':
        input_value = float(request.form['input'])
        prediction = model.predict([[input_value]])
        return f"The predicted value is {prediction[0]:.2f}"
    return render_template('predict.html')

@app.route('/add-item', methods=['POST'])
def add_item():
    name = request.form['name']
    description = request.form['description']
    new_item = Item(name=name, description=description)
    db.session.add(new_item)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
