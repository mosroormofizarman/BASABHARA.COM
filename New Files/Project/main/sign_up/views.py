from xmlrpc.client import boolean
import firebase_admin, requests
from firebase_admin import credentials, db, auth
from django.shortcuts import render, redirect

# Initialize Firebase Admin with service account credentials
cred = credentials.Certificate('main/firebase_config.json')

try:
    firebase_admin.get_app()
except ValueError:
    firebase_admin.initialize_app(cred)

def signup(request):
    success = False
    message = ""
    if request.method == 'POST':
        username = request.POST.get('Uname')
        email = request.POST.get('Mail')
        password = request.POST.get('Pass')
        age = request.POST.get('Age')
        address = request.POST.get('Address')
        location = request.POST.get('Location')
        gender = request.POST.get('gender')

        ref = db.reference('Registered Users')

        # Check if username or email already exists
        username_exists = ref.child(username).get()
        email_exists = False
        users = ref.get()
        if users is not None:
            for user in users.values():
                if user['email'] == email:
                    email_exists = True
                    break

        if username_exists or email_exists:
            message = "User already registered!"
        else:
            try:
                ad_ref = ref.child(username)
                ad_ref.set({
                        'email': email,
                        'password': password,
                        'age': age,
                        'address': address,
                        'location': location,
                        'gender': gender,
                    })
                user = auth.create_user(email=email, password=password)
                message = ("User registered successfully!")
                success = True
            except:
                success = False
                message = "Data storing failed!"

    if success == True:
        return render(request, 'post.html', {'message': message})
    else:
        return render(request, 'signup.html', {'message': message})


