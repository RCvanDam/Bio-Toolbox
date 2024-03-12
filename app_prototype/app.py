
# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, render_template, flash, request, redirect, url_for # delete werkzeug and reinstall it's 2.2 version
import werkzeug
import os
import flask

os.environ["FLASK_DEBUG"]="1" #turn on debug mode
 
# Flask constructor takes the name of 
# current module (__name__) as argument.
UPLOAD_FOLDER = "\\app_prototype\\user_input_files"
ALLOWED_EXTENSIONS = {'txt', 'fasta'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    if "." in filename and filename.rsplit(".",1)[1].lower in ALLOWED_EXTENSIONS:
        return True
    else:
        return False
 
# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.
@app.route('/', methods=["POST","GET"])
# ‘/’ URL is bound with hello_world() function.
def homepage():
    print("this is the app.root folder from homepage",app.root_path)
    if request.method == "GET":
        return render_template("prototype.html")
    elif request.method == 'POST':

        
        # response when the submit button is clicked in the 'form/form_GET.html'
        # pack the variables in a dictionary
        kwargs = {
        'course': request.form['course'],
        'ec': request.form['ec'],
        'teacher': request.form['test_teacher'],} # request.form refers to the input's name in html
        user_file = request.files["user_file"]
        filename = werkzeug.utils.secure_filename(user_file.filename)
        user_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) #saves the file under a new secure filename.
        unpacked_kwargs = kwargs.keys()
        
        for iterate in unpacked_kwargs:
            print(kwargs[iterate])
        return render_template("prototype.html")
            

@app.route('/download')
def download():
    uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    outputs = os.path.join(app.root_path, "output_files\\test_output_delete_this.txt")
    return flask.send_file(outputs, as_attachment=True)


 

@app.route('/test')
# ‘/’ URL is bound with hello_world() function.
def testing_url():
    return 'TESTIOMGWORKS!'
 

# main driver function
if __name__ == '__main__':   #this statement basically checks if the file is being run directly by the user, or is being run by another file, for example for importing
    
    # run() method of Flask class runs the application 
    # on the local development server.
    app.run()
    print("this is the app.root folder",app.root_path)

