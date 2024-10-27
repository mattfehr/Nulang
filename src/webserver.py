from flask import Flask, request, jsonify, render_template, send_from_directory
import subprocess
import os
import time

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pages_dir = os.path.join(parent_dir, 'pages')

app = Flask(__name__, template_folder=pages_dir)

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')  # No '../pages/' needed now

@app.route('/docs')
def docs():
    return render_template('docs.html')  # No '../pages/' needed now

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(pages_dir, filename)

@app.route('/run-code', methods=['POST'])
def run_code():
    code = request.json['code']
    filename = f'temp_{int(time.time())}.nu'

    with open(filename, 'w') as f:
        f.write(code)

    result = subprocess.run(['python', 'src/main.py', filename], capture_output=True, text=True, timeout=30)
    output = result.stdout if result.returncode == 0 else result.stderr

    return jsonify({'output': output})

if __name__ == '__main__':
    app.run(port=3000)
