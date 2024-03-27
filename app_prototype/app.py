
# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, render_template, flash, request, redirect, url_for 
import werkzeug
import os
import flask
from FIMO_MEME_Commandline import Meme, Fimo

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
            return render_template("prototype_bootstrap.html") #render template adds

        
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
 

@app.route("/fimo", methods=["POST","GET"])
def html_render_fimo():
    method = request.method
    # print(request.form)
    # print(request.form.get("default_pvalue"))
    if method == "GET":#basically the first time the homepage loads or if the page gets reloaded without user inputs. or any other page refresh without clicking the submit button.
        flash("inititial visit!!!")
        return render_template("fimopage.html") #just renders the default fimo page
    
    elif method == "POST":#user submitted inputs
        user_input_values = { #here I save all the input button values as variables
        "chosen_database": request.form["chosen_database"],
        "other_variable": request.form["other_variable"],
        "input_custom_pvalue": request.form["input_custom_pvalue"],
        "max_amount_motifs": request.form["max_amount_motifs"],
        "maxsize": request.form["maxsize"],
        "minsize": request.form["minsize"],
        } # request.form refers to the input's name in html

        if request.form.get("motif_file_option") != None: #radio buttons aren't present if they're turned off so I gotta cheeck if they are before storing them
            user_input_values["motif_file_option"] = request.form["motif_file_option"]

        if request.form.get("motif_database_option") != None:
            user_input_values["motif_database_option"] = request.form["motif_database_option"]

        if request.form.get("default_pvalue") != None: 
            user_input_values["default_pvalue"] = request.form["default_pvalue"]

        if request.form.get("custom_pvalue") != None:
            user_input_values["custom_pvalue"] = request.form["custom_pvalue"]

        input_fasta_file = request.files["input_fasta_file"] #here we define the file the user submitted as input_fasta_file
        input_motif_file = request.files["input_fasta_file"] #here we define the file the user submitted as input_motif_file

        working_dir = os.path.dirname(os.path.realpath(__file__)) # to check current dir
        output_path_fimo = "{}/User_ouput/fimo".format(working_dir)

        # execute Fimo with user parameters
        fimo = Fimo(user_input_values["motif_database_option"], user_input_values["default_pvalue"], user_input_values["custom_pvalue"], user_input_values["input_motif_file"], user_input_values["input_fasta_file"], output_path_fimo)
        #database_to_use, use_default_p_value, p_value, input_motif_file, input_sequence_path_fimo, output_path_fimo
        print(str(fimo)) # redirect to website
        fimo.run()



        if input_fasta_file.filename == "" or input_motif_file.filename == "": #if the user submits no file, a file without a name will be submitted anyway so this checks against that
            flash("submitted filename(s) must contain atleast 1 character!")
            print("submitted filename(s) must contain atleast 1 character!")
            return render_template("fimopage.html")
        
        # fimo_command, meme_command = FIMO_MEME_Commandline.input_commands(FIMO_MEME_Commandline.receive_input())
        # FIMO_MEME_Commandline.process_commands(fimo_command)
        
        


        #****** validation
        

        flash(f"file: {input_fasta_file.filename} received!!")
        

        return render_template("fimopage.html")
        
        
        
        # elif user_file == True and allowed_file(user_file.filename) == True: #if the userfile is both present an has a valid extension it will continue
        #     secure_filename = werkzeug.utils.secure_filename(user_file.filename)# make it so the filename is secure by replacing risky characters with safe ones like a space with _
        #     # user_file.save(os.path.join(app.root_path, secure_filename))#save the file in the apps root directory
        #     flash("file submitted!") # still working on the flashes
        #     return render_template("fimopage.html")
        # else:
        #     flash("something wen't wrong")
        #     return render_template("fimopage.html") #render template adds 
        flash("input received")
        return render_template("fimopage.html")


@app.route('/meme', methods=["POST","GET"])
def html_render_meme():
    method = request.method
    if method == "GET":
        flash("inititial visit!!!")
        return render_template("memePage.html") #just renders the default fimo page

    elif request.method == "POST":#user submitted inputs
            user_input_values = { #here I save all the input button values as variables
            "max_motif_amount": request.form["max_motif_amount"],
            "other_variable1": request.form["other_variable1"],
            "other_variable2": request.form["other_variable2"],
            "other_variable3": request.form["other_variable3"],
            "max_motif_size": request.form["max_motif_size"],
            "min_motif_size": request.form["min_motif_size"],
            } # request.form refers to the inputlabel's name="" in html page

            if request.form.get("seq_type_dna") != None: #radio buttons aren't present if they're turned off so I gotta cheeck if they are before storing them
                user_input_values["seq_type_dna"] = request.form["seq_type_dna"]

            if request.form.get("seq_type_rna") != None:
                user_input_values["seq_type_rna"] = request.form["seq_type_rna"]

            if request.form.get("seq_type_protein") != None: 
                user_input_values["seq_type_protein"] = request.form["seq_type_protein"]

            input_sequence_path_meme = request.files["input_user_file"] #here we define the file the user submitted as input_fasta_file
            working_dir = os.path.dirname(os.path.realpath(__file__)) # to check current dir
            output_path_meme = "{}/User_ouput/meme".format(working_dir)

            # execute Meme with user parameters
            meme = Meme(user_input_values["max_amount_of_motifs"], user_input_values["max_motif_size"], user_input_values["min_motif_size"], "dna", input_sequence_path_meme, output_path_meme)
            print(str(meme)) # redirect to website
            meme.run()


            if input_sequence_path_meme.filename == "" : #if the user submits no file, a file without a name will be submitted anyway so this checks against that
                flash("submitted filename(s) must contain atleast 1 character!")
                return render_template("memepage.html")
            

            flash("file received!!")
            return render_template("memepage.html")

# Error handeling:
@app.errorhandler(429)
def error_429():
    return "Error 429 Too Many Requests"

@app.errorhandler(500)
def error_500():
    return "Error 500: Internal Server Error"

@app.errorhandler(502)
def error_502():
    return "Error 502: Bad Gateway"

@app.errorhandler(503)
def error_503():
    return "Error 503: Service Unavailable"

@app.errorhandler(504)
def error_504():
    return "Error 504: Gateway Timeout"



# main driver function
if __name__ == '__main__': #this statement basically checks if the file is being run directly by the user, or is being run by another file, for example for importing
    print(app.root_path)
    # run() method of Flask class runs the application 
    # on the local development server.
    app.run()


