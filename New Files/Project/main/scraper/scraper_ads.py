import requests
from bs4 import BeautifulSoup

def get_ads():
    # The URLs to extract ad names from, along with their respective search patterns
    urls = {
        "https://rents.com.bd/all-properties/": ('h2', {'class': 'item-title'}),
        "https://www.bproperty.com/en/dhaka/apartments-for-rent/": ('h2', {'class': '_7f17f34f'}),
        
    }

    ad_names = []
    for url, search_pattern in urls.items():
       
        response = requests.get(url)
        html_content = response.text

        soup = BeautifulSoup(html_content, 'html.parser')
        for ad_name in soup.find_all(*search_pattern):
            ad_names.append(ad_name.get_text().strip())

    return ad_names
