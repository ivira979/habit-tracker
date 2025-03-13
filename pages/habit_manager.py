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

conn = sqlite3.connect('habits.db')
cursor = conn.cursor()

st.write(
    "Use this form to add new habits to the database:"
)
st.write(
    "__Note: You cannot have two habits with the same name at the same time. Please check the habit list below.__"
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
        st.write("Habit Type -", habit_type)
        st.write("Notes -", habit_notes)


st.write(
    "Use this form to activate/deactivate a habit:"
)
st.write(
    "__Note: A deactivated habit will be excluded from the"
    " submission form but still show up on metrics such as"
    " last completed. If you wish to completely delete a habit"
    " from existence, please reach out to the administrator. 'Water Consumed' may not be deactivated at this time.__"
)



habit_query = "select habit_id, habit_name from habits where habit_name not like 'water consumed (oz)';"
df = pd.read_sql(habit_query, conn)
habit_vals = {}



with st.form("Activate/Deactivate a Habit", True):
    st.write("Activate/Deactivate a Habit")
    for index, row in df.iterrows():
        habit_vals[row['habit_id']] = row['habit_name']

    
    habit_selection = st.selectbox("Which habit do you want to manage?",(habit_vals.values()))
    habit_status = st.selectbox("What status do you want to set it to?",("Active","Inactive"))
    habit_notes = st.text_area("Optional: Enter any habit notes you want to add:")
    submitted = st.form_submit_button("Submit")
    
    if submitted:
        active_flag = "True" if habit_status == "Active" else "False"
        update_habit_query = "UPDATE habits SET active_flag = '" + active_flag + \
            "', habit_notes = '" + habit_notes + \
            "' WHERE habit_name like '" + habit_selection + "'"
        run_query(cursor, update_habit_query)
        st.write("**Habit updated successfully!**")
        st.write("**Habit details:**")
        st.write("Habit Name -", habit_selection)
        st.write("Habit Status -", habit_status)
        st.write("Notes -", habit_notes)


habits_all = "select * from habits;"
habits_df = pd.read_sql(habits_all, conn)

st.write(habits_df)