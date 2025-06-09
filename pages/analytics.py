import streamlit as st
import sqlalchemy as db
import pandas as pd
import sqlite3
import calendar
from streamlit_option_menu import option_menu




page_title = "Analytics Old"
page_list = ["Home",  "Submission Form", "Last Completed", "Analytics", "Statistics", "Habit Manager"]  # Remove Analytics Test and itself

curr_index = page_list.index(page_title) if page_title in page_list else 0
date_type = ""
habit_q_type = ""

st.title(page_title)
selected = option_menu(None, page_list, 
    icons=['house', "list-task", "calendar-check", "clipboard-data", "bar-chart", "database-fill-gear"], 
    menu_icon="cast", default_index=curr_index, orientation="vertical")

# Add page description
st.caption("📋 Analytics Old: Legacy analytics and reports for your habits.")

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
        habit_q_type = st.selectbox("Select habit type", ("Daily", "Other"))
 
        submitted = st.form_submit_button("Next")

        if submitted:
            st.write("You have selected:") 
            st.write("Search type: ", date_type)
            st.write("Habit type: ", habit_q_type)
            print()

    if(habit_q_type) == "Daily":
        if date_type == "Custom Range":
            with st.form("Custom Range", False):
                st.write("Date Range")
                input_start_date = st.date_input("Enter the start of the date range:")
                input_end_date = st.date_input("Enter the end of the date range:")
                division_period = (input_end_date-input_start_date).days

                submitted = st.form_submit_button("Run report")
                cr_q = "select h.habit_name, (cast(sum(hs.submission_value) as float)/"+str(division_period)+")*100.00 completion_percent from habit_submission hs join habits h on hs.sub_habit_id = h.habit_id where submission_date in (select date_dt from date_dim where date_dt between '"+ str(input_start_date) +"' and '" + str(input_end_date) + "') and h.habit_type = 'D' group by h.habit_name"
                if submitted:
                    date_type = ""
                    st.write("Results:")
                    st.write(conn.query(cr_q))
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
                
                m_q = "select h.habit_name, (cast(sum(hs.submission_value) as float)/"+str(len_month)+")*100.00 completion_percent from habit_submission hs join habits h on hs.sub_habit_id = h.habit_id where submission_date in (select date_dt from date_dim where month_nm = '"+ input_month +"' and cast(year_num as integer) ="+ str(input_m_year) +") and h.habit_type = 'D' group by h.habit_name"

                submitted = st.form_submit_button("Run report")

                if submitted:
                    date_type = ""
                    st.write("For the month of ",input_month,", ", str(input_m_year))
                    st.write("Results:")
                    st.write(conn.query(m_q))
                    print()

        if date_type == "Week":
            with st.form("Week", False):
                st.write("Select Week and Year")
                input_week = st.selectbox("Select week:", options=list(range(1,54)))
                input_w_year = st.selectbox("Select year:", (2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026))

                w_q = "select h.habit_name, (cast(sum(hs.submission_value) as float) / 7)*100.00 completion_percent from habit_submission hs join habits h on hs.sub_habit_id = h.habit_id where submission_date in (select date_dt from date_dim where cast(week_num as integer) ="+str(input_week)+" and cast(year_num as integer) = "+str(input_w_year)+") and h.habit_type = 'D' group by h.habit_name"
                
                submitted = st.form_submit_button("Run report")

                if submitted:
                    date_type = ""
                    st.write("from", conn.query("SELECT MAX(week_start_date) week_start from date_dim where cast(week_num as integer) ="+str(input_week)+" and cast(year_num as integer) = "+str(input_w_year),conn)," to ",pd.read_sql("SELECT MAX(week_end_date) week_end from date_dim where cast(week_num as integer) ="+str(input_week)+" and cast(year_num as integer) = "+str(input_w_year)))
                    st.write("results:", conn.query(w_q))
                    print()

        if date_type == "Year":
            with st.form("Year", False):
                st.write("Select Year")
                input_year = st.selectbox("Select year:", (2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026))

                submitted = st.form_submit_button("Run report")
                y_q = "select h.habit_name, (cast(sum(hs.submission_value) as float) / 365)*100.00 completion_percent from habit_submission hs join habits h on hs.sub_habit_id = h.habit_id where submission_date in (select date_dt from date_dim where cast(year_num as integer) = "+str(input_year)+") and h.habit_type = 'D' group by h.habit_name"


                if submitted:
                    date_type = ""
                    st.write("For the year of ", str(input_year))
                    st.write("results:", conn.query(y_q))
                    print()

    
    if(habit_q_type) == "Other":
        if date_type == "Custom Range":
            with st.form("Custom Range", False):
                st.write("Date Range")
                input_start_date = st.date_input("Enter the start of the date range:")
                input_end_date = st.date_input("Enter the end of the date range:")
                division_period = (input_end_date-input_start_date).days

                submitted = st.form_submit_button("Run report")
                cr_q = "select h.habit_name, sum(hs.submission_value) number_of_completions from habit_submission hs join habits h on hs.sub_habit_id = h.habit_id where submission_date in (select date_dt from date_dim where date_dt between '"+ str(input_start_date) +"' and '" + str(input_end_date) + "') and h.habit_type = 'O' group by h.habit_name"
                if submitted:
                    date_type = ""
                    st.write("Results:")
                    st.write(conn.query(cr_q))
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
                
                m_q = "select h.habit_name, sum(hs.submission_value) number_of_completions from habit_submission hs join habits h on hs.sub_habit_id = h.habit_id where submission_date in (select date_dt from date_dim where month_nm = '"+ input_month +"' and cast(year_num as integer) ="+ str(input_m_year) +") and h.habit_type = 'O' group by h.habit_name"

                submitted = st.form_submit_button("Run report")

                if submitted:
                    date_type = ""
                    st.write("For the month of ",input_month,", ", str(input_m_year))
                    st.write("Results:")
                    st.write(conn.query(m_q))
                    print()

        if date_type == "Week":
            with st.form("Week", False):
                st.write("Select Week and Year")
                input_week = st.selectbox("Select week:", options=list(range(1,54)))
                input_w_year = st.selectbox("Select year:", (2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026))

                w_q = "select h.habit_name, sum(hs.submission_value) number_of_completions from habit_submission hs join habits h on hs.sub_habit_id = h.habit_id where submission_date in (select date_dt from date_dim where cast(week_num as integer) ="+str(input_week)+" and cast(year_num as integer) = "+str(input_w_year)+") and h.habit_type = 'O' group by h.habit_name"
                
                submitted = st.form_submit_button("Run report")

                if submitted:
                    date_type = ""
                    st.write("from", conn.query("SELECT MAX(week_start_date) week_start from date_dim where cast(week_num as integer) ="+str(input_week)+" and cast(year_num as integer) = "+str(input_w_year),conn)," to ",pd.read_sql("SELECT MAX(week_end_date) week_end from date_dim where cast(week_num as integer) ="+str(input_week)+" and cast(year_num as integer) = "+str(input_w_year)))
                    st.write("results:", conn.query(w_q))
                    print()

        if date_type == "Year":
            with st.form("Year", False):
                st.write("Select Year")
                input_year = st.selectbox("Select year:", (2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026))

                submitted = st.form_submit_button("Run report")
                y_q = "select h.habit_name, sum(hs.submission_value) number_of_completions from habit_submission hs join habits h on hs.sub_habit_id = h.habit_id where submission_date in (select date_dt from date_dim where cast(year_num as integer) = "+str(input_year)+") and h.habit_type = 'O' group by h.habit_name"


                if submitted:
                    date_type = ""
                    st.write("For the year of ", str(input_year))
                    st.write("results:", conn.query(y_q))
                    print()
except sqlite3.Error as error:
    print("Error while connecting to sqlite", error)
finally:
    print("")