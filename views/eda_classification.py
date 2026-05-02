import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go


def show_eda_classification_page():
    # ── Back button ──────────────────────────────────────────
    if st.button("← Kembali ke Projects", key="back_eda_cls"):
        st.session_state.project_view = 'grid'
        st.rerun()

    st.markdown("""
    <div style="background:linear-gradient(135deg,rgba(16,185,129,0.15),rgba(5,150,105,0.05));
                border:1px solid rgba(16,185,129,0.3); border-radius:16px; padding:2rem; margin-bottom:2rem;">
        <div style="font-size:2rem; font-weight:800; color:#f1f5f9; font-family:'Plus Jakarta Sans',sans-serif;">
            📊 EDA & Klasifikasi Data
        </div>
        <div style="color:#94a3b8; margin-top:0.5rem; font-size:0.95rem;">
            Assignment Day 28 · Analisis data eksplorasi lengkap + klasifikasi multi-model dengan evaluasi komprehensif
        </div>
        <div style="display:flex; gap:0.5rem; flex-wrap:wrap; margin-top:1rem;">
            <span style="background:rgba(16,185,129,0.2);border:1px solid rgba(16,185,129,0.4);border-radius:20px;padding:3px 12px;font-size:0.78rem;color:#6ee7b7;">Pandas</span>
            <span style="background:rgba(16,185,129,0.2);border:1px solid rgba(16,185,129,0.4);border-radius:20px;padding:3px 12px;font-size:0.78rem;color:#6ee7b7;">Plotly</span>
            <span style="background:rgba(16,185,129,0.2);border:1px solid rgba(16,185,129,0.4);border-radius:20px;padding:3px 12px;font-size:0.78rem;color:#6ee7b7;">Scikit-learn</span>
            <span style="background:rgba(16,185,129,0.2);border:1px solid rgba(16,185,129,0.4);border-radius:20px;padding:3px 12px;font-size:0.78rem;color:#6ee7b7;">EDA</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Upload or Sample ─────────────────────────────────────
    st.markdown("### 📂 Dataset")
    use_sample = st.radio(
        "Pilih sumber data:",
        ["Gunakan Data Sampel (Iris)", "Upload CSV Sendiri"],
        horizontal=True, key="eda_cls_source"
    )

    df = None
    target_col = None

    if use_sample == "Gunakan Data Sampel (Iris)":
        from sklearn.datasets import load_iris
        iris = load_iris(as_frame=True)
        df = iris.frame.copy()
        df['target'] = iris.target_names[df['target'].values]
        target_col = 'target'
        st.success(f"✅ Dataset Iris dimuat: {len(df):,} baris, {len(df.columns)} kolom")
    else:
        uploaded = st.file_uploader("Upload file CSV", type=["csv"], key="eda_cls_upload")
        if uploaded:
            try:
                df = pd.read_csv(uploaded)
                st.success(f"✅ File dimuat: {len(df):,} baris, {len(df.columns)} kolom")
                target_col = st.selectbox(
                    "Pilih kolom target (label/kelas):",
                    df.columns.tolist(), key="eda_cls_target"
                )
            except Exception as e:
                st.error(f"❌ Gagal memuat file: {e}")
                return

    if df is None:
        st.info("👆 Pilih sumber data untuk memulai analisis.")
        return

    # ── Dataset Overview ─────────────────────────────────────
    st.markdown("---")
    st.markdown("### 🔍 Overview Dataset")

    c1, c2, c3, c4 = st.columns(4)
    num_cols = df.select_dtypes(include='number').columns.tolist()
    cat_cols = [c for c in df.select_dtypes(include='object').columns if c != target_col]
    missing = df.isnull().sum().sum()

    for col, (val, lbl, color) in zip([c1, c2, c3, c4], [
        (f"{len(df):,}", "Baris", "#10b981"),
        (f"{len(df.columns)}", "Kolom", "#f59e0b"),
        (f"{len(num_cols)}", "Fitur Numerik", "#06b6d4"),
        (f"{missing}", "Missing Values", "#ef4444"),
    ]):
        with col:
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,rgba(30,41,59,0.8),rgba(15,23,42,0.8));
                        border:1px solid rgba(255,255,255,0.1); border-radius:12px;
                        padding:1rem; text-align:center;">
                <div style="font-size:1.6rem; font-weight:800; color:{color};">{val}</div>
                <div style="font-size:0.75rem; color:#94a3b8;">{lbl}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    with st.expander("📄 Lihat Data (5 baris pertama)"):
        st.dataframe(df.head(), use_container_width=True)
    with st.expander("📈 Statistik Deskriptif"):
        st.dataframe(df.describe(), use_container_width=True)

    # ── EDA Tabs ─────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 📊 Exploratory Data Analysis")

    tab1, tab2, tab3, tab4 = st.tabs([
        "🎯 Target", "📉 Distribusi", "🔗 Korelasi", "📦 Boxplot"
    ])

    with tab1:
        if target_col and target_col in df.columns:
            vc = df[target_col].value_counts().reset_index()
            vc.columns = ['Kelas', 'Jumlah']
            col_a, col_b = st.columns(2)
            with col_a:
                fig = px.pie(vc, names='Kelas', values='Jumlah',
                             title="Distribusi Kelas",
                             color_discrete_sequence=px.colors.qualitative.Set2)
                fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                                  font_color='#94a3b8', title_font_color='#f1f5f9')
                st.plotly_chart(fig, use_container_width=True)
            with col_b:
                fig2 = px.bar(vc, x='Kelas', y='Jumlah', color='Kelas',
                              color_discrete_sequence=px.colors.qualitative.Set2,
                              title="Jumlah per Kelas")
                fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                                   plot_bgcolor='rgba(0,0,0,0)',
                                   font_color='#94a3b8', title_font_color='#f1f5f9',
                                   showlegend=False)
                st.plotly_chart(fig2, use_container_width=True)

    with tab2:
        if num_cols:
            sel = st.selectbox("Pilih fitur numerik:", num_cols, key="eda_num")
            fig = px.histogram(df, x=sel, nbins=30,
                               color=target_col if target_col in df.columns else None,
                               color_discrete_sequence=px.colors.qualitative.Set2,
                               marginal="box", title=f"Distribusi {sel}")
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                              font_color='#94a3b8', title_font_color='#f1f5f9')
            st.plotly_chart(fig, use_container_width=True)

    with tab3:
        if len(num_cols) >= 2:
            corr = df[num_cols].corr()
            fig = px.imshow(corr, text_auto='.2f', color_continuous_scale='RdBu_r',
                            title="Heatmap Korelasi Fitur Numerik")
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color='#94a3b8',
                              title_font_color='#f1f5f9')
            st.plotly_chart(fig, use_container_width=True)

            if len(num_cols) >= 2:
                x_feat = st.selectbox("Sumbu X:", num_cols, key="scatter_x")
                y_feat = st.selectbox("Sumbu Y:", [c for c in num_cols if c != x_feat], key="scatter_y")
                fig_sc = px.scatter(df, x=x_feat, y=y_feat,
                                    color=target_col if target_col in df.columns else None,
                                    color_discrete_sequence=px.colors.qualitative.Set2,
                                    title=f"Scatter: {x_feat} vs {y_feat}")
                fig_sc.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                                     font_color='#94a3b8', title_font_color='#f1f5f9')
                st.plotly_chart(fig_sc, use_container_width=True)

    with tab4:
        if num_cols and target_col in df.columns:
            sel_box = st.selectbox("Pilih fitur untuk boxplot:", num_cols, key="box_feat")
            fig = px.box(df, x=target_col, y=sel_box,
                         color=target_col,
                         color_discrete_sequence=px.colors.qualitative.Set2,
                         title=f"Distribusi {sel_box} per Kelas")
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                              font_color='#94a3b8', title_font_color='#f1f5f9',
                              showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

    # ── Classification ───────────────────────────────────────
    st.markdown("---")
    st.markdown("### 🤖 Klasifikasi Multi-Model")

    if not target_col or target_col not in df.columns:
        st.warning("⚠️ Kolom target belum dipilih.")
        return

    col_s1, col_s2 = st.columns(2)
    with col_s1:
        test_pct = st.slider("Test Size (%)", 10, 40, 20, 5, key="cls_test") / 100
    with col_s2:
        cv_folds = st.slider("Cross-Validation Folds", 3, 10, 5, key="cls_cv")

    if st.button("🚀 Latih Semua Model", key="train_cls", use_container_width=True):
        with st.spinner("Melatih model..."):
            results = _train_classifiers(df, target_col, test_pct, cv_folds)
            if results:
                st.session_state['cls_results'] = results
                st.success("✅ Semua model selesai dilatih!")

    if 'cls_results' in st.session_state:
        _display_classifier_results(st.session_state['cls_results'])


def _train_classifiers(df, target_col, test_size, cv_folds):
    try:
        from sklearn.preprocessing import LabelEncoder, StandardScaler
        from sklearn.model_selection import train_test_split, cross_val_score
        from sklearn.tree import DecisionTreeClassifier
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.linear_model import LogisticRegression
        from sklearn.svm import SVC
        from sklearn.metrics import accuracy_score, f1_score

        dfc = df.copy()
        for col in dfc.select_dtypes(include='object').columns:
            le = LabelEncoder()
            dfc[col] = le.fit_transform(dfc[col].astype(str))

        y = dfc[target_col]
        X = dfc.drop(columns=[target_col])

        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=test_size, random_state=42, stratify=y
        )

        models = {
            'Decision Tree': DecisionTreeClassifier(max_depth=5, random_state=42),
            'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1),
            'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
            'SVM': SVC(kernel='rbf', probability=True, random_state=42),
        }

        results = {}
        for name, model in models.items():
            cv_scores = cross_val_score(model, X_scaled, y, cv=cv_folds, scoring='accuracy', n_jobs=-1)
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            results[name] = {
                'accuracy': accuracy_score(y_test, y_pred),
                'f1': f1_score(y_test, y_pred, average='weighted', zero_division=0),
                'cv_mean': cv_scores.mean(),
                'cv_std': cv_scores.std(),
            }
            if hasattr(model, 'feature_importances_'):
                results[name]['feature_importance'] = dict(zip(X.columns, model.feature_importances_))

        return results
    except Exception as e:
        st.error(f"❌ Error: {e}")
        return None


def _display_classifier_results(results):
    rows = []
    for name, m in results.items():
        rows.append({
            'Model': name,
            'Test Accuracy': f"{m['accuracy']:.4f}",
            'F1-Score': f"{m['f1']:.4f}",
            f'CV Accuracy (Mean)': f"{m['cv_mean']:.4f}",
            'CV Std': f"±{m['cv_std']:.4f}",
        })

    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    # Bar chart
    fig = go.Figure()
    colors = ['#10b981', '#f59e0b', '#06b6d4', '#8b5cf6']
    for i, (name, m) in enumerate(results.items()):
        fig.add_trace(go.Bar(
            name=name,
            x=['Test Accuracy', 'F1-Score', 'CV Accuracy'],
            y=[m['accuracy'], m['f1'], m['cv_mean']],
            marker_color=colors[i % len(colors)]
        ))

    fig.update_layout(
        barmode='group', title="Perbandingan Performa Model",
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font_color='#94a3b8', title_font_color='#f1f5f9',
        legend=dict(bgcolor='rgba(0,0,0,0)')
    )
    st.plotly_chart(fig, use_container_width=True)

    # Feature importance
    for name, m in results.items():
        if 'feature_importance' in m:
            fi = pd.DataFrame(list(m['feature_importance'].items()),
                               columns=['Feature', 'Importance']).sort_values('Importance', ascending=True)
            fig_fi = px.bar(fi, x='Importance', y='Feature', orientation='h',
                            title=f"Feature Importance ({name})",
                            color='Importance', color_continuous_scale='Greens')
            fig_fi.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                font_color='#94a3b8', title_font_color='#f1f5f9'
            )
            st.plotly_chart(fig_fi, use_container_width=True)
            break
