import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Pengeluaran Mahasiswa", layout="wide")

st.title("📊 Dashboard Interaktif: Analisis Pengeluaran Mahasiswa")
st.markdown("Dashboard ini menampilkan analisis interaktif mengenai pola pengeluaran mahasiswa.")

@st.cache_data
def load_data():
    # Pastikan file CSV kamu sudah di-upload ke Colab!
    df = pd.read_csv('Course Evaluation (Responses) - Form Responses 1.csv')
    col_mapping = {
        'Status Tempat Tinggal': 'Tempat_Tinggal',
        'Berapa rata-rata uang saku/pemasukan Anda per bulan?': 'Uang_Saku',
        'Berapa rata-rata pengeluaran makan Anda per hari?': 'Pengeluaran_Makan',
        'Berapa rata-rata pengeluaran transportasi Anda per minggu?': 'Transportasi',
        'Seberapa sering Anda melakukan belanja online dalam 1 bulan?': 'Belanja_Online',
        'Berapa rata-rata pengeluaran hiburan (nongkrong, streaming, game, dll.) per bulan?': 'Hiburan',
        'Apakah Anda memiliki tabungan pribadi?': 'Tabungan'
    }
    df = df.rename(columns=col_mapping)
    return df

df = load_data()

st.sidebar.header("⚙️ Filter Data")
pilihan_tempat_tinggal = st.sidebar.multiselect(
    "Pilih Status Tempat Tinggal:",
    options=df['Tempat_Tinggal'].unique(),
    default=df['Tempat_Tinggal'].unique()
)

df_filtered = df[df['Tempat_Tinggal'].isin(pilihan_tempat_tinggal)]

st.write(f"Menampilkan data untuk **{len(df_filtered)}** responden.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Distribusi Uang Saku")
    fig_saku = px.histogram(df_filtered, x='Uang_Saku', color='Tempat_Tinggal',
                            barmode='group', color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig_saku, use_container_width=True)

with col2:
    st.subheader("Frekuensi Belanja Online")
    fig_belanja = px.pie(df_filtered, names='Belanja_Online', hole=0.3,
                         color_discrete_sequence=px.colors.qualitative.Set2)
    st.plotly_chart(fig_belanja, use_container_width=True)

st.divider()

st.subheader("Heatmap Interaktif: Pengeluaran Makan vs Transportasi")
fig_makan = px.density_heatmap(df_filtered, x='Pengeluaran_Makan', y='Transportasi',
                               color_continuous_scale="Viridis", text_auto=True)
st.plotly_chart(fig_makan, use_container_width=True)
