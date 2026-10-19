import traceback
import rayx
import os
import subprocess


def call_rayx(rml_path, output_file_name, output_path: str) -> None:
    """
    Calls RayX as a subprocess and saves the output as a .h5 file in the output folder.
    """
    rayx_cmd = ["./rayx/rayx", "-i", rml_path]
    rayx_cmd += ["-o", str(output_path) + "/" + output_file_name]
    result = subprocess.run(rayx_cmd, capture_output=True, text=True)

    if result.stderr:
        print("STDERR:\n", result.stderr)
    if result.returncode != 0:
        print("Error occurred while running rayx.")
        raise Exception(result.stderr)


def get_beamline(rml_file) -> rayx.Rays:
    """
    Takes an RML file and returns a traced beamline using the RayX python package.
    """
    try:
        # Get the absolute path
        base_dir = os.path.dirname(os.path.realpath(__file__))
        path = os.path.join(base_dir, "uploads", rml_file.filename)

        # Import the beamline
        beamLine = rayx.import_beamline(path)
        return beamLine
    except Exception:
        traceback.print_exc()
        return 0  # render_template("displayPy.html", exception=e)
