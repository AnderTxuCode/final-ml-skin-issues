import os
import kagglehub

# Ruta local donde se guardará el dataset
local_dataset_dir = os.path.join(os.path.dirname(__file__), 'isic-dataset')

# Solo descargar si no existe la carpeta
if not os.path.exists(local_dataset_dir):
    path = kagglehub.dataset_download("tomooinubushi/all-isic-data-20240629", path=local_dataset_dir)
    print("Dataset descargado en:", path)
else:
    print("El dataset ya existe en:", local_dataset_dir)

from flask import Flask, render_template, request, jsonify

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

if __name__ == '__main__':
    app.run(debug=True)