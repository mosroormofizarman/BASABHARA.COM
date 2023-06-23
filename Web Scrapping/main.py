import requests
from bs4 import BeautifulSoup
import csv

# Function to get data from a single listing page
def scrape_listing(listing_url):
    res = requests.get(listing_url)
    soup = BeautifulSoup(res.text, 'html.parser')

    # Get house name
    house_name = soup.find('h1', {'class': 'ds-address-container'}).text.strip()

    # Get address
    address = soup.find('h1', {'class': 'ds-address-container'}).find('span', {'class': 'ds-address-container'}).text.strip()

    # Get photo
    photo = soup.find('div', {'class': 'gallery-image-container'}).find('img')['src']

    # Get details
    details = {}
    for li in soup.find_all('li', {'class': 'ds-bed-bath-living-area'}):
        label = li.find('span', {'class': 'ds-bed-bath-living-area-label'}).text.strip()
        value = li.find('span', {'class': 'ds-bed-bath-living-area-value'}).text.strip()
        details[label] = value

    # Get price
    price = soup.find('span', {'class': 'ds-value'}).text.strip()

    # Create dictionary with all the data
    data = {
        'House Name': house_name,
        'Address': address,
        'Photo': photo,
        'Bedrooms': details.get('Beds', ''),
        'Bathrooms': details.get('Baths', ''),
        'Area (sq ft)': details.get('Sq. Ft.', ''),
        'Price': price
    }

    return data


# Function to scrape multiple listings
def scrape_listings():
    # Define the URLs to scrape
    urls = [
        'https://bikroy.com/bn/ads/dhaka/apartment-rentals/',
        'https://www.bproperty.com/en/dhaka/apartments-for-rent/',
        'https://rents.com.bd/property-type/residential/',
        'https://www.bdhousing.com/homes/listings/Rent/Residential/Apartment/'
        'https://www.sharif.com.bd/rent/'
    ]

    # Create a CSV file to store the data
    with open('listings.csv', 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['House Name', 'Address', 'Photo', 'Bedrooms', 'Bathrooms', 'Area (sq ft)', 'Price'])
        writer.writeheader()

        # Loop through the URLs and scrape each listing
        for url in urls:
            data = scrape_listing(url)
            writer.writerow(data)


# Call the scrape_listings function
scrape_listings()
