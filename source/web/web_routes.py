from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    """
    Main route. Renders landing page.
    """
    return render_template("displayPy.html")


@app.route("/reflectivity")
def reflectivity():
    """
    This function renders the web page for the "Reflectivity" tool.

    The "Reflectivity" tool is used to visualize the reflectivity of a material at a given angle and energy range.

    Returns:
        render_template: The rendered web page.
    """
    return render_template("reflectivity.html")
