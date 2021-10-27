from facelandmark import FaceLandMark
from blockchain import Blockchain

import requests
from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = "./uploads/"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Instantiate the Node
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Instantiate the Blockchain
blockchain = Blockchain()

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def verify_and_upload_image(image):
    if image.filename == '':
        flash('No selected file')
        return False
    #Check allowed extensions
    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(filepath)
        return filepath
    else:
        return False

@app.route('/image/add', methods=['POST'])
def add_flandmark():
    #check if the post request has the file part
    if 'image' not in request.files:
        flash('No file part')
        return 'No file part', 400
    image = request.files['image']

    filepath = verify_and_upload_image(image)
    if filepath is not None:
        faceLM = FaceLandMark(filepath)
        hashImage = faceLM.createHashImage()

        if hashImage is not None:
            index = blockchain.new_information(hashImage)

            if index > 0:
                response = {'message': f'hashed face landmarks will be added to Block {index}'}
                return jsonify(response), 201
            else:
                response = {'message': 'hashed face landmarks already found in blockchain!'}
                return jsonify(response), 400
        else:
            response = {'message': f'error in adding face landmarks'}
            return jsonify(response), 400

@app.route('/image/find', methods=['POST'])
def find_flandmark():
    #check if the post request has the file part
    if 'image' not in request.files:
        flash('No file part')
        return 'No file part', 400
    image = request.files['image']
    filepath = verify_and_upload_image(image)
    if filepath is not None:
        faceLM = FaceLandMark(filepath)
        hashImage = faceLM.createHashImage()

        if hashImage is not None:
            result = blockchain.find_information(hashImage)

            if result:
                response = {'message': 'hashed face landmarks already saved in blockchain.'}
            else:
                response = {'message': 'hashed face landmarks hasn\'t been found in blockchain.'}
            return jsonify(response), 201
        else:
            response = {'message': f'error in creating hash of face landmarks'}
            return jsonify(response), 400

@app.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain.last_block

    # Forge the new Block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'information': block['information'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5001, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port)
