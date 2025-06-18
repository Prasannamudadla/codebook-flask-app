from flask import Flask, render_template,request,redirect
import sqlite3

#create the Flask app 
app = Flask(__name__)

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
    conn = sqlite3.connect('db/codebook.db') 
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * from questions")
    questions = cursor.fetchall()
    
    conn.close()
    return render_template("tracker.html",questions = questions)

@app.route('/add',methods = ['GET','POST'])
def add_question():
    if request.method == 'POST':
        title = request.form["title"]
        topic = request.form["topic"]
        status = request.form["status"]
        notes = request.form["notes"]
        
        conn = sqlite3.connect('db/codebook.db')
        cursor = conn.cursor()
        cursor.execute(''' 
                    INSERT INTO questions (title,topic,status,notes)
                    VALUES(?,?,?,?)   
                ''',(title,topic,status,notes))
        conn.commit()
        conn.close()
        return redirect('/tracker')
    return render_template('add.html')



        
@app.route('/edit/<int:id>',methods = ['GET','POST'])
def edit_question(id):
    conn = sqlite3.connect('db/codebook.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    if request.method == 'POST':
        title = request.form['title']
        topic = request.form['topic']
        status =request.form['status']
        notes = request.form['notes']
        
        cursor.execute(''' 
                       UPDATE questions
                       SET title = ?,topic = ?,status = ?,notes = ?
                       WHERE id = ?
                       ''',(title,topic,status,notes,id))
        
        conn.commit()
        conn.close()
        return redirect('/tracker')

    #GET request - fetch question data to prefill form
    cursor.execute('SELECT * FROM questions WHERE id = ?',(id,))
    question = cursor.fetchone()
    conn.close()
    return render_template('edit.html',question = question)

@app.route('/delete/<int:id>')
def delete_question(id):
    conn = sqlite3.connect('db/codebook.db')
    cursor =conn.cursor()
    cursor.execute("DELETE FROM questions WHERE id = ?",(id,))
    conn.commit()
    conn.close()
    return redirect('/tracker')

if __name__ == '__main__':
    app.run(debug = True)