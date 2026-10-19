from source.web.web_routes import app
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--Port", help="Port-number.", default=5001)
    args = parser.parse_args()

    app.run(host="0.0.0.0", port=args.Port, debug=True)
