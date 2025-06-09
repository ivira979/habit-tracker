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
    icons=['house', "list-task", "calendar-check", "bar-chart", "graph-up-arrow", "database-fill-gear"], 
    menu_icon="cast", default_index=curr_index, orientation="vertical")

# Add page description
st.caption("🏠 Home: Overview and changelog for the Habit Tracker app.")

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

CHANGELOG_LINES_TO_SKIP = 6  # header lines
DISPLAY_LATEST = 1  # number or latest versions to display


def show_changelog():
    # suppose that ChangeLog.md is located at the same folder as Streamlit app
    with open('./changelog.md', 'r', encoding='utf-8') as f:
        lines = f.readlines()[CHANGELOG_LINES_TO_SKIP:]

    # lines which contain version numbers only
    version_numbers = [line for line in lines if line.startswith('## [')]

    # number of line, which separates displayed entries from hidden ones
    version_idx = lines.index(version_numbers[DISPLAY_LATEST])

    # display entries
    st.header('Change Log')
    st.markdown(''.join(lines[:version_idx]))

    # hide others with expander
    with st.expander('Previous Versions'):
        st.markdown(''.join(lines[version_idx:]))


show_changelog()







#engine = db.create_engine("sqlite:///habits.db")
#query = 'select * from habits'

#conn = engine.connect()

#df = pd.read_sql(
#    sql=query,
 #   con=conn.connection
#)

#st.write(df)
