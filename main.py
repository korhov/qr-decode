from dotenv import load_dotenv
import os
from flask import Flask, request, json

from decode.decode import Decode

import cv2

import tempfile

from pdf2image import convert_from_path

load_dotenv()

UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/", methods = ['POST'])
def qr_decode():
    file = request.files['scan']

    tf = tempfile.NamedTemporaryFile(dir = UPLOAD_FOLDER)
    tmp_filename = tf.name
    tf.close()
    file.save(tmp_filename)

    if file.filename.rsplit('.', 1)[1].lower() == 'pdf':
        pages = convert_from_path(tmp_filename, 300)
        if len(pages) > 0:
            pages[0].save(tmp_filename, 'JPEG')

    im = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], tmp_filename))
    os.unlink(tmp_filename)
    dec = Decode().decode(im)
    if dec:
        return app.response_class(
            response = json.dumps({'text': dec, 'error': None}),
            mimetype = 'application/json'
        )
    return app.response_class(
        response = json.dumps({'text': None, 'error': "QR code not decoded"}),
        mimetype = 'application/json'
    )


if __name__ == "__main__":
    app.run(host = os.getenv("HTTP_HOST"), port = os.getenv("HTTP_PORT"))  # debug=True
