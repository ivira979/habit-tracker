import streamlit as st
import sqlalchemy as db
import pandas as pd
import sqlite3
import psycopg2
import altair as alt
from streamlit_option_menu import option_menu




page_title = "Last Completed"
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


conn = st.connection("postgresql", type="sql")
df = conn.query('select habit_name, last_completed_relative_to_now from v_hab_last_completed;', ttl=5)
df.rename(columns={'habit_name': 'Habit Name', 'last_completed_relative_to_now': 'Last Completed'}, inplace=True)
st.dataframe(df, height=425)