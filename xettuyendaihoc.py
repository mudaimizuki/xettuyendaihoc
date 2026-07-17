import streamlit as st
import pandas as pd
import numpy as np
from streamlit_option_menu import option_menu

# --- 1. CẤU HÌNH TRANG & GIAO DIỆN LUXURY ---
st.set_page_config(page_title="UniCompass Elite", page_icon="🎓", layout="wide", initial_sidebar_state="expanded")

# CSS Tuỳ chỉnh cho giao diện sang trọng (Màu vàng kim, font chữ gọn gàng)
st.markdown("""
    <style>
    :root {
        --primary-gold: #D4AF37;
        --dark-bg: #121212;
    }
    h1, h2, h3 {
        color: var(--primary-gold) !important;
        font-family: 'Georgia', serif;
    }
    .stButton>button {
        background-color: transparent;
        color: var(--primary-gold);
        border: 1px solid var(--primary-gold);
        border-radius: 5px;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: var(--primary-gold);
        color: #fff;
    }
    .metric-card {
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #333;
        background-color: rgba(255, 255, 255, 0.05);
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. DỮ LIỆU MẪU (MOCK DATABASE) ---
# Trong thực tế, bạn sẽ thay thế phần này bằng: df = pd.read_csv('du_lieu_dai_hoc.csv')
data = {
    "Trường": ["ĐH Bách Khoa ĐHQG-HCM", "ĐH Khoa học Tự nhiên ĐHQG-HCM", "ĐH Kinh tế TP.HCM", "ĐH Sư phạm Kỹ thuật"],
    "Ngành": ["Khoa học Máy tính", "Vật lý học", "Kinh doanh Quốc tế", "Công nghệ Kỹ thuật Ô tô"],
    "Khối_Thi": ["A00, A01", "A00, A01", "A00, A01, D01", "A00, A01"],
    "MBTI": [["INTJ", "INTP", "ISTJ"], ["INTP", "INTJ", "INFJ"], ["ENTJ", "ESTJ", "ENFJ"], ["ISTP", "ESTP"]],
    "Enneagram": [[5, 3, 1], [5, 4], [3, 8], [8, 5]],
    "Diem_2023": [28.0, 24.5, 27.2, 25.5],
    "Diem_2024": [28.2, 25.0, 27.5, 26.0],
    "Diem_2025": [28.5, 25.2, 27.8, 26.3],
    "Phuong_Thuc": ["THPTQG, ĐGNL, ƯTXT", "THPTQG, ĐGNL", "THPTQG, ĐGNL, Học Bạ", "THPTQG, Học Bạ"],
    "Co_Hoi_Viec_Lam": ["Rất cao, thiếu hụt kỹ sư AI/Phần mềm.", "Cao, đặc biệt trong R&D và giảng dạy.", "Trung bình, cạnh tranh cao.", "Rất cao, ngành công nghiệp đang khát nhân lực."],
    "Uu_diem_Nganh": ["Thu nhập cao, nhiều cơ hội toàn cầu.", "Cơ sở nền tảng vững chắc cho mọi khoa học.", "Môi trường năng động, thu nhập hấp dẫn.", "Thực hành nhiều, dễ xin việc ngay."],
    "Nhuoc_diem_Nganh": ["Áp lực lớn, công nghệ thay đổi liên tục.", "Cần học lên cao (Thạc sĩ/Tiến sĩ) để tối ưu thu nhập.", "Đào thải nhanh nếu không có ngoại ngữ tốt.", "Môi trường làm việc đôi khi nặng nhọc."]
}
df = pd.DataFrame(data)

# --- 3. MENU ĐIỀU HƯỚNG ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/8074/8074804.png", width=100) # Placeholder logo
    st.markdown("<h2 style='text-align: center; color: #D4AF37;'>UniCompass Elite</h2>", unsafe_allow_html=True)
    
    selected_menu = option_menu(
        menu_title=None,
        options=["Phân tích Hồ sơ", "Tìm kiếm Ngành/Trường", "Đánh giá Năng lực"],
        icons=["person-vcard", "search", "bar-chart-line"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#D4AF37", "font-size": "18px"}, 
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px"},
            "nav-link-selected": {"background-color": "rgba(212, 175, 55, 0.2)"},
        }
    )
    
    st.markdown("---")
    st.caption("💡 Chế độ Tối/Sáng: Sử dụng cài đặt (Settings) góc phải trên cùng của Streamlit.")

# --- 4. LOGIC XỬ LÝ & GIAO DIỆN CHÍNH ---

def calculate_pass_probability(user_score, avg_score, method):
    """Hàm tính toán tỷ lệ đậu dựa trên điểm và phương thức"""
    diff = user_score - avg_score
    if "ĐGNL" in method and "Học Bạ" not in method:
        base_prob = 60 # Cạnh tranh cao hơn
    else:
        base_prob = 70
        
    prob = base_prob + (diff * 15)
    prob = max(5, min(99, prob)) # Giới hạn từ 5% đến 99%
    return round(prob, 2)

if selected_menu == "Phân tích Hồ sơ":
    st.title("Phân Tích Mức Độ Phù Hợp Chuyên Sâu")
    st.markdown("Cung cấp thông tin cá nhân để hệ thống đối chiếu với dữ liệu lịch sử và tâm lý học.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        mbti_input = st.selectbox("Kiểu MBTI của bạn:", ["INTJ", "INTP", "ENTJ", "ENTP", "INFJ", "INFP", "ENFJ", "ENFP", "ISTJ", "ISFJ", "ESTJ", "ESFJ", "ISTP", "ISFP", "ESTP", "ESFP"])
    with col2:
        enneagram_input = st.selectbox("Type Enneagram:", [1, 2, 3, 4, 5, 6, 7, 8, 9])
    with col3:
        khoi_thi = st.selectbox("Khối thi dự kiến:", ["A00", "A01", "B00", "C00", "D01", "D07"])
        
    diem_du_kien = st.slider("Điểm xét tuyển dự kiến (Thang 30):", 15.0, 30.0, 24.0, 0.25)
    
    if st.button("Bắt đầu Phân tích Hệ thống 🚀"):
        st.markdown("---")
        st.subheader("Kết quả đề xuất dành cho bạn")
        
        # Lọc dữ liệu logic
        matched_results = []
        for index, row in df.iterrows():
            mbti_match = mbti_input in row["MBTI"]
            ennea_match = enneagram_input in row["Enneagram"]
            khoi_match = khoi_thi in row["Khối_Thi"]
            
            if (mbti_match or ennea_match) and khoi_match:
                avg_3_years = round((row["Diem_2023"] + row["Diem_2024"] + row["Diem_2025"]) / 3, 2)
                prob = calculate_pass_probability(diem_du_kien, avg_3_years, row["Phuong_Thuc"])
                
                matched_results.append({
                    "Trường": row["Trường"],
                    "Ngành": row["Ngành"],
                    "Điểm_TB_3_Năm": avg_3_years,
                    "Tỷ_lệ_đậu": prob,
                    "Cơ_hội_việc_làm": row["Co_Hoi_Viec_Lam"],
                    "Ưu_điểm": row["Uu_diem_Nganh"],
                    "Nhược_điểm": row["Nhuoc_diem_Nganh"],
                    "Phương_thức": row["Phuong_Thuc"]
                })
        
        if not matched_results:
            st.warning("Hệ thống chưa tìm thấy dữ liệu hoàn toàn khớp với hồ sơ của bạn. Hãy thử điều chỉnh lại khối thi hoặc điểm số.")
        else:
            for res in matched_results:
                with st.expander(f"🏫 {res['Trường']} - Ngành: {res['Ngành']}", expanded=True):
                    sc1, sc2, sc3 = st.columns(3)
                    sc1.metric("Điểm chuẩn TB 3 năm", res['Điểm_TB_3_Năm'])
                    sc2.metric("Khả năng đậu (Ước tính)", f"{res['Tỷ_lệ_đậu']}%")
                    sc3.metric("Phương thức xét", res['Phương_thức'].split(",")[0] + "...")
                    
                    st.markdown(f"**💡 Cơ hội việc làm thực tế:** {res['Cơ_hội_việc_làm']}")
                    st.markdown(f"**✅ Ưu điểm:** {res['Ưu_điểm']}")
                    st.markdown(f"**⚠️ Nhược điểm:** {res['Nhược_điểm']}")
                    
                    st.progress(int(res['Tỷ_lệ_đậu']))

elif selected_menu == "Tìm kiếm Ngành/Trường":
    st.title("Tra Cứu Dữ Liệu Tuyển Sinh Tự Do")
    search_term = st.text_input("🔍 Nhập tên Trường hoặc Ngành học (VD: Bách Khoa, Vật lý...):")
    
    if search_term:
        filtered_df = df[df['Trường'].str.contains(search_term, case=False) | df['Ngành'].str.contains(search_term, case=False)]
        if not filtered_df.empty:
            st.dataframe(filtered_df[['Trường', 'Ngành', 'Khối_Thi', 'Diem_2023', 'Diem_2024', 'Diem_2025']], use_container_width=True)
            
            st.subheader("Phân tích biến động điểm 3 năm gần nhất")
            chart_data = filtered_df.set_index('Ngành')[['Diem_2023', 'Diem_2024', 'Diem_2025']].T
            st.line_chart(chart_data)
        else:
            st.info("Không tìm thấy kết quả phù hợp.")

elif selected_menu == "Đánh giá Năng lực":
    st.title("Bản Đồ Cạnh Tranh Phương Thức Xét Tuyển")
    st.write("Phân tích lợi thế của bạn qua các hình thức tuyển sinh hiện hành.")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.info("**Xét tuyển THPTQG**\n\nPhù hợp với học sinh có nền tảng kiến thức SGK vững vàng. Độ rủi ro: Trung bình.")
    with col_b:
        st.success("**Đánh giá năng lực (ĐGNL)**\n\nĐòi hỏi tư duy logic, phổ kiến thức rộng. Phù hợp nhóm ngành Công nghệ, Kỹ thuật. Độ rủi ro: Thấp nếu tư duy tốt.")
    
    st.warning("**Xét Học bạ**\n\nCạnh tranh cực kỳ gắt gao ở các trường Top đầu. Điểm thường lạm phát từ 28.0+.")
