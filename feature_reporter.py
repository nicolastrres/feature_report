import re
from jinja2 import evalcontextfilter, Markup, escape
from flask import Flask, render_template, request

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


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST' and 'feature_file' in request.files:
        file = request.files['feature_file']
        if allowed_file(file.filename):
            lines = [line.decode('utf-8') for line in file.readlines()]
            feature = parse_feature_files.get_feature(lines)
            scenarios = parse_feature_files.get_scenarios(lines)
            return render_template('file_upload.html', feature=feature, scenarios=scenarios)
        else:
            return render_template(
                'index.html',
                error="Invalid file extension: Please provide a file with an extension \'.feature\'"), 400


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.run(debug=True)
