import streamlit as st
from supabase import create_client

# 1. Cấu hình kết nối Supabase (Giữ nguyên thông tin chuẩn của Đại vương)
URL = "https://tujqkhhbfdzleocflfbo.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InR1anFraGhiZmR6bGVvY2ZsZmJvIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3Nzc4OTAyNCwiZXhwIjoyMDkzMzY1MDI0fQ.eDHou_MwdllE-CnqShTUrQTeW6_xEGj7P-EIxk_uyno"

supabase = create_client(URL, KEY)

# 2. Hàm tự động load danh sách từ Database
@st.cache_data(ttl=300) # Lưu tạm dữ liệu 5 phút để load cho nhanh, tránh quá tải
def load_data_lists():
    try:
        # Lấy danh sách giáo viên (Giả định cột lưu tên là name hoặc teacher_name)
        res_teachers = supabase.table("teachers").select("*").execute()
        # Tìm xem bảng dùng cột 'name' hay cột nào khác, mặc định thử lấy 'name'
        teachers = [t.get("name") or t.get("teacher_name") or str(t) for t in res_teachers.data] if res_teachers.data else []
        
        # Lấy danh sách học sinh
        res_students = supabase.table("students").select("*").execute()
        students = [s.get("name") or s.get("student_name") or str(s) for s in res_students.data] if res_students.data else []
        
        # Sắp xếp theo thứ tự chữ cái cho dễ tìm
        teachers.sort()
        students.sort()
        
        return teachers, students
    except Exception as e:
        return [], []

# Gọi hàm lấy danh sách dữ liệu
list_teachers, list_students = load_data_lists()

# Nếu db trống hoặc lỗi, cho sẵn vài tên dự phòng để web không bị lỗi đứng im
if not list_teachers: list_teachers = ["Chọn giáo viên...", "Cô Vương Thảo", "Giáo viên khác"]
if not list_students: list_students = ["Chọn học sinh...", "Tuyết Vy", "Học sinh khác"]

# 3. Giao diện trang Web
st.markdown("<h1 style='text-align: center; color: #1E88E5;'>🎓 EDUCATION TOWN</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; gray;'>Hệ thống điểm danh giáo viên từ xa</p>", unsafe_allow_html=True)
st.write("---")

# Tạo form nhập liệu bằng Dropdown/Selectbox (Bấm là chọn)
teacher_name = st.selectbox("👤 Tên Giáo viên", options=list_teachers)
student_name = st.selectbox("👶 Tên Học sinh", options=list_students)
subject = st.selectbox("📚 Môn học", options=["Ngữ Văn", "Toán", "Tiếng Anh", "Kỹ năng sống"])
note = st.text_area("📝 Nhận xét buổi học", placeholder="Hôm nay con học thế nào? Có bài tập về nhà không?...")

# Nút xác nhận điểm danh
if st.button("XÁC NHẬN ĐIỂM DANH", use_container_width=True):
    if teacher_name and student_name:
        # Chuẩn bị dữ liệu gửi lên bảng remote_checkin
        data = {
            "teacher_name": teacher_name,
            "student_name": student_name,
            "subject": subject,
            "note": note,
            "processed": False
        }
        
        try:
            # Lệnh đẩy dữ liệu lên Supabase
            response = supabase.table("remote_checkin").insert(data).execute()
            st.success(f"🎉 Đã điểm danh thành công học sinh {student_name}!")
        except Exception as e:
            st.error(f"❌ Lỗi kết nối database: {e}")
    else:
        st.warning("⚠️ Vui lòng chọn đầy đủ Giáo viên và Học sinh!")
