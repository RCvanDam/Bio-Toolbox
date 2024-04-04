# 2 apr 2024
# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.

from flask import Flask, render_template, flash, request, redirect, url_for
import werkzeug
import os
import flask
from FIMO_MEME_Commandline import Meme, Fimo
import sys
from werkzeug.middleware.profiler import ProfilerMiddleware
import cProfile, pstats



os.environ["FLASK_DEBUG"] = "1"  # turn on debug mode

CORRECT_OS = True

# Flask constructor takes the name of 
# current module (__name__) as argument.
UPLOAD_FOLDER = r"\app_prototype\user_input_files"
ALLOWED_EXTENSIONS = {'txt', 'fasta'}
WORKING_DIR = os.path.dirname(os.path.realpath(__file__)) # to check current dir



app = Flask(__name__)
app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=('/app.py',))

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "poep"

OUTPUT_FOLDER = WORKING_DIR + r"\user_output"
UPLOAD_FOLDER = WORKING_DIR + r"\user_input_files"

HUMAN_DATABASE_OPTION_ = WORKING_DIR + r"/Motif_databases/HOCOMOCOv11_full_HUMAN_mono_meme_format.meme"
MOUSE_DATABASE_OPTION_ = WORKING_DIR + r"/Motif_databases/HOCOMOCOv11_full_MOUSE_mono_meme_format.meme"
FLY_DATABASE_OPTION_ = WORKING_DIR + r"/Motif_databases/OnTheFly_2014_Drosophila.meme"
ECOLI_DATABASE_OPTION_ = WORKING_DIR + r"/Motif_databases/SwissRegulon_e_coli.meme"
JASPAR_DATABASE_OPTION_ = WORKING_DIR + r"/Motif_databases/SwissRegulon_human_and_mouse.meme"


def allowed_file(filename):
    if "." in filename and filename.rsplit(".", 1)[1].lower in ALLOWED_EXTENSIONS:
        return True
    else:
        return False


def correct_os():

    """
    reusable function to flash on every page
    the fact that the use of the tool is not possible on the current os
    """
    if not CORRECT_OS:
        flash("""This operating system is not compatible with our tool, 
              refer to the readme for the system requirements""")
        flash("""This operating system is not compatible with our tool, 
              refer to the readme for the system requirements""")


@app.route('/')
def home_redirect():
    return redirect(url_for("home_about_page"))


# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.
@app.route('/about', methods=["POST","GET"])
# ‘/’ URL is bound with hello_world() function.
def home_about_page():
    correct_os()

    if request.method == "GET":
        return render_template("prototype_bootstrap.html")
        #basically the first time the homepage loads or if the page gets reloaded without user inputs.



            

@app.route('/download')
def download():
    outputs = os.path.abspath(os.path.join(app.root_path, "output_files\\test_output_delete_this.txt")) # generate a variable absolute path so it works on anyone's pc
    return flask.send_file(outputs, as_attachment=True)


 

@app.route("/fimo", methods=["POST","GET"])
def html_render_fimo():
    correct_os()
    method = request.method
    # print(request.form)
    # print(request.form.get("default_pvalue"))

    #the page loading without any forms being submitted
    if method == "GET":
        return render_template("fimopage.html") #just renders the default fimo page
    
    elif method == "POST":#user submitted inputs

        user_input_values = { #here I save all the input button values as variables
        "chosen_database": request.form["chosen_database"],
        "input_custom_pvalue": request.form["input_custom_pvalue"],
        "max_amount_motifs": request.form["max_amount_motifs"],
        "maxsize": request.form["maxsize"],
        "minsize": request.form["minsize"],
        } # request.form refers to the input's name in html
        
        print("|",request.form["chosen_database"],"|")

        motif_file_option = request.form.get("motif_file_option")
        motif_database_option = request.form.get("motif_database_option")
        default_pvalue = request.form.get("default_pvalue")
        custom_pvalue = request.form.get("custom_pvalue")

        
        #checking if neither of the motif options have been chosen.
        if motif_file_option == None and motif_database_option == None: 
            flash("a motif option must be chosen")
            return render_template("fimopage.html")

        #checking if both motif options have been chosen.
        if motif_file_option != None and motif_database_option != None:
            flash("only one motif option can be chosen")
            return render_template("fimopage.html")
        
        #checking if neither of the pvalue options have been chosen.
        if default_pvalue == None and custom_pvalue == None:
            flash("a pvalue option must be chosen")
            return render_template("fimopage.html")
        
        #checking if both pvalue options have been chosen.
        if custom_pvalue != None and default_pvalue != None:
            flash("only one p value option can be chosen")
            return render_template("fimopage.html")
        
        #radio buttons aren't present if they're turned off so I gotta check if they are before storing them
        if motif_file_option != None: 
            user_input_values["motif_file_option"] = motif_file_option

        #temporarily putting it on on anyways because the tool won't work otherwise for now
        else:
            user_input_values["motif_database_option"] = "on" 
            
        if default_pvalue != None: 
            user_input_values["default_pvalue"] = default_pvalue

        else:
            user_input_values["default_pvalue"] = True

        if custom_pvalue != None:
            user_input_values["custom_pvalue"] = request.form["custom_pvalue"]

        if motif_database_option != None:
            user_input_values["motif_database_option"] = motif_database_option

            #checking to see if a database has been chosen if the database option is on
            if user_input_values["chosen_database"] == "PLease select a database to use":
                flash("please select a database to use")
                return render_template("fimopage.html")
            
            #replacing the value in user_input_values with the path to the motif files
            elif user_input_values["chosen_database"] == "Human":
                user_input_values["chosen_database"] = HUMAN_DATABASE_OPTION_
            elif user_input_values["chosen_database"] == "Mouse":
                user_input_values["chosen_database"] = MOUSE_DATABASE_OPTION_
            elif user_input_values["chosen_database"] == "Drosophilla (fly)":
                user_input_values["chosen_database"] = FLY_DATABASE_OPTION_
            elif user_input_values["chosen_database"] == "E.coli (Bacterium)":
                user_input_values["chosen_database"] = ECOLI_DATABASE_OPTION_
            elif user_input_values["chosen_database"] == "Jaspar":
                user_input_values["chosen_database"] = JASPAR_DATABASE_OPTION_

        #temporarily putting it on on anyways because the tool won't work otherwise for now
        else:
            user_input_values["motif_database_option"] = "on" 


         #here we define the files the user submitted.
        input_fasta_file = request.files["input_fasta_file"]
        input_motif_file = request.files["input_motif_file"]

        output_path_fimo = "{}/User_ouput/fimo".format(WORKING_DIR)

        #if the user submits no file, 
        #a file without a name will be submitted anyway
        #so this checks against that
        if input_fasta_file.filename == "" or input_motif_file.filename == "":
            flash("submitted filename(s) must contain atleast 1 character!")
            return render_template("fimopage.html")
        
        # execute Fimo with user parameters
        fimo = Fimo(user_input_values["motif_database_option"], 
                    user_input_values["default_pvalue"], 
                    user_input_values["custom_pvalue"], 
                    input_motif_file, input_fasta_file, 
                    output_path_fimo)
        #database_to_use, use_default_p_value, p_value, input_motif_file, input_sequence_path_fimo, output_path_fimo
        
        #fimo output for commandline terminal to check input variables
        print(str(fimo))
        fimo.run()


        #confirmation for front end that the files have been received
        flash(f"file: {input_fasta_file.filename} received!!")
        
        #redirects to the path for fimo's html output
        return redirect(url_for("render_fimo_output_html"))
        
        
        
        # elif user_file == True and allowed_file(user_file.filename) == True: #if the userfile is both present an has a valid extension it will continue
        #     secure_filename = werkzeug.utils.secure_filename(user_file.filename)# make it so the filename is secure by replacing risky characters with safe ones like a space with _
        #     # user_file.save(os.path.join(app.root_path, secure_filename))#save the file in the apps root directory
        #     flash("file submitted!") # still working on the flashes
        #     return render_template("fimopage.html")
        # else:
        #     flash("something wen't wrong")
        #     return render_template("fimopage.html") #render template adds 



@app.route('/meme', methods=["POST","GET"])
def html_render_meme():
    correct_os()
    method = request.method
    if method == "GET":
        flash("inititial visit!!!")
        return render_template("memePage.html") #just renders the default fimo page

    elif request.method == "POST":#user submitted inputs
        user_input_values = { #here I save all the input button values as variables
        "max_amount_of_motifs": request.form["max_amount_of_motifs"],
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
        output_path_meme = "{}/User_ouput/meme".format(WORKING_DIR)

        # execute Meme with user parameters
        meme = Meme(user_input_values["max_amount_of_motifs"], user_input_values["max_motif_size"], user_input_values["min_motif_size"], "dna", input_sequence_path_meme, output_path_meme)
        print(str(meme)) # redirect to website
        meme.run()


        if input_sequence_path_meme.filename == "" : #if the user submits no file, a file without a name will be submitted anyway so this checks against that
            flash("submitted filename(s) must contain atleast 1 character!")
            return render_template("memepage.html")
        

        flash("file received!!")
        return redirect(url_for("render_meme_output_html"))



@app.route('/fimo_output')
def render_fimo_output_html():
    """ Route to show the FIMO output"""
    
    
    return render_template("fimo.html")


@app.route('/meme_output')
def render_meme_output_html():
    """ Route to show the FIMO output"""
    return



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
    if sys.platform.startswith("linux") == False:
        CORRECT_OS = False
    profiler = cProfile.Profile()
    profiler.enable()
    app.run()
    profiler.disable()
    profiler.dump_stats("app.prof")

    results = pstats.Stats(profiler)
    results.print_stats()


    # run() method of Flask class runs the application
    # on the local development server.


