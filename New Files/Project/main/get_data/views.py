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

def getdata(request):
    search_query = request.GET.get('search')
    
    ref = db.reference('Details').order_by_key()
    data_dict = dict(ref.get() or {})

    ads = []
    for unique_code, ad_data in data_dict.items():
        ad = {}
        ad_name = list(ad_data.keys())[0]
        ad['name'] = ad_name
        ad['location'] = ad_data[ad_name]['location']
        ad['phone_number'] = ad_data[ad_name]['phone_number']
        ad['cost'] = ad_data[ad_name]['cost']
        ads.append(ad)

    if search_query:
        ads = [ad for ad in ads if search_query.lower() in ad['name'].lower()]

    app = firebase_admin.get_app()
    bucket = storage.bucket(app=app)

    images = []
    for ad in ads:
        blob = bucket.blob(ad['name'])
        if blob.exists():
            image_data = blob.download_as_bytes()
            encoded_data = base64.b64encode(image_data).decode('utf-8')
            images.append('data:{};base64,{}'.format(blob.content_type, encoded_data))

    context = {
        'ads': ads,
        'images': images,
        'search_query': search_query,
    }
    return render(request, 'get_data.html', context)









