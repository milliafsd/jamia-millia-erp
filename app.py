import streamlit as st
import pandas as pd
from datetime import datetime

# پیج کی سیٹنگز
st.set_page_config(page_title="Online Madrasa", page_icon="🕌", layout="wide")

st.title("🕌 آن لائن مدرسہ سسٹم (پروٹوٹائپ)")
st.write("یہ سٹریم لٹ پر مبنی ایک ابتدائی خاکہ ہے جہاں ہم مختلف یوزرز کے انٹرفیس دیکھ سکتے ہیں۔")

st.markdown("---")

# سائیڈ بار میں صارف کا کردار منتخب کرنے کا آپشن
st.sidebar.title("صارف (User Role)")
role = st.sidebar.radio("اپنا اکاؤنٹ منتخب کریں:", ["طالب علم / والدین (Student)", "استاد (Teacher)", "ایڈمن (Admin)"])

# ---------------- طالب علم کا انٹرفیس ----------------
if role == "طالب علم / والدین (Student)":
    st.header("👨‍🎓 ڈیش بورڈ: طالب علم / والدین")
    
    # کلاس کا الرٹ
    st.info("🕒 اگلی کلاس شروع ہونے میں 15 منٹ باقی ہیں!")
    
    # کلاس جوائن کرنے کا بٹن
    if st.button("🔴 لائیو کلاس جوائن کریں (Join Live Class)", use_container_width=True):
        st.success("آپ کلاس میں شامل ہو گئے ہیں! (یہاں زوم یا ویڈیو کال کی اسکرین نظر آئے گی)")
    
    st.markdown("### 📊 حالیہ کارکردگی (Progress Report)")
    
    # فرضی ڈیٹا بیس (طالب علم کے اسباق کا ریکارڈ)
    student_data = {
        'تاریخ': ['10-May', '11-May', '12-May'], 
        'سبق': ['سورۃ البقرہ آیت 1-5', 'سورۃ البقرہ آیت 6-10', 'سورۃ البقرہ آیت 11-15'], 
        'تجوید سٹارز': ['⭐⭐⭐⭐', '⭐⭐⭐', '⭐⭐⭐⭐⭐'],
        'استاد کا نوٹ': ['بہتر ہے', 'غنہ پر توجہ دیں', 'ماشاءاللہ بہت عمدہ']
    }
    df = pd.DataFrame(student_data)
    st.table(df)

# ---------------- استاد کا انٹرفیس ----------------
elif role == "استاد (Teacher)":
    st.header("👨‍🏫 ڈیش بورڈ: استاد (Teacher)")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 📅 آج کی کلاسز")
        st.write("- 11:00 AM - احمد (حفظ)")
        st.write("- 11:30 AM - فاطمہ (ناظرہ)")
        st.write("- 12:00 PM - عبداللہ (قاعدہ)")
    
    with col2:
        st.markdown("### 📝 اسمارٹ روزنامچہ (Logbook)")
        # ریکارڈ درج کرنے کا فارم
        with st.form("teacher_log_form"):
            student_name = st.selectbox("طالب علم کا نام", ["احمد", "فاطمہ", "عبداللہ"])
            sabaq = st.text_input("آج کا سبق (پارہ / سورۃ / آیت)")
            mistakes = st.text_area("تجوید کی غلطیاں یا نوٹ")
            rating = st.slider("کارکردگی (Stars)", 1, 5, 5)
            
            submitted = st.form_submit_button("ریکارڈ محفوظ کریں")
            if submitted:
                st.success(f"{student_name} کا ریکارڈ کامیابی سے محفوظ ہو گیا!")

# ---------------- ایڈمن کا انٹرفیس ----------------
else:
    st.header("⚙️ ڈیش بورڈ: منتظم (Admin Panel)")
    
    st.write("ایڈمن یہاں سے مدرسہ کے مکمل نظام کا جائزہ لے سکتا ہے۔")
    
    # مدرسہ کے اعداد و شمار
    col1, col2, col3 = st.columns(3)
    col1.metric(label="کل طلباء", value="150", delta="12 نئے")
    col2.metric(label="کل اساتذہ", value="12", delta="0")
    col3.metric(label="رواں ماہ کی فیس وصولی", value="85%", delta="5% اضافہ")
    
    st.markdown("---")
    st.markdown("### 🛠️ کوئیک ایکشنز")
    st.button("نیا طالب علم رجسٹر کریں")
    st.button("فیس کے ریمائنڈر بھیجیں")
