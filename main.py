import requests
import json
from bs4 import BeautifulSoup

# web scrap individual staff url
# data has set type, no duplicated values
# nullEmails is indexes of nth-staff who does not have email on site
def scrap(url, data, nullEmails = []):
    # Initialization
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')

    # Start web scraping
    names = soup.select("#ISS_Main_T467AEC33012_Col00 h2 a")
    names = map(lambda x: x.text.strip(), names)
    names = list(names)

    titles = soup.select("#ISS_Main_T467AEC33012_Col00 h3")
    titles = titles[0::2]
    titles = map(lambda x: x.text.strip(), titles)
    titles = list(titles)

    emails = soup.select("#ISS_Main_T467AEC33012_Col00 my-email");
    emails = map(lambda x: x["data-user"].strip()+"@"+x["data-domain"].strip(), emails)
    emails = list(emails)

    # Insert blank entry into emails
    for i in nullEmails:
        emails.insert(i, "")

    # Error checking. Make sure data count is same, else throw an exception
    dataCounts = [len(names), len(titles), len(emails)]
    if(len(set(dataCounts)) > 1):
        raise Exception("The data count is different in " + url);

    # Print all the data
    count = len(names)
    for i in range(0, count):
        data.add('|'.join([names[i],
                           titles[i],
                           emails[i]]))

    print("scrap() executed successfully for " + url)

def scrapAll(urls):
    # Define a set for storing data to avoid duplication.
    data = set()

    # Special case, missing emails for some staffs
    for url in urls:
        if(url=="https://www.iss.nus.edu.sg/about-us/iss-team/adjunct-staff"):
            scrap(url, data, [5])
        elif(url=="https://www.iss.nus.edu.sg/about-us/iss-team/adjunct-staff/2"):
            scrap(url, data, [0])
        else:
            scrap(url, data)

    # Write data into csv file
    with open('data.csv', 'w') as csvWriter:
        for d in data:
            csvWriter.write(d + "\n")

    print("scrapAll() executed successfully.")

with open('config.json') as config:
    urls = json.load(config)["urls"]

scrapAll(urls)
