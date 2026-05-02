import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff

def show_eda_page():
    if st.button("⬅️ Kembali ke Daftar Project"):
        st.session_state.project_view = 'grid'
        st.rerun()
        
    st.title("📊 Exploratory Data Analysis Dashboard")
    st.markdown("Sebuah dashboard interaktif untuk menganalisis dan menggali wawasan tersembunyi dari dataset Anda.")
    st.write("---")
    
    # Pilihan mode data
    with st.expander("⚙️ Pengaturan Sumber Data", expanded=True):
        mode_data = st.radio(
            "Pilih Sumber Data:",
            ("Gunakan Data Contoh (Dari GitHub)", "Upload Dataset Anda Sendiri (CSV)"),
            horizontal=True
        )
        
        df = None
        
        if mode_data == "Gunakan Data Contoh (Dari GitHub)":
            st.info("💡 Menampilkan dataset contoh penjualan toko.")
            import numpy as np
            np.random.seed(42)
            n = 100
            df = pd.DataFrame({
                "Bulan": np.random.choice(["Jan","Feb","Mar","Apr","Mei","Jun","Jul","Agt","Sep","Okt","Nov","Des"], n),
                "Kategori": np.random.choice(["Elektronik", "Pakaian", "Makanan", "Furnitur", "Olahraga"], n),
                "Total_Sales": np.random.randint(500, 5000, n),
                "Profit": np.random.randint(50, 1200, n),
                "Rating": np.round(np.random.uniform(3.0, 5.0, n), 1),
                "Quantity": np.random.randint(1, 50, n),
            })
            
        elif mode_data == "Upload Dataset Anda Sendiri (CSV)":
            uploaded_file = st.file_uploader("Upload file CSV di sini", type=['csv'])
            if uploaded_file is not None:
                try:
                    df = pd.read_csv(uploaded_file)
                    st.success("✅ File berhasil diunggah!")
                except Exception as e:
                    st.error(f"Terjadi kesalahan saat membaca file: {e}")
                    
    # Jika dataset berhasil dimuat, tampilkan Dashboard
    if df is not None:
        kolom_numerik     = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
        kolom_kategorikal = df.select_dtypes(include=['object', 'category']).columns.tolist()

        # ── KPI Metrics ─────────────────────────
        st.markdown("### 📈 Key Performance Indicators")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Baris Data",  f"{df.shape[0]:,}")
        with col2:
            st.metric("Total Kolom",       f"{df.shape[1]}")
        with col3:
            if kolom_numerik:
                st.metric(f"Total {kolom_numerik[0]}", f"{df[kolom_numerik[0]].sum():,.0f}")
            else:
                st.metric("Missing Values", f"{df.isna().sum().sum()}")
        with col4:
            if len(kolom_numerik) > 1:
                st.metric(f"Rata-rata {kolom_numerik[1]}", f"{df[kolom_numerik[1]].mean():,.1f}")
            else:
                st.metric("Data Duplikat", f"{df.duplicated().sum()}")
                
        st.write("---")
        
        # ── 5 TABS ──────────────────────────────
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Visualisasi Data",
            "📉 Distribusi Fitur",
            "🔥 Korelasi Heatmap",
            "🔍 Statistik Deskriptif",
            "📂 Data Mentah"
        ])
        
        # ── TAB 1: Visualisasi ───────────────────
        with tab1:
            st.markdown("### Eksplorasi Visual Interaktif")
            if kolom_kategorikal and kolom_numerik:
                c1, c2 = st.columns(2)
                with c1:
                    kat_pilihan = st.selectbox("Pilih Dimensi (Sumbu X)", kolom_kategorikal, key="eda_kat")
                with c2:
                    num_pilihan = st.selectbox("Pilih Metrik (Sumbu Y)", kolom_numerik, key="eda_num")
                    
                try:
                    chart_data = df.groupby(kat_pilihan)[num_pilihan].sum().reset_index()
                    chart_data = chart_data.sort_values(by=num_pilihan, ascending=False)
                    
                    chart_col1, chart_col2 = st.columns([2, 1])
                    
                    with chart_col1:
                        fig_bar = px.bar(
                            chart_data, x=kat_pilihan, y=num_pilihan, color=kat_pilihan,
                            title=f"Total {num_pilihan} berdasarkan {kat_pilihan}",
                            template="plotly_white",
                            color_discrete_sequence=px.colors.qualitative.Pastel
                        )
                        fig_bar.update_layout(showlegend=False, margin=dict(l=0, r=0, t=40, b=0))
                        st.plotly_chart(fig_bar, use_container_width=True)
                        
                    with chart_col2:
                        if df[kat_pilihan].nunique() <= 10:
                            fig_pie = px.pie(
                                chart_data, names=kat_pilihan, values=num_pilihan,
                                title=f"Proporsi {kat_pilihan}", hole=0.4,
                                template="plotly_white",
                                color_discrete_sequence=px.colors.qualitative.Pastel
                            )
                            fig_pie.update_layout(margin=dict(l=0, r=0, t=40, b=0))
                            st.plotly_chart(fig_pie, use_container_width=True)
                        else:
                            st.info("Pie chart disembunyikan karena kategori terlalu banyak.")
                except Exception:
                    st.warning("Gagal membuat visualisasi. Pastikan tipe data sesuai.")
                    
            elif kolom_numerik:
                st.line_chart(df[kolom_numerik])
            else:
                st.info("Tidak cukup data untuk memunculkan visualisasi otomatis.")

        # ── TAB 2: Distribusi Fitur ──────────────
        with tab2:
            st.markdown("### 📉 Distribusi Fitur Numerik")
            if kolom_numerik:
                fitur_dist = st.selectbox("Pilih fitur:", kolom_numerik, key="eda_dist_feat")
                
                dist_col1, dist_col2 = st.columns(2)
                
                with dist_col1:
                    # Histogram
                    fig_hist = px.histogram(
                        df, x=fitur_dist,
                        nbins=20,
                        title=f"Histogram — {fitur_dist}",
                        template="plotly_white",
                        color_discrete_sequence=["#4F46E5"],
                        marginal="box"
                    )
                    fig_hist.update_layout(margin=dict(t=50, b=0))
                    st.plotly_chart(fig_hist, use_container_width=True)
                    
                with dist_col2:
                    # Box plot per kategori (jika ada)
                    if kolom_kategorikal:
                        kat_box = st.selectbox("Kelompokkan berdasarkan:", kolom_kategorikal, key="eda_box_kat")
                        fig_box = px.box(
                            df, x=kat_box, y=fitur_dist, color=kat_box,
                            title=f"Box Plot {fitur_dist} per {kat_box}",
                            template="plotly_white",
                            color_discrete_sequence=px.colors.qualitative.Pastel
                        )
                        fig_box.update_layout(showlegend=False, margin=dict(t=50, b=0))
                        st.plotly_chart(fig_box, use_container_width=True)
                    else:
                        fig_box = px.box(
                            df, y=fitur_dist,
                            title=f"Box Plot — {fitur_dist}",
                            template="plotly_white",
                            color_discrete_sequence=["#10B981"]
                        )
                        st.plotly_chart(fig_box, use_container_width=True)

                # Scatter Plot antar 2 fitur
                if len(kolom_numerik) >= 2:
                    st.markdown("#### 🔵 Scatter Plot — Hubungan Antar Fitur")
                    sc1, sc2, sc3 = st.columns(3)
                    with sc1:
                        x_feat = st.selectbox("Fitur X:", kolom_numerik, index=0, key="eda_sc_x")
                    with sc2:
                        y_feat = st.selectbox("Fitur Y:", kolom_numerik, index=min(1, len(kolom_numerik)-1), key="eda_sc_y")
                    with sc3:
                        color_feat = st.selectbox("Warna (opsional):", ["—"] + kolom_kategorikal, key="eda_sc_color")

                    fig_sc = px.scatter(
                        df, x=x_feat, y=y_feat,
                        color=color_feat if color_feat != "—" else None,
                        title=f"Scatter: {x_feat} vs {y_feat}",
                        template="plotly_white",
                        trendline="ols",
                        color_discrete_sequence=px.colors.qualitative.Pastel
                    )
                    fig_sc.update_layout(margin=dict(t=50))
                    st.plotly_chart(fig_sc, use_container_width=True)
            else:
                st.info("Tidak ada kolom numerik dalam dataset.")

        # ── TAB 3: Korelasi Heatmap ──────────────
        with tab3:
            st.markdown("### 🔥 Correlation Heatmap")
            st.write("Menampilkan korelasi antar fitur numerik. Nilai mendekati **+1** = korelasi positif kuat, mendekati **-1** = korelasi negatif kuat.")

            if len(kolom_numerik) >= 2:
                corr_matrix = df[kolom_numerik].corr().round(2)

                fig_heatmap = go.Figure(data=go.Heatmap(
                    z=corr_matrix.values,
                    x=corr_matrix.columns.tolist(),
                    y=corr_matrix.index.tolist(),
                    text=corr_matrix.values,
                    texttemplate="%{text}",
                    colorscale="RdBu",
                    zmid=0,
                    zmin=-1, zmax=1,
                    colorbar=dict(title="Korelasi"),
                ))
                fig_heatmap.update_layout(
                    title="Correlation Matrix Heatmap",
                    template="plotly_white",
                    height=500,
                    margin=dict(t=60, l=0, r=0, b=0),
                    xaxis=dict(tickangle=-30),
                )
                st.plotly_chart(fig_heatmap, use_container_width=True)

                # Pasangan korelasi tertinggi
                st.markdown("#### 🏆 Top 5 Pasangan Fitur Paling Berkorelasi")
                corr_pairs = (
                    corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
                    .stack()
                    .reset_index()
                )
                corr_pairs.columns = ["Fitur A", "Fitur B", "Korelasi"]
                corr_pairs["Korelasi Absolut"] = corr_pairs["Korelasi"].abs()
                top5 = corr_pairs.sort_values("Korelasi Absolut", ascending=False).head(5)
                st.dataframe(
                    top5[["Fitur A", "Fitur B", "Korelasi"]].reset_index(drop=True)
                    .style.background_gradient(cmap="RdYlGn", subset=["Korelasi"]),
                    use_container_width=True
                )
            else:
                st.info("Dibutuhkan minimal 2 kolom numerik untuk menampilkan korelasi.")
                
        # ── TAB 4: Statistik ─────────────────────
        with tab4:
            st.markdown("### 🔍 Ringkasan Statistik Deskriptif")
            st.write("Tabel di bawah ini menampilkan metrik statistik penting dari seluruh kolom numerik.")
            st.dataframe(df.describe().T, use_container_width=True)
            
            if kolom_kategorikal:
                st.markdown("### 🏷️ Distribusi Kolom Kategorikal")
                for kat in kolom_kategorikal:
                    with st.expander(f"Kolom: **{kat}**"):
                        val_counts = df[kat].value_counts().reset_index()
                        val_counts.columns = [kat, "Jumlah"]
                        st.dataframe(val_counts, use_container_width=True)
            
        # ── TAB 5: Data Mentah ───────────────────
        with tab5:
            st.markdown("### 📂 Preview Data Asli")
            st.dataframe(df, use_container_width=True)
