from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from auth_routes import auth_blueprint
from user_routes import user_blueprint

app = Flask(__name__)
CORS(app)  # Enable CORS without any restrictions


app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(user_blueprint, url_prefix='/user')

@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)
