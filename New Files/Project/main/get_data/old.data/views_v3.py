import firebase_admin
from firebase_admin import db, credentials, storage
from django.shortcuts import render
import base64, os, requests
from bs4 import BeautifulSoup

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
    # The URLs to extract ad names from, along with their respective search patterns
    urls = {
        "https://rents.com.bd/all-properties/": ('h2', {'class': 'item-title'}),
    }

    # Scraping location, phone number, cost, and images from ad detail page
    location_pattern = ('address', {'class': 'item-address'})
    phone_number_pattern = ('a', {'class': 'detail-contact--phone-link'})
    cost_pattern = ('li', {'class': 'item-price item-price-text'})
    image_pattern = ('img', {'src': lambda s: s.endswith('.jpg') or s.endswith('.jpeg')})

    ad_details = []
    for url, search_pattern in urls.items():
        # Fetching the HTML content of the webpage
        response = requests.get(url)
        html_content = response.text

        soup = BeautifulSoup(html_content, 'html.parser')
        for ad_detail in soup.find_all(*search_pattern):
            ad_name = ad_detail.get_text().strip()
            ad_detail_url = ad_detail.a['href'] if ad_detail.a else ''

            location = 'empty'
            phone_number = 'empty'
            cost = 'empty'
            images = []

            if ad_detail_url:
                ad_detail_soup = BeautifulSoup(requests.get(ad_detail_url).text, 'html.parser')

                location_element = ad_detail_soup.find(*location_pattern)
                location = location_element.get_text().strip() if location_element else 'empty'

                phone_number_element = ad_detail_soup.find(*phone_number_pattern)
                phone_number = phone_number_element.get_text().strip() if phone_number_element else 'empty'

                cost_element = ad_detail_soup.find(*cost_pattern)
                cost = cost_element.get_text().strip() if cost_element else 'empty'

                image_elements = ad_detail_soup.find_all(*image_pattern)
                for image_element in image_elements:
                    image_url = image_element['src']
                    if image_url.startswith('//'):
                        image_url = 'https:' + image_url
                    response = requests.get(image_url)
                    encoded_image = base64.b64encode(response.content).decode('utf-8')
                    images.append(encoded_image)

            ad_details.append({
                'name': ad_name,
                'location': location,
                'phone_number': phone_number,
                'cost': cost,
                'images': images,
            })

    context = {
        'ad_details' : ad_details,
    }

    return render(request, 'get_data.html', context)

