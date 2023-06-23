import firebase_admin
from firebase_admin import credentials, db
from django.shortcuts import render
from .forms import MyForm

# Initialize Firebase Admin with service account credentials
cred = credentials.Certificate('main/firebase_config.json')

try:
    firebase_admin.get_app()
except ValueError:
    firebase_admin.initialize_app(cred)

ref = db.reference('Ads')

def save_data(request):
    if request.method == 'POST':
        form = MyForm(request.POST)
        if form.is_valid():
            
            ref.push(form.cleaned_data['AdsName'])
            return render(request, 'success.html')
    else:
        form = MyForm()
    return render(request, 'form.html', {'form': form})

