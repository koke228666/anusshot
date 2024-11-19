from flask import Flask, request, Response, jsonify, send_from_directory
import os, uuid, json

app = Flask(__name__)

#папочка с картиночками
UPLOAD_FOLDER = 'anusshot\imgs'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

#путь дб
shortdb = 'anusshot\links.json'

#функция для обновления бд
def load_links():
    if os.path.exists(shortdb):
        with open(shortdb, 'r') as f:
            links = json.load(f)
    else:
        links = {}
    return links

#основной маршрут загрузки скриншотов
@app.route('/anusshot/upload/<path:path>', methods=['POST'])
def upload_image(path):
    if 'image' not in request.files:
        return Response('<response><status>error</status><message>no file</message></response>', status=400, mimetype='application/xml')
    links = load_links()
    file = request.files['image']
    filename = str(uuid.uuid4()) + '.png'
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)
    short_link = str(uuid.uuid4())[:8]
    links[short_link] = filename
    with open(shortdb, 'w') as f:
        json.dump(links, f)
    share_link = f'http://127.0.0.1/anusshot/files/{short_link}'
    response_xml = f'<response><status>success</status><share>{share_link}</share></response>'
    return Response(response_xml, status=200, mimetype='application/xml')

#маршрут файлов
@app.route('/anusshot/files/<short_link>', methods=['GET'])
def serve_image(short_link):
    links = load_links()
    if short_link in links:
        filename = links[short_link]
        return send_from_directory(UPLOAD_FOLDER, filename)
    else:
        return 404

if __name__ == '__main__':
    app.run(debug=True, port=80)