import requests
import json
from bs4 import BeautifulSoup

# Load configurations
with open('config.json') as config:
    settings = json.load(config)
    delimiter = settings["delimiter"]
    targetUrls = settings["urls"]

# Web scrap individual staff url
# Parameter "data" is a set with guarantee of no duplicated records
def scrap(url, data):
    # Initialization
    names = []
    titles = []
    emails = []
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    profiles = soup.select("#ISS_Main_T467AEC33012_Col00 .block-profile-thumb");

    # Extract information based on css selectors
    for profile in profiles:
        element_name = profile.select_one("h2 a")
        element_title = profile.select_one("h3")
        element_email = profile.select_one("my-email")

        # Skip the records if is blank profile
        if (element_name is None and
                    element_title is None and
                    element_email is None): continue

        # At least one of the attribute is not blank
        # Save the data in corresponding list
        names.append(element_name.text.strip() if element_name is not None else "")
        titles.append(element_title.text.strip() if element_title is not None else "")
        emails.append(element_email["data-user"].strip() + "@" + element_email[
            "data-domain"].strip() if element_email is not None else "")

    # Store the concatenated values with delimiter
    for i in range(0, len(names)):
        data.add(delimiter.join([names[i], titles[i], emails[i]]))

    print("scrap() executed successfully for " + url)

# Web scrap on a list of urls
def scrapAll(urls):
    # Define a set for storing data to avoid duplication.
    data = set()

    # Special case, missing emails for some staffs
    for url in urls:
        scrap(url, data)

    # Write data into csv file
    with open('data.csv', 'w') as csvWriter:
        # Print header
        csvWriter.write(delimiter.join(["Name", "Title", "Email(s)"]) + "\n")

        # Print body
        for d in data:
            csvWriter.write(d + "\n")

    print("scrapAll() executed successfully.")

# Main execution
scrapAll(targetUrls)
