
# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, render_template, flash, request, redirect, url_for 
import werkzeug
import os
import flask

os.environ["FLASK_DEBUG"]="1" #turn on debug mode
 
# Flask constructor takes the name of 
# current module (__name__) as argument.
UPLOAD_FOLDER = r"\app_prototype\user_input_files"
ALLOWED_EXTENSIONS = {'txt', 'fasta'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key="poep"



def allowed_file(filename):
    if "." in filename and filename.rsplit(".",1)[1].lower in ALLOWED_EXTENSIONS:
        return True
    else:
        return False
    

@app.route('/')
def home_redirect():
    return redirect(url_for("home_about_page"))


# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.
@app.route('/about', methods=["POST","GET"])
# ‘/’ URL is bound with hello_world() function.
def home_about_page():

    if request.method == "GET":
        flash("inititial visit!!!")
        return render_template("prototype_bootstrap.html")#basically the first time the homepage loads or if the page gets reloaded without user inputs.
    

    elif request.method == 'POST':#user submitted inputs
        kwargs = {
        'course': request.form['course'],
        'ec': request.form['ec'],
        'teacher': request.form['test_teacher'],} # request.form refers to the input's name in html

        user_file = request.files["user_file"] #here we define the file the user submitted as user_file

        if user_file.filename == '': #if the user submits no file, a file without a name will be submitted anyway so thi checks against that
            flash("submitted filename must contain atleast 1 character!")
            print("flasj was triggered")
            return render_template("prototype_bootstrap.html")
        
        elif user_file == True and allowed_file(user_file.filename) == True: #if the userfile is both present an has a valid extension it will continue
            secure_filename = werkzeug.utils.secure_filename(user_file.filename)# make it so the filename is secure by replacing risky characters with safe ones like a space with _
            user_file.save(os.path.join(app.root_path, secure_filename))#save the file in the apps root directory
            flash("file submitted!") # still working on the flashes
            print("flash was triggered")
            return render_template("prototype_bootstrap.html")
        else:
            flash("something wen't wrong")
            return render_template("prototype_bootstrap.html")

        
        # unpacked_kwargs = kwargs.keys()
        
        # for iterate in unpacked_kwargs:
        #     print(kwargs[iterate])
    return render_template("prototype_bootstrap.html")
            

@app.route('/download')
def download():
    outputs = os.path.abspath(os.path.join(app.root_path, "output_files\\test_output_delete_this.txt")) # generate a variable absolute path so it works on anyone's pc
    return flask.send_file(outputs, as_attachment=True)


 

@app.route('/test')
# ‘/’ URL is bound with hello_world() function.
def testing_url():
    return 'TESTIOMGWORKS!'
 

# main driver function
if __name__ == '__main__': #this statement basically checks if the file is being run directly by the user, or is being run by another file, for example for importing
    print(app.root_path)
    # run() method of Flask class runs the application 
    # on the local development server.
    app.run()


@app.route('/FIMO')
def fimo():
    return render_template()