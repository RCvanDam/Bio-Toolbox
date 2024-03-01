
# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, render_template

import os

os.environ["FLASK_DEBUG"]="1" #turn on debug mode
 
# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__)
 
# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.
@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def homepage():
    return render_template("page.html")
 

@app.route('/test')
# ‘/’ URL is bound with hello_world() function.
def testing_url():
    return 'TESTIOMGWORKS!'
 

# main driver function
if __name__ == '__main__':   #this statement basically checks if the file is being run directly by the user, or is being run by another file, for example for importing
 
    # run() method of Flask class runs the application 
    # on the local development server.
    app.run()

