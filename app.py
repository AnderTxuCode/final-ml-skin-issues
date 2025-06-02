# import os
# import kaggle
# from kaggle.api.kaggle_api_extended import KaggleApi
# # Ruta local donde se guardará el dataset
# local_dataset_dir = os.path.join(os.path.dirname(__file__), 'isic-dataset')


# api = KaggleApi()
# api.authenticate()

# dataset = "tomooinubushi/all-isic-data-20240629"

# # Ruta del archivo ZIP que se descargará
# zip_path = os.path.join(local_dataset_dir, "isic-2019.zip")


# if not os.path.exists(zip_path):
#     print("Descargando dataset...")
#     api.dataset_download_files(dataset, path=local_dataset_dir, unzip=False)
#     print("Dataset descargado y extraído en:", local_dataset_dir)
# else:
#     print("El dataset ya fue descargado.")

# Solo descargar si no existe la carpeta
# if not os.path.exists(local_dataset_dir):
#     path = kaggle.dataset_download("tomooinubushi/all-isic-data-20240629", path=local_dataset_dir)
#     print("Dataset descargado en:", path)
# else:
#     print("El dataset ya existe en:", local_dataset_dir)

# from flask import Flask, render_template, request, jsonify

# app = Flask(__name__, static_folder='static', template_folder='templates')

# @app.route('/', methods=['GET', 'POST'])
# def home():
#     if request.method == 'POST':
#         if 'photo' in request.files:
#             photo = request.files['photo']
#             if photo.filename != '':
#                 print(True) 
#                 return jsonify({'status': 'success', 'message': 'Archivo subido bien'})
#             else:
#                 print(False)
#                 return jsonify({'status': 'error', 'message': 'El archivo no es valido'}), 400
#         else:
#             print("No se encontró 'photo' en request.files")
#             return jsonify({'status': 'error', 'message': 'No se ha recibido archivo'}), 400
#     return render_template('index.html')

# if __name__ == '__main__':
#     app.run(debug=True)



# import tensorflow as tf
# import numpy as np
# import matplotlib.pyplot as plt
# import os
# # Ruta a la carpeta con imágenes
# image_dir = "Data/images"

# # Obtener la lista de archivos
# image_files = [f for f in os.listdir(image_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]

# plt.figure(figsize=(8,8))
# for i in range(9):
#     image_path = os.path.join(image_dir, image_files[i])
#     image = tf.io.read_file(image_path)
#     image = tf.image.decode_jpeg(image, channels=3)
#     image = tf.image.resize(image, [256, 256])  
#     plt.subplot(3, 3, i+1)
#     plt.imshow(image.numpy().astype("uint8"))
#     plt.axis('off')
# plt.tight_layout()
# plt.show()

import pandas as pd

data = pd.read_csv("Data/metadata.csv")
data_uni = data.drop_duplicates()
print(data_uni.size)
print(data_uni.head())