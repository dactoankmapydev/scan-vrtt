from flask import Flask
from upload import upload

def create_app():

    app = Flask(__name__)
    app.add_url_rule('/upload', 'upload', upload, methods=['POST', 'GET'])
    return app

serve = create_app()

if __name__ == '__main__':
    serve.run(debug=True)
