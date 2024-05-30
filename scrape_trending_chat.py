import requests
from bs4 import BeautifulSoup
import csv
from datetime import date
import os

url = "https://huggingface.co/chat/assistants/"
image_base_url = 'https://huggingface.co'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find the leaderboard container
leaderboard = soup.find('div', {'class': 'mt-8 grid grid-cols-2 gap-3 sm:gap-5 md:grid-cols-3 lg:grid-cols-4'})

# Get today's date
today = date.today()

# Open the CSV file for appending
with open(os.path.join(os.getcwd(), 'trending_per_day.csv'), 'a', newline='') as file:
    writer = csv.writer(file)
    # Write the header only if the file is empty
    if file.tell() == 0:
        writer.writerow(["Name", "Description", "Date", "Image"])

    # Find all button elements within the leaderboard, each representing an entry
    for entry in leaderboard.find_all('button'):
        # Find the h3 and p elements within each entry
        name_element = entry.find('h3')
        description_element = entry.find('p')
        # Find images
        image_element = entry.find('img')
        # if there is no image, set the image URL to None, otherwise create a URL to the image
        image_url = None
        if image_element:
            image_url = image_base_url + image_element['src']

        # Extract the text from these elements
        if name_element and description_element:
            name = name_element.get_text()
            description = description_element.get_text()

            # Write the name, description, and date to the CSV file
            writer.writerow([name, description, today, image_url])
