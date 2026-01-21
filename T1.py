import streamlit as st



st.set_page_config(page_title="เครื่องคำนวณค่าแรง", layout="centered")
st.image("B3.jpg",use_container_width=True)


st.title("เครื่องคำนวณค่าแรงและ OT TC.Sec")

st.subheader("By JOB")



# 1. เลือกประเภทพนักงาน

emp_type = st.radio("ประเภทพนักงาน", ["รายวัน", "รายเดือน"], horizontal=True)



# 2. ข้อมูลรายได้พื้นฐานและการเข้ากะ

if emp_type == "รายเดือน":

    salary_full = st.number_input("เงินเดือนเต็ม (ตามสัญญาจ้าง)", min_value=0.0, step=100.0)

    pay_period = st.selectbox("งวดการจ่ายเงิน", ["1 เดือน (เต็ม)", "ครึ่งเดือน (15 วัน)"])

    base_pay = salary_full / 2 if pay_period == "ครึ่งเดือน (15 วัน)" else salary_full

    # ฐานการคำนวณต่อชั่วโมงรายเดือน

    hourly_rate_base = ((salary_full+800)/30)/8

else:

    daily_wage = st.number_input("ค่าจ้างรายวัน (บาท)", min_value=0.0, step=10.0)

    hourly_rate_base = (daily_wage+26.67) / 8


st.divider()



# 3. เลือกประเภทกะ (Day หรือ Day-Night Shift)

shift_type = st.radio("ประเภทการเข้ากะ", ["Day", "Day_night Shift"], horizontal=True)



# ตั้งค่าเริ่มต้นสำหรับชั่วโมงทำงาน

days_day = 0

days_night = 0



if shift_type == "Day":

    # ถ้าเป็นกะ Day อย่างเดียว

    if emp_type == "รายวัน":

        # เฉพาะรายวันให้ระบุจำนวนวันทำงาน

        days_day = st.number_input("จำนวนวันที่ทำงาน (วัน)", min_value=0, step=1, value=30)

    else:

        # รายเดือน กะ Day ปกติ ไม่ต้องกรอกจำนวนวัน (ใช้ฐานเงินเดือน)

        days_day = 30 

    hr_per_day = 8.0

else:

    # ถ้าเป็นกะ Day_night Shift ให้แสดงช่องกรอกทั้งสองกะ

    st.subheader("ระบุจำนวนวันทำงานแต่ละกะ")

    col_s1, col_s2 = st.columns(2)

    with col_s1:

        days_day = st.number_input("จำนวนวัน กะกลางวัน (Day)", min_value=0, step=1)

    with col_s2:

        days_night = st.number_input("จำนวนวัน กะกลางคืน (Night)", min_value=0, step=1)

    

# คำนวณค่าจ้างพื้นฐานใหม่สำหรับพนักงานรายวันตามจำนวนวันที่กรอกจริง

if emp_type == "รายวัน":

    base_pay = daily_wage * (days_day + days_night)



st.divider()



# 4. ส่วนกรอกชั่วโมง OT

st.subheader("จำนวนชั่วโมง OT ในงวดนี้")

c_ot1, c_ot2 = st.columns(2)



with c_ot1:

    ot1_0 = st.number_input("OT 1.0 เท่า (ชม.)", min_value=0.0, step=0.5, key="ot1")

    ot1_5 = st.number_input("OT 1.5 เท่า (ชม.)", min_value=0.0, step=0.5, key="ot15")



with c_ot2:

    ot2_0 = st.number_input("OT 2.0 เท่า (ชม.)", min_value=0.0, step=0.5, key="ot2")

    ot3_0 = st.number_input("OT 3.0 เท่า (ชม.)", min_value=0.0, step=0.5, key="ot3")



# คำนวณเงิน OT (ยึดตามฐานค่าแรงต่อชั่วโมง 8 ชม. ตามกฎหมาย)

pay_ot = (ot1_0 * hourly_rate_base * 1.0) + \
(ot1_5 * hourly_rate_base * 1.5) + \
(ot2_0 * hourly_rate_base * 2.0) + \
(ot3_0 * hourly_rate_base * 3.0)



# 5. สรุปผล

st.divider()

total_income = base_pay + pay_ot



st.success(f"### รายได้รวมงวดนี้: {total_income:,.2f} บาท")

st.write(f"**สรุปรายละเอียด:**")

st.write(f"- ค่าจ้างพื้นฐาน: {base_pay:,.2f} บาท")

st.write(f"- ค่า OT รวม: {pay_ot:,.2f} บาท")

st.write(f"- ค่าแรงต่อชม: {hourly_rate_base:,.2f} บาท")
