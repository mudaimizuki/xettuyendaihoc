import streamlit as st
import pandas as pd
import numpy as np

# 1. CẤU HÌNH TRANG & GIAO DIỆN LUXURY
st.set_page_config(page_title="EduVision Premium", page_icon="🎓", layout="wide")

# Inject CSS để tạo phong cách sang trọng
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Roboto:wght@300;400;500&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Roboto', sans-serif;
    }
    h1, h2, h3 {
        font-family: 'Playfair Display', serif !important;
        color: #D4AF37 !important; /* Premium Gold */
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
    }
    .stTabs [data-baseweb="tab"] {
        font-family: 'Playfair Display', serif;
        font-size: 1.1rem;
        font-weight: bold;
    }
    .stTabs [aria-selected="true"] {
        border-bottom: 3px solid #D4AF37 !important;
        color: #D4AF37 !important;
    }
    .premium-card {
        padding: 25px;
        border-radius: 12px;
        border: 1px solid rgba(212, 175, 55, 0.3);
        background: linear-gradient(145deg, rgba(212,175,55,0.05) 0%, rgba(0,0,0,0) 100%);
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }
    .highlight-gold {
        color: #D4AF37;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# 2. DỮ LIỆU DEMO (NGÔN NGỮ - SƯ PHẠM)
@st.cache_data
def load_data():
    majors_data = [
        {
            "Tên ngành": "Sư phạm Tiếng Anh",
            "Trường": "ĐH Sư phạm TP.HCM (HCMUE)",
            "Khối thi": ["D01", "A01"],
            "MBTI phù hợp": ["ENFJ", "ESFJ", "INFJ", "ENFP"],
            "Enneagram phù hợp": ["Type 2", "Type 1", "Type 9"],
            "Điểm 2023": 27.5, "Điểm 2024": 27.8, "Điểm 2025": 28.1,
            "Học phí (Tr/năm)": "Miễn phí (Cam kết phục vụ) / 30tr",
            "Ưu điểm": "Cơ hội việc làm cao, thu nhập ổn định từ dạy thêm, không đóng học phí nếu theo ngạch Sư phạm.",
            "Nhược điểm": "Áp lực ngành giáo dục, cạnh tranh đầu vào cực kỳ gắt gao.",
            "Cơ hội việc làm": "Giáo viên trường công/quốc tế, Giảng viên, Trung tâm ngoại ngữ, Khởi nghiệp giáo dục."
        },
        {
            "Tên ngành": "Ngôn ngữ Anh",
            "Trường": "ĐH Khoa học Xã hội & Nhân văn (USSH)",
            "Khối thi": ["D01", "D14"],
            "MBTI phù hợp": ["INFP", "INTJ", "ENTP", "ENFP"],
            "Enneagram phù hợp": ["Type 4", "Type 5", "Type 3"],
            "Điểm 2023": 26.8, "Điểm 2024": 27.0, "Điểm 2025": 27.2,
            "Học phí (Tr/năm)": "25 - 30",
            "Ưu điểm": "Môi trường học thuật sâu sắc, linh hoạt chuyển hướng (Biên phiên dịch, Marketing, Đối ngoại).",
            "Nhược điểm": "Phải tự định hướng chuyên sâu rõ ràng, Tiếng Anh hiện nay là kỹ năng cơ bản nên cạnh tranh lao động cao.",
            "Cơ hội việc làm": "Biên/Phiên dịch viên, Ngoại giao, Chuyên viên truyền thông, Hướng dẫn viên quốc tế."
        },
        {
            "Tên ngành": "Ngôn ngữ Trung Quốc",
            "Trường": "ĐH Ngoại thương (FTU) - Cơ sở II",
            "Khối thi": ["D01", "D04"],
            "MBTI phù hợp": ["ESTJ", "ENTJ", "ISTJ", "ESFP"],
            "Enneagram phù hợp": ["Type 3", "Type 8", "Type 6"],
            "Điểm 2023": 28.0, "Điểm 2024": 28.2, "Điểm 2025": 28.5,
            "Học phí (Tr/năm)": "35 - 45",
            "Ưu điểm": "Cơ hội làm việc tại các tập đoàn đa quốc gia, mức lương khởi điểm cực kỳ hấp dẫn.",
            "Nhược điểm": "Yêu cầu cao về áp lực và cường độ học tập, điểm chuẩn luôn ở mức 'chạm trần'.",
            "Cơ hội việc làm": "Chuyên viên xuất nhập khẩu, Quản lý chuỗi cung ứng, Phiên dịch viên thương mại cao cấp."
        }
    ]
    
    admission_methods = {
        "Học bạ THPT": {"Chỉ tiêu": "20%", "Độ khó": "Trung bình", "Khả năng đậu": "Cao nếu học bạ >9.0, nhưng rủi ro lạm phát điểm."},
        "Đánh giá năng lực (ĐHQG)": {"Chỉ tiêu": "35%", "Độ khó": "Cao", "Khả năng đậu": "Rất ổn định, ít bị ảo điểm. Cần >850 điểm cho top đầu."},
        "Xét điểm THPT Quốc gia": {"Chỉ tiêu": "35%", "Độ khó": "Cao", "Khả năng đậu": "Cạnh tranh nhất, điểm chuẩn tăng nhẹ mỗi năm do phổ điểm."},
        "Xét tuyển thẳng / IELTS": {"Chỉ tiêu": "10%", "Độ khó": "Rất cao", "Khả năng đậu": "Chắc chắn nếu có giải Quốc gia hoặc IELTS > 7.5 + Học bạ đẹp."}
    }
    return pd.DataFrame(majors_data), admission_methods

df_majors, admission_dict = load_data()

# 3. HEADER & THANH TÌM KIẾM
col1, col2 = st.columns([2, 1])
with col1:
    st.title("🏛️ EduVision Premium")
    st.markdown("*Nền tảng phân tích học thuật & Định hướng tinh hoa*")
with col2:
    st.write("")
    st.write("")
    search_query = st.text_input("🔍 Tìm kiếm nhanh trường/ngành...", placeholder="Vd: Sư phạm, FTU...")

# 4. SIDEBAR - NHẬP HỒ SƠ CÁ NHÂN
with st.sidebar:
    st.header("Hồ Sơ Năng Lực")
    
    mbti = st.selectbox("Tính cách MBTI", ["Chưa rõ", "INTJ", "INTP", "ENTJ", "ENTP", "INFJ", "INFP", "ENFJ", "ENFP", "ISTJ", "ISFJ", "ESTJ", "ESFJ", "ISTP", "ISFP", "ESTP", "ESFP"])
    enneagram = st.selectbox("Kiểu Enneagram", ["Chưa rõ", "Type 1", "Type 2", "Type 3", "Type 4", "Type 5", "Type 6", "Type 7", "Type 8", "Type 9"])
    
    exam_block = st.selectbox("Khối thi dự kiến", ["Tất cả", "A01", "D01", "D04", "D14", "D15"])
    est_score = st.slider("Điểm xét tuyển dự kiến (THPT)", 20.0, 30.0, 25.0, 0.1)
    
    st.markdown("---")
    st.markdown("💡 **Tip:** Hệ thống sẽ tự động đối chiếu hồ sơ của bạn với ma trận dữ liệu tuyển sinh 3 năm gần nhất.")

# 5. LOGIC LỌC DỮ LIỆU
filtered_df = df_majors.copy()
if search_query:
    filtered_df = filtered_df[filtered_df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]
if exam_block != "Tất cả":
    filtered_df = filtered_df[filtered_df['Khối thi'].apply(lambda x: exam_block in x)]

# 6. HIỂN THỊ CHÍNH - TABS
tab1, tab2, tab3 = st.tabs(["📊 Đề Xuất & Phân Tích", "💼 Cơ Hội & Đánh Giá", "📈 Phương Thức Xét Tuyển"])

with tab1:
    st.header("Ngành & Trường Phù Hợp Với Bạn")
    if filtered_df.empty:
        st.warning("Chưa tìm thấy ngành/trường phù hợp với tiêu chí hiện tại.")
    else:
        for index, row in filtered_df.iterrows():
            # Tính toán độ phù hợp
            mbti_match = mbti in row["MBTI phù hợp"] if mbti != "Chưa rõ" else True
            ennea_match = enneagram in row["Enneagram phù hợp"] if enneagram != "Chưa rõ" else True
            score_diff = est_score - row["Điểm 2025"]
            
            # Hiển thị thẻ thông tin
            with st.container():
                st.markdown(f'<div class="premium-card">', unsafe_allow_html=True)
                
                col_a, col_b, col_c = st.columns([3, 1, 1])
                with col_a:
                    st.subheader(f"{row['Tên ngành']}")
                    st.markdown(f"**Trường:** {row['Trường']} | **Khối:** {', '.join(row['Khối thi'])}")
                    
                    # Cảnh báo tính cách
                    if mbti != "Chưa rõ" and not mbti_match:
                        st.caption(f"⚠️ *Lưu ý: MBTI {mbti} có thể gặp chút thách thức với đặc thù ngành này.*")
                    if mbti_match and mbti != "Chưa rõ":
                        st.caption(f"✨ *Tuyệt vời! Tính cách {mbti} sinh ra là để dành cho ngành này.*")

                with col_b:
                    st.metric("Điểm chuẩn 2025", f"{row['Điểm 2025']}", f"{round(score_diff, 1)} (so với bạn)", 
                              delta_color="normal" if score_diff >= 0 else "inverse")
                with col_c:
                    st.metric("Xu hướng 3 năm", "Tăng nhẹ", f"+{round(row['Điểm 2025'] - row['Điểm 2023'], 2)} đ")
                
                # Chart nhỏ so sánh điểm 3 năm
                chart_data = pd.DataFrame(
                    {"Năm": ["2023", "2024", "2025"], "Điểm": [row["Điểm 2023"], row["Điểm 2024"], row["Điểm 2025"]]}
                ).set_index("Năm")
                st.line_chart(chart_data, height=150, use_container_width=True)
                
                st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.header("Cơ Hội Việc Làm & Đánh Giá Thực Tế")
    for index, row in filtered_df.iterrows():
        st.markdown(f"### {row['Tên ngành']} - {row['Trường']}")
        col_pros, col_cons = st.columns(2)
        with col_pros:
            st.success(f"**Ưu điểm:**\n{row['Ưu điểm']}")
        with col_cons:
            st.error(f"**Nhược điểm:**\n{row['Nhược điểm']}")
        
        st.info(f"**Cơ hội việc làm sau khi ra trường:** {row['Cơ hội việc làm']}")
        st.markdown(f"**Mức học phí tham khảo:** {row['Học phí (Tr/năm)']} triệu VNĐ/năm")
        st.divider()

with tab3:
    st.header("Phân Tích Phương Thức Tuyển Sinh (3 Năm Gần Nhất)")
    st.markdown("Khảo sát dựa trên dữ liệu tuyển sinh chung của nhóm ngành Ngôn ngữ - Sư phạm.")
    
    for method, info in admission_methods.items():
        with st.expander(f"📌 {method} (Chiếm khoảng {info['Chỉ tiêu']} chỉ tiêu)", expanded=True):
            c1, c2 = st.columns(2)
            c1.markdown(f"**Độ khó cạnh tranh:** {info['Độ khó']}")
            c2.markdown(f"**Phân tích khả năng đậu:** {info['Khả năng đậu']}")
            
            # Giả lập thanh Progress bar tỉ lệ cạnh tranh
            if info['Độ khó'] == "Trung bình":
                st.progress(50)
            elif info['Độ khó'] == "Cao":
                st.progress(80)
            else:
                st.progress(95)

st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>Phát triển cho học sinh Khối 10 (Phiên bản 2026) | Dữ liệu mang tính chất tham khảo định hướng.</p>", unsafe_allow_html=True)
