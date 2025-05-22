import streamlit as st
import sqlalchemy as db
import pandas as pd
import calendar
import sqlite3
from streamlit_option_menu import option_menu




page_title = "Statistics"
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
try:
    conn = st.connection("postgresql", type="sql")

    with st.form("Report Period", False):
        st.write("Date Type")
        date_type = st.selectbox("Select date type",("Week","Month","Year", "Custom Range"))
        submitted = st.form_submit_button("Next")

        if submitted:
            st.write("You have selected:") 
            st.write("Search type: ", date_type)
            print()

    
    if date_type == "Custom Range":
        with st.form("Custom Range", False):
            st.write("Date Range")
            input_start_date = st.date_input("Enter the start of the date range:")
            input_end_date = st.date_input("Enter the end of the date range:")
            division_period = (input_end_date-input_start_date).days

            submitted = st.form_submit_button("Run report")
            cr_q = "with a as (select h.habit_name, (cast(sum(hs.submission_value) as float)/"+str(division_period)+")*100.00 number_of_submissions from habit_submission hs join habits h on hs.sub_habit_id = h.habit_id where submission_date in (select date_dt from date_dim where date_dt between '"+ str(input_start_date) +"' and '" + str(input_end_date) + "') and h.habit_type = 'D' group by h.habit_name) select sum(a.number_of_submissions) All_Daily_Habits from a"
            if submitted:
                date_type = ""
                cr_q_r = conn.query(cr_q, ttl='1m')
                r = cr_q_r['all_daily_habits'].iloc[0]
                r = int(0 if r is None else r)
                st.write("Results: ", round(r, 2), "% of daily tasks have been completed! Wah Wah!")
                print()

    if date_type == "Month":
        with st.form("Month", False):
            st.write("Select Month and Year")
            input_month = st.selectbox("Select month:", ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"))
            input_m_year = st.selectbox("Select year:", (2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026))
            
            year = int(input_m_year)
            month_index = 0
            
            if input_month == "January":
                month_index = 1
            if input_month == "February":
                month_index = 2
            if input_month == "March":
                month_index = 3
            if input_month == "April":
                month_index = 4
            if input_month == "May":
                month_index = 5
            if input_month == "June":
                month_index = 6
            if input_month == "July":
                month_index = 7
            if input_month == "August":
                month_index = 8
            if input_month == "September":
                month_index = 9
            if input_month == "October":
                month_index = 10
            if input_month == "November":
                month_index = 11
            if input_month == "December":
                month_index = 12

            len_month = calendar.monthrange(year, month_index)[1]
            
            m_q = "with a as(select h.habit_name, (cast(sum(hs.submission_value) as float)/"+str(len_month)+")*100.00 number_of_submissions from habit_submission hs join habits h on hs.sub_habit_id = h.habit_id where submission_date in (select date_dt from date_dim where month_nm = '"+ input_month +"' and cast(year_num as integer) ="+ str(input_m_year) +") and h.habit_type = 'D' group by h.habit_name) select sum(a.number_of_submissions) All_Daily_Habits from a"

            submitted = st.form_submit_button("Run report")

            if submitted:
                date_type = ""
                st.write("For the month of ",input_month,", ", str(input_m_year))
                m_q_r = conn.query(m_q,ttl='1m')
                r = m_q_r['All_Daily_Habits'].iloc[0]
                r = int(0 if r is None else r)
                st.write("Results: ", round(r, 2), "% of daily tasks have been completed! Wah Wah!")
                print()

    if date_type == "Week":
        with st.form("Week", False):
            st.write("Select Week and Year")
            input_week = st.selectbox("Select week:", options=list(range(1,54)))
            input_w_year = st.selectbox("Select year:", (2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026))

            w_q = "with a as(select h.habit_name, (cast(sum(hs.submission_value) as float) / 7)*100.00 number_of_submissions from habit_submission hs join habits h on hs.sub_habit_id = h.habit_id where submission_date in (select date_dt from date_dim where cast(week_num as integer) ="+str(input_week)+" and cast(year_num as integer) = "+str(input_w_year)+") and h.habit_type = 'D' group by h.habit_name) select sum(a.number_of_submissions) All_Daily_Habits from a"
            
            submitted = st.form_submit_button("Run report")

            if submitted:
                date_type = ""
                st.write("from", conn.query("SELECT MAX(week_start_date) week_start from date_dim where cast(week_num as integer) ="+str(input_week)+" and cast(year_num as integer) = "+str(input_w_year))," to ",conn.query("SELECT MAX(week_end_date) week_end from date_dim where cast(week_num as integer) ="+str(input_week)+" and cast(year_num as integer) = "+str(input_w_year)))
                w_q_r = conn.query(w_q, ttl='1m')
                r = w_q_r['all_daily_habits'].iloc[0]
                r = int(0 if r is None else r)
                st.write("Results: ", round(r, 2), "% of daily tasks have been completed! Wah Wah!")
                print()

    if date_type == "Year":
        with st.form("Year", False):
            st.write("Select Year")
            input_year = st.selectbox("Select year:", (2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026))

            submitted = st.form_submit_button("Run report")
            y_q = "with a as (select h.habit_name, (cast(sum(hs.submission_value) as float) / 365)*100.00 number_of_submissions from habit_submission hs join habits h on hs.sub_habit_id = h.habit_id where submission_date in (select date_dt from date_dim where cast(year_num as integer) = "+str(input_year)+") and h.habit_type = 'D' group by h.habit_name) select sum(a.number_of_submissions) All_Daily_Habits from a"


            if submitted:
                date_type = ""
                st.write("For the year of ", str(input_year))
                y_q_r = conn.query(y_q, ttl='1m')
                r = y_q_r['all_daily_habits'].iloc[0]
                r = int(0 if r is None else r)
                st.write("Results: ", round(r, 2), "% of daily tasks have been completed! Wah Wah!")
                print()

except RuntimeError as error:
    print("Error while connecting to sqlite", error)
