from flask import Flask, request, jsonify, render_template, send_from_directory
import subprocess
import os
import sys
import tempfile
import time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES_DIR = os.path.join(BASE_DIR, 'pages')
SRC_DIR = os.path.join(BASE_DIR, 'src')
MAIN_PATH = os.path.join(SRC_DIR, 'main.py')

app = Flask(__name__, template_folder=PAGES_DIR, static_folder=PAGES_DIR)

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/docs')
def docs():
    return render_template('docs.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(PAGES_DIR, filename)

@app.post('/run-code')
def run_code():
    payload = request.get_json(force=True) or {}
    code = payload.get('code', '')

    # Basic guardrails
    if len(code) > 50_000:
        return jsonify({'output': 'Error: code too large (50k char limit).'}), 400

    # Use OS temp dir (writable even with a read-only app dir)
    with tempfile.NamedTemporaryFile(dir='/tmp', prefix='nu_', suffix='.nu', delete=False) as f:
        f.write(code.encode('utf-8'))
        temp_path = f.name

    try:
        result = subprocess.run(
            [sys.executable, MAIN_PATH, temp_path],
            capture_output=True,
            text=True,
            timeout=5  # tighter than 30s to reduce DoS risk
        )
        output = (result.stdout or '') + (result.stderr or '')
        if len(output) > 20_000:
            output = output[:20_000] + '\n...\n[truncated]'
        return jsonify({'output': output})
    except subprocess.TimeoutExpired:
        return jsonify({'output': 'Error: execution timed out.'}), 408
    finally:
        try:
            os.remove(temp_path)
        except OSError:
            pass

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port)
