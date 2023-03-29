
import os
from dotenv.main import load_dotenv
import openai
from flask import Flask, request, render_template,redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:@localhost/loginpage'
db=SQLAlchemy(app)



class user_details(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20),nullable=False)
    
# Set up OpenAI API credentials
load_dotenv()
openai.api_key =os.environ.get('API_KEY')

# Set up OpenAI completion engine
engine_id = "text-davinci-003"

history = []

# Login page
@app.route('/', methods=['GET', 'POST'])
def login():
    # if request.method == 'POST':
    #     # Get the username and password from the form
    #     username = request.form['username']
    #     password = request.form['password']
        
    #     # Check if the username and password are correct
    #     if username == 'electrika' and password == 'test@electrika':
    #         # If the login is successful, redirect to the home page
    #         return redirect('/home')
    #     else:
    #         # If the login is unsuccessful, render the login page with an error message
    #         return render_template('login.html', error='Invalid username or password')
    # else:
    #     # If the request method is GET, render the login page
    #     return render_template('login.html')
    if request.method == 'POST':
        # Get the username and password from the form
        email = request.form['username']
        password = request.form['password']

        # Check if the email and password are correct
        user = user_details.query.filter_by(email=email, password=password).first()
        if user:
            # If the login is successful, redirect to the home page
            return redirect('/home')
        else:
            # If the login is unsuccessful, render the login page with an error message
            return render_template('login.html', error='Invalid email or password')
    else:
        # If the request method is GET, render the login page
        return render_template('login.html')


# User registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get the email and password from the form
        email = request.form['username']
        password = request.form['password']

        # Check if the email already exists in the database
        user = user_details.query.filter_by(email=email).first()
        if user:
            # If the email already exists, render the register page with an error message
            return render_template('register.html', error='User already exists please login')
        else:
            # If the email does not exist, add the user to the database and redirect to the login page
            new_user = user_details(email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            return redirect('/')
    else:
        # If the request method is GET, render the register page
        return render_template('register.html')





@app.route('/home')
def index():
    # Render the template with the chat history
    return render_template('index.html', history=history)

@app.route('/message', methods=['POST'])
def message():
    # Get the user's message from the request
    user_message = request.form['message']

    # Send the user's message to the OpenAI completion engine
    response = openai.Completion.create(
        engine=engine_id,
        prompt=f"User: {user_message}\nAI:",
        max_tokens=250,
        n=1,
        stop=None,
        temperature=0.7
    )

    # Extract the AI's response from the OpenAI response
    ai_message = response.choices[0].text.strip()

    # Add the messages to the chat history
    history.append(('User', user_message))
    history.append(('AI', ai_message))

    # Render the template with the updated chat history
    return render_template('index.html', history=history)

# @app.route("/login",methods=['GET','POST'])
# def home():
#   if request.method=='POST':
#     email=request.form.get('username')
#     password=request.form.get('password')
    
#     entry=user_details(email=email,password=password)
#     db.session.add(entry)
#     db.session.commit()
#   return render_template("login.html")


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
