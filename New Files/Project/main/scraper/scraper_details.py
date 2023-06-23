import requests
from bs4 import BeautifulSoup


def get_ad_details():
    # URLs to extract ad details from
    urls = [
        {
            'url': 'https://rents.com.bd/all-properties/',
            'ad_selector': '.item-listing-wrap.hz-item-gallery-js.card',
            'name_selector': '.item-title',
            'location_selector': '.item-address',
            'phone_number_selector': '.detail-contact--phone-link',
            'cost_selector': '.item-price-text',
        },
        {
            'url': 'https://www.bproperty.com/en/dhaka/apartments-for-rent/',
            'ad_selector': '.ef447dde',
            'name_selector': '._7f17f34f',
            'location_selector': '._7afabd84',
            'phone_number_selector': '.listing-details__contact > .d-inline-block',
            'cost_selector': '.f343d9ce',
        },
        {
            'url': 'https://bikroy.com/en/ads/q/bangladesh/house-rent',
            'ad_selector': '.ui-item',
            'name_selector': '.ui-item-title > a',
            'location_selector': '.ui-item-location',
            'phone_number_selector': '.ui-item-bottom-row > .ui-item-phone',
            'cost_selector': '.ui-item-price',
        },
    ]

    ad_details = []
    for url_info in urls:
        # Fetching the HTML content of the webpage
        response = requests.get(url_info['url'])
        html_content = response.text

        soup = BeautifulSoup(html_content, 'html.parser')
        for ad_element in soup.select(url_info['ad_selector']):
            name_element = ad_element.select_one(url_info['name_selector'])
            ad_name = name_element.get_text().strip() if name_element else 'empty'

            location_element = ad_element.select_one(url_info['location_selector'])
            location = location_element.get_text().strip() if location_element else 'empty'

            phone_number_element = ad_element.select_one(url_info['phone_number_selector'])
            phone_number = phone_number_element.get_text().strip() if phone_number_element else 'empty'

            cost_element = ad_element.select_one(url_info['cost_selector'])
            cost = cost_element.get_text().strip() if cost_element else 'empty'

            ad_details.append({
                'name': ad_name,
                'location': location,
                'phone_number': phone_number,
                'cost': cost,
            })

    return ad_details

