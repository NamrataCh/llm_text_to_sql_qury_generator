import streamlit as st 
from dotenv import load_dotenv
import os
import sqlite3
import google.generativeai as genai



load_dotenv()


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# function to load google gemini model 

def get_gemini_response(question, prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([prompt, question])
    return response.text 

# function to retrieve query from sql database
def read_sql_query(sql, db):
    conn=sqlite3.connect(db)
    cursor=conn.cursor()
    cursor.execute(sql)
    rows=cursor.fetchall()
    conn.commit()
    conn.close()
    for row in rows:
        print(row)

    return rows

prompt="""
    You are an expert in converting English questions to SQL query!
    The SQL database has the table Student and has following columns - name, class, section and marks. 
    
    For Example: 

    Example 1: How many entries of records are present ? ,
    the SQL command will be something like this:
    Select count(*) from student;

    Example 2: Tell me all the students studying in Data Science class ?,
    the SQL command will be something like this:
    select * from student where class="Data Science" ;

    also the sql code should not have ``` in the beginning or end and sql word in the output.

"""


## streamlit app
st.set_page_config(page_title="retrieve SQL Query")
st.header("Gemini App to retrieve SQL data")

query_text=st.text_input("Enter query here", key="input")
submit=st.button("Ask the Question")

if submit: 
    print(query_text)
    print("************************")
    response=get_gemini_response(query_text, prompt)
    print(response)
    print("************************")
    data=read_sql_query(response, "student.db")
    st.subheader("The Response is:")
    for row in data:
        print(row)
        st.header(row)
