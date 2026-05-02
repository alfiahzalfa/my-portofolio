import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split, learning_curve
from sklearn.metrics import (
    confusion_matrix, classification_report,
    accuracy_score, precision_score, recall_score, f1_score
)
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.datasets import load_iris, load_wine, load_breast_cancer
import warnings
warnings.filterwarnings('ignore')


# ─────────────────────────────────────
# HELPER: Load sample datasets
# ─────────────────────────────────────
def load_sample_dataset(name):
    if name == "Iris (Klasifikasi Bunga)":
        data = load_iris()
    elif name == "Wine (Klasifikasi Anggur)":
        data = load_wine()
    else:
        data = load_breast_cancer()

    df = pd.DataFrame(data.data, columns=data.feature_names)
    df['target'] = data.target
    df['target_name'] = [data.target_names[i] for i in data.target]
    return df, data.target_names.tolist()


# ─────────────────────────────────────
# HELPER: Train model
# ─────────────────────────────────────
def get_model(model_name):
    models = {
        "Logistic Regression": LogisticRegression(max_iter=500, random_state=42),
        "Random Forest":       RandomForestClassifier(n_estimators=100, random_state=42),
        "Support Vector Machine (SVM)": SVC(kernel='rbf', probability=True, random_state=42),
    }
    return models[model_name]


# ─────────────────────────────────────
# MAIN PAGE
# ─────────────────────────────────────
def show_prediction_page():
    if st.button("⬅️ Kembali ke Daftar Project"):
        st.session_state.project_view = 'grid'
        st.rerun()

    st.title("🤖 Machine Learning Prediction & Model Analysis")
    st.markdown("Platform interaktif untuk melatih, mengevaluasi, dan menggunakan model machine learning.")
    st.write("---")

    # ── SIDEBAR CONTROLS ────────────────────────
    st.sidebar.markdown("## ⚙️ Konfigurasi Model")

    model_name = st.sidebar.selectbox(
        "Pilih Model:",
        ["Logistic Regression", "Random Forest", "Support Vector Machine (SVM)"],
        key="pred_model_select"
    )

    test_size = st.sidebar.slider("Ukuran Data Test (%)", 10, 40, 20, key="pred_test_size") / 100

    # ── DATA SOURCE ─────────────────────────────
    st.markdown("### 📂 Sumber Data")
    data_mode = st.radio(
        "Pilih sumber data:",
        ["Gunakan Dataset Contoh", "Upload Dataset CSV Sendiri"],
        horizontal=True,
        key="pred_data_mode"
    )

    df = None
    target_col = None
    class_names = None

    if data_mode == "Gunakan Dataset Contoh":
        dataset_choice = st.selectbox(
            "Pilih dataset:",
            ["Iris (Klasifikasi Bunga)", "Wine (Klasifikasi Anggur)", "Breast Cancer (Deteksi Kanker)"],
            key="pred_dataset_choice"
        )
        df, class_names = load_sample_dataset(dataset_choice)
        target_col = "target"
        st.success(f"✅ Dataset **{dataset_choice}** berhasil dimuat — {df.shape[0]} baris, {df.shape[1]} kolom")

    else:
        uploaded_file = st.file_uploader(
            "Upload file CSV (pastikan ada kolom target/label):", type=["csv"], key="pred_uploader"
        )
        if uploaded_file:
            try:
                df = pd.read_csv(uploaded_file)
                st.success(f"✅ File berhasil diunggah — {df.shape[0]} baris, {df.shape[1]} kolom")
                target_col = st.selectbox("Pilih kolom Target (Label):", df.columns.tolist(), key="pred_target")
            except Exception as e:
                st.error(f"Gagal membaca file: {e}")

    # ── MAIN CONTENT ────────────────────────────
    if df is not None and target_col is not None:
        # Encode jika target berupa string
        df_model = df.copy()
        le = LabelEncoder()
        if df_model[target_col].dtype == object:
            df_model[target_col] = le.fit_transform(df_model[target_col])
            class_names = le.classes_.tolist()

        if class_names is None:
            unique_vals = sorted(df_model[target_col].unique())
            class_names = [str(v) for v in unique_vals]

        # Pisahkan fitur dan target
        numeric_cols = df_model.select_dtypes(include=[np.number]).columns.tolist()
        numeric_cols = [c for c in numeric_cols if c != target_col]

        if len(numeric_cols) == 0:
            st.error("Tidak ada kolom numerik yang bisa digunakan sebagai fitur.")
            return

        X = df_model[numeric_cols].fillna(0)
        y = df_model[target_col]

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )

        # Scale
        scaler = StandardScaler()
        X_train_sc = scaler.fit_transform(X_train)
        X_test_sc  = scaler.transform(X_test)

        # Train model
        model = get_model(model_name)
        model.fit(X_train_sc, y_train)
        y_pred = model.predict(X_test_sc)
        y_prob = model.predict_proba(X_test_sc) if hasattr(model, "predict_proba") else None

        # ── METRICS KPI ─────────────────────────
        st.write("---")
        st.markdown(f"### 📊 Performa Model: **{model_name}**")

        acc  = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, average='weighted', zero_division=0)
        rec  = recall_score(y_test, y_pred, average='weighted', zero_division=0)
        f1   = f1_score(y_test, y_pred, average='weighted', zero_division=0)

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("🎯 Accuracy",  f"{acc:.2%}")
        m2.metric("🔎 Precision", f"{prec:.2%}")
        m3.metric("📡 Recall",    f"{rec:.2%}")
        m4.metric("⚖️ F1-Score",  f"{f1:.2%}")

        st.write("---")

        # ── TABS ────────────────────────────────
        tab1, tab2, tab3, tab4 = st.tabs([
            "🔮 Prediksi",
            "📉 Confusion Matrix",
            "📈 Learning Curve",
            "🌟 Feature Importance"
        ])

        # ── TAB 1: PREDIKSI ─────────────────────
        with tab1:
            st.markdown("### 🔮 Pipeline Prediksi")
            pred_mode = st.radio(
                "Pilih mode prediksi:",
                ["Upload CSV untuk Prediksi Massal", "Input Manual (Form)"],
                horizontal=True,
                key="pred_mode_tab"
            )

            if pred_mode == "Upload CSV untuk Prediksi Massal":
                st.info(f"Upload CSV dengan kolom: **{', '.join(numeric_cols)}**")
                pred_file = st.file_uploader("Upload CSV untuk diprediksi:", type=["csv"], key="pred_file")

                if pred_file:
                    df_pred = pd.read_csv(pred_file)
                    available_cols = [c for c in numeric_cols if c in df_pred.columns]

                    if len(available_cols) < len(numeric_cols):
                        st.warning(f"⚠️ Beberapa kolom tidak ditemukan. Menggunakan kolom: {available_cols}")

                    if len(available_cols) > 0:
                        X_new = df_pred[available_cols].fillna(0)
                        # Sesuaikan urutan kolom dengan training
                        for c in numeric_cols:
                            if c not in X_new.columns:
                                X_new[c] = 0
                        X_new = X_new[numeric_cols]
                        X_new_sc = scaler.transform(X_new)

                        if st.button("🚀 Jalankan Prediksi", type="primary", key="run_pred_btn"):
                            preds = model.predict(X_new_sc)
                            df_pred["Prediksi_Label"] = preds
                            if class_names:
                                df_pred["Prediksi_Kelas"] = [
                                    class_names[int(p)] if int(p) < len(class_names) else str(p)
                                    for p in preds
                                ]
                            st.success(f"✅ Prediksi selesai untuk {len(df_pred)} baris data!")
                            st.dataframe(df_pred, use_container_width=True)

                            # Download hasil
                            csv_out = df_pred.to_csv(index=False).encode("utf-8")
                            st.download_button(
                                "⬇️ Download Hasil Prediksi",
                                data=csv_out,
                                file_name="hasil_prediksi.csv",
                                mime="text/csv"
                            )

            else:
                st.markdown("**Masukkan nilai fitur secara manual:**")
                input_vals = {}
                cols_form = st.columns(min(3, len(numeric_cols)))
                for idx, feat in enumerate(numeric_cols):
                    with cols_form[idx % 3]:
                        mn = float(X[feat].min())
                        mx = float(X[feat].max())
                        me = float(X[feat].mean())
                        input_vals[feat] = st.number_input(feat, value=round(me, 4), key=f"inp_{feat}")

                if st.button("🚀 Prediksi Sekarang", type="primary", key="manual_pred_btn"):
                    X_input = pd.DataFrame([input_vals])
                    X_input_sc = scaler.transform(X_input)
                    result = model.predict(X_input_sc)[0]
                    label = class_names[int(result)] if class_names and int(result) < len(class_names) else str(result)

                    st.success(f"### 🎯 Hasil Prediksi: **{label}**")

                    if y_prob is not None:
                        prob_input = model.predict_proba(X_input_sc)[0]
                        prob_df = pd.DataFrame({
                            "Kelas": class_names[:len(prob_input)],
                            "Probabilitas": prob_input
                        }).sort_values("Probabilitas", ascending=False)

                        fig_prob = px.bar(
                            prob_df, x="Kelas", y="Probabilitas",
                            color="Probabilitas", color_continuous_scale="Blues",
                            title="Probabilitas per Kelas",
                            template="plotly_white"
                        )
                        fig_prob.update_layout(margin=dict(t=40, b=0))
                        st.plotly_chart(fig_prob, use_container_width=True)

        # ── TAB 2: CONFUSION MATRIX ─────────────
        with tab2:
            st.markdown("### 📉 Confusion Matrix")
            cm = confusion_matrix(y_test, y_pred)
            labels = class_names[:cm.shape[0]]

            fig_cm = ff.create_annotated_heatmap(
                z=cm,
                x=labels,
                y=labels,
                annotation_text=cm.astype(str),
                colorscale="Blues",
                showscale=True
            )
            fig_cm.update_layout(
                title="Confusion Matrix",
                xaxis_title="Predicted Label",
                yaxis_title="True Label",
                xaxis=dict(side="bottom"),
                template="plotly_white",
                margin=dict(t=60)
            )
            st.plotly_chart(fig_cm, use_container_width=True)

            st.markdown("### 📋 Classification Report")
            report_dict = classification_report(
                y_test, y_pred,
                target_names=class_names[:len(np.unique(y))],
                output_dict=True,
                zero_division=0
            )
            report_df = pd.DataFrame(report_dict).T.round(3)
            st.dataframe(report_df.style.background_gradient(cmap="Blues", subset=["precision", "recall", "f1-score"]),
                         use_container_width=True)

        # ── TAB 3: LEARNING CURVE ───────────────
        with tab3:
            st.markdown("### 📈 Learning Curve")
            st.info("Menunjukkan bagaimana performa model berkembang seiring bertambahnya data latih.")

            with st.spinner("Menghitung learning curve..."):
                train_sizes, train_scores, val_scores = learning_curve(
                    get_model(model_name),
                    X, y,
                    cv=5,
                    n_jobs=-1,
                    train_sizes=np.linspace(0.1, 1.0, 8),
                    scoring='accuracy'
                )

            train_mean = train_scores.mean(axis=1)
            val_mean   = val_scores.mean(axis=1)
            train_std  = train_scores.std(axis=1)
            val_std    = val_scores.std(axis=1)

            fig_lc = go.Figure()
            fig_lc.add_trace(go.Scatter(
                x=train_sizes, y=train_mean,
                mode='lines+markers', name='Training Score',
                line=dict(color='#4F46E5', width=2),
                error_y=dict(type='data', array=train_std, visible=True, color='rgba(79,70,229,0.3)')
            ))
            fig_lc.add_trace(go.Scatter(
                x=train_sizes, y=val_mean,
                mode='lines+markers', name='Validation Score',
                line=dict(color='#10B981', width=2),
                error_y=dict(type='data', array=val_std, visible=True, color='rgba(16,185,129,0.3)')
            ))
            fig_lc.update_layout(
                title=f"Learning Curve — {model_name}",
                xaxis_title="Jumlah Data Latih",
                yaxis_title="Accuracy",
                yaxis=dict(range=[0, 1.05]),
                template="plotly_white",
                legend=dict(x=0.01, y=0.01),
                margin=dict(t=50)
            )
            st.plotly_chart(fig_lc, use_container_width=True)

        # ── TAB 4: FEATURE IMPORTANCE ───────────
        with tab4:
            st.markdown("### 🌟 Feature Importance / Bobot Fitur")

            if model_name == "Random Forest":
                importances = model.feature_importances_
                fi_df = pd.DataFrame({
                    "Fitur": numeric_cols,
                    "Importance": importances
                }).sort_values("Importance", ascending=True)

                fig_fi = px.bar(
                    fi_df, x="Importance", y="Fitur",
                    orientation='h',
                    color="Importance",
                    color_continuous_scale="Viridis",
                    title="Feature Importance (Random Forest)",
                    template="plotly_white"
                )
                fig_fi.update_layout(margin=dict(t=50, l=0, r=0))
                st.plotly_chart(fig_fi, use_container_width=True)

            elif model_name == "Logistic Regression":
                coef = np.abs(model.coef_).mean(axis=0)
                fi_df = pd.DataFrame({
                    "Fitur": numeric_cols,
                    "Koefisien (abs)": coef
                }).sort_values("Koefisien (abs)", ascending=True)

                fig_fi = px.bar(
                    fi_df, x="Koefisien (abs)", y="Fitur",
                    orientation='h',
                    color="Koefisien (abs)",
                    color_continuous_scale="Blues",
                    title="Bobot Fitur (Logistic Regression)",
                    template="plotly_white"
                )
                fig_fi.update_layout(margin=dict(t=50, l=0, r=0))
                st.plotly_chart(fig_fi, use_container_width=True)

            else:
                st.info("💡 Feature importance tidak tersedia langsung untuk SVM. Gunakan **Random Forest** atau **Logistic Regression** untuk melihat feature importance.")

                # Tampilkan permutation-style info
                st.markdown("""
                **Alternatif untuk SVM:**
                - Gunakan metode **SHAP (SHapley Additive exPlanations)** untuk menjelaskan prediksi SVM.
                - Atau ganti model ke **Random Forest** untuk melihat feature importance secara langsung.
                """)
