import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import warnings
warnings.filterwarnings("ignore")

PLOTLY_DARK = "plotly_dark"

def _card(icon, label, value, color="#667eea"):
    return f"""<div style="background:linear-gradient(145deg,#1e293b,#0f172a);border-radius:14px;
    padding:1.1rem 1.3rem;border:1px solid {color}44;flex:1;min-width:130px;">
    <div style="font-size:1.3rem">{icon}</div>
    <div style="font-size:1.6rem;font-weight:800;color:#f1f5f9;font-family:'Plus Jakarta Sans',sans-serif">{value}</div>
    <div style="font-size:0.72rem;color:#94a3b8;text-transform:uppercase;letter-spacing:.5px">{label}</div>
    <div style="height:3px;border-radius:4px;margin-top:.7rem;background:linear-gradient(90deg,{color},transparent)"></div></div>"""

def _gen_sample_data():
    np.random.seed(42)
    dates = pd.date_range("2022-01-01", periods=365, freq="D")
    trend  = np.linspace(10000, 18000, 365)
    season = 3000 * np.sin(2 * np.pi * np.arange(365) / 30)
    noise  = np.random.normal(0, 800, 365)
    rev    = trend + season + noise
    qty    = (rev / np.random.uniform(80, 150, 365)).astype(int)
    return pd.DataFrame({"Date": dates, "Total_Revenue": np.round(rev, 2), "Qty_Orders": qty})

def show_timeseries_page():
    if st.button("⬅️ Kembali ke Daftar Project"):
        st.session_state.project_view = "grid"
        st.rerun()

    st.markdown("""
    <div style="background:linear-gradient(135deg,#14532d,#166534);border-radius:20px;
    padding:2rem 2.5rem;margin-bottom:1.5rem;border-left:5px solid #4ade80;">
        <div style="font-family:'Plus Jakarta Sans',sans-serif;font-size:1.8rem;font-weight:800;color:#fff;margin-bottom:.3rem">
            📈 E-Commerce Sales Forecasting — ARIMA</div>
        <div style="color:#bbf7d0;font-size:.95rem">
            Analisis tren penjualan harian/mingguan/bulanan dan forecasting menggunakan model ARIMA.</div>
    </div>""", unsafe_allow_html=True)

    # ── Sidebar ──────────────────────────────────────────────
    st.sidebar.markdown("## ⚙️ Konfigurasi Forecasting")
    forecast_days = st.sidebar.slider("Hari Forecast:", 7, 60, 30, key="ts_fdays")
    arima_p = st.sidebar.slider("ARIMA p (AR):", 0, 3, 1, key="ts_p")
    arima_q = st.sidebar.slider("ARIMA q (MA):", 0, 3, 1, key="ts_q")

    # ── Data source ──────────────────────────────────────────
    st.markdown("### 📂 Sumber Data")
    mode = st.radio("Pilih sumber data:",
                    ["Dataset Contoh (Synthetic E-Commerce)", "Upload CSV Sendiri"],
                    horizontal=True, key="ts_mode")

    df, date_col, val_col = None, None, None

    if mode == "Dataset Contoh (Synthetic E-Commerce)":
        df = _gen_sample_data()
        date_col = "Date"
        val_col  = "Total_Revenue"
        st.success(f"✅ Dataset sintetis e-commerce — {df.shape[0]} baris (365 hari 2022)")
        with st.expander("ℹ️ Info Dataset"):
            st.markdown("Dataset simulasi penjualan harian dengan **tren naik** + **pola musiman bulanan** + noise.")
    else:
        up = st.file_uploader("Upload CSV (harus ada kolom tanggal & numerik):", type=["csv"], key="ts_up")
        if up:
            df = pd.read_csv(up)
            st.success(f"✅ {df.shape[0]:,} baris, {df.shape[1]} kolom")
            date_col = st.selectbox("Kolom Tanggal:", df.columns.tolist(), key="ts_date")
            num_cols = df.select_dtypes(include=np.number).columns.tolist()
            val_col  = st.selectbox("Kolom Nilai (Revenue/Sales/etc):", num_cols, key="ts_val")

    if df is None:
        st.info("Pilih sumber data untuk memulai analisis.")
        return

    # ── Preprocess ───────────────────────────────────────────
    try:
        df[date_col] = pd.to_datetime(df[date_col])
        df = df.dropna(subset=[date_col, val_col]).sort_values(date_col).reset_index(drop=True)
    except Exception as e:
        st.error(f"Gagal memproses tanggal: {e}")
        return

    # Agregasi harian
    daily = df.groupby(date_col)[val_col].sum().reset_index()
    daily.columns = ["Date", "Revenue"]

    # ── KPI ───────────────────────────────────────────────────
    total   = daily["Revenue"].sum()
    avg_day = daily["Revenue"].mean()
    peak    = daily["Revenue"].max()
    n_days  = len(daily)

    st.markdown(f"""<div style="display:flex;gap:1rem;flex-wrap:wrap;margin-bottom:1.5rem">
        {_card("💰","Total Revenue", f"${total:,.0f}", "#10b981")}
        {_card("📅","Rata-rata/Hari", f"${avg_day:,.0f}", "#667eea")}
        {_card("🔝","Peak Revenue",  f"${peak:,.0f}",  "#f59e0b")}
        {_card("📆","Total Hari",    f"{n_days}",      "#8b5cf6")}
    </div>""", unsafe_allow_html=True)

    st.markdown("<hr style='border-color:rgba(99,102,241,0.2);margin:.5rem 0 1rem'>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📊 Analisis Tren", "🔮 Forecasting ARIMA", "📂 Data Mentah"])

    # TAB 1 — Tren ─────────────────────────────────────────
    with tab1:
        st.markdown("### 📊 Tren Penjualan")
        agg_opt = st.radio("Granularitas:", ["Harian", "Mingguan", "Bulanan"], horizontal=True, key="ts_agg")

        if agg_opt == "Harian":
            plot_df = daily.copy()
        elif agg_opt == "Mingguan":
            plot_df = daily.set_index("Date").resample("W")["Revenue"].sum().reset_index()
        else:
            plot_df = daily.set_index("Date").resample("M")["Revenue"].sum().reset_index()

        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            x=plot_df["Date"], y=plot_df["Revenue"],
            mode="lines+markers", name="Revenue",
            line=dict(color="#10b981", width=2),
            marker=dict(size=4)
        ))
        # 7-day MA
        if agg_opt == "Harian" and len(plot_df) > 7:
            ma7 = plot_df["Revenue"].rolling(7).mean()
            fig_trend.add_trace(go.Scatter(
                x=plot_df["Date"], y=ma7,
                mode="lines", name="7-Day MA",
                line=dict(color="#f59e0b", width=2, dash="dot")
            ))
        fig_trend.update_layout(
            title=f"Tren Revenue {agg_opt}",
            template=PLOTLY_DARK, height=380,
            paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#e2e8f0"),
            margin=dict(t=50,b=0), legend=dict(x=0.01, y=0.99)
        )
        st.plotly_chart(fig_trend, use_container_width=True)

        # Month & weekday breakdown if enough data
        if len(daily) > 30:
            daily["Month"]   = daily["Date"].dt.month_name()
            daily["Weekday"] = daily["Date"].dt.day_name()

            c1, c2 = st.columns(2)
            with c1:
                month_df = daily.groupby("Month")["Revenue"].sum().reset_index()
                month_order = ["January","February","March","April","May","June",
                               "July","August","September","October","November","December"]
                month_df["Month"] = pd.Categorical(month_df["Month"], categories=month_order, ordered=True)
                month_df = month_df.sort_values("Month")
                fig_m = px.bar(month_df, x="Month", y="Revenue", title="Revenue per Bulan",
                               template=PLOTLY_DARK, color="Revenue", color_continuous_scale="Viridis")
                fig_m.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#e2e8f0"),
                                    margin=dict(t=50,b=0), showlegend=False, xaxis=dict(tickangle=-30))
                st.plotly_chart(fig_m, use_container_width=True)

            with c2:
                day_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
                day_df = daily.groupby("Weekday")["Revenue"].mean().reset_index()
                day_df["Weekday"] = pd.Categorical(day_df["Weekday"], categories=day_order, ordered=True)
                day_df = day_df.sort_values("Weekday")
                fig_d = px.bar(day_df, x="Weekday", y="Revenue", title="Avg Revenue per Hari",
                               template=PLOTLY_DARK, color="Revenue", color_continuous_scale="Plasma")
                fig_d.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#e2e8f0"),
                                    margin=dict(t=50,b=0), showlegend=False)
                st.plotly_chart(fig_d, use_container_width=True)

    # TAB 2 — ARIMA ─────────────────────────────────────────
    with tab2:
        st.markdown("### 🔮 Forecasting dengan ARIMA")

        try:
            from statsmodels.tsa.arima.model import ARIMA
            from statsmodels.tsa.stattools import adfuller
        except ImportError:
            st.error("❌ `statsmodels` belum terinstall. Jalankan: `pip install statsmodels`")
            return

        ts_series = daily.set_index("Date")["Revenue"]

        # ADF Test
        adf_res = adfuller(ts_series.dropna())
        p_val   = adf_res[1]
        is_stationary = p_val < 0.05

        st.markdown(f"""
        <div style="background:{'rgba(16,185,129,0.1)' if is_stationary else 'rgba(245,158,11,0.1)'};
        border:1px solid {'rgba(16,185,129,0.4)' if is_stationary else 'rgba(245,158,11,0.4)'};
        border-radius:10px;padding:.8rem 1rem;color:{'#6ee7b7' if is_stationary else '#fde68a'};
        font-size:.875rem;margin-bottom:1rem;">
            📊 <strong>Uji ADF (Augmented Dickey-Fuller):</strong> p-value = {p_val:.4f} —
            {'✅ Data STASIONER (p &lt; 0.05)' if is_stationary else '⚠️ Data TIDAK STASIONER — akan diterapkan differencing (d=1)'}
        </div>""", unsafe_allow_html=True)

        d_val = 0 if is_stationary else 1

        with st.spinner("⏳ Melatih model ARIMA..."):
            try:
                model = ARIMA(ts_series, order=(arima_p, d_val, arima_q))
                result = model.fit()

                # Forecast
                forecast_obj  = result.get_forecast(steps=forecast_days)
                forecast_mean = forecast_obj.predicted_mean
                conf_int      = forecast_obj.conf_int()

                future_dates = pd.date_range(
                    start=ts_series.index[-1] + pd.Timedelta(days=1),
                    periods=forecast_days
                )

                # Plot
                fig_fc = go.Figure()
                # Actual (last 90 days)
                recent = ts_series.iloc[-90:]
                fig_fc.add_trace(go.Scatter(
                    x=recent.index, y=recent.values,
                    mode="lines", name="Actual",
                    line=dict(color="#10b981", width=2)
                ))
                # Forecast
                fig_fc.add_trace(go.Scatter(
                    x=future_dates, y=forecast_mean.values,
                    mode="lines+markers", name="Forecast",
                    line=dict(color="#f59e0b", width=2),
                    marker=dict(size=4)
                ))
                # CI band
                fig_fc.add_trace(go.Scatter(
                    x=list(future_dates) + list(future_dates[::-1]),
                    y=list(conf_int.iloc[:, 1]) + list(conf_int.iloc[:, 0][::-1]),
                    fill="toself", fillcolor="rgba(245,158,11,0.1)",
                    line=dict(color="rgba(0,0,0,0)"), name="95% CI"
                ))
                fig_fc.update_layout(
                    title=f"ARIMA({arima_p},{d_val},{arima_q}) — Forecast {forecast_days} Hari",
                    template=PLOTLY_DARK, height=420,
                    paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#e2e8f0"),
                    margin=dict(t=50,b=0), legend=dict(x=0.01, y=0.99)
                )
                st.plotly_chart(fig_fc, use_container_width=True)

                # Forecast table
                fc_df = pd.DataFrame({
                    "Tanggal":      future_dates.strftime("%Y-%m-%d"),
                    "Forecast Revenue": np.round(forecast_mean.values, 2),
                    "Lower 95% CI": np.round(conf_int.iloc[:, 0].values, 2),
                    "Upper 95% CI": np.round(conf_int.iloc[:, 1].values, 2),
                })
                st.markdown("#### 📋 Tabel Hasil Forecast")
                st.dataframe(fc_df, use_container_width=True, height=300)

                csv_fc = fc_df.to_csv(index=False).encode("utf-8")
                st.download_button("⬇️ Download Hasil Forecast", csv_fc,
                                   "forecast_arima.csv", "text/csv")

                # Model info
                with st.expander("📑 Detail Model ARIMA (Summary)"):
                    st.text(result.summary().as_text())

            except Exception as e:
                st.error(f"❌ Gagal melatih ARIMA: {e}")
                st.info("Coba ubah parameter p dan q di sidebar.")

    # TAB 3 — Data ─────────────────────────────────────────
    with tab3:
        st.markdown("### 📂 Data Harian")
        st.dataframe(daily.sort_values("Date", ascending=False), use_container_width=True, height=400)
