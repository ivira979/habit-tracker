import streamlit as st
import sqlalchemy as db
import sqlite3
import pandas as pd
import random as rd
from sqlalchemy import text
from datetime import datetime
from streamlit_option_menu import option_menu


page_title = "Submission Form"
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
    "Use the below form to submit your tracking:"
)

conn = st.connection("postgresql", type="sql")

try:
   
    habit_query = "select habit_id, habit_name from habits where habit_name not like 'water consumed (oz)' and active_flag = TRUE;"
    df = conn.query(habit_query)
    habit_vals = {}

    with st.form("Submit Your Tracking", True):
        st.write("Submit Your Tracking")
        sub_date = st.date_input("Insert submission date:")
        for index, row in df.iterrows():
            habit_vals[(row['habit_id'],row['habit_name'])] = int(st.checkbox(row['habit_name']))
        habit_vals[(8,'drink water')] = int(st.number_input('How many ounces of water did you drink today?:', step=1))
        st.caption("💧 Reference: 1 cup = 8 oz | 1 mug = 16 oz | 1 liter ≈ 34 oz | 355ml can = 12 oz | 500ml bottle ≈ 17 oz")
        submitted = st.form_submit_button("Create Submission")
        
        if submitted:
            s = str(rd.randint(9, 999999999))
            vals = []
            st.write("**Submission created successfully!**")
            st.write("**Submission details:**")
            st.write("Date - ", sub_date)
            for key in habit_vals:
                st.write(key[1], " - ", habit_vals[key])
                vals.append("("+ "'" + sub_date.strftime("%Y-%m-%d") +"'" + ", " + "'" + str(habit_vals[key]) + "'" + ", " + "'" + str(key[0]) + "'"+ ", " + "'" + s + "'"+ ")")
            q = "INSERT INTO HABIT_SUBMISSION (submission_date, submission_value, sub_habit_id, session_id) VALUES " + ','.join(vals) + ";"
            with conn.session as session:
                session.execute(text(q))
                session.commit()
        else:
            habit_vals = {}


except sqlite3.Error as error:
    print("Error while connecting to sqlite", error)
finally:
    print("")



st.write(
    "Use the below form to search for submissions on a given date:"
)
try:

    with st.form("Search Submission", True):
        st.write("Search Submissions for Date")
        search_date = st.date_input("Select date:")
        submitted = st.form_submit_button("Search")

        if submitted:
            st.info(f"Searching for submissions on: **{search_date.strftime('%Y-%m-%d')}**")
            q = "select h.habit_name, sum(hs.submission_value) number_of_submissions from habit_submission hs join habits h on hs.sub_habit_id = h.habit_id where submission_date = '" + search_date.strftime("%Y-%m-%d") + "' group by h.habit_name"
            pdf = conn.query(q, ttl=5)
            pdf.rename(columns={'habit_name': 'Habit Name', 'number_of_submissions': 'Number of Submissions'}, inplace=True)
            st.write(pdf)

except sqlite3.Error as error:
    print("Error while connecting to sqlite", error)
finally:
    print("")

st.write(
    "Use the below form to clear the submissions for a given date:"
)
try:

    with st.form("Clear Submission", True):
        st.write("Clear Submissions for Date")
        clear_date = st.date_input("Select date:")
        submitted = st.form_submit_button("Clear")

        if submitted:
            st.warning(f"Clearing submissions for date: **{clear_date.strftime('%Y-%m-%d')}**")
            q = "DELETE FROM habit_submission where submission_date = '" + clear_date.strftime("%Y-%m-%d") + "'"
            with conn.session as session:
                session.execute(text(q))
                session.commit()
            st.write("**Submission cleared successfully!**")
           

except sqlite3.Error as error:
    print("Error while connecting to sqlite", error)
finally:
    print("")

