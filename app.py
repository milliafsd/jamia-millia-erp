import streamlit as st
import pandas as pd
import database as db
import datetime

# پیج کی سیٹنگ (Wide Layout تاکہ گراف اچھے لگیں)
st.set_page_config(page_title="جامعہ ای آر پی", page_icon="🕌", layout="wide")

# اردو کے لیے کسٹم ڈیزائن (RTL)
st.markdown("""
    <style>
    body, p, h1, h2, h3, h4, h5, h6, div, span, label {
        direction: rtl;
        text-align: right;
        font-family: 'Jameel Noori Nastaleeq', 'Urdu Typesetting', Arial, sans-serif;
    }
    /* سائیڈ بار کو بہتر بنانے کے لیے */
    [data-testid="stSidebar"] {
        direction: rtl;
    }
    /* میٹرک باکس کا ڈیزائن */
    [data-testid="stMetricValue"] {
        direction: ltr; /* نمبر سیدھے نظر آئیں */
    }
    </style>
""", unsafe_allow_html=True)

# ڈیٹا بیس کو شروع کرنا
db.init_db()

# مین ہیڈنگ
st.title("🕌 جامعہ ملیہ - ای آر پی سسٹم")
st.markdown("---")

# سائیڈ بار مینیو
st.sidebar.header("📌 مین مینیو")
menu = ["گھر (Home)", "نیا طالب علم", "اساتذہ کا اندراج", "طلباء کی لسٹ", "حفظ کی روزانہ ڈائری", "تعلیمی رپورٹ کارڈ"]
choice = st.sidebar.radio("یہاں سے انتخاب کریں:", menu)

# -------------------------------------------------------------------
# 1. ہوم پیج (ڈیش بورڈ)
# -------------------------------------------------------------------
if choice == "گھر (Home)":
    st.subheader("ڈیش بورڈ - جامعہ کا تعلیمی خاکہ")
    
    col1, col2, col3 = st.columns(3)
    
    students_data = db.view_students()
    teachers_data = db.view_teachers()
    
    with col1:
        st.metric("کل طلباء", len(students_data))
    with col2:
        st.metric("کل اساتذہ", len(teachers_data))
    with col3:
        # آج کی تاریخ
        st.metric("آج کی تاریخ", datetime.date.today().strftime("%d-%m-%Y"))
        
    st.info("👈 بائیں جانب موجود مینیو سے اپنی مطلوبہ کیٹیگری کا انتخاب کریں۔")

# -------------------------------------------------------------------
# 2. نیا طالب علم داخل کرنا
# -------------------------------------------------------------------
elif choice == "نیا طالب علم":
    st.subheader("📝 نیا داخلہ فارم")
    
    with st.form("student_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("طالب علم کا نام *")
            darja = st.selectbox("درجہ/کلاس *", ["حفظ", "نظارہ", "قاعدہ", "اولیٰ", "ثانیہ", "ثالثہ", "رابعہ", "خامسہ", "سادسہ", "موقوف علیہ", "دورہ حدیث"])
        with col2:
            father = st.text_input("ولدیت *")
            
            # اساتذہ کی لسٹ لانا
            teachers_list = db.view_teachers()
            if teachers_list:
                teacher_names = {t[1]: t[0] for t in teachers_list} # {Name: ID}
                selected_teacher = st.selectbox("نگراں استاد *", list(teacher_names.keys()))
            else:
                st.warning("پہلے اساتذہ کا اندراج کریں!")
                selected_teacher = None
                
        submit = st.form_submit_button("داخلہ مکمل کریں")
        
        if submit:
            if name and father and selected_teacher:
                teacher_id = teacher_names[selected_teacher]
                db.add_student(name, father, darja, teacher_id)
                st.success(f"ماشاءاللہ! {name} کا داخلہ ہو گیا ہے۔")
            else:
                st.error("براہ کرم تمام ضروری خانے (جن پر * ہے) پُر کریں۔")

# -------------------------------------------------------------------
# 3. اساتذہ کا اندراج
# -------------------------------------------------------------------
elif choice == "اساتذہ کا اندراج":
    st.subheader("👨‍🏫 نیا استاد شامل کریں")
    with st.form("teacher_form", clear_on_submit=True):
        full_name = st.text_input("مکمل نام *")
        u_name = st.text_input("صارف نام (Username) * - لاگ ان کے لیے")
        pwd = st.text_input("پاس ورڈ *", type="password")
        
        t_submit = st.form_submit_button("استاد شامل کریں")
        
        if t_submit:
            if full_name and u_name and pwd:
                res = db.add_teacher(u_name, full_name, pwd)
                if res:
                    st.success("استاد کا ریکارڈ کامیابی سے محفوظ کر لیا گیا ہے۔")
                else:
                    st.error("یہ صارف نام پہلے سے موجود ہے، کوئی اور نام چنیں۔")
            else:
                st.error("تمام معلومات درج کرنا لازمی ہے۔")

# -------------------------------------------------------------------
# 4. طلباء کی لسٹ
# -------------------------------------------------------------------
elif choice == "طلباء کی لسٹ":
    st.subheader("📋 موجودہ طلباء کا ریکارڈ")
    data = db.view_students()
    
    if data:
        # کالمز کے نام اردو میں
        df = pd.DataFrame(data, columns=["آئی ڈی", "نام", "ولدیت", "درجہ", "استاد کا نام"])
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("ابھی تک کوئی طالب علم داخل نہیں ہوا۔")

# -------------------------------------------------------------------
# 5. حفظ کی روزانہ ڈائری
# -------------------------------------------------------------------
elif choice == "حفظ کی روزانہ ڈائری":
    st.subheader("📖 روزانہ تعلیمی کارکردگی (حفظِ قرآن)")
    
    students_list = db.view_students()
    if not students_list:
        st.warning("پہلے طلباء کا داخلہ کریں۔")
    else:
        # طالب علم کا انتخاب
        student_dict = {f"{s[1]} (ولد {s[2]}) - {s[3]}": s[0] for s in students_list}
        selected_student_name = st.selectbox("طالب علم منتخب کریں", list(student_dict.keys()))
        student_id = student_dict[selected_student_name]
        
        with st.form("hifz_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                date = st.date_input("تاریخ")
                sabaq = st.text_input("نیا سبق (مثلاً: پارہ 1، رکوع 2)")
                sabqi = st.text_input("سبقی")
                
            with col2:
                status = st.radio("حاضری", ["حاضر", "ناغہ", "رخصت"], horizontal=True)
                manzil = st.text_input("منزل")
                
            col3, col4 = st.columns(2)
            with col3:
                mistakes = st.number_input("کل غلطیاں", min_value=0, step=1)
            with col4:
                hesitation = st.number_input("کل اٹکن", min_value=0, step=1)
                
            btn = st.form_submit_button("ریکارڈ محفوظ کریں")
            
            if btn:
                db.add_hifz_entry(student_id, str(date), sabaq, sabqi, manzil, mistakes, hesitation, status)
                st.success(f"الحمدللہ! {selected_student_name.split(' ')[0]} کا آج کا ریکارڈ محفوظ کر لیا گیا ہے۔")

# -------------------------------------------------------------------
# 6. تعلیمی رپورٹ کارڈ
# -------------------------------------------------------------------
elif choice == "تعلیمی رپورٹ کارڈ":
    st.subheader("📊 طالب علم کا ماہانہ / سالانہ تعلیمی خلاصہ")

    students_list = db.view_students()
    if not students_list:
        st.warning("ڈیٹا بیس میں طلباء موجود نہیں ہیں۔")
    else:
        student_dict = {f"{s[1]} (ولد {s[2]})": s[0] for s in students_list}
        selected_student = st.selectbox("رپورٹ دیکھنے کے لیے نام منتخب کریں", list(student_dict.keys()))
        student_id = student_dict[selected_student]

        if st.button("رپورٹ تیار کریں"):
            report = db.get_student_report(student_id)
            
            if report:
                df = pd.DataFrame(report, columns=["تاریخ", "سبق", "سبقی", "منزل", "غلطی", "اٹکن", "حاضری"])
                
                # میٹرکس دکھانا
                st.markdown("### 📌 کارکردگی کا خلاصہ")
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("کل ریکارڈ شدہ دن", len(df))
                c2.metric("اوسط غلطیاں (روزانہ)", round(df["غلطی"].mean(), 1))
                c3.metric("کل اٹکن", df["اٹکن"].sum())
                
                total_absents = len(df[df["حاضری"] == "ناغہ"])
                c4.metric("کل ناغے", total_absents)

                st.divider()
                
                # غلطیوں کا گراف
                st.markdown("### 📉 غلطیوں کا گراف (Progress)")
                # گراف کے لیے تاریخ کو انڈیکس بنانا ضروری ہے
                graph_data = df[['تاریخ', 'غلطی']].set_index('تاریخ')
                st.line_chart(graph_data)
                
                # مکمل ریکارڈ ٹیبل
                st.markdown("### 🗓️ تفصیلی ریکارڈ")
                st.dataframe(df, use_container_width=True, hide_index=True)
                
            else:
                st.warning("اس طالب علم کا ابھی کوئی تعلیمی ریکارڈ ڈائری میں موجود نہیں ہے۔")
