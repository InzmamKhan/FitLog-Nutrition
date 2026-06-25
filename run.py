import threading
import time
from flask import Flask
import webview
import config
from server.routes import server_bp

def create_app():
    """Initializes the Flask framework context, binding configuration definitions."""
    app = Flask(__name__)
    app.secret_key = config.FLASK_SECRET_KEY
    
    app.register_blueprint(server_bp)
    
    return app

def run_flask_server(app_instance):
    """Executes the Flask server loop inside a dedicated background thread execution context."""
    app_instance.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)

if __name__ == '__main__':
    flask_app = create_app()

    server_thread = threading.Thread(target=run_flask_server, args=(flask_app,))
    server_thread.daemon = True
    server_thread.start()

    time.sleep(0.5)

    webview.create_window(
        title="FitLog Nutrition",
        url="http://127.0.0.1:5000/",
        width=1100,
        height=850,
        resizable=True,
        min_size=(900, 700)
    )
    
    webview.start()