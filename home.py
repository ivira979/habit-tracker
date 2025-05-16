import streamlit as st
import sqlalchemy as db
import pandas as pd
from streamlit_option_menu import option_menu

st.set_page_config(page_title="Home",initial_sidebar_state="collapsed")


page_title = "Home"
page_list = ["Home",  "Submission Form", "Last Completed", "Analytics", "Statistics", "Habit Manager"]
curr_index = page_list.index(page_title)

st.title(page_title)
selected = option_menu(None, page_list, 
    icons=['house', "list-task", "calendar-check", "clipboard-data", "graph-up-arrow", "database-fill-gear"], 
    menu_icon="cast", default_index=curr_index, orientation="vertical")

if selected == page_title:
    print()
elif selected == "Home":
    st.switch_page("home.py")
elif selected == "Submission Form":
    st.switch_page("pages/submission_form.py")
elif selected == "Last Completed":
    st.switch_page("pages/last_completed.py")
elif selected == "Analytics":
    st.switch_page("pages/analytics.py")
elif selected == "Statistics":
    st.switch_page("pages/statistics.py")
elif selected == "Habit Manager":
    st.switch_page("pages/habit_manager.py")
else:
    print()

st.write(
    "Welcome to the Habit Tracker! Please select a tile to get started."
)

st.write(
    "Application is under maintainence - new entries will not be saved. ETA for fix is 05/18"
)







#engine = db.create_engine("sqlite:///habits.db")
#query = 'select * from habits'

#conn = engine.connect()

#df = pd.read_sql(
#    sql=query,
 #   con=conn.connection
#)

#st.write(df)
