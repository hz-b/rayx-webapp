from source.web.web_routes import app
import argparse

API_URL = "http://localhost:5001/"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--Port", help="Port-number.", default=5000)
    args = parser.parse_args()

    app.run(host="0.0.0.0", port=args.Port, debug=True)
