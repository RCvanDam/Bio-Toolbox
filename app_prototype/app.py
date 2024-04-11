# 4 apr 2024

import os
import flask
import sys
from pathlib import Path
from FIMO_MEME_Commandline import Meme, Fimo
from werkzeug.utils import secure_filename
from werkzeug.middleware.profiler import ProfilerMiddleware
from flask import Flask, render_template, flash, request, redirect, url_for, helpers, session

MOTIF_DICT_PLACEHOLDER = {"test":"this shouldn't be visible","test1":"poep","example_motif": ('2.0e-049', '19', '18', '4.3e-009', 'logo0.png')
}

os.environ["FLASK_DEBUG"] = "1"  # turn on debug mode

CORRECT_OS = True

WORKING_DIR = Path.cwd()
if "/app_prototype" not in str(WORKING_DIR): # If the working dir is in the root of the project.
    WORKING_DIR = WORKING_DIR / "app_prototype/"

print(f"Working dir: {WORKING_DIR}")

# Flask constructor takes the name of 
# current module (__name__) as argument.
UPLOAD_FOLDER = WORKING_DIR / "user_input_files"

print(f"UPload folder: {UPLOAD_FOLDER}")

#WORKING_DIR = os.path.dirname(os.path.realpath(__file__))  # to check current dir


app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "AMOGUS"

OUTPUT_FOLDER = WORKING_DIR / r"/user_output"
# UPLOAD_FOLDER = WORKING_DIR / r"/user_input_files"


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
    # redirects the user to the about page if they visit the root website
    return redirect(url_for("home_about_page"))


# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.
@app.route('/about', methods=["POST", "GET"])
# ‘/’ URL is bound with hello_world() function.
def home_about_page():
    correct_os()

    # the page loading without any forms being submitted
    if request.method == "GET":
        return render_template("prototype_bootstrap.html")


@app.route('/download')
def download():
    # temporary variable so the concept works
    # make this a global variable later
    download_file_name = "meme.tar"

    # generate a variable absolute path, so it works on anyone's pc
    outputs = WORKING_DIR / r"User_output/" / download_file_name

    return flask.send_file(outputs, as_attachment=True)


@app.route("/fimo", methods=["POST", "GET"])
def html_render_fimo():
    correct_os()
    method = request.method

    # the page loading without any forms being submitted
    if method == "GET":

        # just renders the default fimo page
        return render_template("fimopage.html")

    # if the user clicks on the submit button on the page
    elif method == "POST":

        # here I save all the input button values as variables
        # request.form refers to the input's name in html
        user_input_values = {
            "chosen_database": request.form["chosen_database"],
            "input_custom_pvalue": request.form["input_custom_pvalue"],
            "max_amount_motifs": request.form["max_amount_motifs"],
            "maxsize": request.form["maxsize"],
            "minsize": request.form["minsize"],
            }
        

        motif_file_option = request.form.get("motif_file_option")
        motif_database_option = request.form.get("motif_database_option")
        default_pvalue = request.form.get("default_pvalue")
        custom_pvalue = request.form.get("custom_pvalue")

        # checking if the input is actually a number
        if user_input_values["input_custom_pvalue"].replace(".", "").isnumeric() is False:
            flash("the custom")


        # checking if neither of the motif options have been chosen.
        if motif_file_option is None and motif_database_option is None:
            flash("a motif option must be chosen")
            return render_template("fimopage.html")

        # checking if both motif options have been chosen.
        if motif_file_option is not None and motif_database_option is not None:
            flash("only one motif option can be chosen")
            return render_template("fimopage.html")
        
        # checking if neither of the pvalue options have been chosen.
        if default_pvalue is None and custom_pvalue is None:
            flash("a pvalue option must be chosen")
            return render_template("fimopage.html")
        
        # checking if both pvalue options have been chosen.
        if custom_pvalue is not None and default_pvalue is not None:
            flash("only one p value option can be chosen")
            return render_template("fimopage.html")
        
        # radio buttons aren't present if they're turned off, so I have to check if they are before storing them
        if motif_file_option is not None:
            user_input_values["motif_file_option"] = motif_file_option

        # temporarily putting it on, on anyway because the tool won't work otherwise for now
        else:
            user_input_values["motif_database_option"] = "on" 
            
        if default_pvalue is not None:
            user_input_values["default_pvalue"] = request.form["default_pvalue"]

        else:
            user_input_values["default_pvalue"] = False

        if custom_pvalue is not None:
            user_input_values["custom_pvalue"] = request.form["custom_pvalue"]

            # checking if the input is actually a number
            if user_input_values["input_custom_pvalue"].replace(".", "").isnumeric() is False:
                flash("the custom pvalue has to be a float(0.0)")
                return render_template("fimopage.html")

        else:
            user_input_values["custom_pvalue"] = False


        user_input_values["motif_database_option"] = motif_database_option

        # checking to see if a database has been chosen if the database option is on
        if user_input_values["chosen_database"] == "PLease select a database to use":
            flash("please select a database to use")
            return render_template("fimopage.html")


        # here we define the files the user submitted.
        input_fasta_file = request.files["input_fasta_file"]

        input_motif_file = request.files["input_motif_file"]

        output_path_fimo = WORKING_DIR / "User_ouput/fimo"

        # if the user submits no file,
        # a file without a name will be submitted anyway
        # so this checks against that
        if input_fasta_file.filename == "" or input_motif_file.filename == "":
            flash("submitted filename(s) must contain atleast 1 character!")
            return render_template("fimopage.html")
        

        # with open(input_motif_file) as motifs:
        #     for i in motifs:
        #         print(i)
        # execute Fimo with user parameters
        print(f"motif file: {input_motif_file}")
        fimo = Fimo(user_input_values["motif_database_option"], 
                    user_input_values["default_pvalue"], 
                    user_input_values["custom_pvalue"], 
                    input_motif_file, input_fasta_file, 
                    output_path_fimo)
        # database_to_use, use_default_p_value, p_value, input_motif_file, input_sequence_path_fimo, output_path_fimo
        
        # fimo output for commandline terminal to check input variables
        print(str(fimo))
        fimo.run()

        # confirmation for front end that the files have been received
        # flash(f"file: {input_fasta_file.filename} received!!")
        
        # redirects to the path for fimo's html output
        return redirect(url_for("render_fimo_output_html"))


@app.route('/meme', methods=["POST", "GET"])
def html_render_meme():
    correct_os()
    method = request.method
    if method == "GET":
        # just renders the default meme page
        return render_template("memePage.html")
        

    # if the user clicks on the submit button on the page
    elif request.method == "POST":
        # here I save all the input button values as variables
        # request.form refers to the input's name in html
    
        if request.form.get("seq_type_dna"):
            alphabet = "dna"
            print("aaaaaaaaaaaaaaaaaaaaa")
        elif request.form.get("seq_type_rna"):
            alphabet = "rna"
            print("bbbbbbbbbbbbbbbbbbbbbbbbbbbb")
        elif request.form.get("seq_type_protein"):
            alphabet = "protein"
            print("cccccccccccccccccccccccccc")
        else:
            alphabet = "dna" # backup 

        #alphabet = "dna"
        print(f"Selected alphabet: {alphabet}")


        user_input_values = {
            "max_amount_of_motifs": request.form["max_amount_of_motifs"],
            "max_motif_size": request.form["max_motif_size"],
            "min_motif_size": request.form["min_motif_size"],
            "alphabet": alphabet

            }
 


        # checks if max_motif_size field isn't left empty
        if user_input_values["max_motif_size"] == "":
            flash("please input a max motif size!")
            return render_template("memePage.html")

        # checks if min_motif_size field isn't left empty
        if user_input_values["min_motif_size"] == "":
            flash("please input a min motif size!")
            return render_template("memePage.html")

        # checks if max_amount_of_motifs field isn't left empty
        if user_input_values["max_amount_of_motifs"] == "":
            flash("please input a max amount of motifs!")
            return render_template("memePage.html")

        # radio buttons aren't present if they're turned off, so I have to check if they are before storing them
        # checking if radio button is present in request.form
        # if request.form.get("seq_type_dna") is not None:

        #     # checking if the other buttons aren't on
        #     if request.form.get("seq_type_rna") is not None or\
        #           request.form.get("seq_type_protein") is not None:
                
        #         flash("Only 1 sequence type can be chosen!")
        #         return render_template("memePage.html")

        #     else:
        #         user_input_values["seq_type_dna"] = request.form["seq_type_dna"]
        # else:
        #     user_input_values["seq_type_dna"] = False

        # # checking if radio button is present in request.form
        # if request.form.get("seq_type_rna") is not None:

        #     # checking if the other buttons aren't on
        #     if request.form.get("seq_type_protein") is not None or\
        #           request.form.get("seq_type_dna") is not False:
                
        #         flash("Only 1 sequence type can be chosen!")
        #         return render_template("memePage.html")

        #     else:
        #         user_input_values["seq_type_rna"] = request.form["seq_type_rna"]
        # else:
        #     user_input_values["seq_type_rna"] = False

        # # checking if radio button is present in request.form
        # if request.form.get("seq_type_protein") is not None:

        #     # checking if the other buttons aren't on
        #     if request.form.get("seq_type_rna") is not False or\
        #           request.form.get("seq_type_dna") is not False:
                
        #         flash("Only 1 sequence type can be chosen!")
        #         return render_template("memePage.html")
             
        #     else:
        #         user_input_values["seq_type_protein"] = request.form["seq_type_protein"]
        # else:
        #     user_input_values["seq_type_protein"] = False



        # path to give the MEME class to refer to the input file. 
        input_sequence_meme_path = UPLOAD_FOLDER / request.files["input_user_file"].filename
        print(f"input sequence path meme: {input_sequence_meme_path}")

        # here we define the file the user submitted as input_fasta_file
        input_sequence_meme = request.files["input_user_file"] 
        output_path_meme = WORKING_DIR / "User_output/meme/"
        print(f"Output path meme: {output_path_meme}")

        # Save the uploaded file to the upload folder.
        input_sequence_meme.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(input_sequence_meme.filename)))


        # if the user submits no file,
        # a file without a name will be submitted anyway
        # so this checks against that
        if input_sequence_meme.filename == "":
            flash("submitted filename(s) must contain atleast 1 character!")
            return render_template("memePage.html")

        # execute Meme with user parameters
        meme = Meme(user_input_values["max_amount_of_motifs"],
                    user_input_values["max_motif_size"],
                    user_input_values["min_motif_size"],
                    user_input_values["alphabet"],
                    input_sequence_meme_path,
                    output_path_meme)

        # meme output for commandline terminal to check input variables
        print(str(meme)) 
        meme.run() # execute meme with the user given parameters.
        motif_dict = meme.motif_dict
        session["motif_dict"] = motif_dict
        flash("Output Generated!")
        flash("(press show output to view your output!)")
        return render_template("memePage.html")


@app.route('/fimo_output')
def render_fimo_output_html():
    """ Route to show the FIMO output"""

    return render_template("fimo.html")


@app.route('/meme_output')
def render_meme_output_html():
    """ Route to show the MEME output"""
    motif_dict = MOTIF_DICT_PLACEHOLDER

    if session.get("motif_dict")is not None:
        motif_dict = session["motif_dict"]

    return render_template("memeplaceholder.html", motif_dict=motif_dict)





# Error handling:

@app.errorhandler(400)
def bad_request(e):
    """function to catch and handle the 400 error"""
    return render_template("400.html"), 400

@app.errorhandler(403)
def Acces_forbidden(e):
    """function to catch and handle the 403 error"""
    return render_template("400.html"), 403

@app.errorhandler(404)
def Page_not_found(e):
    """function to catch and handle the 404 error"""
    return render_template("404.html"), 404


@app.errorhandler(429)
def too_many_request(e):
    """function to catch and handle the 429 error"""
    return render_template("429.html"), 429

@app.errorhandler(500)
def internal_server_error(e):
    """function to catch and handle the 500 error"""
    
    return render_template("500.html"), 500

@app.errorhandler(502)
def Bad_Gateway(e):
    """function to catch and handle the 502 errors"""
    
    return render_template("502.html"), 502


@app.errorhandler(503)
def service_unavailable(e):
    """function to catch and handle the 503 errors"""
    return render_template("503.html"), 503


@app.errorhandler(504)
def gateway_error(e):
    """function to catch and handle the 504 errors"""

    return render_template("504.html"), 504


# main driver function
# this statement basically checks if the file is being run directly by the user,
# or is being run by another file, for example for importing
if __name__ == '__main__':
    if not sys.platform.startswith("linux"):
        CORRECT_OS = False
        
    # run() method of Flask class runs the application on the local development server
    app.run()
