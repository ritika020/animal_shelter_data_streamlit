#import os
#
## Ensure required packages are installed
#try:
#    import db_dtypes
#except ImportError:
#    os.system("pip install db-dtypes")
#
#
#import streamlit as st
#import pandas as pd
#import matplotlib.pyplot as plt
#import seaborn as sns
#import calendar
#from google.cloud import bigquery
#
## Set the correct service account key file path
#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/ritikakhandelwal/Streamlit_app/animalshelter-452610-615f02b0ce22.json"
#
## Function to load data from Google BigQuery
#@st.cache_data
#def load_data():
#    # Set up BigQuery Client
#    project_id = "animalshelter-452610"
#    client = bigquery.Client(project=project_id)
#    
#    # Define dataset and table
#    dataset_id = "animal_shelter_data"
#    table_id = "processed_animalshelterdata"
#
#    # Query to fetch Animal Shelter Data
#    query = f"""
#    SELECT AnimalID, AnimalType, IntakeDate, OutcomeDate, OutcomeType, AgeInMonths, Month
#    FROM `{project_id}.{dataset_id}.{table_id}`
#    """
#
#    # Execute query and load into Pandas DataFrame
#    df = client.query(query).to_dataframe()
#
#    # Convert date columns to datetime format
#    df["IntakeDate"] = pd.to_datetime(df["IntakeDate"], errors='coerce')
#    df["OutcomeDate"] = pd.to_datetime(df["OutcomeDate"], errors='coerce')
#
#    return df
#
## Load data from BigQuery
#df = load_data()
#
## Streamlit UI
#st.title("Animal Shelter Dashboard")
#
## -------------------------------
## Animal Intake Distribution by Type
## -------------------------------
#st.subheader("Animal Intake Distribution by Type")
#
## Create a count of each animal type
#animal_counts = df["AnimalType"].value_counts()
#
## Display bar chart
#st.bar_chart(animal_counts)
#
## -------------------------------
## Animal Outcome Distribution
## -------------------------------
#st.subheader("Animal Outcome Distribution")
#
## Filter data for valid outcomes
#df_outcomes = df.dropna(subset=["OutcomeType"])
#
## Count each OutcomeType
#outcome_counts = df_outcomes["OutcomeType"].value_counts()
#
## Display pie chart
#fig, ax = plt.subplots(figsize=(6, 6))
#ax.pie(
#    outcome_counts, 
#    labels=outcome_counts.index, 
#    autopct='%1.1f%%', 
#    colors=sns.color_palette("Set2"),
#    startangle=90
#)
#ax.set_title("Animal Outcome Distribution")
#
## Show Pie Chart in Streamlit
#st.pyplot(fig)
#
## -------------------------------
## Animal Intakes Over Time
## -------------------------------
#st.subheader("Animal Intakes Over Time")
#
## Convert Month column to datetime
#df["Month"] = pd.to_datetime(df["Month"], format="%Y-%m", errors="coerce")
#
## Group by Month and count intakes
#df_monthly = df.groupby(df["Month"]).size().reset_index(name="Intake Count")
#
## Display line chart
#st.line_chart(df_monthly.set_index("Month")["Intake Count"])
#
## -------------------------------
## Animal Age Distribution
## -------------------------------
#st.subheader("Animal Age Distribution")
#
## Plot histogram
#fig, ax = plt.subplots(figsize=(8, 5))
#sns.histplot(df["AgeInMonths"], bins=20, kde=True, ax=ax)
#ax.set_title("Age Distribution of Animals")
#ax.set_xlabel("Age (Months)")
#
## Show Histogram in Streamlit
#st.pyplot(fig)
#
## -------------------------------
## Animal Type Filter
## -------------------------------
#st.subheader("Filter Data by Animal Type")
#
## Create dropdown filter for AnimalType
#selected_animals = st.multiselect("Select Animal Type(s)", df["AnimalType"].unique(), default=df["AnimalType"].unique())
#
## Filter DataFrame
#filtered_df = df[df["AnimalType"].isin(selected_animals)]
#
## Show filtered data
#st.dataframe(filtered_df)
#
## Run Streamlit app
## Use `streamlit run shelter_dashboard.py` in the terminal

#
#import os
#import json
#import streamlit as st
#import pandas as pd
#import matplotlib.pyplot as plt
#import seaborn as sns
#from google.cloud import bigquery
#
## ✅ Load credentials from Streamlit Secrets
#if "GOOGLE_APPLICATION_CREDENTIALS" in st.secrets:
#    credentials_dict = dict(st.secrets["GOOGLE_APPLICATION_CREDENTIALS"])
#
#    # ✅ Create a temporary JSON file
#    with open("/tmp/gcp_credentials.json", "w") as f:
#        json.dump(credentials_dict, f)
#
#    # ✅ Set the environment variable for authentication
#    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/tmp/gcp_credentials.json"
#
## ✅ Load Data from BigQuery
#@st.cache_data
#def load_data():
#    project_id = "animalshelter-452610"
#    client = bigquery.Client(project=project_id)
#    dataset_id = "animal_shelter_data"
#    table_id = "processed_animalshelterdata"
#
#    query = f"SELECT * FROM `{project_id}.{dataset_id}.{table_id}`"
#    df = client.query(query).to_dataframe()
#    return df
#
## Load data
#df = load_data()
#st.title("Animal Shelter Dashboard")

import os
import json
import base64
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from google.cloud import bigquery

# ✅ Load credentials from Streamlit Secrets
if "GOOGLE_APPLICATION_CREDENTIALS" in st.secrets:
    encoded_credentials = st.secrets["GOOGLE_APPLICATION_CREDENTIALS"]["encoded_key"]

    # ✅ Decode Base64 back to JSON
    credentials_json = base64.b64decode(encoded_credentials).decode("utf-8")
    credentials_dict = json.loads(credentials_json)

    # ✅ Save the credentials to a temporary JSON file
    credentials_path = "/tmp/gcp_credentials.json"
    with open(credentials_path, "w") as f:
        json.dump(credentials_dict, f)

    # ✅ Set the environment variable for authentication
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

# ✅ Load Data from BigQuery
@st.cache_data
def load_data():
    project_id = "animalshelter-452610"
    client = bigquery.Client(project=project_id)
    dataset_id = "animal_shelter_data"
    table_id = "processed_animalshelterdata"

    query = f"SELECT * FROM `{project_id}.{dataset_id}.{table_id}`"
    df = client.query(query).to_dataframe()
    return df

# Load data
df = load_data()
st.title("Animal Shelter Dashboard")
