import streamlit as st
import sqlalchemy as db
from sqlalchemy import text
import pandas as pd
import random as rd
from datetime import datetime
from streamlit_option_menu import option_menu




page_title = "Habit Manager"
page_list = ["Home",  "Submission Form", "Last Completed", "Analytics", "Statistics", "Habit Manager"]
curr_index = page_list.index(page_title)

st.title(page_title)
selected = option_menu(None, page_list, 
    icons=['house', "list-task", "calendar-check", "bar-chart", "graph-up-arrow", "database-fill-gear"], 
    menu_icon="cast", default_index=curr_index, orientation="vertical")

# Add page description
st.caption("⚙️ Habit Manager: Add, activate, or deactivate habits.")

if selected == page_title:
    print()
elif selected == "Home":
    st.switch_page("home.py")
elif selected == "Submission Form":
    st.switch_page("pages/submission_form.py")
elif selected == "Last Completed":
    st.switch_page("pages/last_completed.py")
elif selected == "Analytics":
    st.switch_page("pages/analytics_test.py")
elif selected == "Statistics":
    st.switch_page("pages/statistics.py")
elif selected == "Habit Manager":
    st.switch_page("pages/habit_manager.py")
else:
    print()


conn = st.connection("postgresql", type="sql")

st.write(
    "__Note: You cannot have two habits with the same name at the same time. Please check the habit list below.__"
)
with st.form("Add a Habit", True):
    st.write("Add a Habit")
    habit_name = st.text_input("Insert habit name:")
    habit_type = st.selectbox("What type of habit is this?",("Daily","Other"))
    submitted = st.form_submit_button("Create")
    
    if submitted:
        st.write("**Habit created successfully!**")
        st.write("**Habit details:**")
        st.write("Habit Name -", habit_name)
        st.write("Habit Type -", habit_type)
        habit_type = 'D' if habit_type == 'Daily' else 'O'
        insert_habit_query = "INSERT INTO habits (habit_name, habit_type, active_flag) VALUES ('"+habit_name+"','"+habit_type+"',TRUE)"
        with conn.session as session:
                session.execute(text(insert_habit_query))
                session.commit()

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
df = conn.query(habit_query, ttl=5)
habit_vals = {}



with st.form("Activate/Deactivate a Habit", True):
    st.write("Activate/Deactivate a Habit")
    for index, row in df.iterrows():
        habit_vals[row['habit_id']] = row['habit_name']

    
    habit_selection = st.selectbox("Which habit do you want to manage?",(habit_vals.values()))
    habit_status = st.selectbox("What status do you want to set it to?",("Active","Inactive"))
    submitted = st.form_submit_button("Submit")
    
    if submitted:
        active_flag = "True" if habit_status == "Active" else "False"
        update_habit_query = "UPDATE habits SET active_flag = '" + active_flag + \
            "' WHERE habit_name like '" + habit_selection + "'"
        with conn.session as session:
                session.execute(text(update_habit_query))
                session.commit()
        st.write("**Habit updated successfully!**")
        st.write("**Habit details:**")
        st.write("Habit Name -", habit_selection)
        st.write("Habit Status -", habit_status)
       


habits_all = "select * from habits;"
habits_df = conn.query(habits_all, ttl=5)

st.write(habits_df)