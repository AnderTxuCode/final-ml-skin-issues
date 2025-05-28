import os
import kagglehub
from flask import Flask, render_template, request, jsonify, send_from_directory
import random
import matplotlib.pyplot as plt
import tensorflow as tf

local_dataset_dir = os.path.join(os.path.dirname(__file__), 'isic-dataset')


app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'photo' in request.files:
            photo = request.files['photo']
            if photo.filename != '':
                print(True) 
                return jsonify({'status': 'success', 'message': 'Archivo subido bien'})
            else:
                print(False)
                return jsonify({'status': 'error', 'message': 'El archivo no es valido'}), 400
        else:
            print("No se encontró 'photo' en request.files")
            return jsonify({'status': 'error', 'message': 'No se ha recibido archivo'}), 400
    return render_template('index.html')


@app.route('/show-sample-images')
def show_sample_images():
    images_dir = os.path.join(os.path.dirname(__file__), 'images')
    image_files = [f for f in os.listdir(images_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
    sample = random.sample(image_files, min(5, len(image_files)))
    html = '<h2>5 imágenes de ejemplo</h2>'
    for img in sample:
        html += f'<img src="/images/{img}" style="max-width:200px; margin:10px;">'
    return html

@app.route('/images/<path:filename>')
def serve_image(filename):
    images_dir = os.path.join(os.path.dirname(__file__), 'images')
    return send_from_directory(images_dir, filename)

@app.route('/ver-galeria')
def ver_galeria():
    image_dir = os.path.join(os.path.dirname(__file__), 'images')
    image_files = [f for f in os.listdir(image_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
    plt.figure(figsize=(8,8))
    for i in range(9):
        image_path = os.path.join(image_dir, image_files[i])
        image = tf.io.read_file(image_path)
        image = tf.image.decode_jpeg(image, channels=3)
        image = tf.image.resize(image, [256, 256])
        plt.subplot(3, 3, i+1)
        plt.imshow(image.numpy().astype("uint8"))
        plt.axis('off')
    plt.tight_layout()
    plt.show()
    return '<h2>Se ha mostrado una galería de 9 imágenes en una ventana aparte.</h2>'

if __name__ == '__main__':
    app.run(debug=True)