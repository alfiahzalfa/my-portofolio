import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
import requests
from PIL import Image
import pandas as pd
import plotly.express as px
from views.eda_portfolio import show_eda_page
from views.prediction_portfolio import show_prediction_page

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
    # ── Main Title (sesuai soal) ────────────────
    st.markdown(
        "<h1 style='text-align:center; font-size:2.8rem;'>My Portfolio with Streamlit 🚀</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='text-align:center; color:#6B7280; font-size:1.1rem;'>A showcase of my data science projects, skills, and learning journey.</p>",
        unsafe_allow_html=True
    )
    st.write("")

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
                    "id": "eda_portfolio",
                    "title": "Exploratory Data Analysis",
                    "tags": ["Streamlit", "Pandas", "EDA"],
                    "desc": "Interactive EDA dashboard — upload dataset CSV atau gunakan data contoh, lalu eksplorasi visualisasi, distribusi fitur, dan korelasi heatmap.",
                    "img": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=600&q=80",
                    "link": "",
                    "button_text": "Lihat Detail 👀",
                    "is_internal": True
                },
                {
                    "id": "ml_prediction",
                    "title": "ML Prediction & Model Analysis",
                    "tags": ["Scikit-learn", "Plotly", "ML"],
                    "desc": "Platform prediksi machine learning interaktif — pilih model (Logistic Regression, Random Forest, SVM), upload CSV, jalankan prediksi, dan lihat performa model.",
                    "img": "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=600&q=80",
                    "link": "",
                    "button_text": "Lihat Detail 🤖",
                    "is_internal": True
                },
                {
                    "id": "portfolio_web",
                    "title": "Portfolio Website",
                    "tags": ["Streamlit", "CSS", "Python"],
                    "desc": "The exact portfolio you are looking at right now! Built from scratch using Streamlit and custom CSS styling.",
                    "img": "https://images.unsplash.com/photo-1467232004584-a241de8bcf5d?w=600&q=80",
                    "link": "https://github.com/alfiahzalfa/my-portofolio",
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
                            # Gambar proyek
                            st.image(proj["img"], use_container_width=True)

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
            show_eda_page()

        elif st.session_state.project_view == 'ml_prediction':
            show_prediction_page()

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
