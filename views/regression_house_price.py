import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.metrics import mean_absolute_error, mean_squared_error
import warnings
warnings.filterwarnings("ignore")

PLOTLY_DARK = "plotly_dark"
COLORS = ["#667eea", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6"]

def rmse(y_true, y_pred):
    return np.sqrt(mean_squared_error(y_true, y_pred))

def mape(y_true, y_pred):
    return np.mean(np.abs((y_true - y_pred) / (y_true + 1e-8))) * 100

def _card(icon, label, value, color="#667eea"):
    return f"""<div style="background:linear-gradient(145deg,#1e293b,#0f172a);border-radius:14px;
    padding:1.1rem 1.3rem;border:1px solid {color}44;flex:1;min-width:130px;">
    <div style="font-size:1.3rem">{icon}</div>
    <div style="font-size:1.6rem;font-weight:800;color:#f1f5f9;font-family:'Plus Jakarta Sans',sans-serif">{value}</div>
    <div style="font-size:0.72rem;color:#94a3b8;text-transform:uppercase;letter-spacing:.5px">{label}</div>
    <div style="height:3px;border-radius:4px;margin-top:.7rem;background:linear-gradient(90deg,{color},transparent)"></div></div>"""

def show_regression_page():
    if st.button("⬅️ Kembali ke Daftar Project"):
        st.session_state.project_view = "grid"
        st.rerun()

    st.markdown("""
    <div style="background:linear-gradient(135deg,#1e3a5f,#2d6a9f);border-radius:20px;
    padding:2rem 2.5rem;margin-bottom:1.5rem;border-left:5px solid #60a5fa;">
        <div style="font-family:'Plus Jakarta Sans',sans-serif;font-size:1.8rem;font-weight:800;color:#fff;margin-bottom:.3rem">
            🏠 House Price Prediction — Ridge & Lasso Regression</div>
        <div style="color:#bfdbfe;font-size:.95rem">
            Prediksi harga rumah menggunakan Linear, Ridge, dan Lasso Regression dengan perbandingan alpha terbaik.</div>
    </div>""", unsafe_allow_html=True)

    # ── Sidebar config ───────────────────────────────────────
    st.sidebar.markdown("## ⚙️ Konfigurasi Model")
    test_size  = st.sidebar.slider("Test Size (%)", 10, 40, 20, key="reg_ts") / 100
    alphas_sel = st.sidebar.multiselect("Alpha candidates:", [0.01, 0.1, 1, 10, 100],
                                        default=[0.01, 0.1, 1, 10, 100], key="reg_alphas")
    if not alphas_sel:
        alphas_sel = [0.01, 0.1, 1, 10, 100]

    # ── Data source ──────────────────────────────────────────
    st.markdown("### 📂 Sumber Data")
    mode = st.radio("Pilih sumber data:", ["Dataset Contoh (California Housing)", "Upload CSV Sendiri"],
                    horizontal=True, key="reg_mode")

    df, target_col, feature_cols = None, None, None

    if mode == "Dataset Contoh (California Housing)":
        raw = fetch_california_housing()
        df  = pd.DataFrame(raw.data, columns=raw.feature_names)
        df["MedHouseVal"] = raw.target
        target_col   = "MedHouseVal"
        feature_cols = list(raw.feature_names)
        st.success(f"✅ California Housing Dataset — {df.shape[0]:,} baris, {df.shape[1]} kolom")
        with st.expander("ℹ️ Info Kolom"):
            st.markdown("""
            | Kolom | Keterangan |
            |---|---|
            | MedInc | Median income (per $10k) |
            | HouseAge | Median house age |
            | AveRooms | Rata-rata jumlah kamar |
            | AveBedrms | Rata-rata jumlah kamar tidur |
            | Population | Jumlah populasi |
            | AveOccup | Rata-rata penghuni |
            | Latitude / Longitude | Koordinat lokasi |
            | **MedHouseVal** | 🎯 **Target: Median house value ($100k)** |
            """)
    else:
        up = st.file_uploader("Upload CSV:", type=["csv"], key="reg_up")
        if up:
            df = pd.read_csv(up)
            st.success(f"✅ {df.shape[0]:,} baris, {df.shape[1]} kolom")
            num_cols = df.select_dtypes(include=np.number).columns.tolist()
            target_col   = st.selectbox("Pilih kolom Target:", num_cols, key="reg_tgt")
            feature_cols = st.multiselect("Pilih kolom Fitur:", [c for c in num_cols if c != target_col],
                                          default=[c for c in num_cols if c != target_col][:6], key="reg_feat")

    if df is None or target_col is None or not feature_cols:
        st.info("Pilih sumber data dan kolom untuk memulai.")
        return

    # ── Prepare ──────────────────────────────────────────────
    df_clean = df[feature_cols + [target_col]].dropna()
    X = df_clean[feature_cols]
    y = df_clean[target_col]

    X_tr, X_tmp, y_tr, y_tmp = train_test_split(X, y, test_size=test_size + 0.15, random_state=42)
    X_val, X_te, y_val, y_te = train_test_split(X_tmp, y_tmp, test_size=0.5, random_state=42)

    sc = StandardScaler()
    X_tr_s  = sc.fit_transform(X_tr)
    X_val_s = sc.transform(X_val)
    X_te_s  = sc.transform(X_te)

    # ── Train ─────────────────────────────────────────────────
    lr = LinearRegression().fit(X_tr_s, y_tr)

    ridge_res = [{"alpha": a, "RMSE": rmse(y_val, Ridge(alpha=a).fit(X_tr_s, y_tr).predict(X_val_s))} for a in alphas_sel]
    ridge_df  = pd.DataFrame(ridge_res)
    best_ra   = ridge_df.loc[ridge_df.RMSE.idxmin(), "alpha"]
    ridge_best = Ridge(alpha=best_ra).fit(X_tr_s, y_tr)

    lasso_res = [{"alpha": a, "RMSE": rmse(y_val, Lasso(alpha=a, max_iter=5000).fit(X_tr_s, y_tr).predict(X_val_s))} for a in alphas_sel]
    lasso_df  = pd.DataFrame(lasso_res)
    best_la   = lasso_df.loc[lasso_df.RMSE.idxmin(), "alpha"]
    lasso_best = Lasso(alpha=best_la, max_iter=5000).fit(X_tr_s, y_tr)

    models = {
        "Linear Regression": lr,
        f"Ridge (α={best_ra})": ridge_best,
        f"Lasso (α={best_la})": lasso_best,
    }

    results = {}
    for name, m in models.items():
        yp = m.predict(X_te_s)
        results[name] = {"RMSE": rmse(y_te, yp), "MAE": mean_absolute_error(y_te, yp), "MAPE": mape(y_te, yp)}

    best_name = min(results, key=lambda k: results[k]["RMSE"])
    best_res  = results[best_name]

    # ── KPI ───────────────────────────────────────────────────
    st.markdown("### 🏆 Performa Model Terbaik: **" + best_name + "**")
    st.markdown(f"""<div style="display:flex;gap:1rem;flex-wrap:wrap;margin-bottom:1.5rem">
        {_card("🎯","RMSE", f"{best_res['RMSE']:.4f}", "#667eea")}
        {_card("📏","MAE",  f"{best_res['MAE']:.4f}",  "#10b981")}
        {_card("📊","MAPE", f"{best_res['MAPE']:.2f}%","#f59e0b")}
        {_card("📋","Test samples", f"{len(y_te):,}",   "#8b5cf6")}
    </div>""", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 EDA", "📉 Alpha Tuning", "🏆 Evaluasi Model",
                                             "🌟 Koefisien Fitur", "🔮 Prediksi"])

    # TAB 1 — EDA
    with tab1:
        st.markdown("### Distribusi & Korelasi")
        col1, col2 = st.columns(2)
        with col1:
            feat_sel = st.selectbox("Pilih fitur:", feature_cols, key="reg_eda_feat")
            fig_h = px.histogram(df_clean, x=feat_sel, nbins=30, title=f"Distribusi {feat_sel}",
                                 template=PLOTLY_DARK, color_discrete_sequence=["#667eea"], marginal="violin")
            fig_h.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#e2e8f0"), margin=dict(t=50,b=0))
            st.plotly_chart(fig_h, use_container_width=True)
        with col2:
            fig_sc = px.scatter(df_clean, x=feat_sel, y=target_col,
                                title=f"{feat_sel} vs {target_col}", template=PLOTLY_DARK,
                                color_discrete_sequence=["#10b981"], opacity=0.5)
            fig_sc.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#e2e8f0"), margin=dict(t=50,b=0))
            st.plotly_chart(fig_sc, use_container_width=True)

        corr = df_clean.corr().round(2)
        fig_heat = go.Figure(go.Heatmap(z=corr.values, x=corr.columns.tolist(), y=corr.index.tolist(),
                                         text=corr.values, texttemplate="<b>%{text}</b>",
                                         colorscale="RdBu", zmid=0, zmin=-1, zmax=1))
        fig_heat.update_layout(title="Correlation Heatmap", template=PLOTLY_DARK, height=450,
                                paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#e2e8f0"),
                                margin=dict(t=50,l=0,r=0,b=0), xaxis=dict(tickangle=-30))
        st.plotly_chart(fig_heat, use_container_width=True)

    # TAB 2 — Alpha Tuning
    with tab2:
        st.markdown("### RMSE vs Alpha (Validation Set)")
        r1, r2 = st.columns(2)
        with r1:
            fig_r = px.line(ridge_df, x="alpha", y="RMSE", markers=True,
                            title="Ridge: RMSE vs Alpha", log_x=True, template=PLOTLY_DARK,
                            color_discrete_sequence=["#667eea"])
            fig_r.add_vline(x=best_ra, line_dash="dash", line_color="#f59e0b",
                            annotation_text=f"Best α={best_ra}", annotation_font_color="#f59e0b")
            fig_r.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#e2e8f0"), margin=dict(t=50,b=0))
            st.plotly_chart(fig_r, use_container_width=True)
        with r2:
            fig_l = px.line(lasso_df, x="alpha", y="RMSE", markers=True,
                            title="Lasso: RMSE vs Alpha", log_x=True, template=PLOTLY_DARK,
                            color_discrete_sequence=["#10b981"])
            fig_l.add_vline(x=best_la, line_dash="dash", line_color="#f59e0b",
                            annotation_text=f"Best α={best_la}", annotation_font_color="#f59e0b")
            fig_l.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#e2e8f0"), margin=dict(t=50,b=0))
            st.plotly_chart(fig_l, use_container_width=True)

    # TAB 3 — Evaluasi
    with tab3:
        st.markdown("### Perbandingan Metrik Evaluasi")
        res_df = pd.DataFrame(results).T.reset_index().rename(columns={"index":"Model"})
        for metric, color in [("RMSE","#667eea"), ("MAE","#10b981"), ("MAPE","#f59e0b")]:
            fig_m = px.bar(res_df, x="Model", y=metric, color="Model", title=f"Perbandingan {metric}",
                           template=PLOTLY_DARK, color_discrete_sequence=COLORS, text_auto=".4f")
            fig_m.update_layout(showlegend=False, paper_bgcolor="rgba(0,0,0,0)",
                                font=dict(color="#e2e8f0"), margin=dict(t=50,b=0))
            st.plotly_chart(fig_m, use_container_width=True)

        # Actual vs Predicted
        best_model_obj = models[best_name]
        y_pred_best = best_model_obj.predict(X_te_s)
        fig_avp = px.scatter(x=y_te, y=y_pred_best, labels={"x":"Actual","y":"Predicted"},
                             title=f"Actual vs Predicted — {best_name}", template=PLOTLY_DARK,
                             color_discrete_sequence=["#667eea"], opacity=0.6)
        mn, mx = float(y_te.min()), float(y_te.max())
        fig_avp.add_shape(type="line", x0=mn, y0=mn, x1=mx, y1=mx,
                          line=dict(color="#f59e0b", dash="dash", width=2))
        fig_avp.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#e2e8f0"), margin=dict(t=50,b=0))
        st.plotly_chart(fig_avp, use_container_width=True)

    # TAB 4 — Koefisien
    with tab4:
        st.markdown("### Perbandingan Koefisien Model")
        coef_df = pd.DataFrame({
            "Feature":          feature_cols,
            "Linear Regression": lr.coef_,
            f"Ridge (α={best_ra})": ridge_best.coef_,
            f"Lasso (α={best_la})": lasso_best.coef_,
        })
        st.dataframe(coef_df.set_index("Feature").style.background_gradient(cmap="RdYlGn", axis=1),
                     use_container_width=True)

        model_coef = st.selectbox("Visualisasi koefisien model:", list(models.keys()), key="reg_coef_sel")
        coef_vals = models[model_coef].coef_
        fi_df = pd.DataFrame({"Fitur": feature_cols, "Koefisien": coef_vals}).sort_values("Koefisien")
        fig_fi = px.bar(fi_df, x="Koefisien", y="Fitur", orientation="h",
                        title=f"Koefisien — {model_coef}", template=PLOTLY_DARK,
                        color="Koefisien", color_continuous_scale="RdBu")
        fig_fi.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#e2e8f0"), margin=dict(t=50,b=0))
        st.plotly_chart(fig_fi, use_container_width=True)

    # TAB 5 — Prediksi manual
    with tab5:
        st.markdown("### 🔮 Input Manual — Coba Prediksi Sendiri")
        inp = {}
        cols_form = st.columns(min(4, len(feature_cols)))
        for i, feat in enumerate(feature_cols):
            with cols_form[i % 4]:
                mn_v, mx_v, me_v = float(X[feat].min()), float(X[feat].max()), float(X[feat].mean())
                inp[feat] = st.number_input(feat, value=round(me_v, 3), key=f"reg_inp_{feat}")

        if st.button("🚀 Prediksi Harga", type="primary", key="reg_pred_btn"):
            X_inp = pd.DataFrame([inp])
            X_inp_s = sc.transform(X_inp)
            preds = {name: float(m.predict(X_inp_s)[0]) for name, m in models.items()}
            avg = np.mean(list(preds.values()))

            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#065f46,#047857);border-radius:16px;
            padding:1.5rem 2rem;text-align:center;border:1px solid rgba(16,185,129,.4);
            box-shadow:0 4px 20px rgba(16,185,129,.2);margin:1rem 0;">
                <div style="font-size:.85rem;color:#6ee7b7;text-transform:uppercase;letter-spacing:1px">Prediksi Rata-rata</div>
                <div style="font-size:2.5rem;font-weight:800;color:#fff;font-family:'Plus Jakarta Sans',sans-serif">{avg:.4f}</div>
            </div>""", unsafe_allow_html=True)

            for name, val in preds.items():
                st.markdown(f"**{name}:** `{val:.4f}`")
