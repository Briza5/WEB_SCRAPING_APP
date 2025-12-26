import requests # library to handle HTTP requests
import selectorlib # library to extract data from HTML
from send_email import send_email
import time
import sqlite3 # Added for database connection

# URL of the page to be scraped
url = "https://programmer100.pythonanywhere.com/tours/"
# Headers to mimic a real browser visit
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

connection = sqlite3.connect('data.db') # Instance of the database connection



# Function to scrape the page source
def scrape(url):
    """scrape the page source from the url"""
    response = requests.get(url, headers=HEADERS) # make a GET request to fetch the raw HTML content
    source = response.text # extract the text content from the response object
    return source

# Function to extract data using selectorlib
def extract(source):
    """extract data from the page source"""
    extractor = selectorlib.Extractor.from_yaml_file("extract.yml") # create an extractor object using the YAML file
    value = extractor.extract(source)["tours"] # extract data from the source using the extractor
    return value


# Function to store extracted data in a text file
def store(extracted):
    row = extracted.split(", ")
    row = [item.strip() for item in row]
    cursor = connection.cursor() # Cursor to execute SQL commands
    cursor.execute("INSERT INTO events (band, city, date) VALUES (?, ?, ?)", row) # Insert a new row into the events table
    connection.commit() # Commit the changes to the database

# Function to read read stored data from the database
def read(extracted):
    row = extracted.split(", ")
    row = [item.strip() for item in row]
    band, city, date = row
    cursor = connection.cursor() # Cursor to execute SQL commands
    cursor.execute("SELECT * FROM events WHERE band = ? AND city = ? AND date = ?", (band, city, date)) # Execute SQL query to select events
    rows = cursor.fetchall() # Fetch all results from the executed query¨
    print(rows) # Print the fetched rows      ]
    return rows

# Main loop to continuously check for new tours
if __name__ == "__main__":
   while True:
    scraped = scrape(url)
    extracted = extract(scraped)
    print(extracted)
    
    if extracted != "No upcoming tours":
        row = read(extracted)
        if  not row:
            store(extracted)
            send_email(message="New tour available")
    time.sleep(2)
    