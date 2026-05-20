from flask import Flask, request, Response
from flask_cors import CORS
import requests
import logging

logging.basicConfig(
    filename='C:/Users/soren/OneDrive/Desktop/MPPT100/proxy.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

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

    target_url = requests.Request(method=request.method, url=url, params=request.args).prepare().url
    logging.info(f'→ {request.method} {target_url}')

    try:
        resp = requests.request(
            method=request.method,
            url=url,
            params=request.args,
            headers={k: v for k, v in request.headers if k.lower() not in skip_headers},
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=True,
            timeout=30,
        )
        logging.info(f'← {resp.status_code} | {resp.text[:300]}')
    except Exception as e:
        logging.error(f'PROXY ERROR: {e}')
        return Response(f'{{"error": "{e}"}}', 502, content_type='application/json')

    excluded = {'content-encoding', 'content-length', 'transfer-encoding', 'connection'}
    headers = [(k, v) for k, v in resp.headers.items() if k.lower() not in excluded]
    return Response(resp.content, resp.status_code, headers)

if __name__ == '__main__':
    app.run(debug=False, port=5000)
