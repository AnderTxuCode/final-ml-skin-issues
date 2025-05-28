import os
import kagglehub
from flask import Flask, render_template, request, jsonify, send_from_directory
import random
import matplotlib.pyplot as plt
import tensorflow as tf
import pandas as pd

local_dataset_dir = os.path.join(os.path.dirname(__file__), 'isic-dataset')


app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/', methods=['GET', 'POST'])
#def home():
   # if request.method == 'POST':
   #     if 'photo' in request.files:
   #         photo = request.files['photo']
   #         if photo.filename != '':
   #             print(True) 
   #             return jsonify({'status': 'success', 'message': 'Archivo subido bien'})
   #         else:
   #             print(False)
   #             return jsonify({'status': 'error', 'message': 'El archivo no es valido'}), 400
   #     else:
    #        print("No se encontró 'photo' en request.files")
   #         return jsonify({'status': 'error', 'message': 'No se ha recibido archivo'}), 400
  # return render_template('index.html')
@app.route('/', methods=['GET', 'POST'])
def home():
    df = pd.read_csv('metadata.csv')

    total_registros = len(df)
    valores_nulos = df.isnull().sum().to_dict()
    porcentaje_nulos = (df.isnull().sum() / len(df) * 100).round(2).to_dict()

    numeric_cols = ['age_approx', 'clin_size_long_diam_mm', 'pixels_x', 'pixels_y']
    stats = df[numeric_cols].describe().round(2).to_dict()

    html = f"""
    <h1>DETECCIÓN DE PROBLEMAS DE PIEL</h1>
    <div style='margin: 20px 0;'>
        <h2>Análisis del Dataset</h2>
        <p>Total de registros: {total_registros}</p>
        
        <h3>Valores Nulos por Columna:</h3>
        <table style='border-collapse: collapse; width: 80%; margin: 20px auto;'>
            <tr style='background-color: #4e54c8; color: white;'>
                <th style='padding: 10px; border: 1px solid #ddd;'>Columna</th>
                <th style='padding: 10px; border: 1px solid #ddd;'>Valores Nulos</th>
                <th style='padding: 10px; border: 1px solid #ddd;'>Porcentaje</th>
            </tr>
    """
    for columna in valores_nulos:
        html += f"""
            <tr>
                <td style='padding: 8px; border: 1px solid #ddd;'>{columna}</td>
                <td style='padding: 8px; border: 1px solid #ddd;'>{valores_nulos[columna]}</td>
                <td style='padding: 8px; border: 1px solid #ddd;'>{porcentaje_nulos[columna]}%</td>
            </tr>
        """
    html += """
        </table>
    """
    html += """
        <h3>Estadísticas Descriptivas de Columnas Numéricas:</h3>
        <table style='border-collapse: collapse; width: 80%; margin: 20px auto;'>
            <tr style='background-color: #4e54c8; color: white;'>
                <th style='padding: 10px; border: 1px solid #ddd;'>Columna</th>
                <th style='padding: 10px; border: 1px solid #ddd;'>Media</th>
                <th style='padding: 10px; border: 1px solid #ddd;'>Desviación Estándar</th>
                <th style='padding: 10px; border: 1px solid #ddd;'>Mínimo</th>
                <th style='padding: 10px; border: 1px solid #ddd;'>Máximo</th>
            </tr>
    """
    for col in numeric_cols:
        html += f"""
            <tr>
                <td style='padding: 8px; border: 1px solid #ddd;'>{col}</td>
                <td style='padding: 8px; border: 1px solid #ddd;'>{stats[col].get('mean', 'N/A')}</td>
                <td style='padding: 8px; border: 1px solid #ddd;'>{stats[col].get('std', 'N/A')}</td>
                <td style='padding: 8px; border: 1px solid #ddd;'>{stats[col].get('min', 'N/A')}</td>
                <td style='padding: 8px; border: 1px solid #ddd;'>{stats[col].get('max', 'N/A')}</td>
            </tr>
        """
    html += "</table>"
    categorical_cols = ['anatom_site_general', 'benign_malignant', 'sex', 'diagnosis']
    html += "<h3>Frecuencia de Variables Categóricas:</h3>"
    for col in categorical_cols:
        freq = df[col].value_counts(dropna=False).to_dict()
        html += f"""
            <h4>{col}</h4>
            <table style='border-collapse: collapse; width: 50%; margin: 10px auto;'>
                <tr style='background-color: #4e54c8; color: white;'>
                    <th style='padding: 8px; border: 1px solid #ddd;'>Categoría</th>
                    <th style='padding: 8px; border: 1px solid #ddd;'>Frecuencia</th>
                </tr>
        """
        for category, count in freq.items():
            html += f"""
                <tr>
                    <td style='padding: 8px; border: 1px solid #ddd;'>{category if pd.notna(category) else "NaN"}</td>
                    <td style='padding: 8px; border: 1px solid #ddd;'>{count}</td>
                </tr>
            """
        html += "</table>"

    html += """
    <form id="uploadForm" method="post" enctype="multipart/form-data">
        <label for="photo">Sube una fotografía:</label>
        <input type="file" id="photo" name="photo" accept="image/*">
        <button type="submit">Subir</button>
    </form>
    <div id="preview" style="display:none;">
        <img id="previewImg" src="#" alt="Vista previa de la foto" />
        <p id="fileName"></p>
        <button class="remove" type="button" id="removeBtn">Eliminar</button>
    </div>
    """  
    return html

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