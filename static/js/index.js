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
