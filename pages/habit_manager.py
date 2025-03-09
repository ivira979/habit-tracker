import streamlit as st
import sqlalchemy as db
import sqlite3
import pandas as pd
import random as rd
from datetime import datetime
from streamlit_option_menu import option_menu




page_title = "Habit Manager"
page_list = ["Home",  "Submission Form", "Last Completed", "Analytics", "Statistics", "Habit Manager"]
curr_index = page_list.index(page_title)

st.title(page_title)
selected = option_menu(None, page_list, 
    icons=['house', "list-task"], 
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

def run_query(c, q):
    try:
        c.execute(q)
    except sqlite3.Error as error:
        match error.sqlite_errorname:
            case "SQLITE_CONSTRAINT_NOTNULL":
                st.write("Error: Please enter a valid habit name.")
            case "SQLITE_CONSTRAINT_UNIQUE":
                st.write("Error: This habit already exists - please try a different name.")
            case _:
                st.write("Something went wrong! Please try again.")

st.write(
    "Use the below form to add new habits to the database:"
)
with st.form("Add a Habit", True):
    st.write("Add a Habit")
    habit_name = st.text_input("Insert habit name:")
    habit_type = st.selectbox("What type of habit is this?",("Daily","Other"))
    habit_notes = st.text_area("Enter any habit notes:")
    submitted = st.form_submit_button("Create")
    
    if submitted:
        st.write("**Habit created successfully!**")
        st.write("**Habit details:**")
        st.write("Habit Name -", habit_name)
        st.write("Repeat (Y/N) -", habit_repeat)
        st.write("Notes -", habit_notes)


