import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io

def show_churn_page():
    # ── Back button ──────────────────────────────────────────
    if st.button("← Kembali ke Projects", key="back_churn"):
        st.session_state.project_view = 'grid'
        st.rerun()

    st.markdown("""
    <div style="background:linear-gradient(135deg,rgba(239,68,68,0.15),rgba(220,38,38,0.05));
                border:1px solid rgba(239,68,68,0.3); border-radius:16px; padding:2rem; margin-bottom:2rem;">
        <div style="font-size:2rem; font-weight:800; color:#f1f5f9; font-family:'Plus Jakarta Sans',sans-serif;">
            🏦 Bank Customer Churn Prediction
        </div>
        <div style="color:#94a3b8; margin-top:0.5rem; font-size:0.95rem;">
            Assignment Day 37 · Prediksi churn nasabah bank menggunakan Machine Learning (Decision Tree, Random Forest, Logistic Regression, XGBoost)
        </div>
        <div style="display:flex; gap:0.5rem; flex-wrap:wrap; margin-top:1rem;">
            <span style="background:rgba(239,68,68,0.2);border:1px solid rgba(239,68,68,0.4);border-radius:20px;padding:3px 12px;font-size:0.78rem;color:#fca5a5;">Random Forest</span>
            <span style="background:rgba(239,68,68,0.2);border:1px solid rgba(239,68,68,0.4);border-radius:20px;padding:3px 12px;font-size:0.78rem;color:#fca5a5;">XGBoost</span>
            <span style="background:rgba(239,68,68,0.2);border:1px solid rgba(239,68,68,0.4);border-radius:20px;padding:3px 12px;font-size:0.78rem;color:#fca5a5;">SMOTE</span>
            <span style="background:rgba(239,68,68,0.2);border:1px solid rgba(239,68,68,0.4);border-radius:20px;padding:3px 12px;font-size:0.78rem;color:#fca5a5;">Sklearn</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Dataset Info ─────────────────────────────────────────
    st.markdown("### 📋 Tentang Dataset")
    col1, col2, col3, col4 = st.columns(4)
    metrics = [
        ("10,127", "Total Nasabah", "#ef4444"),
        ("20", "Fitur", "#f59e0b"),
        ("16.07%", "Churn Rate", "#8b5cf6"),
        ("4", "Model ML", "#06b6d4"),
    ]
    for col, (val, label, color) in zip([col1, col2, col3, col4], metrics):
        with col:
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,rgba(30,41,59,0.8),rgba(15,23,42,0.8));
                        border:1px solid rgba(255,255,255,0.1); border-radius:12px; padding:1rem; text-align:center;">
                <div style="font-size:1.6rem; font-weight:800; color:{color}; font-family:'Plus Jakarta Sans',sans-serif;">{val}</div>
                <div style="font-size:0.75rem; color:#94a3b8;">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Upload or Sample ─────────────────────────────────────
    st.markdown("### 📂 Dataset")
    use_sample = st.radio(
        "Pilih sumber data:",
        ["Gunakan Data Sampel (Bank Churn)", "Upload CSV Sendiri"],
        horizontal=True, key="churn_data_source"
    )

    df = None
    if use_sample == "Gunakan Data Sampel (Bank Churn)":
        df = _generate_churn_sample()
        st.success(f"✅ Data sampel dimuat: {len(df):,} baris, {len(df.columns)} kolom")
    else:
        uploaded = st.file_uploader(
            "Upload file CSV (harus punya kolom: Attrition_Flag, Customer_Age, Gender, dll)",
            type=["csv"], key="churn_upload"
        )
        if uploaded:
            try:
                df = pd.read_csv(uploaded)
                st.success(f"✅ File berhasil dimuat: {len(df):,} baris, {len(df.columns)} kolom")
            except Exception as e:
                st.error(f"❌ Gagal memuat file: {e}")
                return

    if df is None:
        st.info("👆 Pilih sumber data untuk memulai analisis.")
        return

    # ── EDA ──────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 🔍 Exploratory Data Analysis")

    tab1, tab2, tab3 = st.tabs(["📊 Distribusi Target", "📈 Fitur Numerik", "🧩 Fitur Kategorikal"])

    target_col = 'Attrition_Flag' if 'Attrition_Flag' in df.columns else df.columns[0]

    with tab1:
        if target_col in df.columns:
            churn_counts = df[target_col].value_counts().reset_index()
            churn_counts.columns = ['Status', 'Count']
            churn_counts['Percent'] = (churn_counts['Count'] / len(df) * 100).round(2)

            col_a, col_b = st.columns([1, 1])
            with col_a:
                fig_pie = px.pie(
                    churn_counts, names='Status', values='Count',
                    color_discrete_sequence=['#ef4444', '#22c55e'],
                    title="Distribusi Churn vs Non-Churn"
                )
                fig_pie.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    font_color='#94a3b8', title_font_color='#f1f5f9'
                )
                st.plotly_chart(fig_pie, use_container_width=True)
            with col_b:
                fig_bar = px.bar(
                    churn_counts, x='Status', y='Count',
                    color='Status', color_discrete_sequence=['#ef4444', '#22c55e'],
                    text='Percent', title="Jumlah Nasabah per Status"
                )
                fig_bar.update_traces(texttemplate='%{text}%', textposition='outside')
                fig_bar.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    font_color='#94a3b8', title_font_color='#f1f5f9',
                    showlegend=False
                )
                st.plotly_chart(fig_bar, use_container_width=True)

    with tab2:
        num_cols = df.select_dtypes(include='number').columns.tolist()
        if num_cols:
            sel = st.selectbox("Pilih fitur numerik:", num_cols, key="churn_num_feat")
            if target_col in df.columns:
                fig_hist = px.histogram(
                    df, x=sel, color=target_col,
                    barmode='overlay', nbins=30,
                    color_discrete_sequence=['#ef4444', '#22c55e'],
                    title=f"Distribusi {sel} per Status Churn"
                )
                fig_hist.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    font_color='#94a3b8', title_font_color='#f1f5f9'
                )
                st.plotly_chart(fig_hist, use_container_width=True)

            # Correlation heatmap
            corr = df[num_cols].corr()
            fig_heat = px.imshow(
                corr, text_auto='.2f', color_continuous_scale='RdBu_r',
                title="Correlation Heatmap"
            )
            fig_heat.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', font_color='#94a3b8',
                title_font_color='#f1f5f9'
            )
            st.plotly_chart(fig_heat, use_container_width=True)

    with tab3:
        cat_cols = df.select_dtypes(include='object').columns.tolist()
        if cat_cols:
            sel_cat = st.selectbox("Pilih fitur kategorikal:", cat_cols, key="churn_cat_feat")
            if target_col in df.columns:
                ct = pd.crosstab(df[sel_cat], df[target_col], normalize='index') * 100
                ct = ct.reset_index()
                ct_melt = ct.melt(id_vars=sel_cat, var_name='Status', value_name='Persen')
                fig_cat = px.bar(
                    ct_melt, x=sel_cat, y='Persen', color='Status',
                    barmode='group', color_discrete_sequence=['#ef4444', '#22c55e'],
                    title=f"Churn Rate per {sel_cat} (%)"
                )
                fig_cat.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    font_color='#94a3b8', title_font_color='#f1f5f9'
                )
                st.plotly_chart(fig_cat, use_container_width=True)

    # ── Model Training ───────────────────────────────────────
    st.markdown("---")
    st.markdown("### 🤖 Model Training & Evaluasi")

    col_s1, col_s2 = st.columns(2)
    with col_s1:
        test_size = st.slider("Test Size (%)", 10, 40, 20, 5, key="churn_test") / 100
    with col_s2:
        use_smote = st.checkbox("Gunakan SMOTE (handle imbalance)", value=True, key="churn_smote")

    # Cek library yang tersedia
    _smote_ok = False
    _xgb_ok = False
    try:
        from imblearn.over_sampling import SMOTE  
        _smote_ok = True
    except ImportError:
        pass
    try:
        from xgboost import XGBClassifier  
        _xgb_ok = True
    except ImportError:
        pass

    lib_status = []
    lib_status.append(f"{'✅' if _smote_ok else '❌'} imbalanced-learn (SMOTE)")
    lib_status.append(f"{'✅' if _xgb_ok else '❌'} xgboost")
    st.info("📦 **Library Status:** " + " &nbsp;|&nbsp; ".join(lib_status))

    if st.button("🚀 Latih Semua Model", key="train_churn", use_container_width=True):
        with st.spinner("Melatih model..."):
            results = _train_churn_models(df, target_col, test_size, use_smote)
            if results:
                st.session_state['churn_results'] = results
                st.success("✅ Semua model berhasil dilatih!")

    if 'churn_results' in st.session_state:
        results = st.session_state['churn_results']
        _display_churn_results(results)


def _generate_churn_sample():
    """Generate realistic-looking bank churn sample data."""
    np.random.seed(42)
    n = 500
    attrition = np.random.choice(
        ['Attrited Customer', 'Existing Customer'],
        n, p=[0.16, 0.84]
    )
    is_churned = (attrition == 'Attrited Customer').astype(int)

    data = {
        'Attrition_Flag': attrition,
        'Customer_Age': np.clip(np.random.normal(46, 8, n).astype(int), 26, 73),
        'Gender': np.random.choice(['M', 'F'], n, p=[0.47, 0.53]),
        'Dependent_Count': np.random.choice([0,1,2,3,4,5], n),
        'Education_Level': np.random.choice(
            ['High School','Graduate','Uneducated','Unknown','College','Post-Graduate','Doctorate'], n
        ),
        'Marital_Status': np.random.choice(['Married','Single','Unknown','Divorced'], n, p=[0.46,0.39,0.07,0.08]),
        'Income_Category': np.random.choice(
            ['Less than $40K','$40K - $60K','$60K - $80K','$80K - $120K','$120K +','Unknown'], n
        ),
        'Card_Category': np.random.choice(['Blue','Silver','Gold','Platinum'], n, p=[0.93,0.05,0.015,0.005]),
        'Months_on_Book': np.clip(np.random.normal(36, 8, n).astype(int), 13, 56),
        'Total_Relationship_Count': np.random.choice([1,2,3,4,5,6], n),
        'Months_Inactive_12_Mon': np.clip(
            np.random.normal(2.5 + is_churned * 0.8, 1, n).astype(int), 0, 6
        ),
        'Contacts_Count_12_Mon': np.clip(
            np.random.normal(2.5 + is_churned * 0.5, 1, n).astype(int), 0, 6
        ),
        'Credit_Limit': np.clip(np.random.exponential(8000, n), 1438, 34516).round(2),
        'Total_Revolving_Bal': np.clip(
            np.random.normal(1163 - is_churned * 400, 800, n).astype(int), 0, 2517
        ),
        'Total_Trans_Amt': np.clip(
            np.random.normal(4404 - is_churned * 1500, 3000, n).astype(int), 510, 18484
        ),
        'Total_Trans_Ct': np.clip(
            np.random.normal(65 - is_churned * 20, 23, n).astype(int), 10, 139
        ),
    }
    return pd.DataFrame(data)


def _train_churn_models(df, target_col, test_size, use_smote):
    try:
        from sklearn.preprocessing import LabelEncoder, StandardScaler
        from sklearn.model_selection import train_test_split
        from sklearn.tree import DecisionTreeClassifier
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.linear_model import LogisticRegression
        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

        dfc = df.copy()

        # Encode categoricals
        for col in dfc.select_dtypes(include='object').columns:
            if col == target_col:
                le_target = LabelEncoder()
                dfc[col] = le_target.fit_transform(dfc[col])
            else:
                le = LabelEncoder()
                dfc[col] = le.fit_transform(dfc[col].astype(str))

        y = dfc[target_col]
        X = dfc.drop(columns=[target_col])

        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=test_size, random_state=42, stratify=y
        )

        if use_smote:
            try:
                from imblearn.over_sampling import SMOTE
                sm = SMOTE(random_state=42)
                X_train, y_train = sm.fit_resample(X_train, y_train)
            except ImportError:
                st.warning("⚠️ imbalanced-learn belum terinstall. Jalankan: `pip install imbalanced-learn`\nSMOTE dilewati, training tetap dilanjutkan.")

        models = {
            'Decision Tree': DecisionTreeClassifier(max_depth=5, random_state=42),
            'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1),
            'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
        }

        try:
            from xgboost import XGBClassifier
            models['XGBoost'] = XGBClassifier(n_estimators=100, random_state=42,
                                               eval_metric='logloss', verbosity=0)
        except ImportError:
            st.info("ℹ️ xgboost belum terinstall — hanya 3 model yang dilatih. Jalankan: `pip install xgboost`")

        results = {}
        for name, model in models.items():
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            y_prob = model.predict_proba(X_test)[:, 1] if hasattr(model, 'predict_proba') else y_pred

            results[name] = {
                'accuracy': accuracy_score(y_test, y_pred),
                'precision': precision_score(y_test, y_pred, average='weighted', zero_division=0),
                'recall': recall_score(y_test, y_pred, average='weighted', zero_division=0),
                'f1': f1_score(y_test, y_pred, average='weighted', zero_division=0),
                'roc_auc': roc_auc_score(y_test, y_prob) if len(np.unique(y_test)) == 2 else 0.0,
            }

            if hasattr(model, 'feature_importances_'):
                results[name]['feature_importance'] = dict(zip(X.columns, model.feature_importances_))

        return results
    except Exception as e:
        st.error(f"❌ Error training: {e}")
        return None


def _display_churn_results(results):
    # Metrics table
    rows = []
    for name, m in results.items():
        rows.append({
            'Model': name,
            'Accuracy': f"{m['accuracy']:.4f}",
            'Precision': f"{m['precision']:.4f}",
            'Recall': f"{m['recall']:.4f}",
            'F1-Score': f"{m['f1']:.4f}",
            'ROC-AUC': f"{m['roc_auc']:.4f}",
        })

    df_results = pd.DataFrame(rows)
    st.dataframe(df_results, use_container_width=True, hide_index=True)

    # Bar chart comparison
    metrics_list = ['accuracy', 'precision', 'recall', 'f1', 'roc_auc']
    fig = go.Figure()
    colors = ['#ef4444', '#f59e0b', '#22c55e', '#06b6d4']
    for i, (name, m) in enumerate(results.items()):
        fig.add_trace(go.Bar(
            name=name,
            x=metrics_list,
            y=[m[k] for k in metrics_list],
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
                               columns=['Feature', 'Importance']).sort_values('Importance', ascending=True).tail(10)
            fig_fi = px.bar(fi, x='Importance', y='Feature', orientation='h',
                            title=f"Top 10 Feature Importance ({name})",
                            color='Importance', color_continuous_scale='Reds')
            fig_fi.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                font_color='#94a3b8', title_font_color='#f1f5f9'
            )
            st.plotly_chart(fig_fi, use_container_width=True)
            break  # Show only first model with feature importance
