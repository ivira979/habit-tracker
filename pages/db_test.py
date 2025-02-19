import sqlite3
import streamlit as st
import pandas as pd

def run_query(c, q):
    try:
        c.execute(q)
        st.write("Success!")
    except sqlite3.Error as error:
        match error.sqlite_errorname:
            case "SQLITE_CONSTRAINT_NOTNULL":
                st.write("Error: Please enter a valid habit name.")
            case "SQLITE_CONSTRAINT_UNIQUE":
                st.write("Error: This habit already exists - please try a different name.")
            case _:
                st.write("Something went wrong! Please try again.")
        


try:
    conn = sqlite3.connect('habits.db')
    cursor = conn.cursor()
    print("Database created and Successfully Connected to SQLite")

    query = "select * from habits;"
    #run_query(cursor, "DELETE FROM HABITS WHERE habit_name LIKE LOWER('test_cursor%')")
    record = cursor.fetchall()
    df = pd.read_sql(query, conn)
    st.write(df)
    cursor.close()
    conn.commit()

except sqlite3.Error as error:
    print("Error while connecting to sqlite", error)
finally:
    if conn:
        conn.close()
        print("The SQLite connection is closed")