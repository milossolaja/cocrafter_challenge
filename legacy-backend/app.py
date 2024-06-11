from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/v1/ping', methods=['GET'])
def ping():
  return "pong", 200

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8003)