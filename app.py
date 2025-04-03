from flask import Flask
from routes.aes import encryption_blueprint
from routes.user import user_blueprint

app = Flask(__name__)

app.register_blueprint(encryption_blueprint, url_prefix='/api')
app.register_blueprint(user_blueprint, url_prefix='/')

if __name__ == '__main__':
    app.run()
