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