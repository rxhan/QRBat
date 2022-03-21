import os.path
import time
from qr import decodeimg

from flask import Flask, render_template, request

from qr.validate import checker

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/validate', methods=['GET', 'POST'])
def validate():
    result = []
    errors = []
    for file in request.files:
        file = request.files[file]
        if file.filename:
            # Saving uploaded File
            name, ext = os.path.splitext(file.filename)
            new_name = f'upl_{int(round(time.time()*1000, 0))}{ext}'
            new_dst = os.path.join('uploads', new_name)
            file.save(new_dst)
            if os.path.isfile(new_dst):
                try:
                    # Try to extract QR-Code
                    result+= decodeimg.read(new_dst)
                except:
                    errors.append(f'File not readable {file.filename}')

                # Remove uploaded file
                os.remove(new_dst)


    image_input = "\n".join([d['text'] for d in result])

    input = request.form['qrcodes']
    if image_input:
        input += "\n" + image_input

    qrcodes = []

    if len(input) > 16000:
        errors.append('input length too long')
        codes = []
    else:
        codes = [code.strip().replace(' ', '') for code in input.split("\n")]

        i = 1
        for code in codes:
            if code != '':
                try:
                    # Validating codes
                    qrcodes.append(checker(code, i))

                except Exception as e:
                    errors.append(f'{str(i).zfill(4)} - ERROR: {e} Input: {code}')
            else:
                errors.append(f'{str(i).zfill(4)} - Ignore empty line')

            i += 1

    return render_template('index.html', qrcodes="\n".join(codes), errors=errors, codes=qrcodes)

if __name__ == '__main__':
    app.run()
