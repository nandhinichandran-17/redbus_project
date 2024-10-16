# importing libraries
import pandas as pd
import mysql.connector
import streamlit as slt
from streamlit_option_menu import option_menu
import plotly.express as px
import time
import base64
import datetime
 #Load bus data for each state
def load_route_data():
    data = {}
    state_files = {
        "Kerala": (r"C:\Users\USER\Desktop\redbus_project/df_k.csv"),
        "Andhra Pradesh": (r"C:\Users\USER\Desktop\redbus_project/df_A.csv"),
        "Telangana": (r"C:\Users\USER\Desktop\redbus_project/df_T.csv"),
        "Goa": (r"C:\Users\USER\Desktop\redbus_project/df_G.csv"),
        "Rajasthan": (r"C:\Users\USER\Desktop\redbus_project/df_R.csv"),
        "South Bengal": (r"C:\Users\USER\Desktop\redbus_project/df_SB.csv"),
        "Haryana": (r"C:\Users\USER\Desktop\redbus_project/df_H.csv"),
        "Assam": (r"C:\Users\USER\Desktop\redbus_project/df_AS.csv"),
        "Uttar Pradesh": (r"C:\Users\USER\Desktop\redbus_project/df_UP.csv"),
        "West Bengal": (r"C:\Users\USER\Desktop\redbus_project/df_WB.csv")
    }
    
    for state, file in state_files.items():
        df = pd.read_csv(file)
        data[state] = df["Route_name"].tolist()
    return data

route_data = load_route_data()

# Setting up Streamlit page
slt.set_page_config(layout="wide")

# Function to encode the image to base64
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Path to your image
img_path = r"C:\Users\USER\Desktop\rebus.png"
bg_img = get_base64(img_path)

# Streamlit CSS to apply the background image
slt.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{bg_img}");
        background-size: cover;
        background-position: center;
    }}
    </style>
    """,
    unsafe_allow_html=True
)
# Sidebar for the menu
with slt.sidebar:
    web = option_menu(
        menu_title="REDBUS",  # Title of the menu
        options=["Home", "📍States and Routes"],  # Options in the menu
        icons=["house", "info-circle"],  # Icons for each option
        orientation="vertical",  # Orientation of the menu
        default_index=0,  # Default selected option
    )

# Home page setting
if web == "Home":
    slt.title("Redbus Data Scraping with Selenium & Dynamic Filtering using Streamlit")
    slt.subheader(":blue[Domain:] Transportation")
    slt.subheader(":blue[Objective:]")
    slt.markdown("The 'Redbus Data Scraping and Filtering with Streamlit Application' aims to revolutionize the transportation industry by providing a comprehensive solution for collecting, analyzing, and visualizing bus travel data. By utilizing Selenium for web scraping, this project automates the extraction of detailed information from Redbus, including bus routes, schedules, prices, and seat availability. By streamlining data collection and providing powerful tools for data-driven decision-making, this project can significantly improve operational efficiency and strategic planning in the transportation industry.")
    slt.subheader(":blue[Overview:]")
    slt.markdown("Selenium: Selenium is a tool used for automating web browsers. It is commonly used for web scraping, which involves extracting data from websites. Selenium allows you to simulate human interactions with a web page, such as clicking buttons, filling out forms, and navigating through pages, to collect the desired data...")
    slt.markdown('''Pandas: Use the powerful Pandas library to transform the dataset from CSV format into a structured dataframe.
                    Pandas helps data manipulation, cleaning, and preprocessing, ensuring that data was ready for analysis.''')
    slt.markdown('''MySQL: With help of SQL to establish a connection to a SQL database, enabling seamless integration of the transformed dataset
                    and the data was efficiently inserted into relevant tables for storage and retrieval.''')
    slt.markdown("Streamlit: Developed an interactive web application using Streamlit, a user-friendly framework for data visualization and analysis.")
    slt.subheader(":blue[Skills Learnt:]")
    slt.markdown("Web Scraping using Selenium, Python, Streamlit, SQL")
    slt.subheader(":blue[Developed By:] Nandhini")

# Main page for States and Routes
if web == "📍States and Routes":
    slt.title("Bus Details by State and Route")

    # Select box for the list of states
    selected_state = slt.selectbox("Select a State", list(route_data.keys()))

        # Select box for the list of routes based on selected state
    selected_route = slt.selectbox("Select a Route", route_data[selected_state])
    # Columns for bus type selection
    col1, col2, col3= slt.columns(3)

    # Step 3: Select bus seating type (Sleeper, Semi-sleeper, Seater)
    with col1:
        select_seating_type = slt.selectbox("Choose Seating Type", ("Sleeper", "Semi-Sleeper", "Seater"))

    # Step 4: Select AC or Non-AC option
    with col2:
        select_ac_type = slt.selectbox("Choose AC Type", ("AC", "Non-AC"))

    # Step 5: Select ratings
    with col3:
        select_ratings = slt.selectbox("Choose Minimum Rating", ("All", "1+", "2+", "3+", "4+", "5"))

    # Step 6: Select bus fare range
    col1, col2= slt.columns(2)
    with col1:
        select_fare_min = slt.number_input("Choose Minimum Fare", min_value=50, max_value=5000, step=50, value=500)
    with col2:
        select_fare_max = slt.number_input("Choose Maximum Fare", min_value=50, max_value=5000, step=50, value=1000)

    # Step 7: Select the time
    TIME = slt.time_input("Select the time", value=datetime.time(12, 00))  # Default time set to 12:00 PM

    # Function to filter and fetch bus details
    def type_and_fare(bus_type, ac_type, fare_min, fare_max, ratings,selected_route):
        conn = mysql.connector.connect(host="localhost", user="root", password="nandu17@", database="RED_BUS_DETAILS")
        my_cursor = conn.cursor()
# Define seating type condition using LIKE to allow flexible matching
        bus_type_condition = ""
        if bus_type == "Sleeper":
            bus_type_condition = "LOWER(Bus_type) LIKE '%sleeper%' AND LOWER(Bus_type) NOT LIKE '%semi%'"
        elif bus_type == "Semi-Sleeper":
            bus_type_condition = "LOWER(Bus_type) LIKE '%semi%'"
        elif bus_type == "Seater":
            bus_type_condition = "LOWER(Bus_type) LIKE '%seater%'"

    
    # Strict condition for AC or Non-AC buses
        if ac_type == "AC":
            ac_condition = "LOWER(Bus_type) LIKE '%a/c%'"
        elif ac_type == "Non-AC":
            ac_condition = "LOWER(Bus_type) NOT LIKE '%a/c%'"
        else:
            ac_condition = "1=1"

        # Define rating condition
        if ratings != "All":
            rating_condition = f"Ratings >= {int(ratings[0])}"
        else:
            rating_condition = "1=1"  # Always true, no rating filter applied

        # SQL query to fetch bus data and remove duplicates
        query = f'''
            SELECT * FROM bus_details 
            WHERE Price BETWEEN {fare_min} AND {fare_max}
            AND Route_name = "{selected_route}"
            AND {bus_type_condition}
            AND {ac_condition}
            AND {rating_condition}
            AND Start_time >= '{TIME}'
            ORDER BY Price DESC, Start_time DESC
        '''
         # Debugging: Check the SQL query being executed
        print(f"Generated SQL query: {query}")


        my_cursor.execute(query)
        out = my_cursor.fetchall()
        conn.close()

        # Load results into pandas dataframe
        df = pd.DataFrame(out, columns=[
            "ID", "Bus_name", "Bus_type", "Start_time", "End_time", "Total_duration",
            "Price", "Seats_Available", "Ratings", "Route_link", "Route_name"
        ])

        # Remove duplicates based on relevant columns
        df = df.drop_duplicates(subset=["Bus_name", "Start_time", "Route_name"])

        return df

    # Fetch the filtered data based on user selections
    df_result = type_and_fare(select_seating_type, select_ac_type, select_fare_min, select_fare_max, select_ratings,selected_route)

    # Display the resulting dataframe if there are results
    if not df_result.empty:
        slt.dataframe(df_result)
    else:
        slt.warning("No buses found for the selected criteria.")



    