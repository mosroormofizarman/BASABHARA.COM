import os
from .scraper_ads import get_ads
from .scraper_imgs import get_imgs
from .scraper_details import get_ad_details
import firebase_admin
from firebase_admin import credentials, storage
from firebase_admin import db
from django.shortcuts import render

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Path to the Firebase admin SDK JSON file
FIREBASE_ADMIN_SDK_FILE = os.path.join(BASE_DIR, 'main', 'firebase_config.json')

# Initialize the Firebase app with the admin SDK credentials
cred = credentials.Certificate(FIREBASE_ADMIN_SDK_FILE)
firebase_admin.initialize_app(cred, name='my-app', options={
    'databaseURL': 'https://authentication-2244f-default-rtdb.firebaseio.com',
    'storageBucket': 'authentication-2244f.appspot.com'
})

def scrape_ads(request):
    
    ad_names = get_ads()
    
    # Save ad names to Firebase (Not compulsory)
    ref = db.reference('Ads')
    for name in ad_names:
        ref.push(name)
    
    # Getting images
    get_imgs(firebase_admin.get_app(name='my-app'))

    # Getting ads details
    ad_details = get_ad_details()
    
    # Save ad details to Firebase
    ref = db.reference('Details')
    for ad_detail in ad_details:
        ad_name = ad_detail['name']
        ad_location = ad_detail['location']
        ad_phone_number = ad_detail['phone_number']
        ad_cost = ad_detail['cost']

        print(f"Saving details for ad '{ad_name}', location '{ad_location}', phone_number '{ad_phone_number}', cost '{ad_cost}'")
        

        ad_name = ad_name.replace('.', ' ').replace('$', ' ').replace('#', ' ').replace('[', ' ').replace(']', ' ').replace('/', ' ').replace('-', ' ')

        ad_ref = ref.push().child(ad_name)
        ad_ref.set({
            'location': ad_location,
            'phone_number': ad_phone_number,
            'cost': ad_cost
        })

    return render(request, 'success_scrap.html', {'count': len(ad_names)}, {'count': len(ad_details)})
