
import streamlit as st
import pandas as pd

from database import init_db
from auth import login
from design import load_css

conn=init_db()

load_css()

st.markdown("""
<div class='main-header'>
<h1>جامعہ ملیہ اسلامیہ</h1>
<p>مدرسہ مینجمنٹ سسٹم</p>
</div>
""",unsafe_allow_html=True)


if "login" not in st.session_state:

    st.session_state["login"]=False


if not st.session_state["login"]:

    login()
    st.stop()


menu=st.sidebar.selectbox("مینو",[
"ڈیش بورڈ",
"طلباء",
"اساتذہ",
"رپورٹس"
])


c=conn.cursor()

if menu=="ڈیش بورڈ":

    s=c.execute("SELECT COUNT(*) FROM students").fetchone()[0]

    t=c.execute("SELECT COUNT(*) FROM teachers").fetchone()[0]

    col1,col2=st.columns(2)

    col1.metric("کل طلباء",s)

    col2.metric("کل اساتذہ",t)


elif menu=="طلباء":

    st.subheader("نیا طالب علم")

    name=st.text_input("نام")

    father=st.text_input("ولدیت")

    teacher=st.text_input("استاد")

    if st.button("محفوظ کریں"):

        c.execute(
        "INSERT INTO students(name,father,teacher) VALUES(?,?,?)",
        (name,father,teacher)
        )

        conn.commit()

        st.success("محفوظ ہوگیا")


    df=pd.read_sql("SELECT * FROM students",conn)

    st.dataframe(df)
