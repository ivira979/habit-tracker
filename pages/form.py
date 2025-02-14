import streamlit as st
from streamlit_option_menu import option_menu


st.title("Habits Management")
selected = option_menu(None, ["Home", "Form"], 
    icons=['house', "list-task"], 
    menu_icon="cast", default_index=1, orientation="vertical")
if selected == "Home":
    st.switch_page("streamlit_app.py")
st.write(
    "Use the below form to add new habits to the database:"
)
with st.form("Add a Habit", True):
    st.write("Add a Habit")
    habit_name = st.text_input("Insert habit name:")
    habit_repeat = st.checkbox(" repeating? (Y/N)")
    habit_notes = st.text_area("Enter any habit notes:")
    submitted = st.form_submit_button("Create")
    if submitted:
        st.write("**Habit created successfully!**")
        st.write("**Habit details:**")
        st.write("Habit Name -", habit_name)
        st.write("Repeat (Y/N) -", habit_repeat)
        st.write("Notes -", habit_notes)

