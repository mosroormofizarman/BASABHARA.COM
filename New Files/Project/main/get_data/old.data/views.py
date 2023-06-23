import firebase_admin
from firebase_admin import db, credentials, storage
from django.shortcuts import render
import base64, os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#Path to the Firebase admin SDK JSON file
FIREBASE_ADMIN_SDK_FILE = os.path.join(BASE_DIR, 'main', 'firebase_config.json')

#Initialize the Firebase app with the admin SDK credentials
cred = credentials.Certificate(FIREBASE_ADMIN_SDK_FILE)
firebase_admin.initialize_app(cred, {
'databaseURL': 'https://authentication-2244f-default-rtdb.firebaseio.com',
'storageBucket': 'authentication-2244f.appspot.com'
})

def index(request):
    # Get data from Firebase Realtime Database
    ref = db.reference('Ads').order_by_key()
    data_dict = dict(reversed(list(ref.get().items())))
    ads_names = list(data_dict.values())

    app = firebase_admin.get_app()
    bucket = storage.bucket(app=app)

    images = []
    for blob in bucket.list_blobs():
        if blob.content_type.startswith('image/'):
            image_data = blob.download_as_bytes()
            encoded_data = base64.b64encode(image_data).decode('utf-8')
            images.append('data:{};base64,{}'.format(blob.content_type, encoded_data))

    context = {
        'ads_names': ads_names,
        'images': images,
    }
    return render(request, 'get_data.html', context)
