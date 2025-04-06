from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello from DevSecOps!"

@app.route('/danger')
def danger():
    cmd = request.args.get('cmd')
    return f"Simulated execution: {cmd}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
