import sys
sys.path.append('.')
sys.path.append('..')

import argparse

from flask import Flask, render_template
import os
import yaml 
from utils.config import Config

PEOPLE_FOLDER = os.path.join('static')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER

@app.route('/')
@app.route('/index')

def show_index():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'last.jpeg')
    return render_template("index.html", user_image = full_filename)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default='config.yaml', help='Configuration')
    args = parser.parse_args()
    config = Config(yaml.load(open(args.config, 'r'), Loader=yaml.Loader))

    port = int(os.environ.get('PORT', config.APP.PORT))
    app.run(port = port, debug = True, use_reloader = False)

