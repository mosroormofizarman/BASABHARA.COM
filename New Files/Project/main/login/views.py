import firebase_admin, requests
from firebase_admin import credentials, db, auth
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

# Initialize Firebase Admin with service account credentials
cred = credentials.Certificate('main/firebase_config.json')

try:
    firebase_admin.get_app()
except ValueError:
    firebase_admin.initialize_app(cred)

def login_view(request):
    message = ""
    if request.method == 'POST':
        email = request.POST.get('Mail')
        password = request.POST.get('Pass')
        try:
            url = 'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=AIzaSyBa2p_ux3mmCgpBraYM82nuFkJsWAhqBFE'
            data = {
                'email': email,
                'password': password,
                'returnSecureToken': True
            }
            response = requests.post(url, json=data)
            user = response.json()
            if 'error' not in user:
                request.session['uid'] = user['localId']
                message = 'Success'
                return render(request, 'login.html', {'message': message})
            else:
                error_message = user['error']['message']
                if error_message == 'EMAIL_NOT_FOUND':
                    message = 'Email not found!'
                elif error_message == 'INVALID_PASSWORD':
                    message = 'Incorrect password!'
                else:
                    message = 'Authentication error occurred!'
                return render(request, 'login.html', {'message': message})
        except requests.exceptions.RequestException as e:
            message = 'Error occurred during authentication!'
            return render(request, 'login.html', {'message': message})
    else:
        return render(request, 'login.html')