import streamlit as st
import sqlalchemy as db
import pandas as pd
from streamlit_option_menu import option_menu

st.set_page_config(page_title="Home",initial_sidebar_state="collapsed")



st.title("Home")
selected = option_menu(None, ["Home", "Form"], 
    icons=['house', "list-task"], 
    menu_icon="cast", default_index=0, orientation="vertical")
if selected == "Form":
    st.switch_page("pages/form.py")
st.write(
    "Welcome to the Habit Tracker! Please select a tile to get started."
)








#engine = db.create_engine("sqlite:///habits.db")
#query = 'select * from habits'

#conn = engine.connect()

#df = pd.read_sql(
#    sql=query,
 #   con=conn.connection
#)

#st.write(df)
