from flask import Flask, request, render_template
import generate_for_go
from datetime import datetime
import time
# render_template('index.html')

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    print(f"Received a {request.method} request.")  # Add this line
    if request.method == 'POST':
        path = request.form.get('path')
        prompt = request.form.get('prompt')
        if not path:
            raise ValueError("Path cannot be empty.")
        if not prompt:
            raise ValueError("Prompt cannot be empty.")
        generate_for_go.generate_new_code(path, prompt)
        time.sleep(10000)
        # return 'Refactor Done!'
    return render_template('index.html')


@app.route('/progress', methods=['GET'])
def get_progress():
    return {'progress': generate_for_go.progress}


@app.route('/file_list', methods=['GET'])
def get_file_list():
    return {'file_list': generate_for_go.file_list}


if __name__ == '__main__':
    app.run(debug=True)
