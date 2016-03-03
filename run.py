
from flask import Flask, render_template
from feature_file_parser import parse_feature_files

app = Flask(__name__)


@app.route('/')
def index():
    test_file = 'tests/test.feature'
    with open(test_file) as file:
        lines = file.readlines()
        feature = parse_feature_files.get_feature(lines)
    return render_template('index.html', feature=feature)


if __name__ == '__main__':
    app.run(debug=True)
