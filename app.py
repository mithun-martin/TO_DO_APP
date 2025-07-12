from flask import Flask, render_template, request, redirect
#👉 This imports Flask (the web framework), render_template (to show HTML pages), and request (to read form data sent by user).
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
#1)👉 This creates your Flask application object — it runs your web server.

#to itialize sql alchemy" the followig line suse chatgpt or  documentatons neo need to byehart
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./todo.db'
#👉 This tells Flask where your database will be.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  #dont think much here


#2)SETTING UP THE DATABASE  
db = SQLAlchemy(app)
#📌 What is SQLAlchemy here?
#It’s the ORM (Object Relational Mapper) you’re using to connect your Python code to a database.
#In this case, you’re using SQLite as the database, and SQLAlchemy is the library that lets you interact with it via Python classes instead of raw SQL queries.
#the line here ✅ Initializes SQLAlchemy for your Flask app.

#3)initializing model class
class ToDo(db.Model):
    #👉 A Python class defining your ToDo table basically MODEL LIEK IN SB
    sno = db.Column(db.Integer,primary_key = True) #defining the primary key
    title = db.Column(db.String(200), nullable = False)
    desc = db.Column(db.String(500),nullable = False)
    comment = db.Column(db.String(200))      # ✅ New
    status = db.Column(db.String(50), nullable=False, default="None")        # ✅ New
    date_created = db.Column(db.DateTime,default = datetime.now)

    # def __repr__(self) -> str: #not much think agin
    #     return f"{self.sno} - {self.title}"
    #__repr__ is a special method in Python used to define what the "official string representation" of an object should be 
    #(what you see when you type print(todo) in consle fore easy debuggig



#4)defining routes
@app.route("/",methods =["GET", "POST"])
def create_read():
    #✅ What happens when the browser sends a GET request (like when you first visit localhost:5000/)
    #The if request.method == 'POST': block is skipped and alltodo = ToDo.query.all() runs
    #👉 It queries all records from the ToDo table and stores them in allToDo
    #👉 It renders the page and passes your to-do list data to the template for display


    #🔥 So short answer:
    #Yes — ToDo.query.all() is for handling the GET part of the request, both after a form submission and when the page first loads.

    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        status = request.form['status']        # ✅ New
        #get title and desc from form
        todo = ToDo(title=title, desc=desc , status = status) #other 2 automatcaly comes
        #create a new todo object and then adding to database but we dont do in update isnce we dot wnat a new rcrd
        db.session.add(todo)
        db.session.commit()
       
    allToDo = ToDo.query.all()  #dont byheart check for the query code in google
    #👉 Fetch all to-do items from the database.
    return render_template("index.html", allToDo = allToDo) 
    #👉 Open index.html and pass the list of to-do items to it as allToDo




@app.route("/update/<int:sno>",methods=["GET","POST"])
def update(sno):
    todo = ToDo.query.get_or_404(sno) #furst gets the get request chekc for no then it goes to the return render_html part
    #which means u can chekc the a code as well of fromnend opens a new form for us to tyep new title and desc only
    #wehen  we press update button in that /update page then the post request will be activates and if block will run and after entry it will rdirect to homepage
    if request.method == "POST":
        todo.title = request.form["title"]
        todo.desc = request.form["desc"]
        todo.status = request.form["status"]
        db.session.commit()
        return redirect("/")
    
    return render_template("update.html", todo=todo)

# 📌 Why create `update.html` separately?

# Because it’s a different page.
# When you click the Update button, it:

# * opens a new page
# * shows a form with current values filled
# * allows you to edit and submit it

# So — that page needs its own HTML template to display.

# 👉 That’s why we created
# `templates/update.html`



# 📌 First: What happens when you click the Update button in your table now?
# Current flow:

# 1️⃣ You click
# <a href="/update/{{ todo.sno }}">Update</a>
# 👉 Browser sends a GET request to /update/3 (for example)
# 👉 Flask runs the GET part of this:

# todo = ToDo.query.get_or_404(sno)
# return render_template("update.html", todo=todo)



# 📌 Now: What happens when you submit the update form on that page?
# 👉 That form sends a POST request to the same /update/<sno> URL
# 👉 Flask runs this part:

# 👉 Updates the data in the database
# 👉 Then redirects back to the homepage /


# 📌 Why redirect to / after POST?
# Because otherwise, after updating, you’d still be sitting on the /update/<sno> page.



@app.route("/delete/<int:sno>")
def delete(sno):
    record = ToDo.query.filter_by(sno=sno).first() #first() to delte the first record which matches
    db.session.delete(record)
    db.session.commit()
    return redirect("/") #after deleting coem to back to slash ie the sam epage home



if __name__ == "__main__":
   app.run(debug = True)

   #THESE LINES TELL APP TO RUN AND IN DEBUGGER MODE SO THAT IF ANY ERRO HAPPENS IT WILLL BE SHOW IN BROWSER