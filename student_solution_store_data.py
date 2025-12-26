import requests # library to handle HTTP requests
import selectorlib # library to extract data from HTML
import time
import sqlite3 # Added for database connection

url = "https://programmer100.pythonanywhere.com"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
connection = sqlite3.connect('data.db') # Instance of the database connection

def scrape(url):
    """scrape the page source from the url"""
    response = requests.get(url, headers=HEADERS) # make a GET request to fetch the raw HTML content
    source = response.text # extract the text content from the response object
    return source


def extract(source):
    """extract data from the page source"""
    extractor = selectorlib.Extractor.from_yaml_file("extract.yml") # create an extractor object using the YAML file
    value = extractor.extract(source)["home"] # extract data from the source using the extractor
    return value



def store(extracted):
    current_datetime = time.strftime("%d:%m:%Y:%H:%M:%S", time.localtime())
    cursor = connection.cursor() # Cursor to execute SQL commands
    cursor.execute("INSERT INTO Temperatures (timestamp, temperature) VALUES (?, ?)", (current_datetime, extracted)) # Insert a new row into the Temperatures table
    connection.commit() # Commit the changes to the database

if __name__ == "__main__":
   while True:
    scraped = scrape(url)
    extracted = extract(scraped)
    print(extracted)
    store(extracted) # store the scraped data
    time.sleep(2)