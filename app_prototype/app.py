
# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, render_template, flash, request, redirect, url_for, werkzeug

import os

os.environ["FLASK_DEBUG"]="1" #turn on debug mode
 
# Flask constructor takes the name of 
# current module (__name__) as argument.
UPLOAD_FOLDER = "\app_prototype\user_input_files"
ALLOWED_EXTENSIONS = {'txt', 'fasta'}

werkzeug.secure_filename()
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    if "." in filename and filename.rsplit(".",1)[1].lower in ALLOWED_EXTENSIONS:
        return True
    else:
        return False


    # return '.' in filename and \
    #        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

 
# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.
@app.route('/', methods=["POST","GET"])
# ‘/’ URL is bound with hello_world() function.
def homepage():
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        else:
            file = request.files["file"]
        if file.filename == '': #if the user submits no file, a file without a name will be submitted anyway so thi checks against that
            flash("No selected file")
            return redirect(request.url)
        if file == True and allowed_file(file.filename) == True:
            filename = werkzeug.utils.secure_filename(file.filename)
            if filename == "":
                flash("we're still working on this filename error!")
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) #saves the file under a new secure filename.
            return redirect(url_for('download_file', name=filename)) # to be edited


    return render_template("prototype.html")
 

@app.route('/test')
# ‘/’ URL is bound with hello_world() function.
def testing_url():
    return 'TESTIOMGWORKS!'
 

# main driver function
if __name__ == '__main__':   #this statement basically checks if the file is being run directly by the user, or is being run by another file, for example for importing
    
    # run() method of Flask class runs the application 
    # on the local development server.
    app.run()

