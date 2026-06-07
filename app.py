import threading
import webbrowser
from flask import Flask, render_template
from api.routes import bp as api_bp
from config import DEFAULT_PORT

app = Flask(__name__)
app.register_blueprint(api_bp)


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    url = f"http://127.0.0.1:{DEFAULT_PORT}"
    print(f"\n  Music Organizer → {url}\n")
    threading.Timer(1.2, lambda: webbrowser.open(url)).start()
    app.run(port=DEFAULT_PORT, debug=False)
