import requests
from bs4 import BeautifulSoup

# Initialization
html = requests.get("https://www.iss.nus.edu.sg/about-us/iss-team/graduate-programme-chiefs").text
soup = BeautifulSoup(html, 'html.parser')

# Start web scraping
names = soup.select("#ISS_Main_T467AEC33012_Col00 h2 a")
names = map(lambda x: x.text, names)
names = list(names)

jobTitles = soup.select("#ISS_Main_T467AEC33012_Col00 h3")
jobTitles = map(lambda x: x.text, jobTitles)
jobTitles = filter(lambda x: x != "", jobTitles)
jobTitles = list(jobTitles)

emails = soup.select("#ISS_Main_T467AEC33012_Col00 my-email");
emails = map(lambda x: x["data-user"]+"@"+x["data-domain"], emails)
emails = list(emails)

# Make sure data count is same, else throw an exception
dataCounts = [len(names), len(jobTitles), len(emails)]
if(len(set(dataCounts)) > 1):
    raise Exception("The data count is different!");

# Print all the data
count = len(names)
for i in range(0, count):
    print('{0}. {1} has position of "{2}" with email "{3}".'
          .format(i+1, names[i], jobTitles[i], emails[i]))

with open('data.csv', 'w') as f:
    f.write("Name, Rank, Title, Email" + "\n")
    for i in range(0, count):
        f.write(",".join([names[i], jobTitles[i], emails[i]]) + "\n")


