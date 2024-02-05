# edu-auth-flask

## prepare

```bash
cd ~
cd ws
mkdir auth-server && cd auth-server
pip install Flask PyJWT flask_cors
mkdir -p {./static,./static/js,./static/css,./static/img}
touch ./{server.py,auth_routes.py}
toouch {./static/js/index.js,./static/css/index.css}
mkdir templates
touch ./templates/index.html
#python3 -m venv venv
#source venv/bin/activate
echo "Flask" > requirements.txt
echo "PyJWT" >> requirements.txt
echo "flask_cors" >> requirements.txt
```

## server.py

```bash
cd ~
cd ws
cd auth-server
cat > server.py << 'EOF'
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from auth_routes import auth_blueprint


app = Flask(__name__)
CORS(app)  # Enable CORS without any restrictions


app.register_blueprint(auth_blueprint, url_prefix='/auth')


@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, port=3000)
EOF
```

## auth_routes.py

```bash
cd ~
cd ws
cd auth-server
cat > auth_routes.py << 'EOF'
from flask import Blueprint, request, jsonify
import jwt
from datetime import datetime, timedelta
from functools import wraps

auth_blueprint = Blueprint('auth', __name__)

def isValidUser(username, password):
    # This is a mock validation function. Replace it with your actual user validation logic
    return username == 'user@example.com' and password == 'password'

def getUserRole(username):
    # This is a mock function. Replace it with your actual logic to get a user's role
    return 'admin' if username == 'admin@example.com' else 'user'

@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if isValidUser(username, password):
        # Adjust 'secretKey' and expiration time as needed
        token = jwt.encode({'username': username, 'role': getUserRole(username), 'exp': datetime.utcnow() + timedelta(hours=1)}, 'secretKey', algorithm="HS256")
        return jsonify({'token': token})
    else:
        return jsonify({'error': 'Invalid login'}), 401
EOF
```

## templates/index.html

```bash
cd ~
cd ws
cd auth-server
cat > ./templates/index.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login Page</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/index.css') }}">
</head>
<body>
    <div id="login-form">
        <input type="username" id="username" placeholder="Email">
        <input type="password" id="password" placeholder="Password">
        <button id="login" onclick="login()">Login</button>
        <p id="login-message"></p> <!-- Added paragraph for login messages -->
    </div>
    <div id="data"></div>
    <script src="{{ url_for('static', filename='js/index.js') }}"></script>
</body>
</html>
EOF
```


## static/js/index.js

```bash
cd ~
cd ws
cd auth-server
cat > ./static/js/index.js << 'EOF'
function login() {
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;

    fetch('/auth/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({username: username, password: password}),
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Login Failed');
        }
    })
    .then(data => {
        localStorage.setItem('token', data.token);
        document.getElementById('login-message').textContent = 'Login Successful!';
        fetchSecretData();
    })
    .catch((error) => {
        document.getElementById('login-message').textContent = error.message;
    });
}

function fetchSecretData() {
    const token = localStorage.getItem('token');
    if (!token) {
        document.getElementById('data').innerText = 'No access';
        return;
    }

    fetch('/auth/data', {
        method: 'GET',
        headers: {
            'Authorization': 'Bearer ' + token,
        },
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('No access or token expired');
        }
    })
    .then(data => {
        document.getElementById('data').innerText = data.data;
    })
    .catch(error => {
        document.getElementById('data').innerText = error.message;
    });
}
EOF
```


## static/css/index.css

```bash
cd ~
cd ws
cd auth-server
cat > ./static/css/index.css << 'EOF'
/* Simple CSS for login form */
#login-form {
    display: flex;
    flex-direction: column;
    width: 200px;
    margin: auto;
    margin-top: 100px;
}

#login-form input[type=email], #login-form input[type=password] {
    margin-bottom: 10px;
}

#login-form button {
    cursor: pointer;
}
EOF
```

## Test server

```bash
curl -X POST http://localhost:5000/auth/login -H "Content-Type: application/json" -d '{"username": "user@example.com", "password": "password"}' -w '%{http_code}' -o /dev/null
```
