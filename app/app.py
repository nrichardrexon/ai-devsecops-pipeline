from flask import Flask, request, escape
import os

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello from DevSecOps!"

@app.route('/danger')
def danger():
    cmd = request.args.get('cmd', '')
    safe_cmd = escape(cmd)
    return f"Simulated execution: {safe_cmd}"

if __name__ == '__main__':
    host = os.getenv("FLASK_RUN_HOST", "127.0.0.1")  # Defaults to localhost for safety
    port = int(os.getenv("FLASK_RUN_PORT", "5000"))
    app.run(host=host, port=port)
