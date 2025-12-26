import requests # library to handle HTTP requests
import selectorlib # library to extract data from HTML
from send_email import send_email
import time

url = "https://programmer100.pythonanywhere.com/tours/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def scrape(url):
    """scrape the page source from the url"""
    response = requests.get(url, headers=HEADERS) # make a GET request to fetch the raw HTML content
    source = response.text # extract the text content from the response object
    return source


def extract(source):
    """extract data from the page source"""
    extractor = selectorlib.Extractor.from_yaml_file("extract.yml") # create an extractor object using the YAML file
    value = extractor.extract(source)["tours"] # extract data from the source using the extractor
    return value



def store(extracted):
    with open("data.txt", "a") as file:
        file.write(extracted + "\n")

def read(extracted):
    with open("data.txt", "r") as file:
        data = file.read()
    return data

if __name__ == "__main__":
   while True:
       
    scraped = scrape(url)
    extracted = extract(scraped)
    print(extracted)
    content = read(extracted)
    if extracted != "No upcoming tours":
        if  extracted not in content:
            store(extracted)
            send_email(message="New tour available")
    time.sleep(2)
    