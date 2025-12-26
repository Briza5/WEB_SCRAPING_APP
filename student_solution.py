import requests # library to handle HTTP requests
import selectorlib # library to extract data from HTML
import time
import streamlit as st
import plotly.express as px

url = "https://programmer100.pythonanywhere.com"
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
    value = extractor.extract(source)["home"] # extract data from the source using the extractor
    return value



def store(extracted):
    with open("temperatures.txt", "a") as file:
        file.write(extracted + "\n")

figure_place = st.empty() # Placeholder for the figure

if __name__ == "__main__":
   while True:
       
    scraped = scrape(url)
    extracted = extract(scraped)
    print(extracted)
    current_datetime = time.strftime("%d:%m:%Y:%H:%M:%S", time.localtime())
    store(current_datetime + "," + extracted)
    

    with open("temperatures.txt", "r") as file: # read the stored data
        data = file.readlines() # read all lines from the file
        timestamp = [] # list to store timestamps
        temperature = [] # list to store temperatures
        for line in data: # iterate through each line in the file
            dt, temp = line.strip().split(",") # split the line into timestamp and temperature
            timestamp.append(dt) # append timestamp to the list
            temperature.append(temp) # append temperature to the list

    # Create and display the line chart using Plotly
    figure = px.line(x=list(timestamp), y=list(temperature), labels={'x': 'Timestamp', 'y': 'Temperature (°C)'}, title='Temperature over Time')
    figure_place.plotly_chart(figure)
    time.sleep(2)