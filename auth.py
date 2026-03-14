import streamlit as st
from database import connect

def login():

    conn=connect()

    c=conn.cursor()

    st.subheader("لاگ ان")

    user=st.text_input("Username")

    pwd=st.text_input("Password",type="password")

    if st.button("لاگ ان"):

        r=c.execute(
        "SELECT * FROM teachers WHERE name=? AND password=?",
        (user,pwd)
        ).fetchone()

        if r:

            st.session_state["login"]=True
            st.session_state["user"]=user

            st.rerun()

        else:

            st.error("غلط معلومات")
