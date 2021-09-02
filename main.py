import io
import os
from flask import Flask, request, send_file, jsonify,render_template
from flask_cors import CORS
from PIL import Image
import logging
import cv2
import numpy as np
import base64
# import threading

import removal
# import consumer

if not os.path.exists("app/logs"):
    os.makedirs("app/logs")
logging.basicConfig(level=logging.INFO,
                    # filename='app/logs/app.log',
                    # filemode='w',
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


def cv2ImgToBytes(img):
    # 如果直接tobytes写入文件会导致无法打开，需要编码成一种图片文件格式(jpg或png)，再tobytes
    # 这里得到的bytes 和 with open("","rb") as f: bytes=f.read()的bytes可能不一样，如果用这里得到的bytes保存过一次，下次就f.read()和cv2ImgToBytes(img)会一样
    return cv2.imencode('.png', img)[1].tobytes()


# Route http posts to this method
@app.route('/', methods=['POST'])
def run():
    # Convert string of image data to uint8
    if 'file' not in request.files:
        return jsonify({'error': 'missing file param `file`'}), 400
    file = request.files['file']
    data = request.files['file'].read()
    if len(data) == 0:
        return jsonify({'error': 'empty image'}), 400

    ext = os.path.splitext(file.filename)


    # Convert string data to PIL Image
    img = Image.open(io.BytesIO(data))
    img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)

    outScale = request.values.get("outScale")
    if outScale is None:
        outScale = 2
    print(outScale)
    result_img = removal.run(img, float(outScale))

    if result_img is not None:

        image = cv2.imencode(ext[1], result_img)[1]
        base64_str = str(base64.b64encode(image))[2:-1]

        result = {}
        result['success'] = True
        result['msg'] = 'success!'
        result['data'] = f"data:image/{ext[1][1:]};base64,{base64_str}"
        return jsonify(result)
    else:
        result = {}
        result['success'] = False
        result['msg'] = 'found error,try again with smaller outScale!'
        return jsonify(result)


if __name__ == '__main__':
    os.environ['FLASK_ENV'] = 'development'

    logging.info("starting service")
    port = int(os.environ.get('PORT', 8086))
    # thread = threading.Thread(target=consumer.initForConsuming)
    # thread.start()
    removal.init()
    app.run(debug=True, host='0.0.0.0', port=port)
