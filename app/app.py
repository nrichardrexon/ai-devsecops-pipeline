from flask import Flask, request, escape

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
    app.run(host='0.0.0.0', port=5000)
