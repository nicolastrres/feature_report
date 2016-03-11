import os

from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

from feature_file_parser import parse_feature_files

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    test_file = 'tests/test.feature'
    with open(test_file) as file:
        lines = file.readlines()
        feature = parse_feature_files.get_feature(lines)
        scenarios = parse_feature_files.get_scenarios(lines)
    return render_template('index.html', feature=feature, scenarios=scenarios)


@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST' and 'feature_file' in request.files:
        file = request.files['feature_file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            with open(file_path) as file:
                lines = file.readlines()
                feature = parse_feature_files.get_feature(lines)
                scenarios = parse_feature_files.get_scenarios(lines)
            return render_template('index.html', feature=feature, scenarios=scenarios)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = {'feature', 'txt'}


if __name__ == '__main__':
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.run(debug=True)
