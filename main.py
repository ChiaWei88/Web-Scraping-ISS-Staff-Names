import requests
from bs4 import BeautifulSoup

def scrap(url, data, nullEmails = []):
    # Initialization
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')

    # Start web scraping
    names = soup.select("#ISS_Main_T467AEC33012_Col00 h2 a")
    names = map(lambda x: x.text.strip(), names)
    names = list(names)

    jobTitles = soup.select("#ISS_Main_T467AEC33012_Col00 h3")
    jobTitles = jobTitles[1::2]
    jobTitles = map(lambda x: x.text.strip(), jobTitles)
    jobTitles = list(jobTitles)

    emails = soup.select("#ISS_Main_T467AEC33012_Col00 my-email");
    emails = map(lambda x: x["data-user"].strip()+"@"+x["data-domain"].strip(), emails)
    emails = list(emails)

    for i in nullEmails:
        emails.insert(i, "")

    # Make sure data count is same, else throw an exception
    dataCounts = [len(names), len(jobTitles), len(emails)]
    if(len(set(dataCounts)) > 1):
        raise Exception("The data count is different! in " + url);

    # Print all the data
    count = len(names)
    for i in range(0, count):
        data.add(','.join([names[i], jobTitles[i], emails[i]]))

    print("Done: " + url)

def scrapAll(urls):
    data = set()
    for url in urls:
        if(url=="https://www.iss.nus.edu.sg/about-us/iss-team/adjunct-staff"):
            # Special case, email is missing for 5th staff
            scrap(url, data, [5])
        elif(url=="https://www.iss.nus.edu.sg/about-us/iss-team/adjunct-staff/2"):
            scrap(url, data, [0])
        else:
            scrap(url, data)

    with open('data.csv', 'w') as csvWriter:
        for d in data:
            csvWriter.write(d + "\n")

urls = ["https://www.iss.nus.edu.sg/about-us/iss-team/management",
        "https://www.iss.nus.edu.sg/about-us/iss-team/centres-of-excellence",
        "https://www.iss.nus.edu.sg/about-us/iss-team/practice-chiefs",
        "https://www.iss.nus.edu.sg/about-us/iss-team/graduate-programme-chiefs",
        "https://www.iss.nus.edu.sg/about-us/iss-team/teaching-staff",
        "https://www.iss.nus.edu.sg/about-us/iss-team/teaching-staff/2",
        "https://www.iss.nus.edu.sg/about-us/iss-team/teaching-staff/3",
        "https://www.iss.nus.edu.sg/about-us/iss-team/teaching-staff/analytics-intelligent-systems",
        "https://www.iss.nus.edu.sg/about-us/iss-team/teaching-staff/digital-innovation-design",
        "https://www.iss.nus.edu.sg/about-us/iss-team/teaching-staff/it-service-management",
        "https://www.iss.nus.edu.sg/about-us/iss-team/teaching-staff/it-strategy-management",
        "https://www.iss.nus.edu.sg/about-us/iss-team/teaching-staff/project-management",
        "https://www.iss.nus.edu.sg/about-us/iss-team/teaching-staff/software-engineering-design",
        "https://www.iss.nus.edu.sg/about-us/iss-team/teaching-staff/startup-smes",
        "https://www.iss.nus.edu.sg/about-us/iss-team/administration-staff",
        "https://www.iss.nus.edu.sg/about-us/iss-team/administration-staff/2",
        "https://www.iss.nus.edu.sg/about-us/iss-team/administration-staff/3",
        "https://www.iss.nus.edu.sg/about-us/iss-team/administration-staff/administration",
        "https://www.iss.nus.edu.sg/about-us/iss-team/administration-staff/administration-directors",
        "https://www.iss.nus.edu.sg/about-us/iss-team/administration-staff/business-development",
        "https://www.iss.nus.edu.sg/about-us/iss-team/administration-staff/career-services",
        "https://www.iss.nus.edu.sg/about-us/iss-team/administration-staff/director's-office",
        "https://www.iss.nus.edu.sg/about-us/iss-team/administration-staff/executive-education",
        "https://www.iss.nus.edu.sg/about-us/iss-team/administration-staff/finance",
        "https://www.iss.nus.edu.sg/about-us/iss-team/administration-staff/graduate-programme",
        "https://www.iss.nus.edu.sg/about-us/iss-team/administration-staff/graduate-programme-recruitment",
        "https://www.iss.nus.edu.sg/about-us/iss-team/administration-staff/human-resource",
        "https://www.iss.nus.edu.sg/about-us/iss-team/administration-staff/it-services",
        "https://www.iss.nus.edu.sg/about-us/iss-team/administration-staff/marketing-communications",
        "https://www.iss.nus.edu.sg/about-us/iss-team/administration-staff/quality-management",
        "https://www.iss.nus.edu.sg/about-us/iss-team/adjunct-staff",
        "https://www.iss.nus.edu.sg/about-us/iss-team/adjunct-staff/2"]

scrapAll(urls)
