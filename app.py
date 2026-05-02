import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
import requests
from PIL import Image
import pandas as pd
import plotly.express as px
from views.eda_portfolio import show_eda_page
from views.regression_house_price import show_regression_page
from views.timeseries_forecast import show_timeseries_page
from views.churn_prediction import show_churn_page
from views.eda_classification import show_eda_classification_page

# -----------------
# PAGE CONFIGURATION
# -----------------
st.set_page_config(
    page_title="My Portfolio with Streamlit",
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
        pass

# Apply custom CSS
local_css("style.css")

# -----------------
# LOAD ASSETS
# -----------------
lottie_coding  = load_lottieurl("https://lottie.host/80e77d01-dbf2-494b-9721-e01e4a3c10a3/eIV1T3Y3pG.json")
lottie_contact = load_lottieurl("https://lottie.host/d19c0b17-09f1-4db5-9e67-0c1fc9372bd1/cIuW8H82fT.json")

# -----------------
# NAVIGATION
# -----------------
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 1.5rem 0 1rem 0;">
        <div style="font-size:3rem;">🚀</div>
        <div style="font-family:'Plus Jakarta Sans',sans-serif; font-weight:800;
                    font-size:1.1rem; color:#f1f5f9; margin-top:0.5rem;">Zalfa's Portfolio</div>
        <div style="font-size:0.75rem; color:#94a3b8; margin-top:0.2rem;">Data Science & ML</div>
    </div>
    """, unsafe_allow_html=True)

    selected = option_menu(
        menu_title=None,
        options=["Home", "About", "Projects", "Contact"],
        icons=["house-fill", "person-fill", "code-slash", "envelope-fill"],
        menu_icon="cast",
        default_index=0,
        orientation="vertical",
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon":      {"color": "#a78bfa", "font-size": "18px"},
            "nav-link":  {
                "font-size": "0.9rem", "text-align": "left", "margin": "2px 0",
                "padding": "10px 16px", "border-radius": "10px",
                "color": "#cbd5e1", "font-weight": "500",
                "--hover-color": "rgba(99,102,241,0.15)"
            },
            "nav-link-selected": {
                "background": "linear-gradient(135deg, #667eea, #764ba2)",
                "color": "white", "font-weight": "700"
            },
        }
    )

    st.markdown("""
    <div style="position:absolute; bottom:2rem; left:0; right:0; text-align:center;
                padding: 0 1rem;">
        <div style="background:rgba(99,102,241,0.15); border:1px solid rgba(99,102,241,0.3);
                    border-radius:10px; padding:0.8rem; font-size:0.75rem; color:#94a3b8;">
            🌐 <a href="https://alfiahzalfa-portofolio.streamlit.app"
               style="color:#818cf8; text-decoration:none;">Live Portfolio</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

# =============================================================
# HOME SECTION
# =============================================================
if selected == "Home":

    # ── Hero Banner ──────────────────────────────────────────
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">My Portfolio with Streamlit 🚀</div>
        <div class="hero-subtitle">A showcase of my data science projects, skills, and learning journey.</div>
        <div class="hero-badges">
            <span class="hero-badge">🐍 Python</span>
            <span class="hero-badge">📊 Data Analysis</span>
            <span class="hero-badge">🤖 Machine Learning</span>
            <span class="hero-badge">📈 Visualization</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Intro + Lottie ───────────────────────────────────────
    col_intro, col_lottie = st.columns([3, 2], gap="large")

    with col_intro:
        st.markdown("""
        <div style="padding-top:1rem;">
            <div style="font-size:0.85rem; font-weight:600; color:#818cf8;
                        text-transform:uppercase; letter-spacing:1px; margin-bottom:0.5rem;">
                👋 Hello, I'm
            </div>
            <div style="font-family:'Plus Jakarta Sans',sans-serif; font-size:3rem;
                        font-weight:800; color:#f1f5f9; line-height:1.1; margin-bottom:0.5rem;">
                Zalfa
            </div>
            <div style="font-size:1.2rem; font-weight:500; color:#a5b4fc; margin-bottom:1rem;">
                Data Enthusiast & ML Explorer
            </div>
            <div style="font-size:0.95rem; color:#94a3b8; line-height:1.8; margin-bottom:1.5rem;">
                A <strong style="color:#e2e8f0;">Physics Engineering</strong> graduate from Telkom University,
                now fully dedicated to the world of data. I build analytical models, create insightful
                dashboards, and develop interactive web applications using Python & Streamlit.
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Stat chips
        st.markdown("""
        <div style="display:flex; gap:1rem; flex-wrap:wrap; margin-bottom:1.5rem;">
            <div style="background:linear-gradient(135deg,rgba(99,102,241,0.2),rgba(139,92,246,0.2));
                        border:1px solid rgba(99,102,241,0.4); border-radius:12px;
                        padding:0.8rem 1.2rem; text-align:center; min-width:100px;">
                <div style="font-family:'Plus Jakarta Sans',sans-serif; font-size:1.6rem;
                            font-weight:800; color:#a5b4fc;">5</div>
                <div style="font-size:0.75rem; color:#94a3b8;">Projects</div>
            </div>
            <div style="background:linear-gradient(135deg,rgba(16,185,129,0.2),rgba(5,150,105,0.2));
                        border:1px solid rgba(16,185,129,0.4); border-radius:12px;
                        padding:0.8rem 1.2rem; text-align:center; min-width:100px;">
                <div style="font-family:'Plus Jakarta Sans',sans-serif; font-size:1.6rem;
                            font-weight:800; color:#34d399;">90%</div>
                <div style="font-size:0.75rem; color:#94a3b8;">Model Accuracy</div>
            </div>
            <div style="background:linear-gradient(135deg,rgba(245,158,11,0.2),rgba(217,119,6,0.2));
                        border:1px solid rgba(245,158,11,0.4); border-radius:12px;
                        padding:0.8rem 1.2rem; text-align:center; min-width:100px;">
                <div style="font-family:'Plus Jakarta Sans',sans-serif; font-size:1.6rem;
                            font-weight:800; color:#fbbf24;">5+</div>
                <div style="font-size:0.75rem; color:#94a3b8;">Skills</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.link_button("📄 Download My Resume", "#", use_container_width=False)

    with col_lottie:
        if lottie_coding:
            st_lottie(lottie_coding, height=320, key="coding")

    # ── What I Do ────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center; margin-bottom:1.5rem;">
        <div style="font-family:'Plus Jakarta Sans',sans-serif; font-size:1.5rem;
                    font-weight:700; color:#f1f5f9;">What I Do</div>
        <div style="font-size:0.9rem; color:#94a3b8;">Skills & focus areas I'm building every day</div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3, gap="medium")
    cards = [
        ("💡", "Analytical Modeling",
         "Build ML models that drive real business decisions — from regression to classification.",
         "#667eea", "#764ba2"),
        ("📊", "Data Visualization",
         "Create interactive, insightful dashboards using Plotly, Streamlit, Tableau, and PowerBI.",
         "#10b981", "#059669"),
        ("💻", "Web Applications",
         "Develop end-to-end data apps with Python and Streamlit for seamless user experience.",
         "#f59e0b", "#d97706"),
    ]
    for col, (icon, title, desc, c1_hex, c2_hex) in zip([c1, c2, c3], cards):
        with col:
            st.markdown(f"""
            <div style="background:linear-gradient(145deg,#1e293b,#0f172a);
                        border-radius:18px; padding:1.8rem; text-align:center;
                        border:1px solid rgba(99,102,241,0.2);
                        transition:transform 0.3s ease; height:100%;
                        box-shadow:0 4px 20px rgba(0,0,0,0.2);">
                <div style="font-size:2.5rem; margin-bottom:0.8rem;">{icon}</div>
                <div style="font-family:'Plus Jakarta Sans',sans-serif; font-size:1rem;
                            font-weight:700; color:#f1f5f9; margin-bottom:0.6rem;">{title}</div>
                <div style="font-size:0.85rem; color:#94a3b8; line-height:1.6;">{desc}</div>
                <div style="margin-top:1rem; height:3px; border-radius:10px;
                            background:linear-gradient(90deg,{c1_hex},{c2_hex});"></div>
            </div>
            """, unsafe_allow_html=True)


# =============================================================
# ABOUT SECTION
# =============================================================
elif selected == "About":
    # Header
    st.markdown("""
    <div class="section-header">
        <h2>🧑‍💻 About Me</h2>
        <p>My background, learning journey, and technical skill set.</p>
    </div>
    """, unsafe_allow_html=True)

    col_left, col_right = st.columns([3, 2], gap="large")

    with col_left:
        st.markdown("""
        <div class="about-card">
            <h3>🎓 My Journey</h3>
            <div style="font-size:0.9rem; color:#cbd5e1; line-height:1.9;">
                Hello! I am a <strong style="color:#a5b4fc;">Physics Engineering</strong> graduate
                from <strong style="color:#a5b4fc;">Telkom University</strong>. Right now, I am fully
                dedicating my time to learning about <em>data analysis</em>, <em>machine learning</em>,
                and <em>programming</em>. I love exploring new tools and continuously expanding my
                knowledge through online courses and personal projects.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="about-card" style="margin-top:1rem;">
            <h3>📚 Learning Focus</h3>
            <div style="display:flex; flex-direction:column; gap:0.8rem;">
                <div style="display:flex; align-items:flex-start; gap:0.8rem;">
                    <div style="background:linear-gradient(135deg,#667eea,#764ba2);
                                border-radius:8px; padding:0.4rem 0.7rem;
                                font-size:0.85rem; white-space:nowrap; color:white; font-weight:600;">
                        🐍 Data Foundation
                    </div>
                    <div style="font-size:0.875rem; color:#94a3b8; line-height:1.6;">
                        Python (Pandas, NumPy, Scikit-learn) and SQL for data manipulation and querying.
                    </div>
                </div>
                <div style="display:flex; align-items:flex-start; gap:0.8rem;">
                    <div style="background:linear-gradient(135deg,#10b981,#059669);
                                border-radius:8px; padding:0.4rem 0.7rem;
                                font-size:0.85rem; white-space:nowrap; color:white; font-weight:600;">
                        📊 Visualization
                    </div>
                    <div style="font-size:0.875rem; color:#94a3b8; line-height:1.6;">
                        Communicating data stories using Plotly, Streamlit, Tableau, and PowerBI.
                    </div>
                </div>
                <div style="display:flex; align-items:flex-start; gap:0.8rem;">
                    <div style="background:linear-gradient(135deg,#f59e0b,#d97706);
                                border-radius:8px; padding:0.4rem 0.7rem;
                                font-size:0.85rem; white-space:nowrap; color:white; font-weight:600;">
                        🤖 ML & AI
                    </div>
                    <div style="font-size:0.875rem; color:#94a3b8; line-height:1.6;">
                        Building classification and regression models with real-world datasets.
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_right:
        st.markdown("""
        <div class="about-card">
            <h3>⚡ Technical Skills</h3>
        </div>
        """, unsafe_allow_html=True)

        skills = [
            ("Python (Pandas, NumPy, Sklearn)", 90, "#667eea", "#764ba2"),
            ("SQL (PostgreSQL, MySQL)",          85, "#10b981", "#059669"),
            ("Data Visualization",               80, "#f59e0b", "#d97706"),
            ("Machine Learning",                 75, "#8b5cf6", "#7c3aed"),
            ("Streamlit / Flask",                85, "#06b6d4", "#0891b2"),
        ]
        for skill, pct, c1h, c2h in skills:
            st.markdown(f"""
            <div style="margin-bottom:1.2rem;">
                <div style="display:flex; justify-content:space-between;
                            font-size:0.82rem; font-weight:600; color:#e2e8f0; margin-bottom:0.4rem;">
                    <span>{skill}</span>
                    <span style="color:#a5b4fc;">{pct}%</span>
                </div>
                <div style="background:#1e293b; border-radius:10px; height:8px; overflow:hidden;">
                    <div style="width:{pct}%; height:8px; border-radius:10px;
                                background:linear-gradient(90deg,{c1h},{c2h});
                                box-shadow:0 0 10px {c1h}66;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)


# =============================================================
# PROJECTS SECTION
# =============================================================
elif selected == "Projects":
    if 'project_view' not in st.session_state:
        st.session_state.project_view = 'grid'

    if st.session_state.project_view == 'grid':
        # Header
        st.markdown("""
        <div class="section-header">
            <h2>🚀 My Projects</h2>
            <p>Hands-on projects covering EDA, machine learning, and interactive dashboards.</p>
        </div>
        """, unsafe_allow_html=True)

        projects = [
            {
                "id": "eda_portfolio",
                "title": "📊 Exploratory Data Analysis",
                "tags": ["Streamlit", "Pandas", "EDA", "Plotly"],
                "desc": "Interactive EDA dashboard — upload CSV atau gunakan data contoh, lalu eksplorasi visualisasi, distribusi fitur, korelasi heatmap, dan statistik deskriptif.",
                "button_text": "Lihat Detail",
                "is_internal": True,
                "color": "#667eea"
            },
            {
                "id": "eda_classification",
                "title": "🧩 EDA & Klasifikasi Data",
                "tags": ["EDA", "Classification", "Decision Tree", "Sklearn"],
                "desc": "Analisis eksplorasi data lengkap (distribusi, korelasi, boxplot) + klasifikasi multi-model (Decision Tree, Random Forest, Logistic Regression, SVM) dengan cross-validation.",
                "button_text": "Lihat Detail",
                "is_internal": True,
                "color": "#10b981"
            },
            {
                "id": "regression_house",
                "title": "🏠 House Price Prediction",
                "tags": ["Ridge", "Lasso", "Regression", "Sklearn"],
                "desc": "Prediksi harga rumah menggunakan Linear, Ridge & Lasso Regression. Lengkap dengan alpha tuning, korelasi heatmap, evaluasi RMSE/MAE/MAPE, dan form prediksi interaktif.",
                "button_text": "Lihat Detail",
                "is_internal": True,
                "color": "#f59e0b"
            },
            {
                "id": "timeseries_forecast",
                "title": "📈 E-Commerce Sales Forecasting",
                "tags": ["ARIMA", "Time Series", "Forecasting", "Statsmodels"],
                "desc": "Analisis tren penjualan harian/mingguan/bulanan & forecasting dengan ARIMA. Upload data transaksi CSV sendiri, lihat uji ADF, dan download hasil forecast.",
                "button_text": "Lihat Detail",
                "is_internal": True,
                "color": "#06b6d4"
            },
            {
                "id": "churn_prediction",
                "title": "🏦 Bank Churn Prediction",
                "tags": ["XGBoost", "Random Forest", "SMOTE", "Sklearn"],
                "desc": "Prediksi churn nasabah bank menggunakan 4 model ML (Decision Tree, Random Forest, Logistic Regression, XGBoost) + SMOTE untuk handle imbalanced data.",
                "button_text": "Lihat Detail",
                "is_internal": True,
                "color": "#ef4444"
            },
        ]

        for i in range(0, len(projects), 3):
            cols = st.columns(3, gap="medium")
            for j, col in enumerate(cols):
                if i + j < len(projects):
                    proj = projects[i + j]
                    with col:
                        tags_html = "".join([
                            f'<span class="tech-tag">{tag}</span>'
                            for tag in proj["tags"]
                        ])
                        accent = proj["color"]

                        st.markdown(f"""
                        <div class="project-card">
                            <div class="project-title">{proj["title"]}</div>
                            <div style="margin-bottom:10px;">{tags_html}</div>
                            <p class="project-desc">{proj["desc"]}</p>
                            <div style="height:2px; border-radius:4px; margin-top:0.5rem;
                                        background:linear-gradient(90deg,{accent},transparent);"></div>
                        </div>
                        """, unsafe_allow_html=True)

                        if proj["is_internal"]:
                            if st.button(proj["button_text"],
                                         key=f"btn_{proj['id']}",
                                         use_container_width=True):
                                st.session_state.project_view = proj["id"]
                                st.rerun()
                        else:
                            st.link_button(proj["button_text"],
                                           proj["link"],
                                           use_container_width=True)

    elif st.session_state.project_view == 'eda_portfolio':
        show_eda_page()

    elif st.session_state.project_view == 'eda_classification':
        show_eda_classification_page()

    elif st.session_state.project_view == 'regression_house':
        show_regression_page()

    elif st.session_state.project_view == 'timeseries_forecast':
        show_timeseries_page()

    elif st.session_state.project_view == 'churn_prediction':
        show_churn_page()


# =============================================================
# CONTACT SECTION
# =============================================================
elif selected == "Contact":
    st.markdown("""
    <div class="section-header">
        <h2>📬 Get In Touch</h2>
        <p>I'm always open to new projects, ideas, or just a friendly chat.</p>
    </div>
    """, unsafe_allow_html=True)

    contact_col1, contact_col2 = st.columns([3, 2], gap="large")

    with contact_col1:
        # Contact links
        st.markdown("""
        <div class="about-card">
            <h3>🔗 Connect With Me</h3>
            <div style="display:flex; flex-direction:column; gap:0.8rem; margin-top:0.5rem;">
                <a href="mailto:alfiahzalfatsabitah@gmail.com"
                   style="display:flex; align-items:center; gap:0.8rem;
                          text-decoration:none; color:inherit;">
                    <div style="background:linear-gradient(135deg,#ea4335,#c62828);
                                border-radius:10px; padding:0.5rem; font-size:1.2rem;">✉️</div>
                    <div>
                        <div style="font-weight:600; color:#e2e8f0; font-size:0.875rem;">Email</div>
                        <div style="color:#94a3b8; font-size:0.8rem;">alfiahzalfatsabitah@gmail.com</div>
                    </div>
                </a>
                <a href="https://linkedin.com/in/alfiahzalfatsabitah"
                   style="display:flex; align-items:center; gap:0.8rem;
                          text-decoration:none; color:inherit;">
                    <div style="background:linear-gradient(135deg,#0077b5,#005582);
                                border-radius:10px; padding:0.5rem; font-size:1.2rem;">🔗</div>
                    <div>
                        <div style="font-weight:600; color:#e2e8f0; font-size:0.875rem;">LinkedIn</div>
                        <div style="color:#94a3b8; font-size:0.8rem;">linkedin.com/in/alfiahzalfatsabitah</div>
                    </div>
                </a>
                <a href="https://github.com/alfiahzalfa"
                   style="display:flex; align-items:center; gap:0.8rem;
                          text-decoration:none; color:inherit;">
                    <div style="background:linear-gradient(135deg,#24292e,#586069);
                                border-radius:10px; padding:0.5rem; font-size:1.2rem;">🐙</div>
                    <div>
                        <div style="font-weight:600; color:#e2e8f0; font-size:0.875rem;">GitHub</div>
                        <div style="color:#94a3b8; font-size:0.8rem;">github.com/alfiahzalfa</div>
                    </div>
                </a>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Contact form
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="font-family:'Plus Jakarta Sans',sans-serif; font-size:1rem;
                    font-weight:700; color:#f1f5f9; margin-bottom:1rem;">
            💬 Send Me a Message
        </div>
        """, unsafe_allow_html=True)

        contact_form = """
        <form action="https://formsubmit.co/alfiahzalfatsabitah@gmail.com" method="POST">
            <input type="hidden" name="_captcha" value="false">
            <input type="text" name="name" placeholder="Your name" required
                   style="width:100%; padding:12px 16px; margin-bottom:12px; border-radius:10px;
                          border:1px solid rgba(99,102,241,0.4); background:#1e293b;
                          color:#f1f5f9; font-family:Inter,sans-serif; font-size:0.875rem; outline:none;">
            <input type="email" name="email" placeholder="Your email" required
                   style="width:100%; padding:12px 16px; margin-bottom:12px; border-radius:10px;
                          border:1px solid rgba(99,102,241,0.4); background:#1e293b;
                          color:#f1f5f9; font-family:Inter,sans-serif; font-size:0.875rem; outline:none;">
            <textarea name="message" placeholder="Your message here..." required
                      style="width:100%; padding:12px 16px; margin-bottom:16px; border-radius:10px;
                             border:1px solid rgba(99,102,241,0.4); background:#1e293b;
                             color:#f1f5f9; font-family:Inter,sans-serif; font-size:0.875rem;
                             height:120px; resize:vertical; outline:none;"></textarea>
            <button type="submit"
                    style="background:linear-gradient(135deg,#667eea,#764ba2); color:white;
                           padding:12px 28px; border:none; border-radius:10px; cursor:pointer;
                           font-family:'Plus Jakarta Sans',sans-serif; font-size:0.9rem;
                           font-weight:700; box-shadow:0 4px 15px rgba(102,126,234,0.4);
                           transition:all 0.3s ease; width:100%;">
                🚀 Send Message
            </button>
        </form>
        """
        st.markdown(contact_form, unsafe_allow_html=True)

    with contact_col2:
        if lottie_contact:
            st_lottie(lottie_contact, height=400, key="contact")
