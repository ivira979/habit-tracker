import streamlit as st
import sqlalchemy as db
import pandas as pd

st.title("Habits Dashboard")
st.write(
    "Here are all the habits I have made so far!"
)

engine = db.create_engine("sqlite:///habits.db")
query = 'select * from habits'

conn = engine.connect()

df = pd.read_sql(
    sql=query,
    con=conn.connection
)

st.write(df)