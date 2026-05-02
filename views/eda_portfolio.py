import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go


# ──────────────────────────────────────────────────────────────
# PLOTLY THEME
# ──────────────────────────────────────────────────────────────
PLOTLY_TEMPLATE = "plotly_dark"
COLOR_SEQ       = px.colors.qualitative.Vivid
GRADIENT_COLORS = ["#667eea", "#764ba2", "#f093fb", "#10b981", "#f59e0b"]


def _metric_card(icon, label, value, color="#667eea"):
    return f"""
    <div style="background:linear-gradient(145deg,#1e293b,#0f172a);
                border-radius:16px; padding:1.2rem 1.4rem;
                border:1px solid {color}44; flex:1; min-width:140px;
                box-shadow:0 4px 20px rgba(0,0,0,0.2);">
        <div style="font-size:1.4rem; margin-bottom:0.3rem;">{icon}</div>
        <div style="font-family:'Plus Jakarta Sans',sans-serif; font-size:1.7rem;
                    font-weight:800; color:#f1f5f9; line-height:1;">{value}</div>
        <div style="font-size:0.75rem; color:#94a3b8; margin-top:0.3rem;
                    text-transform:uppercase; letter-spacing:0.5px;">{label}</div>
        <div style="height:3px; border-radius:4px; margin-top:0.8rem;
                    background:linear-gradient(90deg,{color},transparent);"></div>
    </div>
    """


def show_eda_page():

    # ── Back button ──────────────────────────────────────────
    if st.button("⬅️ Kembali ke Daftar Project"):
        st.session_state.project_view = 'grid'
        st.rerun()

    # ── Page Header ──────────────────────────────────────────
    st.markdown("""
    <div style="background:linear-gradient(135deg,#1e3a5f 0%,#2d6a9f 100%);
                border-radius:20px; padding:2rem 2.5rem; margin-bottom:1.5rem;
                border-left:5px solid #60a5fa; position:relative; overflow:hidden;">
        <div style="position:absolute;top:-30px;right:-30px;width:120px;height:120px;
                    background:radial-gradient(circle,rgba(96,165,250,0.2),transparent);
                    border-radius:50%;"></div>
        <div style="font-family:'Plus Jakarta Sans',sans-serif; font-size:1.8rem;
                    font-weight:800; color:#ffffff; margin-bottom:0.3rem;">
            📊 Exploratory Data Analysis
        </div>
        <div style="color:#bfdbfe; font-size:0.95rem;">
            Dashboard interaktif untuk menganalisis dan menggali wawasan tersembunyi dari dataset Anda.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Data Source ──────────────────────────────────────────
    with st.expander("⚙️ Pengaturan Sumber Data", expanded=True):
        mode_data = st.radio(
            "Pilih Sumber Data:",
            ("Gunakan Data Contoh", "Upload Dataset CSV Sendiri"),
            horizontal=True,
            key="eda_mode"
        )

        df = None

        if mode_data == "Gunakan Data Contoh":
            np.random.seed(42)
            n = 150
            df = pd.DataFrame({
                "Bulan":      np.random.choice(
                    ["Jan","Feb","Mar","Apr","Mei","Jun","Jul","Agt","Sep","Okt","Nov","Des"], n),
                "Kategori":   np.random.choice(
                    ["Elektronik","Pakaian","Makanan","Furnitur","Olahraga"], n),
                "Total_Sales": np.random.randint(500,  5000, n),
                "Profit":      np.random.randint(50,   1200, n),
                "Rating":      np.round(np.random.uniform(3.0, 5.0, n), 1),
                "Quantity":    np.random.randint(1, 50, n),
            })
            st.markdown("""
            <div style="background:rgba(99,102,241,0.1); border:1px solid rgba(99,102,241,0.3);
                        border-radius:10px; padding:0.8rem 1rem; color:#a5b4fc; font-size:0.875rem;">
                💡 Menggunakan dataset <strong>contoh penjualan toko</strong>
                (150 baris, 6 kolom). Upload CSV Anda sendiri untuk analisis nyata.
            </div>
            """, unsafe_allow_html=True)

        else:
            uploaded_file = st.file_uploader("Upload file CSV:", type=["csv"], key="eda_upload")
            if uploaded_file:
                try:
                    df = pd.read_csv(uploaded_file)
                    st.success(f"✅ File berhasil diunggah — **{df.shape[0]}** baris, **{df.shape[1]}** kolom")
                except Exception as e:
                    st.error(f"Gagal membaca file: {e}")

    # ── Main Dashboard ───────────────────────────────────────
    if df is None:
        st.markdown("""
        <div style="text-align:center; padding:3rem; color:#64748b;">
            <div style="font-size:3rem; margin-bottom:1rem;">📂</div>
            <div style="font-size:1rem;">Pilih sumber data di atas untuk memulai analisis.</div>
        </div>
        """, unsafe_allow_html=True)
        return

    kolom_num = df.select_dtypes(include=["int64","float64"]).columns.tolist()
    kolom_kat = df.select_dtypes(include=["object","category"]).columns.tolist()

    # ── KPI Cards ────────────────────────────────────────────
    missing = int(df.isna().sum().sum())
    dup     = int(df.duplicated().sum())

    cards_html = f"""
    <div style="display:flex; gap:1rem; flex-wrap:wrap; margin-bottom:1.5rem;">
        {_metric_card("📋", "Total Baris", f"{df.shape[0]:,}", "#667eea")}
        {_metric_card("📐", "Total Kolom", f"{df.shape[1]}", "#10b981")}
        {_metric_card("❓", "Missing Values", f"{missing:,}", "#f59e0b")}
        {_metric_card("♻️", "Duplikat", f"{dup}", "#ef4444")}
    </div>
    """
    st.markdown(cards_html, unsafe_allow_html=True)

    if kolom_num:
        num_cards = "".join([
            _metric_card("📊", f"Total {c}",
                         f"{df[c].sum():,.0f}" if df[c].sum() >= 1000
                         else f"{df[c].sum():,.1f}", "#8b5cf6")
            for c in kolom_num[:2]
        ])
        st.markdown(f"""
        <div style="display:flex; gap:1rem; flex-wrap:wrap; margin-bottom:1.5rem;">
            {num_cards}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr style='border-color:rgba(99,102,241,0.2); margin:0.5rem 0 1rem 0;'>",
                unsafe_allow_html=True)

    # ── Tabs ─────────────────────────────────────────────────
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Visualisasi Data",
        "📉 Distribusi Fitur",
        "🔥 Korelasi Heatmap",
        "🔍 Statistik Deskriptif",
        "📂 Data Mentah",
    ])

    # ═══════════════════════════════════════════
    # TAB 1 — Visualisasi Data
    # ═══════════════════════════════════════════
    with tab1:
        st.markdown("### 📊 Eksplorasi Visual Interaktif")

        if kolom_kat and kolom_num:
            c1, c2 = st.columns(2)
            with c1:
                kat_p = st.selectbox("Dimensi (Sumbu X / Kategori):", kolom_kat, key="t1_kat")
            with c2:
                num_p = st.selectbox("Metrik (Sumbu Y):",             kolom_num, key="t1_num")

            agg_df = df.groupby(kat_p)[num_p].sum().reset_index().sort_values(num_p, ascending=False)

            col_bar, col_pie = st.columns([3, 2])

            with col_bar:
                fig_bar = px.bar(
                    agg_df, x=kat_p, y=num_p, color=kat_p,
                    title=f"Total <b>{num_p}</b> per <b>{kat_p}</b>",
                    template=PLOTLY_TEMPLATE,
                    color_discrete_sequence=COLOR_SEQ,
                    text_auto=".2s"
                )
                fig_bar.update_layout(
                    showlegend=False, margin=dict(l=0, r=0, t=50, b=0),
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#e2e8f0")
                )
                fig_bar.update_traces(textfont_size=10, textposition="outside")
                st.plotly_chart(fig_bar, use_container_width=True)

            with col_pie:
                if df[kat_p].nunique() <= 12:
                    fig_pie = px.pie(
                        agg_df, names=kat_p, values=num_p,
                        title=f"Proporsi <b>{kat_p}</b>", hole=0.5,
                        template=PLOTLY_TEMPLATE,
                        color_discrete_sequence=COLOR_SEQ,
                    )
                    fig_pie.update_layout(
                        margin=dict(l=0, r=0, t=50, b=0),
                        paper_bgcolor="rgba(0,0,0,0)",
                        font=dict(color="#e2e8f0"),
                        legend=dict(font=dict(size=10))
                    )
                    st.plotly_chart(fig_pie, use_container_width=True)

            # Line chart if time-like column exists
            if len(kolom_num) >= 2:
                st.markdown("#### 📈 Tren Komparasi Numerik")
                num2 = st.multiselect("Pilih kolom numerik:", kolom_num,
                                      default=kolom_num[:2], key="t1_line")
                if num2:
                    fig_line = px.line(
                        df.reset_index(), y=num2,
                        title="Tren Data Numerik",
                        template=PLOTLY_TEMPLATE,
                        color_discrete_sequence=GRADIENT_COLORS,
                        markers=True
                    )
                    fig_line.update_layout(
                        margin=dict(l=0, r=0, t=50, b=0),
                        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                        font=dict(color="#e2e8f0")
                    )
                    st.plotly_chart(fig_line, use_container_width=True)
        elif kolom_num:
            st.line_chart(df[kolom_num])
        else:
            st.info("Tidak cukup data untuk visualisasi.")

    # ═══════════════════════════════════════════
    # TAB 2 — Distribusi Fitur
    # ═══════════════════════════════════════════
    with tab2:
        st.markdown("### 📉 Distribusi & Outlier Analysis")

        if not kolom_num:
            st.info("Tidak ada kolom numerik.")
        else:
            feat = st.selectbox("Pilih fitur:", kolom_num, key="t2_feat")

            # Histogram + Box side by side
            col_h, col_b = st.columns(2)
            with col_h:
                fig_hist = px.histogram(
                    df, x=feat, nbins=25,
                    title=f"Distribusi — <b>{feat}</b>",
                    template=PLOTLY_TEMPLATE,
                    color_discrete_sequence=["#667eea"],
                    marginal="violin",
                    opacity=0.85
                )
                fig_hist.update_layout(
                    margin=dict(l=0, r=0, t=50, b=0),
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#e2e8f0")
                )
                st.plotly_chart(fig_hist, use_container_width=True)

            with col_b:
                if kolom_kat:
                    grp = st.selectbox("Kelompokkan:", kolom_kat, key="t2_grp")
                    fig_box = px.box(
                        df, x=grp, y=feat, color=grp,
                        title=f"Box Plot <b>{feat}</b> per <b>{grp}</b>",
                        template=PLOTLY_TEMPLATE,
                        color_discrete_sequence=COLOR_SEQ,
                        points="outliers"
                    )
                else:
                    fig_box = px.box(
                        df, y=feat,
                        title=f"Box Plot — <b>{feat}</b>",
                        template=PLOTLY_TEMPLATE,
                        color_discrete_sequence=["#10b981"]
                    )
                fig_box.update_layout(
                    showlegend=False, margin=dict(l=0, r=0, t=50, b=0),
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#e2e8f0")
                )
                st.plotly_chart(fig_box, use_container_width=True)

            # Scatter Plot
            if len(kolom_num) >= 2:
                st.markdown("#### 🔵 Scatter Plot — Hubungan Antar Fitur")
                sc1, sc2, sc3 = st.columns(3)
                with sc1: x_f = st.selectbox("Fitur X:", kolom_num, index=0, key="t2_scx")
                with sc2: y_f = st.selectbox("Fitur Y:", kolom_num,
                                              index=min(1, len(kolom_num)-1), key="t2_scy")
                with sc3: col_f = st.selectbox("Warna:", ["—"] + kolom_kat, key="t2_scc")

                try:
                    fig_sc = px.scatter(
                        df, x=x_f, y=y_f,
                        color=col_f if col_f != "—" else None,
                        title=f"<b>{x_f}</b> vs <b>{y_f}</b>",
                        template=PLOTLY_TEMPLATE,
                        trendline="ols",
                        color_discrete_sequence=COLOR_SEQ,
                        opacity=0.8
                    )
                except Exception:
                    # Fallback jika statsmodels belum terinstall
                    fig_sc = px.scatter(
                        df, x=x_f, y=y_f,
                        color=col_f if col_f != "—" else None,
                        title=f"<b>{x_f}</b> vs <b>{y_f}</b>",
                        template=PLOTLY_TEMPLATE,
                        color_discrete_sequence=COLOR_SEQ,
                        opacity=0.8
                    )
                fig_sc.update_layout(
                    margin=dict(l=0, r=0, t=50, b=0),
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#e2e8f0")
                )
                st.plotly_chart(fig_sc, use_container_width=True)

    # ═══════════════════════════════════════════
    # TAB 3 — Korelasi Heatmap
    # ═══════════════════════════════════════════
    with tab3:
        st.markdown("### 🔥 Correlation Heatmap")
        st.markdown("""
        <div style="background:rgba(99,102,241,0.1); border:1px solid rgba(99,102,241,0.3);
                    border-radius:10px; padding:0.8rem 1rem; color:#a5b4fc;
                    font-size:0.875rem; margin-bottom:1rem;">
            Nilai mendekati <strong>+1</strong> = korelasi positif kuat &nbsp;|&nbsp;
            Nilai mendekati <strong>-1</strong> = korelasi negatif kuat &nbsp;|&nbsp;
            <strong>0</strong> = tidak berkorelasi
        </div>
        """, unsafe_allow_html=True)

        if len(kolom_num) < 2:
            st.info("Dibutuhkan minimal 2 kolom numerik.")
        else:
            corr = df[kolom_num].corr().round(2)

            fig_heat = go.Figure(data=go.Heatmap(
                z=corr.values,
                x=corr.columns.tolist(),
                y=corr.index.tolist(),
                text=corr.values,
                texttemplate="<b>%{text}</b>",
                textfont=dict(size=11),
                colorscale="RdBu",
                zmid=0, zmin=-1, zmax=1,
                colorbar=dict(title="r", tickfont=dict(color="#e2e8f0")),
                hoverongaps=False,
            ))
            fig_heat.update_layout(
                title=dict(text="Correlation Matrix", font=dict(color="#f1f5f9", size=16)),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#e2e8f0"),
                height=480,
                margin=dict(t=60, l=0, r=0, b=0),
                xaxis=dict(tickangle=-30, color="#e2e8f0"),
                yaxis=dict(color="#e2e8f0"),
            )
            st.plotly_chart(fig_heat, use_container_width=True)

            # Top corr pairs
            st.markdown("#### 🏆 Top Pasangan Fitur Paling Berkorelasi")
            mask = np.triu(np.ones(corr.shape), k=1).astype(bool)
            pairs = (corr.where(mask).stack().reset_index()
                         .rename(columns={"level_0":"Fitur A","level_1":"Fitur B",0:"Korelasi"}))
            pairs["Abs"] = pairs["Korelasi"].abs()
            top5 = pairs.sort_values("Abs", ascending=False).head(5).drop("Abs", axis=1)
            top5 = top5.reset_index(drop=True)

            # Visual table
            for _, row in top5.iterrows():
                r  = row["Korelasi"]
                color = "#10b981" if r > 0 else "#ef4444"
                bar_w = int(abs(r) * 100)
                st.markdown(f"""
                <div style="display:flex; align-items:center; gap:1rem;
                            background:#1e293b; border-radius:10px; padding:0.7rem 1rem;
                            margin-bottom:0.5rem; border:1px solid rgba(99,102,241,0.15);">
                    <div style="min-width:120px; font-size:0.8rem;
                                color:#94a3b8;">{row['Fitur A']}</div>
                    <div style="font-size:0.7rem; color:#64748b;">↔</div>
                    <div style="min-width:120px; font-size:0.8rem;
                                color:#94a3b8;">{row['Fitur B']}</div>
                    <div style="flex:1; background:#0f172a; border-radius:5px; height:8px; overflow:hidden;">
                        <div style="width:{bar_w}%; height:8px; border-radius:5px;
                                    background:linear-gradient(90deg,{color},{color}88);"></div>
                    </div>
                    <div style="min-width:45px; text-align:right; font-weight:700;
                                font-size:0.85rem; color:{color};">{r:+.2f}</div>
                </div>
                """, unsafe_allow_html=True)

    # ═══════════════════════════════════════════
    # TAB 4 — Statistik Deskriptif
    # ═══════════════════════════════════════════
    with tab4:
        st.markdown("### 🔍 Ringkasan Statistik Deskriptif")
        desc = df.describe().T.round(2)
        try:
            styled = desc.style.background_gradient(cmap="Blues", subset=[c for c in ["mean","std"] if c in desc.columns]).format(precision=2)
            st.dataframe(styled, use_container_width=True)
        except Exception:
            st.dataframe(desc, use_container_width=True)

        if kolom_kat:
            st.markdown("### 🏷️ Distribusi Kolom Kategorikal")
            for kat in kolom_kat:
                with st.expander(f"Kolom: **{kat}**"):
                    vc = df[kat].value_counts().reset_index()
                    vc.columns = [kat, "Jumlah"]
                    vc["Persentase"] = (vc["Jumlah"] / vc["Jumlah"].sum() * 100).round(1).astype(str) + "%"

                    fig_kat = px.bar(
                        vc.head(15), x="Jumlah", y=kat, orientation="h",
                        title=f"Distribusi {kat}",
                        template=PLOTLY_TEMPLATE,
                        color="Jumlah", color_continuous_scale="Viridis",
                        text="Jumlah"
                    )
                    fig_kat.update_layout(
                        margin=dict(l=0, r=0, t=50, b=0),
                        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                        font=dict(color="#e2e8f0"), showlegend=False,
                        yaxis=dict(autorange="reversed")
                    )
                    st.plotly_chart(fig_kat, use_container_width=True)
                    st.dataframe(vc, use_container_width=True)

    # ═══════════════════════════════════════════
    # TAB 5 — Data Mentah
    # ═══════════════════════════════════════════
    with tab5:
        st.markdown("### 📂 Preview Data Asli")
        st.markdown(f"""
        <div style="display:flex; gap:1rem; margin-bottom:1rem; flex-wrap:wrap;">
            <div style="background:#1e293b; border-radius:10px; padding:0.5rem 1rem;
                        font-size:0.8rem; color:#94a3b8; border:1px solid rgba(99,102,241,0.2);">
                📋 <strong style="color:#a5b4fc;">{df.shape[0]}</strong> baris
            </div>
            <div style="background:#1e293b; border-radius:10px; padding:0.5rem 1rem;
                        font-size:0.8rem; color:#94a3b8; border:1px solid rgba(99,102,241,0.2);">
                📐 <strong style="color:#a5b4fc;">{df.shape[1]}</strong> kolom
            </div>
            <div style="background:#1e293b; border-radius:10px; padding:0.5rem 1rem;
                        font-size:0.8rem; color:#94a3b8; border:1px solid rgba(99,102,241,0.2);">
                ❓ <strong style="color:#fbbf24;">{missing}</strong> missing values
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True, height=400)
