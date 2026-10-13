from flask import Flask
from source.api.controllers.routes import api, index, display_handle_post, reflectivity, handle_post_reflectivity, download_h5, handle_exception
from scripts.FileOperations import *
from dotenv import load_dotenv
import rayx, os, subprocess, traceback, io, base64, time, math
from scripts.Histogram import Histogram
from scripts.Curve import Curve
from pathlib import Path
from scripts.rml import *
from scripts.Materials import MATERIALS
import pandas as pd
from werkzeug.utils import secure_filename

def run_api():
    # Pre-Run
    create_environment_folders()
    load_configurations()

    # Run API
    api.run(host="0.0.0.0", port=5000, debug=True)

def create_environment_folders():
    """
    Upload- & Output folder, creates one if it doesn't exist
    Used to store rml upload and h5 output
    
    TODO: Implement user specific folder via Slurm & delete after session termination
    """

    upload_folder = Path("./uploads/")
    upload_folder.mkdir(exist_ok=True)
    api.config["UPLOAD_FOLDER"] = upload_folder

    output_folder = Path("./output/")
    output_folder.mkdir(exist_ok=True)
    api.config["OUTPUT_FOLDER"] = output_folder

def load_configurations():
    try:
        load_dotenv("config.env")                               # Load environment variables, if does not exist, create one
        api.config["SECRET_KEY"] = os.getenv("SECRET_KEY")      # Secret Key is used to secure the session and temporarily store user form data     TODO: config.env can be entire deprecated in favor of api.config, however if backend is changed this has to change again.
    except:
        # TODO: Add correct excpetion handling
        api.config["SECRET_KEY"] = "1234567890"

    api.config["MAX_CONTENT_LENGTH"] = 10 * 1000 * 1000         # Limits rml_file size to 10 MB
    api.config["ALLOWED_EXTENSIONS"] = {"rml"}                  # Only allows .rml files to be uploaded

# Runs the server
if __name__ == "__main__":
    run_api()