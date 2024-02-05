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
from flask import Flask, jsonify, request
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

def isValidUser(email, password):
    # This is a mock validation function. Replace it with your actual user validation logic
    return email == 'user@example.com' and password == 'password'

def getUserRole(email):
    # This is a mock function. Replace it with your actual logic to get a user's role
    return 'admin' if email == 'admin@example.com' else 'user'

@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if isValidUser(email, password):
        # Adjust 'secretKey' and expiration time as needed
        token = jwt.encode({'email': email, 'role': getUserRole(email), 'exp': datetime.utcnow() + timedelta(hours=1)}, 'secretKey', algorithm="HS256")
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
    <link rel="stylesheet" href="{{url_for('static', filename='css/index.css')}}">
</head>
<body>
    <div id="login-form">
        <input type="email" id="email" placeholder="Email">
        <input type="password" id="password" placeholder="Password">
        <button onclick="login()">Login</button>
    </div>
    <div id="data"></div>
    <script src="{{url_for('static', filename='js/index.js')}}"></script>
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
    var email = document.getElementById('email').value;
    var password = document.getElementById('password').value;

    fetch('/auth/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({email: email, password: password}),
    })
    .then(response => response.json())
    .then(data => {
        if (data.token) {
            localStorage.setItem('token', data.token);
            fetchSecretData();
        } else {
            alert('Login Failed');
        }
    })
    .catch((error) => {
        console.error('Error:', error);
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
        if (response.ok) return response.json();
        throw new Error('Network response was not ok.');
    })
    .then(data => {
        document.getElementById('data').innerText = data.data;
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('data').innerText = 'No access';
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
