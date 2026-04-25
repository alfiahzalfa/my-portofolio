import streamlit as st
import pandas as pd
import plotly.express as px

def show_eda_page():
    if st.button("⬅️ Kembali ke Daftar Project"):
        st.session_state.project_view = 'grid'
        st.rerun()
        
    st.title("📊 Exploratory Data Analysis Dashboard")
    st.markdown("Sebuah dashboard interaktif untuk menganalisis dan menggali wawasan tersembunyi dari dataset Anda.")
    st.write("---")
    
    # Pilihan mode data diletakkan dalam expander agar lebih rapi
    with st.expander("⚙️ Pengaturan Sumber Data", expanded=True):
        mode_data = st.radio(
            "Pilih Sumber Data:",
            ("Gunakan Data Contoh (Dari GitHub)", "Upload Dataset Anda Sendiri (CSV)"),
            horizontal=True
        )
        
        df = None
        
        if mode_data == "Gunakan Data Contoh (Dari GitHub)":
            st.info("💡 Menampilkan dataset contoh. Nanti bisa diganti dengan dataset asli dari GitHub (menggunakan pd.read_csv).")
            # Dummy data yang lebih bervariasi untuk visualisasi yang lebih bagus
            df = pd.DataFrame({
                "Bulan": ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun"],
                "Kategori": ["Elektronik", "Pakaian", "Elektronik", "Makanan", "Pakaian", "Makanan"],
                "Total_Sales": [1500, 2300, 3100, 800, 1200, 2500],
                "Profit": [300, 400, 600, 100, 250, 450],
                "Rating": [4.5, 4.2, 4.8, 4.9, 4.1, 4.7]
            })
            
        elif mode_data == "Upload Dataset Anda Sendiri (CSV)":
            uploaded_file = st.file_uploader("Upload file CSV di sini", type=['csv'])
            if uploaded_file is not None:
                try:
                    df = pd.read_csv(uploaded_file)
                    st.success("File berhasil diunggah!")
                except Exception as e:
                    st.error(f"Terjadi kesalahan saat membaca file: {e}")
                    
    # Jika dataset berhasil dimuat, tampilkan Dashboard
    if df is not None:
        # Top Level Metrics
        st.markdown("### 📈 Key Performance Indicators")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(label="Total Baris Data", value=f"{df.shape[0]:,}")
        with col2:
            st.metric(label="Total Kolom", value=f"{df.shape[1]}")
        with col3:
            # Mengambil salah satu kolom numerik untuk ditampilkan totalnya
            num_cols_for_metric = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
            if num_cols_for_metric:
                total_sum = df[num_cols_for_metric[0]].sum()
                st.metric(label=f"Total {num_cols_for_metric[0]}", value=f"{total_sum:,.1f}")
            else:
                st.metric(label="Missing Values", value=f"{df.isna().sum().sum()}")
        with col4:
            if len(num_cols_for_metric) > 1:
                avg_val = df[num_cols_for_metric[1]].mean()
                st.metric(label=f"Rata-rata {num_cols_for_metric[1]}", value=f"{avg_val:,.1f}")
            else:
                st.metric(label="Data Duplikat", value=f"{df.duplicated().sum()}")
                
        st.write("---")
        
        # Menggunakan Tabs agar konten tidak terlalu memanjang ke bawah
        tab1, tab2, tab3 = st.tabs(["📊 Visualisasi Data", "🔍 Analisis Statistik", "📂 Data Mentah"])
        
        kolom_numerik = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
        kolom_kategorikal = df.select_dtypes(include=['object', 'category']).columns.tolist()
        
        with tab1:
            st.markdown("### Eksplorasi Visual Interaktif")
            if len(kolom_kategorikal) > 0 and len(kolom_numerik) > 0:
                c1, c2 = st.columns(2)
                with c1:
                    kat_pilihan = st.selectbox("Pilih Dimensi (Sumbu X)", kolom_kategorikal)
                with c2:
                    num_pilihan = st.selectbox("Pilih Metrik (Sumbu Y)", kolom_numerik)
                    
                try:
                    # Mengelompokkan data
                    chart_data = df.groupby(kat_pilihan)[num_pilihan].sum().reset_index()
                    chart_data = chart_data.sort_values(by=num_pilihan, ascending=False)
                    
                    # Layout 2 kolom untuk Bar Chart dan Pie Chart
                    chart_col1, chart_col2 = st.columns([2, 1])
                    
                    with chart_col1:
                        # Plotly Bar Chart
                        fig_bar = px.bar(
                            chart_data, 
                            x=kat_pilihan, 
                            y=num_pilihan, 
                            color=kat_pilihan,
                            title=f"Total {num_pilihan} berdasarkan {kat_pilihan}",
                            template="plotly_white",
                            color_discrete_sequence=px.colors.qualitative.Pastel
                        )
                        fig_bar.update_layout(showlegend=False, margin=dict(l=0, r=0, t=40, b=0))
                        st.plotly_chart(fig_bar, use_container_width=True)
                        
                    with chart_col2:
                        # Plotly Pie Chart (Donut)
                        if df[kat_pilihan].nunique() <= 10:
                            fig_pie = px.pie(
                                chart_data, 
                                names=kat_pilihan, 
                                values=num_pilihan,
                                title=f"Proporsi {kat_pilihan}",
                                hole=0.4,
                                template="plotly_white",
                                color_discrete_sequence=px.colors.qualitative.Pastel
                            )
                            fig_pie.update_layout(margin=dict(l=0, r=0, t=40, b=0))
                            st.plotly_chart(fig_pie, use_container_width=True)
                        else:
                            st.info("Pie chart disembunyikan karena kategori terlalu banyak.")
                except Exception as e:
                    st.warning(f"Gagal membuat visualisasi. Pastikan tipe data sesuai.")
                    
            elif len(kolom_numerik) > 0:
                st.line_chart(df[kolom_numerik])
            else:
                st.info("Tidak cukup data numerik/kategorikal untuk memunculkan visualisasi otomatis.")
                
        with tab2:
            st.markdown("### Ringkasan Statistik Deskriptif")
            st.write("Tabel di bawah ini menampilkan metrik statistik penting dari seluruh kolom numerik.")
            st.dataframe(df.describe().T, use_container_width=True)
            
        with tab3:
            st.markdown("### Preview Data Asli")
            st.dataframe(df, use_container_width=True)
