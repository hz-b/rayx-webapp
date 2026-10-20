from source.api.controllers.api_routes import api
import argparse
from dotenv import load_dotenv
import os
from pathlib import Path


def run_api(port: int = 5000):
    # Pre-Run
    create_environment_folders()
    load_configurations()

    # Run API
    api.run(host="0.0.0.0", port=port, debug=True)


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
        load_dotenv(
            "config.env"
        )  # Load environment variables, if does not exist, create one
        api.config["SECRET_KEY"] = os.getenv(
            "SECRET_KEY"
        )  # Secret Key is used to secure the session and temporarily store user form data     TODO: config.env can be entire deprecated in favor of api.config, however if backend is changed this has to change again.
    except FileNotFoundError:
        api.config["SECRET_KEY"] = "1234567890"

    api.config["MAX_CONTENT_LENGTH"] = 10 * 1000 * 1000  # Limits rml_file size to 10 MB
    api.config["ALLOWED_EXTENSIONS"] = {"rml"}  # Only allows .rml files to be uploaded


# Runs the server
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--Port", help="Port-number.", default=5001)
    args = parser.parse_args()

    run_api(args.Port)
