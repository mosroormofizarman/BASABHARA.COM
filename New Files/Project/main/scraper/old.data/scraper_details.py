def get_ad_details():
    # The URLs to extract ad names from, along with their respective search patterns
    urls = {
        "https://rents.com.bd/all-properties/": ('h2', {'class': 'item-title'}),
        #"https://www.bproperty.com/en/dhaka/apartments-for-rent/": ('h2', {'class': '_7f17f34f'}),
        #"https://bikroy.com/en/ads/q/bangladesh/house-rent": ('h2', {'class': 'heading--2eONR heading-2--1OnX8 title--3yncE block--3v-Ow'}),
    }

    # Scraping location and phone number from ad detail page
    location_pattern = ('address', {'class': 'item-address'},
                        )
    phone_number_pattern = ('a', {'class': 'detail-contact--phone-link'},
                            )
    cost_pattern = ('li', {'class': 'item-price item-price-text'},
                            )

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

            if ad_detail_url:
                ad_detail_soup = BeautifulSoup(requests.get(ad_detail_url).text, 'html.parser')

                location_element = ad_detail_soup.find(*location_pattern)
                location = location_element.get_text().strip() if location_element else 'empty'

                phone_number_element = ad_detail_soup.find(*phone_number_pattern)
                phone_number = phone_number_element.get_text().strip() if phone_number_element else 'empty'

                cost_element = ad_detail_soup.find(*cost_pattern)
                cost = cost_element.get_text().strip() if cost_element else 'empty'

            ad_details.append({
                'name': ad_name,
                'location': location,
                'phone_number': phone_number,
                'cost': cost,
            })

    return ad_details
