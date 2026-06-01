import streamlit as st
from supabase import create_client

# 1. Cấu hình giao diện (Tone màu xanh giáo dục chuyên nghiệp)
st.set_page_config(page_title="Điểm danh Education Town", page_icon="🎓")

st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; background-color: #1E88E5; color: white; border-radius: 10px; height: 3em; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #1E88E5;'>🎓 EDUCATION TOWN</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Hệ thống điểm danh giáo viên từ xa</p>", unsafe_allow_html=True)
st.write("---")

# 2. Thông tin kết nối (Đại vương dán thông tin từ Supabase vào đây)
URL = "https://tujqkhhbfdzleocflfbo.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InR1anFraGhiZmR6bGVvY2ZsZmJvIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3Nzc4OTAyNCwiZXhwIjoyMDkzMzY1MDI0fQ.eDHou_MwdllE-CnqShTUrQTeW6_xEGj7P-EIxk_uyno"
supabase = create_client(URL, KEY)

# 3. Form nhập liệu
with st.container():
    teacher = st.text_input("👤 Tên Giáo viên", placeholder="Nhập họ và tên giáo viên...")
    student = st.text_input("👶 Tên Học sinh", placeholder="Nhập tên học sinh buổi hôm nay...")
    subject = st.selectbox("📚 Môn học", ["Ngữ Văn", "Toán", "Tiếng Anh", "Kỹ năng sống", "Khác"])
    note = st.text_area("📝 Nhận xét buổi học", placeholder="Hôm nay con học thế nào? Có bài tập về nhà không?...")

    if st.button("XÁC NHẬN ĐIỂM DANH"):
        if teacher and student:
            data = {
                "teacher_name": teacher,
                "student_name": student,
                "subject": subject,
                "note": note
            }
            try:
                # Đẩy thẳng vào bảng remote_checkin trong Supabase
                supabase.table("remote_checkin").insert(data).execute()
                st.success(f"Tuyệt vời! Đã ghi nhận điểm danh cho bé {student}")
                st.balloons()
            except Exception as e:
                st.error(f"Đại vương ơi, có lỗi rồi: {e}")
        else:
            st.warning("Vui lòng nhập đầy đủ tên Giáo viên và Học sinh nhé!")