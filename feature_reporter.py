import os
import re
from jinja2 import evalcontextfilter, Markup, escape
from flask import Flask, render_template, request
from werkzeug.exceptions import RequestEntityTooLarge

from feature_file_parser import parse_feature_files


ALLOWED_EXTENSIONS = {'feature'}
_paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')


@evalcontextfilter
def nl2br(eval_ctx, value):
    result = u'\n\n'.join(u'<p>%s</p>' % p.replace('\n', Markup('<br>\n'))
                          for p in _paragraph_re.split(escape(value)))
    if eval_ctx.autoescape:
        result = Markup(result)
    return result


app = Flask(__name__)
app.jinja_env.filters['nl2br'] = nl2br
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    feature_files = []
    try:
        if request.method == 'POST':
            for file in request.files.getlist('feature_files[]'):
                if allowed_file(file.filename):
                    lines = decode_utf8(file)
                    feature = parse_feature_files.get_feature(lines)
                    scenarios = parse_feature_files.get_scenarios(lines)
                    feature_files.append((feature, scenarios))
                else:
                    return render_template(
                        'index.html',
                        error="Invalid file extension: Please provide a file with an extension \'.feature\'"), 400

            return render_template('file_upload.html', feature_files=feature_files)
    except RequestEntityTooLarge:
        return render_template(
            'index.html',
            error="File too large: Please provide a file with a maximum size of 10 MB"), 400


def decode_utf8(file):
    return [line.decode('utf-8') for line in file.readlines()]


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
