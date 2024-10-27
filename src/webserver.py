from flask import Flask, request, jsonify, render_template, send_from_directory
import subprocess
import os
import time

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pages_dir = os.path.join(parent_dir, 'pages')

app = Flask(__name__, template_folder=pages_dir)

# Route for the home page
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')  # No '../pages/' needed now

# Route for the docs page
@app.route('/docs')
def docs():
    return render_template('docs.html')  # No '../pages/' needed now

# Routes for serving static files (CSS and JS)
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(pages_dir, filename)

@app.route('/run-code', methods=['POST'])
def run_code():
    try:
        code = request.json['code']
        filename = f'temp_{int(time.time())}.nu'

        with open(filename, 'w') as f:
            f.write(code)

        try:
            result = subprocess.run(['nulang', filename], capture_output=True, text=True, timeout=30)
            output = result.stdout if result.returncode == 0 else result.stderr
        finally:
            if os.path.exists(filename):
                os.remove(filename)

        return jsonify({'output': output})

    except Exception as e:
        return jsonify({'output': str(e)}), 500

if __name__ == '__main__':
    app.run(port=3000)
