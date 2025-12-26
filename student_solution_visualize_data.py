import streamlit as st
import plotly.express as px
import sqlite3 # Added for database connection

connection = sqlite3.connect('data.db') # Instance of the database connection


# Function to read read stored data from the database
def read():
    cursor = connection.cursor() # Cursor to execute SQL commands
    cursor.execute("SELECT * FROM Temperatures") # Execute SQL query to select events
    rows = cursor.fetchall() # Fetch all results from the executed query
    temperature = []
    timestamp = []
    for row in rows:
        time = row[0]
        temp = row[1]
        timestamp.append(time)
        temperature.append(temp)
    return timestamp, temperature


timestamp, temperature= read() # read the stored data
# Create and display the line chart using Plotly
figure = px.line(x=list(timestamp), y=list(temperature), labels={'x': 'Timestamp', 'y': 'Temperature (°C)'}, title='Temperature over Time')
st.plotly_chart(figure)
