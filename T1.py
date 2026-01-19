import streamlit as st

st.set_page_config(page_title="เครื่องคำนวณค่าแรง", layout="centered")

st.title("เครื่องคำนวณค่าแรงและ OT")
st.subheader("By JOB TC ")
st.write("รองรับการจ่ายแบบรายวัน รายเดือน ครึ่งเดือน และเต็มเดือน")

# 1. เลือกประเภทพนักงาน
emp_type = st.radio("ประเภทพนักงาน", ["รายวัน", "รายเดือน"], horizontal=True)

# 2. ส่วนรับข้อมูลรายได้และงวดการจ่าย
if emp_type == "รายเดือน":
 salary_full = st.number_input("เงินเดือนเต็ม (ตามสัญญาจ้าง)", min_value=0.0, step=100.0)
 
 pay_period = st.selectbox("งวดการจ่ายเงิน", ["1 เดือน (เต็ม)", "ครึ่งเดือน (15 วัน)"])
 Adj_1 = 800
 if pay_period == "ครึ่งเดือน (15 วัน)":
  base_pay = salary_full / 2
 else:
  base_pay = salary_full

# ดึงค่าแรงต่อชั่วโมงออกมาอยู่นอกเงื่อนไขย่อย เพื่อให้โปรแกรมเห็นตลอด
 hourly_rate = (salary_full / 30) / 8

else: # กรณีพนักงานรายวัน
 daily_wage = st.number_input("ค่าจ้างรายวัน (บาท)", min_value=0.0, step=10.0)
 days = st.number_input("จำนวนวันที่ทำงานในงวดนี้ (วัน)", min_value=0, step=1)
 base_pay = daily_wage * days
 hourly_rate = daily_wage / 8

st.divider()

# 3. ส่วนกรอกชั่วโมง OT
st.subheader("จำนวนชั่วโมง OT ในงวดนี้")
col1, col2 = st.columns(2)

with col1:
 ot1_0 = st.number_input("OT 1.0 เท่า (ชม.)", min_value=0.0, step=0.5, key="ot1")
 ot1_5 = st.number_input("OT 1.5 เท่า (ชม.)", min_value=0.0, step=0.5, key="ot15")

with col2:
 ot2_0 = st.number_input("OT 2.0 เท่า (ชม.)", min_value=0.0, step=0.5, key="ot2")
 ot3_0 = st.number_input("OT 3.0 เท่า (ชม.)", min_value=0.0, step=0.5, key="ot3")

# คำนวณเงิน OT (ตอนนี้โปรแกรมจะรู้จัก hourly_rate แล้ว)
pay_ot1_0 = ot1_0 * hourly_rate * 1.0
pay_ot1_5 = ot1_5 * hourly_rate * 1.5
pay_ot2_0 = ot2_0 * hourly_rate * 2.0
pay_ot3_0 = ot3_0 * hourly_rate * 3.0
total_ot_pay = pay_ot1_0 + pay_ot1_5 + pay_ot2_0 + pay_ot3_0

# 4. สรุปผล
st.divider()
total_income = base_pay + total_ot_pay

st.success(f"### รายได้รวมงวดนี้: {total_income:,.2f} บาท")
st.write(f"- ค่าจ้างพื้นฐาน: {base_pay:,.2f} บาท")
st.write(f"- ค่า OT รวม: {total_ot_pay:,.2f} บาท")
