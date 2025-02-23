from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

# Initialize the Flask app
app = Flask(__name__)

# Configure the database URI using an environment variable or directly
# Replace the placeholders below with your actual Supabase connection string
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://your_username:your_password@db.ubdzkaghanlqwecskcvl.supabase.co:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Define a simple model
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f'<Item {self.name}>'

# Home route
@app.route('/')
def home():
    items = Item.query.all()  # Fetch all items from the database
    return render_template('index.html', items=items)

# Add item route
@app.route('/add-item', methods=['POST'])
def add_item():
    name = request.form['name']
    description = request.form.get('description', '')  # Optional field
    new_item = Item(name=name, description=description)
    db.session.add(new_item)
    db.session.commit()
    return redirect(url_for('home'))

# Delete item route
@app.route('/delete-item/<int:item_id>')
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
