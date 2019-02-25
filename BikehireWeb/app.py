from flask import Flask
from apps.backend import back_bp
import config

app = Flask(__name__)
app.config.from_object(config)

app.register_blueprint(back_bp)

if __name__ == '__main__':
    app.run()
