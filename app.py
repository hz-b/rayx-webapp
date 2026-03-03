# region Imports
from flask import Flask, render_template, request, send_file, redirect, flash, url_for, jsonify
from FileOperations import *
import rayx, os, subprocess, traceback, io, base64, time, uuid, json
from Histogram import Histogram
import pandas as pd
import numpy as np
from werkzeug.utils import secure_filename
# endregion

# region Globals
app = Flask(__name__)

# Upload- & Output folder, creates one if it doesn't exist
UPLOAD_FOLDER = "./uploads/"
RESULT_FOLDER = "./results/"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

output_file_name = ""

# Configurations
app.config["MAX_CONTENT_LENGTH"] = 10 * 1000 * 1000     # Limits rml_file size to 10 MB
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {"rml"}

# endregion

# Runs the app and starts the server
@app.route("/",)
def index():
    return render_template("displayPy.html")

# region SLURM
# Handles the the job request
@app.route("/submit_job", methods=["POST"])
def submit_job():
    if "rmlFile" not in request.files:
        return redirect(request.url)
    
    file = request.files["rmlFile"]

    # If the user does not select a file, the browser submits an
    # empty file without a filename. User is redirected to the home page
    if file.filename == '':
        return render_template("displayPy.html")
    
    # Check if file is allowed and save it, if it is
    if file and allowed_file(file.filename):
        job_uuid = str(uuid.uuid4())

        rml_path = os.path.join(UPLOAD_FOLDER, file.filename)
        result_file = os.path.join(RESULT_FOLDER, job_uuid + ".json")

        # submit to Slurm; $1 = RML File, $2 = Result File
        out = subprocess.check_output([
            "sbatch",
            "single_run_job.sh",
            rml_path,
            result_file
        ], text=True)

        # extract job id from sbatch output
        slurm_id = out.strip().split()[-1]

        return jsonify({"job_uuid": job_uuid, "slurm_id": slurm_id})

# Check Job Slurm Status
@app.route("/status/<slurm_id>")
def check_status(slurm_id):
    result = subprocess.run(["squeue", "-h", "-j", slurm_id], capture_output=True, text=True)
    if result.stdout.strip() == "":
        return jsonify({"status": "finished"})
    return jsonify({"status": "running"})

# Get Job Result
@app.route("/result/<job_uuid>")
def get_result(job_uuid):
    path = os.path.join(RESULT_PATH, f"{job_uuid}.json")
    if not os.path.exists(path):
        return jsonify({"error":"not ready"}), 404

    with open(path) as f:
        data = json.load(f)
    return jsonify(data)
# endregion

"""
================================================================================
                                REFACTOR THE BELOW
================================================================================
"""

# Handles the post on the server, displays the content of the rml file on the site
@app.route("/display/handle_post", methods=["POST"])
def display_handle_post():

    plot_data = []

    t = time.time()

    if request.method == "POST":
        
        # Check if the post request has the file part
        if "rmlFile" not in request.files:
            return redirect(request.url)

        rml_file = request.files["rmlFile"]

        # If the user does not select a file, the browser submits an
        # empty file without a filename. User is redirected to the home page
        if rml_file.filename == '':
            return render_template("displayPy.html")
        
        # Check if file is allowed and save it, if it is
        if rml_file and allowed_file(rml_file.filename):
            filename = secure_filename(rml_file.filename)
            rml_file.filename = filename
            save_file(UPLOAD_FOLDER, rml_file)

        output_file_name = rml_file.filename
        
        try:
            # Trace beamline    
            beamline = get_beamline(rml_file)
            traced_beamline = beamline.trace()

            # Create pandas dataframe
            columns = [
                "direction_x", "direction_y", "direction_z",
                "electric_field_x", "electric_field_y", "electric_field_z",
                "energy", "event_type",
                "last_element_id", "order", "path_length",
                "position_x", "position_y", "position_z",
                "ray_id", "source_id",
            ]

            df = pd.DataFrame({col: getattr(traced_beamline, col) for col in columns})

            # Remove file from server
            remove_file(UPLOAD_FOLDER, rml_file)

            # Plot the traced beamline
            last_element = df["last_element_id"]
            pos_x = df["position_x"]
            pos_y = df["position_y"]
            pos_z = df["position_z"]

            # Creates an array that holds all of the beamlines elements as a 2D histogram
            for source in range(len(beamline.sources)):
                mask = last_element == source
                plot = Histogram(pos_x[mask], pos_y[mask], xLabel="x / mm", yLabel="y / mm", title=(beamline.sources[source].name))
                
                plot_data.append(plot)

            # If the beamline has only one element, plot the whole beamline, prevents the histogram from being empty
            if len(beamline.elements) <= 1:
                plot = Histogram(pos_x, pos_z, xLabel="x / mm", yLabel="z / mm", title="")
                
                plot_data.append(plot)
            else:
                index = 1
                try:
                    for element in range(len(beamline.elements)):
                        mask = last_element == element + len(beamline.sources)

                        plot = Histogram(pos_x[mask], pos_z[mask], xLabel="x / mm", yLabel="z / mm", title=(beamline.elements[element].name))

                        plot_data.append(plot)
                except:
                    print("Index out of range" + str(index))
                    pass
        except Exception as e:
            traceback.print_exc()
            return render_template("displayPy.html", exception=e)
      
    return render_template(
        "displayPy.html", 
        RMLFileName=get_cleaned_filename(output_file_name), 
        plot_data=plot_data,
    )

# Returns a traced beamline using the RayX python package
def get_beamline(rml_file) -> rayx.Rays:

    try:
        # Get the absolute path
        base_dir = os.path.dirname(os.path.realpath(__file__))
        path = os.path.join(base_dir, "uploads", rml_file.filename)

        # Import the beamline   
        beamLine = rayx.import_beamline(path)
        return beamLine
    except Exception as e:
        traceback.print_exc()
        return render_template("displayPy.html", exception=e)

# Checks if the uploaded file is allowed
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Runs the server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)