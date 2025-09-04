from flask import Flask, render_template,request,redirect, url_for, session, flash
import sqlite3
from models import db, User

#create the Flask app 
app = Flask(__name__)
app.secret_key = "your_secret_key"  # Required for session/flash
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()  # creates the tables (User in this case)
    
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered. Please log in.', 'danger')
            return redirect(url_for('login'))

        new_user = User(username=username, email=email)
        new_user.set_password(password)   # use helper instead of direct bcrypt

        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):   # use helper
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password. Please try again.', 'danger')

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])  # fetch user object
    return render_template("dashboard.html", user=user)


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))


#Define a route for the home page
@app.route('/')
def home():
    return render_template("home.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact',methods = ["GET","POST"])
def contact():
    if request.method == "POST":
        #Extract form data
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]
        ''' 
        #for testing by printing the data on terminal
        print("New Contact Form Submission:")
        print("Name:",name)
        print("email:",email)
        print("Message:",message)
        '''
        
        with open("Contacts.txt","a") as f:
            f.write(f"Name: {name}\n")
            f.write(f"Email: {email}\n")
            f.write(f"Message: {message}\n")
            f.write("-"*30 + "\n")
            
        
        return render_template("thankyou.html")
    return render_template("contact.html")

@app.route('/tracker')
def tracker():
    if 'user_id' not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for('login'))

    user_id = session['user_id']
    conn = sqlite3.connect('db/codebook.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Fetch only questions for this user
    cursor.execute("SELECT * FROM questions WHERE user_id=?", (user_id,))
    questions = cursor.fetchall()
    conn.close()

    return render_template("tracker.html", questions=questions)


@app.route('/add', methods=['GET','POST'])
def add_question():
    if 'user_id' not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form["title"]
        topic = request.form["topic"]
        status = request.form["status"]
        notes = request.form["notes"]

        conn = sqlite3.connect('db/codebook.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO questions (title, topic, status, notes, user_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (title, topic, status, notes, session['user_id']))
        conn.commit()
        conn.close()
        flash("Question added!", "success")
        return redirect(url_for('tracker'))

    return render_template('add.html')


        
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_question(id):
    if 'user_id' not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for('login'))

    conn = sqlite3.connect('db/codebook.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Fetch the question only if it belongs to this user
    cursor.execute("SELECT * FROM questions WHERE id=? AND user_id=?", (id, session['user_id']))
    question = cursor.fetchone()
    if not question:
        flash("Question not found or you can't edit it!", "danger")
        conn.close()
        return redirect(url_for('tracker'))

    if request.method == 'POST':
        title = request.form['title']
        topic = request.form['topic']
        status = request.form['status']
        notes = request.form['notes']

        cursor.execute('''
            UPDATE questions
            SET title=?, topic=?, status=?, notes=?
            WHERE id=? AND user_id=?
        ''', (title, topic, status, notes, id, session['user_id']))
        conn.commit()
        conn.close()
        flash("Question updated!", "success")
        return redirect(url_for('tracker'))

    conn.close()
    return render_template('edit.html', question=question)


@app.route('/delete/<int:id>')
def delete_question(id):
    if 'user_id' not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for('login'))

    conn = sqlite3.connect('db/codebook.db')
    cursor = conn.cursor()
    
    # Delete only if question belongs to this user
    cursor.execute("DELETE FROM questions WHERE id=? AND user_id=?", (id, session['user_id']))
    conn.commit()
    conn.close()
    
    flash("Question deleted!", "info")
    return redirect(url_for('tracker'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # create User table in site.db
    app.run(debug = True)