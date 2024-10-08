from flask import Flask, jsonify, request
import os
import json
from datetime import datetime

app = Flask(__name__)

# Путь для сохранения данных
DATA_FOLDER = 'data'
IMAGES_FOLDER = os.path.join(DATA_FOLDER, 'images')
JSON_FOLDER = os.path.join(DATA_FOLDER, 'json')

# Маршрут для получения данных о дефекте от нейросети (изображение + координаты)
@app.route('/send_defect_data', methods=['POST'])
def receive_defect_data():
    if 'image' not in request.files:
        return jsonify({"error": "No image part in the request"}), 400

    img_file = request.files['image']
    data = request.form

    if img_file.filename == '':
        return jsonify({"error": "No selected image"}), 400

    if not data or 'result' not in data or 'x' not in data or 'y' not in data or 'z' not in data:
        return jsonify({"error": "Invalid data format. 'result' and coordinates 'x', 'y', 'z' are required."}), 400

    result = data['result']
    x_coord = float(data['x'])
    y_coord = float(data['y'])
    z_coord = float(data['z'])

    # Генерируем уникальное имя для изображения и JSON-файла
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    img_filename = f"defect_{timestamp}.jpg"
    json_filename = f"defect_{timestamp}.json"

    # Путь для сохранения изображения
    img_path = os.path.join(IMAGES_FOLDER, img_filename)

    # Сохраняем изображение
    img_file.save(img_path)

    # Данные для JSON
    defect_data = {
        "result": result,
        "coordinates": {
            "x": x_coord,
            "y": y_coord,
            "z": z_coord
        },
        "image_path": img_path  # Путь к сохраненному изображению
    }

    # Сохранение данных в JSON-файл
    json_path = os.path.join(JSON_FOLDER, json_filename)
    with open(json_path, 'w') as json_file:
        json.dump(defect_data, json_file, indent=4)

    return jsonify({"message": "Defect data saved successfully", "image_path": img_path, "json_path": json_path}), 200

if __name__ == '__main__':
    # Создаем папки для хранения изображений и JSON, если они не существуют
    os.makedirs(IMAGES_FOLDER, exist_ok=True)
    os.makedirs(JSON_FOLDER, exist_ok=True)

    app.run(debug=True)                              
