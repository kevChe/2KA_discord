import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# Replace with your Pixiv username and password
USERNAME = 'sicksticky123'
PASSWORD = 'kedavirr'

# Create a new requests session
session = requests.Session()

# Log in to Pixiv
login_url = 'https://accounts.pixiv.net/login'
login_data = {
    'pixiv_id': USERNAME,
    'password': PASSWORD,
}
response = session.post(login_url, data=login_data)

# Check if login was successful
if 'error' in response.url:
    print('Login failed')
else:
    print('Login successful')

    # Replace with the URL of the Pixiv page you want to scrape
    url = 'https://www.pixiv.net/artworks/106171161'

    # Use the session to get the page content
    page = session.get(url)

    # Check if the page has any content
    if page.content:
        # Parse the page with BeautifulSoup
        soup = BeautifulSoup(page.content, 'html.parser')

        # Find all image elements on the page
        images = soup.find_all('img')

        # Create a directory to store the downloaded images
        directory = urlparse(url).path.split('/')[-1]
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Loop through the images and download them
        for image in images:
            image_url = image['src']
            image_data = session.get(image_url).content
            image_filename = os.path.join(directory, urlparse(image_url).path.split('/')[-1])
            with open(image_filename, 'wb') as f:
                f.write(image_data)
            print(f'Downloaded {image_filename}')
    else:
        print('The page has no content')