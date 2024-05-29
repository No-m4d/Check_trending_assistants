import requests
from bs4 import BeautifulSoup
import csv
from datetime import date
import os

url = "https://huggingface.co/chat/assistants/"
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
        writer.writerow(["Name", "Description", "Date"])

    # Find all button elements within the leaderboard, each representing an entry
    for entry in leaderboard.find_all('button'):
        # Find the h3 and p elements within each entry
        name_element = entry.find('h3')
        description_element = entry.find('p')

        # Extract the text from these elements
        if name_element and description_element:
            name = name_element.get_text()
            description = description_element.get_text()

            # Write the name, description, and date to the CSV file
            writer.writerow([name, description, today])
