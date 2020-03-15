import os

from flask import Flask, session, request, render_template, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


def checkUserAuthStatus():
    try:
        username = session['username']
        if(len(username) >= 4):
            return True

        return False
    except KeyError:
        return False


# ==============================
#       Logged in routes
# ==============================

@app.route("/", methods=['GET', 'POST'])
def index():
    # Check if user is logged in
    if checkUserAuthStatus():
        if(request.method == 'GET'):
            return render_template('index.html', books=None)

        if(request.method == "POST"):
            query = request.form.get('query')
            criteria = request.form.get('search-criteria')
            criteria = "%" + criteria + "%"

            # Search for books
            books = db.execute('SELECT books.id as id, isbn, name AS author, title, \
                published FROM books JOIN authors ON \
                books.author_id = authors.id \
                WHERE :criteria LIKE :value', {
                "criteria": criteria,
                "value": query
                })

            # Just for debugging
            print(list(books))
            return render_template('index.html', books=books)



    return redirect('/login')


# ===========================
#    Authenticate Routes
# ===========================

@app.route('/login', methods=['GET', 'POST'])
def login():
    """ Handles User Login """

    if(request.method == "GET"):
        if checkUserAuthStatus():
            return redirect('/')

        return render_template("login.html", error=None)

    if(request.method == "POST"):
        username = request.form.get('username')
        password = request.form.get('password')

        # check for the valid username and password
        if (len(username) <= 3):
            return render_template('login.html', error="Username should be of minimum 4 characters")

        if (len(password) <= 6):
            return render_template('login.html', error="Password should be of minimum 7 characters")

        # Get user from database
        user = db.execute('SELECT username, hash FROM users WHERE username=:username AND hash=:hash', {"username": username, "hash": password})

        if len(list(user)) != 1:
            return render_template("login.html", error="User does not exists or Invalid Credentials provided.")
        else:
            session['username'] = username
            return redirect("/")

@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/signup', methods=["GET", 'POST'])
def signup():
    if(request.method == "GET"):
        # Check if user is logged in
        if checkUserAuthStatus():
            return redirect('/')

        return render_template("signup.html", error=None)

    if(request.method == "POST"):
        username = request.form.get('username')
        password = request.form.get('password')
        confirmPassword = request.form.get('confirm-password')

        # Make sure passwords match
        if(password != confirmPassword):
            return render_template("signup.html", error="Passwords do not match. please enter passwords again.")

        # check for the valid username and password
        if (len(username) <= 3):
            return render_template('signup.html', error="Username should be of minimum 4 characters")

        if (len(password) <= 6):
            return render_template('signup.html', error="Password should be of minimum 7 characters")

        # Check if user already exists with same username
        users = db.execute("SELECT username FROM users WHERE username=:username", {"username": username})

        if(len(list(users)) != 0):
            return render_template("signup.html", error="User already exists with same username.")

        # Insert the user in database
        try:
            db.execute('INSERT INTO users (username, hash) VALUES(:username, :hash)', {"username": username, "hash": password})
            db.commit()

            # Update the session
            session['username'] = username

            # Redirect the user to home page
            return redirect("/")
        except Exception as ex:
            print(ex)
            return render_template("signup.html", error="User cannot be created. Some error occured.")


        return render_template("signup.html", error=None)
