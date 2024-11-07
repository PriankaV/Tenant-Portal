from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://routes:Password9@localhost/tms_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


from flask import Flask, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db
from models import User

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'error')
            return redirect(url_for('signup'))
        
        # Create new user
        new_user = User(username=username, email=email)
        new_user.set_password(password)  # Use hashed password
        db.session.add(new_user)
        db.session.commit()
        
        flash('Account created successfully. Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        # Check if user exists and password is correct
        if user and user.check_password(password):
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password.', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/home')
def go_home():
    return render_template('home.html')

@app.route('/payments')
def payment_page():
    return render_template('Payments.html')

@app.route('/documents')
def documents_page():
    return render_template('Documents.html')

@app.route('/maintenance')
def maintenance_page():
    return render_template('Maintenance.html')

@app.route('/contacts')
def contacts_page():
    return render_template('Contacts.html')

@app.route('/notifications')
def notifications_page():
    return render_template('Notifications.html')

@app.route('/profile')
def profile_page():
    return render_template('Profile.html')


if __name__ == '__main__':
    app.run(debug=True)

