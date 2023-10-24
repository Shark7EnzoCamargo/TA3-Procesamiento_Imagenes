import os
import tempfile
from flask import Flask, request, redirect, send_file, jsonify
from skimage import io
import base64
import numpy as np

app = Flask(__name__)

# Variables para almacenar datos
X_data = []
y_data = []

@app.route("/")
def main():
    return "Página principal"

@app.route('/upload', methods=['POST'])
def upload():
    try:
        img_data = request.form.get('myImage').replace("data:image/png;base64,", "")
        aleatorio = request.form.get('numero')

        # Almacenar la imagen en la variable de datos
        image = io.imread(io.BytesIO(base64.b64decode(img_data)))[:, :, 3]  # Convertir a una imagen NumPy
        X_data.append(image)
        y_data.append(aleatorio)

        return "Imagen subida exitosamente"

    except Exception as err:
        print("Error occurred")
        print(err)
        return "Error al subir la imagen", 500

@app.route('/prepare', methods=['GET'])
def prepare_dataset():
    try:
        if len(X_data) == 0 or len(y_data) == 0:
            return "No hay datos para preparar", 400

        # Convertir datos a arrays de NumPy
        X = np.array(X_data)
        y = np.array(y_data)

        # Guardar los datos en archivos "X.npy" y "y.npy"
        np.save('X.npy', X)
        np.save('y.npy', y)

        return "Conjunto de datos preparado exitosamente"
    except Exception as err:
        print("Error occurred")
        print(err)
        return "Error al preparar el conjunto de datos", 500

@app.route('/X.npy', methods=['GET'])
def download_X():
    try:
        if os.path.exists('X.npy'):
            return send_file('X.npy')
        else:
            return "Archivo X.npy no encontrado", 404
    except Exception as e:
        return "Error interno del servidor", 500

@app.route('/y.npy', methods=['GET'])
def download_y():
    try:
        if os.path.exists('y.npy'):
            return send_file('y.npy')
        else:
            return "Archivo y.npy no encontrado", 404
    except Exception as e:
        return "Error interno del servidor", 500

if __name__ == "__main__":
    app.run()
