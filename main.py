import io
import os
from flask import Flask, request, send_file, jsonify,render_template
from flask_cors import CORS
from PIL import Image
import logging
# import threading

import removal
# import consumer

if not os.path.exists("app/logs"):
    os.makedirs("app/logs")
logging.basicConfig(level=logging.INFO,
                    filename='app/logs/app.log',
                    filemode='w',
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    )

# Initialize the Flask application
app = Flask(__name__,template_folder="templates", static_folder="static", static_url_path="/static")
CORS(app)


# Simple probe.
@app.route('/', methods=['GET'])
def index():
    return render_template('take_picture.html')


# Route http posts to this method
@app.route('/', methods=['POST'])
def run():
    # Convert string of image data to uint8
    if 'file' not in request.files:
        return jsonify({'error': 'missing file param `file`'}), 400
    data = request.files['file'].read()
    if len(data) == 0:
        return jsonify({'error': 'empty image'}), 400

    # Convert string data to PIL Image
    img = Image.open(io.BytesIO(data))
    scaleSize = request.values.get("scaleSize")
    ver = request.values.get("ver")

    img_buff = removal.run(img, scaleSize,ver)
    del img
    if img_buff is not None:
        return send_file(img_buff, mimetype='image/png')
    else:
        data = {}
        data['result'] = False
        data['msg'] = 'found error,try again with smaller scaleSize!'
        return jsonify(data)


if __name__ == '__main__':
    os.environ['FLASK_ENV'] = 'development'

    logging.info("starting service")
    port = int(os.environ.get('PORT', 8087))
    # thread = threading.Thread(target=consumer.initForConsuming)
    # thread.start()
    # removal.init()
    app.run(debug=True, host='0.0.0.0', port=port)
