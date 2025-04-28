from flask import Flask, jsonify, request, send_from_directory, abort
from flask_cors import CORS
import os
from werkzeug.middleware.proxy_fix import ProxyFix
from routes.lab1 import lab1_routes
from routes.lab2 import lab2_routes

# Ensure the static folder exists
STATIC_FOLDER = 'out'
if not os.path.exists(STATIC_FOLDER):
    raise FileNotFoundError(f"Static folder '{STATIC_FOLDER}' does not exist. Ensure your frontend is built and placed correctly.")

app = Flask(__name__, static_folder=STATIC_FOLDER)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)
CORS(app)  # Enable CORS for all routes

# Register blueprints for each lab
app.register_blueprint(lab1_routes, url_prefix='/api/lab1')
app.register_blueprint(lab2_routes, url_prefix='/api/lab2')

# Serve the Next.js static files
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    file_path = os.path.join(app.static_folder, path)
    if path != "" and os.path.exists(file_path):
        return send_from_directory(app.static_folder, path)
    elif os.path.exists(os.path.join(app.static_folder, 'index.html')):
        return send_from_directory(app.static_folder, 'index.html')
    else:
        abort(404, description="File not found")

# Health check endpoint
@app.route('/api/health')
def health_check():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    # Use debug=True for local testing
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)