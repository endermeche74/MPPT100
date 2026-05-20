from flask import Flask, request, Response
from flask_cors import CORS
import requests

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

SOLARDB_BASE = 'https://solardb.univ-reunion.fr/api/v1'

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/solardb', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/solardb/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(path):
    url = f'{SOLARDB_BASE}/{path}' if path else SOLARDB_BASE
    skip_headers = {'host', 'content-length', 'transfer-encoding', 'connection'}

    resp = requests.request(
        method=request.method,
        url=url,
        params=request.args,
        headers={k: v for k, v in request.headers if k.lower() not in skip_headers},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False,
        timeout=30,
    )

    excluded = {'content-encoding', 'content-length', 'transfer-encoding', 'connection'}
    headers = [(k, v) for k, v in resp.headers.items() if k.lower() not in excluded]
    return Response(resp.content, resp.status_code, headers)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
