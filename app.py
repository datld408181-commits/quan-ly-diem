import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Cấu hình giao diện trang web
st.set_page_config(page_title="Quản Lý Điểm Sinh Viên", layout="wide")

# 1. Chuẩn bị dữ liệu 10 sinh viên
data = {
    'Ho_va_ten': ['An', 'Binh', 'Chi', 'Dung', 'Ha', 'Lan', 'Minh', 'Nam', 'Phuc', 'Trang'],
    'Chuyen_can': [8.0, 9.0, 7.0, 9.5, 7.5, 6.0, 9.0, 7.0, 7.5, 9.5],
    'Giua_ky': [7.5, 8.0, 6.5, 9.0, 7.0, 6.0, 8.5, 7.0, 7.5, 9.0],
    'Cuoi_ky': [8.0, 8.5, 6.5, 9.0, 7.5, 6.0, 8.5, 7.0, 7.5, 9.0]
}

df = pd.DataFrame(data)

# 2. Tính điểm tổng kết theo công thức (20% CC + 30% GK + 50% CK)
df['Tong_ket'] = 0.2 * df['Chuyen_can'] + 0.3 * df['Giua_ky'] + 0.5 * df['Cuoi_ky']

# 3. Hàm xếp loại sinh viên
def xep_loai(dtk):
    if dtk >= 8.5:
        return 'Giỏi'
    elif dtk >= 7.0:
        return 'Khá'
    elif dtk >= 5.0:
        return 'Trung bình'
    else:
        return 'Yếu'

df['Xep_loai'] = df['Tong_ket'].apply(xep_loai)

# ==================== GIAO DIỆN STREAMLIT ====================
st.title("QUẢN LÝ ĐIỂM SINH VIÊN")
st.markdown("---")

# Hiển thị bảng điểm
st.subheader("📋 Bảng điểm chi tiết của 10 sinh viên")
st.dataframe(df.style.format({
    'Chuyen_can': '{:.1f}',
    'Giua_ky': '{:.1f}',
    'Cuoi_ky': '{:.1f}',
    'Tong_ket': '{:.2f}'
}), use_container_width=True)

# Thống kê chung
st.subheader("📊 Thống kê chung của lớp")
dtk_tb = df['Tong_ket'].mean()
max_sv = df.loc[df['Tong_ket'].idxmax()]
min_sv = df.loc[df['Tong_ket'].idxmin()]
so_sv_dat = (df['Tong_ket'] >= 5.0).sum()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Điểm TB lớp", f"{dtk_tb:.2f}")
col2.metric("Số sinh viên đạt", f"{so_sv_dat}/10")
col3.metric("SV cao điểm nhất", f"{max_sv['Ho_va_ten']} ({max_sv['Tong_ket']:.2f})")
col4.metric("SV thấp điểm nhất", f"{min_sv['Ho_va_ten']} ({min_sv['Tong_ket']:.2f})")

st.markdown("---")

# Tra cứu sinh viên theo Selectbox
st.subheader("🔍 Tra cứu thông tin sinh viên")
selected_student = st.selectbox("Chọn tên sinh viên cần xem:", df['Ho_va_ten'])
student_info = df[df['Ho_va_ten'] == selected_student].iloc[0]

st.info(f"""
- **Họ và tên:** {student_info['Ho_va_ten']}
- **Điểm chuyên cần:** {student_info['Chuyen_can']}
- **Điểm giữa kỳ:** {student_info['Giua_ky']}
- **Điểm cuối kỳ:** {student_info['Cuoi_ky']}
- **Điểm tổng kết:** **{student_info['Tong_ket']:.2f}**
- **Xếp loại học lực:** **{student_info['Xep_loai']}**
""")

st.markdown("---")

# Trực quan hóa biểu đồ
st.subheader("📈 Biểu đồ cột thể hiện điểm tổng kết của 10 sinh viên")
fig, ax = plt.subplots(figsize=(10, 4))
bars = ax.bar(df['Ho_va_ten'], df['Tong_ket'], color='skyblue', edgecolor='black')
ax.set_xlabel("Họ và tên sinh viên", fontsize=11, fontweight='bold')
ax.set_ylabel("Điểm tổng kết", fontsize=11, fontweight='bold')
ax.set_ylim(0, 10)

# Hiển thị số điểm trực tiếp trên đầu mỗi cột
for bar in bars:
    height = bar.get_height()
    ax.annotate(f'{height:.2f}',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3),  # 3 points vertical offset
                textcoords="offset points",
                ha='center', va='bottom', fontsize=9)

ax.grid(axis='y', linestyle='--', alpha=0.7)
st.pyplot(fig)

# Chân trang (Footer)
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray; font-size: small;'>Người tạo: Nguyễn Văn A - MSSV: 12345678</p>", unsafe_allow_html=True)
