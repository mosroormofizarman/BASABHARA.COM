import requests
from bs4 import BeautifulSoup
import os, time
from firebase_admin import storage


def get_imgs(firebase_app):

    bucket = storage.bucket(app=firebase_app)

    urls = {
        "https://rents.com.bd/all-properties/": ('h2', {'class': 'item-title'}),
        "https://www.bproperty.com/en/dhaka/apartments-for-rent/": ('h2', {'class': '_7f17f34f'}),
    }

    for url, search_pattern in urls.items():
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        #for item_listing_wrap in soup.find_all('div', {'class': 'item-listing-wrap hz-item-gallery-js card'}):
        for item_listing_wrap in soup.find_all('div', {'class': 'item-listing-wrap hz-item-gallery-js card'}) + soup.find_all('li', {'class': 'ef447dde'}):
            ad_name_element = item_listing_wrap.find(search_pattern[0], search_pattern[1])
            if ad_name_element is not None:
                ad_name = ad_name_element.get_text().strip()
                ad_name = ad_name.replace('.', ' ').replace('$', ' ').replace('#', ' ').replace('[', ' ').replace(']', ' ').replace('/', ' ').replace('-', ' ')
            else:
                ad_name = ''
            
            for img in item_listing_wrap.find_all('img'):
                src = img.get('src')
                if src:
                    filename, extension = os.path.splitext(os.path.basename(src))
                    if extension.lower() in ('.jpg', '.jpeg'):
                        # The image with the same name as the ad name
                        filename = f"{ad_name}"
                        response = requests.get(src)
                        if response.status_code == 200:
                            # Image to Firebase Storage
                            blob = bucket.blob(filename)
                            blob.upload_from_string(response.content, content_type='image/jpeg')
                            print(f'Image {filename} uploaded to Firebase Storage.')
                        else:
                            print(f'Failed to load image {filename}. Status code: {response.status_code}')

    if os.path.exists('images'):
        os.rmdir('images')








