import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
import requests
from PIL import Image
import pandas as pd

# -----------------
# PAGE CONFIGURATION
# -----------------
st.set_page_config(
    page_title="My Portfolio",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------
# HELPER FUNCTIONS
# -----------------
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def local_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning(f"CSS file {file_name} not found.")

# Apply custom CSS
local_css("style.css")

# -----------------
# LOAD ASSETS
# -----------------
# Placeholder Lottie animation (coding)
lottie_coding = load_lottieurl("https://lottie.host/80e77d01-dbf2-494b-9721-e01e4a3c10a3/eIV1T3Y3pG.json") 
lottie_contact = load_lottieurl("https://lottie.host/d19c0b17-09f1-4db5-9e67-0c1fc9372bd1/cIuW8H82fT.json")

# -----------------
# NAVIGATION
# -----------------
with st.sidebar:
    selected = option_menu(
        menu_title=None,
        options=["Home", "About", "Projects", "Contact"],
        icons=["house", "person", "code-slash", "envelope"],
        menu_icon="cast",
        default_index=0,
        orientation="vertical",
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "orange", "font-size": "25px"}, 
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "#4F46E5"},
        }
    )

# -----------------
# HOME SECTION
# -----------------
if selected == "Home":
    with st.container():
        left_column, right_column = st.columns([2, 1])
        with left_column:
            st.title("Hi, I am Zalfa 👋")
            st.subheader("A passionate learner exploring the world of Data from Indonesia.")
            st.write("I am currently focused on learning everything about data. From Python programming to creating visualizations, I am building my foundation step by step to solve real-world problems.")
            st.write("[Download My Resume >](#)")
        with right_column:
            if lottie_coding:
                st_lottie(lottie_coding, height=300, key="coding")

    st.write("---")
    st.write("### What I do")
    st.write(
        """
        - 💡 Build analytical models that drive business decisions.
        - 📊 Create interactive and insightful dashboards.
        - 💻 Develop end-to-end web applications with Python and Streamlit.
        """
    )


# -----------------
# ABOUT SECTION
# -----------------
if selected == "About":
    with st.container():
        st.title("About Me 🧑‍💻")
        st.write("---")
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("### Journey")
            st.write(
                """
                Hello! I am a Physics Engineering graduate from Telkom University. 
                Right now, I am fully dedicating my time to learning about data analysis, machine learning, and programming. 
                I love exploring new tools and continuously expanding my knowledge through online courses and personal projects.
                """
            )
            
            st.write("### My Learning Focus")
            st.write("**Data Foundation**")
            st.write("- Currently learning Python (Pandas, NumPy) and SQL.")
            st.write("**Visualization & Storytelling**")
            st.write("- Learning how to communicate data using charts and dashboards.")

        with col2:
            st.write("### Skills")
            # Instead of simple text, we can use progress bars (simulating proficiency)
            st.write("**Python (Pandas, NumPy, Scikit-learn)**")
            st.progress(90)
            
            st.write("**SQL (PostgreSQL, MySQL)**")
            st.progress(85)
            
            st.write("**Data Visualization (Tableau, PowerBI)**")
            st.progress(80)
            
            st.write("**Machine Learning**")
            st.progress(75)
            
            st.write("**Web Development (Streamlit, Flask)**")
            st.progress(85)

# -----------------
# PROJECTS SECTION
# -----------------
if selected == "Projects":
    with st.container():
        # Initialize session state for project view if it doesn't exist
        if 'project_view' not in st.session_state:
            st.session_state.project_view = 'grid'

        if st.session_state.project_view == 'grid':
            st.title("My Projects 🚀")
            st.write("---")
            st.write("Here are some of my recent works. Feel free to explore!")

            # List of Projects
            projects = [
                {
                    "id": "sales_model",
                    "title": "Sales Prediction Model",
                    "tags": ["Python", "Scikit-learn"],
                    "desc": "A machine learning model to predict future store sales using historical data and promotional events. Achieved 90% accuracy.",
                    "link": "https://github.com/username/sales-prediction-model",
                    "button_text": "View on GitHub",
                    "is_internal": False
                },
                {
                    "id": "eda_portfolio",
                    "title": "Exploratory Data Analysis",
                    "tags": ["Streamlit", "Pandas", "EDA"],
                    "desc": "Interactive EDA dashboard where users can view sample data or upload their own dataset.",
                    "link": "",
                    "button_text": "Lihat Detail 👀",
                    "is_internal": True
                },
                {
                    "id": "portfolio_web",
                    "title": "Portfolio Website",
                    "tags": ["Streamlit", "CSS"],
                    "desc": "The exact portfolio you are looking at right now! Built from scratch using Streamlit and custom CSS styling.",
                    "link": "https://github.com/username/portfolio-website",
                    "button_text": "View Code",
                    "is_internal": False
                }
            ]

            # Dynamically create the project grid rows (3 columns per row)
            for i in range(0, len(projects), 3):
                cols = st.columns(3)
                for j, col in enumerate(cols):
                    if i + j < len(projects):
                        proj = projects[i + j]
                        with col:
                            # Create HTML tags for each tech stack
                            tags_html = "".join([f'<span class="tech-tag">{tag}</span>' for tag in proj["tags"]])
                            
                            # Display the Project Card
                            st.markdown(
                                f"""
                                <div class="project-card">
                                    <div class="project-title">{proj["title"]}</div>
                                    <div>{tags_html}</div>
                                    <p class="project-desc" style="margin-top: 10px;">{proj["desc"]}</p>
                                </div>
                                """, 
                                unsafe_allow_html=True
                            )
                            # Logic for button: Internal vs External
                            if proj["is_internal"]:
                                if st.button(proj["button_text"], key=f"btn_{proj['id']}"):
                                    st.session_state.project_view = proj["id"]
                                    st.rerun()
                            else:
                                st.link_button(proj["button_text"], proj["link"])
                                
        elif st.session_state.project_view == 'eda_portfolio':
            # -----------------
            # EDA DETAIL VIEW
            # -----------------
            if st.button("⬅️ Kembali ke Daftar Project"):
                st.session_state.project_view = 'grid'
                st.rerun()
                
            st.title("📊 Exploratory Data Analysis Dashboard")
            st.write("---")
            
            st.write("Di bagian ini, kamu bisa melihat contoh EDA yang saya buat, atau mencoba mengunggah dataset milikmu sendiri untuk melihat hasilnya secara interaktif.")
            
            # Pilihan mode data
            mode_data = st.radio(
                "Pilih Sumber Data:",
                ("Gunakan Data Contoh (Dari GitHub)", "Upload Dataset Anda Sendiri (CSV)"),
                horizontal=True
            )
            
            st.write("---")
            df = None
            
            if mode_data == "Gunakan Data Contoh (Dari GitHub)":
                st.info("💡 Menampilkan dataset contoh dummy untuk saat ini. Nanti bisa diganti dengan dataset asli dari GitHub.")
                # Dummy data
                df = pd.DataFrame({
                    "Kategori": ["Elektronik", "Pakaian", "Makanan", "Buku", "Mainan"],
                    "Total_Sales": [1500, 2300, 3100, 800, 1200],
                    "Rating": [4.5, 4.2, 4.8, 4.9, 4.1]
                })
                # Untuk pakai Github ganti jadi: df = pd.read_csv("https://raw.githubusercontent.com/...")
                
            elif mode_data == "Upload Dataset Anda Sendiri (CSV)":
                st.info("💡 Format dataset idealnya memiliki kolom numerik dan kategorikal untuk divisualisasikan.")
                uploaded_file = st.file_uploader("Pilih file CSV", type=['csv'])
                
                if uploaded_file is not None:
                    try:
                        df = pd.read_csv(uploaded_file)
                        st.success("File berhasil diunggah!")
                    except Exception as e:
                        st.error(f"Terjadi kesalahan saat membaca file: {e}")
                        
            # Jika dataset berhasil dimuat
            if df is not None:
                st.subheader("1. Data Overview")
                st.write("Preview 5 baris pertama dari dataset:")
                st.dataframe(df.head())
                
                st.subheader("2. Statistik Deskriptif")
                st.write("Rangkuman statistik dari data numerik:")
                st.dataframe(df.describe())
                
                st.subheader("3. Visualisasi")
                st.write("Pilih variabel untuk diplot. Fitur ini secara otomatis mendeteksi kolom tipe data pada CSV Anda.")
                
                # Mendeteksi kolom string dan numerik secara otomatis
                kolom_numerik = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
                kolom_kategorikal = df.select_dtypes(include=['object', 'category']).columns.tolist()
                
                if len(kolom_kategorikal) > 0 and len(kolom_numerik) > 0:
                    col1, col2 = st.columns(2)
                    with col1:
                        kat_pilihan = st.selectbox("Pilih Kolom Kategorikal (X-axis)", kolom_kategorikal)
                    with col2:
                        num_pilihan = st.selectbox("Pilih Kolom Numerik (Y-axis)", kolom_numerik)
                        
                    st.write(f"**Total {num_pilihan} berdasarkan {kat_pilihan}**:")
                    try:
                        chart_data = df.groupby(kat_pilihan)[num_pilihan].sum().reset_index()
                        st.bar_chart(chart_data.set_index(kat_pilihan))
                    except Exception as e:
                        st.warning("Grafik gagal dimuat karena isi data tidak kompatibel.")
                elif len(kolom_numerik) > 0:
                    st.write("Visualisasi tren untuk kolom numerik:")
                    st.line_chart(df[kolom_numerik])
                else:
                    st.warning("Tidak ditemukan kolom yang cocok untuk divisualisasikan secara otomatis.")

# -----------------
# CONTACT SECTION
# -----------------
if selected == "Contact":
    with st.container():
        st.title("Get In Touch 📬")
        st.write("---")
        
        contact_col1, contact_col2 = st.columns(2)
        
        with contact_col1:
            st.write("I am always open to discussing new projects, creative ideas, or opportunities to be part of your visions.")
            
            st.write("### Connect with me:")
            st.write("✉️ **Email:** [alfiahzalfatsabitah@gmail.com](mailto:alfiahzalfatsabitah@gmail.com)")
            st.write("🔗 **LinkedIn:** [linkedin.com/in/yourprofile](https://linkedin.com/in/alfiahzalfatsabitah)")
            st.write("🐙 **GitHub:** [github.com/yourusername](https://github.com/alfiahzalfa)")
            
            st.write("### Send me a message")
            contact_form = """
            <form action="https://formsubmit.co/alfiahzalfatsabitah@gmail.com" method="POST">
                <input type="hidden" name="_captcha" value="false">
                <input type="text" name="name" placeholder="Your name" required style="width: 100%; padding: 10px; margin-bottom: 10px; border-radius: 5px; border: 1px solid #ccc;">
                <input type="email" name="email" placeholder="Your email" required style="width: 100%; padding: 10px; margin-bottom: 10px; border-radius: 5px; border: 1px solid #ccc;">
                <textarea name="message" placeholder="Your message here" required style="width: 100%; padding: 10px; margin-bottom: 10px; border-radius: 5px; border: 1px solid #ccc; height: 100px;"></textarea>
                <button type="submit" style="background-color: #4F46E5; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer;">Send</button>
            </form>
            """
            st.markdown(contact_form, unsafe_allow_html=True)
            
        with contact_col2:
            if lottie_contact:
                st_lottie(lottie_contact, height=400, key="contact")
