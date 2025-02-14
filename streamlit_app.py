import streamlit as st
import sqlalchemy as db
import pandas as pd

st.set_page_config(page_title="Home")



st.title("Home")
st.write(
    "Welcome to the Habit Tracker! Please select a tile to get started."
)

def menu():
    st.sidebar.page_link("pages/form.py", label="TEST")


menu()




'''engine = db.create_engine("sqlite:///habits.db")
query = 'select * from habits'

conn = engine.connect()

df = pd.read_sql(
    sql=query,
    con=conn.connection
)

st.write(df)'''