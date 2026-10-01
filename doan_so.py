import streamlit as st
import sqlite3

# ========== Lớp CSDL ==========
class QuanLySinhVienDB:
    def __init__(self, ten_file="sinhvien.db"):
        self.ten_file = ten_file
        self.ket_noi()

    def ket_noi(self):
        conn = sqlite3.connect(self.ten_file)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS sinh_vien (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ma TEXT UNIQUE NOT NULL,
                ten TEXT NOT NULL,
                tuoi INTEGER,
                lop TEXT,
                diem_tb REAL
            )
        """)
        conn.commit()
        conn.close()

    def them(self, ma, ten, tuoi, lop, diem_tb):
        conn = sqlite3.connect(self.ten_file)
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO sinh_vien VALUES (NULL, ?, ?, ?, ?, ?)
            """, (ma, ten, tuoi, lop, diem_tb))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    def lay_tat_ca(self):
        conn = sqlite3.connect(self.ten_file)
        ds = conn.execute("SELECT * FROM sinh_vien").fetchall()
        conn.close()
        return ds

    def xoa(self, ma):
        conn = sqlite3.connect(self.ten_file)
        cur = conn.cursor()
        cur.execute("DELETE FROM sinh_vien WHERE ma=?", (ma,))
        conn.commit()
        conn.close()

# ========== Giao diện Web ==========
st.set_page_config(page_title="Quản Lý Sinh Viên", page_icon="📚", layout="wide")
db = QuanLySinhVienDB()

st.title("📚 HỆ THỐNG QUẢN LÝ SINH VIÊN")
st.markdown("---")  # Đường kẻ ngang

tab1, tab2, tab3 = st.tabs(["➕ Thêm Sinh Viên", "📋 Danh Sách", "🗑️ Xóa"])

# ========== Tab 1: Thêm ==========
with tab1:
    st.subheader("Thêm thông tin sinh viên mới")
    st.info("Điền đầy đủ thông tin bên dưới và nhấn nút Lưu")
    
    col1, col2 = st.columns(2)
    with col1:
        ma = st.text_input("🔢 Mã sinh viên")
        ten = st.text_input("📝 Họ và tên")
        tuoi = st.number_input("🎂 Tuổi", min_value=15, max_value=60, value=18)
    with col2:
        lop = st.text_input("🏫 Lớp")
        diem_tb = st.number_input("📊 Điểm trung bình", min_value=0.0, max_value=10.0, step=0.1, value=7.0)
    
    if st.button("✅ Lưu vào CSDL", type="primary", use_container_width=True):
        if not ma or not ten:
            st.warning("⚠️ Mã SV và Họ tên không được để trống!")
        elif db.them(ma, ten, tuoi, lop, diem_tb):
            st.success(f"✅ Thêm thành công: **{ten}** — Mã: `{ma}`")
        else:
            st.error(f"❌ Mã `{ma}` đã tồn tại! Vui lòng dùng mã khác.")

# ========== Tab 2: Danh sách ==========
with tab2:
    st.subheader("Danh sách toàn bộ sinh viên")
    ds = db.lay_tat_ca()
    
    if ds:
        st.write(f"📌 Tổng số: **{len(ds)}** sinh viên")
        st.table({
            "Mã SV": [row[1] for row in ds],
            "Họ và Tên": [row[2] for row in ds],
            "Tuổi": [row[3] for row in ds],
            "Lớp": [row[4] for row in ds],
            "Điểm TB": [row[5] for row in ds]
        })
    else:
        st.info("📭 Chưa có sinh viên nào trong cơ sở dữ liệu")

# ========== Tab 3: Xóa ==========
with tab3:
    st.subheader("Xóa thông tin sinh viên")
    st.warning("⚠️ Hành động này không thể hoàn tác!")
    
    ma_xoa = st.text_input("Nhập mã sinh viên cần xóa:")
    if st.button("🗑️ Xóa vĩnh viễn", type="secondary", use_container_width=True):
        if ma_xoa:
            db.xoa(ma_xoa)
            st.success(f"✅ Đã xóa sinh viên có mã: `{ma_xoa}` (nếu có)")
            st.rerun()
        else:
            st.warning("⚠️ Vui lòng nhập mã sinh viên!")