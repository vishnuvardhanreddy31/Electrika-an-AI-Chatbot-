
import openai
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:@localhost/loginpage'
db=SQLAlchemy(app)



class user_details(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20),nullable=False)
    
# Set up OpenAI API credentials
openai.api_key ="API_KEY"

# Set up OpenAI completion engine
engine_id = "text-davinci-003"

history = []

@app.route('/')
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

@app.route("/login",methods=['GET','POST'])
def home():
  if request.method=='POST':
    email=request.form.get('username')
    password=request.form.get('password')
    
    entry=user_details(email=email,password=password)
    db.session.add(entry)
    db.session.commit()
  return render_template("login.html")


if __name__ == '__main__':
    app.run(debug=True)
