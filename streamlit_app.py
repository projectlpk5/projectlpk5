import streamlit as st
from streamlit_lottie import st_lottie
import requests
import pandas as pd
import plotly.express as px
import math
import sqlite3
from datetime import datetime
from io import BytesIO

# ================= DATABASE =================
conn = sqlite3.connect("waterflow_final.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS flow_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    waktu TEXT,
    metode TEXT,
    debit REAL
)
""")
conn.commit()

def save(waktu, metode, debit):
    c.execute("INSERT INTO flow_data (waktu, metode, debit) VALUES (?,?,?)", (waktu, metode, debit))
    conn.commit()

def load():
    return pd.read_sql("SELECT * FROM flow_data ORDER BY id DESC", conn)

def reset():
    c.execute("DELETE FROM flow_data")
    conn.commit()

# ================= CONFIG =================
st.set_page_config("Water Flow", "💧", layout="wide")

def load_lottie(url):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# ================= STYLE =================
st.markdown("""
<style>
/* 1. Background Utama Aplikasi */
.stApp {
    background: linear-gradient(135deg,#001233,#001845,#023E8A,#0077B6,#00B4D8);
}

/* 2. Hero Component */
.hero {
    padding:35px;
    border-radius:20px;
    text-align:center;
    color:white;
    background:linear-gradient(135deg,rgba(0,180,216,.95),rgba(2,62,138,.95));
    box-shadow:0 15px 40px rgba(0,0,0,.35);
}

/* 3. Menargetkan Judul & Teks Utama di Halaman Main (Bukan dalam Input) */
[data-testid="stMainBlockContainer"] h1, 
[data-testid="stMainBlockContainer"] h2, 
[data-testid="stMainBlockContainer"] h3, 
[data-testid="stMainBlockContainer"] h4, 
[data-testid="stMainBlockContainer"] p, 
[data-testid="stMainBlockContainer"] li, 
[data-testid="stMainBlockContainer"] label {
    color: white !important;
}

/* 4. MEMPERBAIKI KOTAK INPUT (Selectbox, Number Input, dll) AGAR TETAP HITAM */
div[data-baseweb="select"] *, div[data-testid="stNumberInput"] input {
    color: #000000 !important;
}

/* 5. MEMPERBAIKI TEKS MENU DI SIDEBAR (GARANSI KONTRAS) */
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p,
[data-testid="stSidebar"] span {
    color: #001233 !important;
    font-weight: bold !important;
}

/* 6. Kotak Info & Success Bawaan Menjadi Putih Bersih, Teks Hitam Pekat */
.stAlert {
    background-color: #ffffff !important;
    border: 1px solid #dddddd !important;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}
.stAlert p, .stAlert span, .stAlert li, .stAlert div {
    color: #000000 !important;
}

/* 7. Perbaikan Semua Tombol (Hitung & Download Excel) */
.stButton button, div[data-testid="stForm"] button, .stDownloadButton button {
    width: 100% !important;
    height: 50px !important;
    border-radius: 12px !important;
    background: linear-gradient(135deg, #00B4D8, #0077B6) !important;
    color: #ffffff !important;
    font-weight: bold !important;
    font-size: 16px !important;
    border: none !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
}

/* Efek saat tombol diarahkan mouse */
.stButton button:hover, div[data-testid="stForm"] button:hover, .stDownloadButton button:hover {
    background: linear-gradient(135deg, #0077B6, #023E8A) !important;
    color: #ffffff !important;
}
</style>
""", unsafe_allow_html=True)

# ================= HERO =================
lottie_water = load_lottie("https://assets9.lottiefiles.com/packages/lf20_jmBauI.json")
if lottie_water:
    st_lottie(lottie_water, height=200)

st.markdown("""
<div class="hero">
<h1>💧 WATER FLOW SYSTEM - KELOMPOK 11</h1>
<p>Simulasi, Perhitungan, Visualisasi & Analisis Debit Air Profesional</p>
</div>
""", unsafe_allow_html=True)

# ================= LOAD DATA =================
df = load()

# ================= SIDEBAR =================
with st.sidebar:
    menu = st.radio("MENU", [
        "🏠 Dashboard",
        "💧 Hitung Debit",
        "📊 Analisis",
        "📈 Visualisasi",
        "📋 Data",
        "🔄 Reset"
    ])

# ================= DASHBOARD =================
if menu == "🏠 Dashboard":

    pilihan = st.selectbox("Pilih Mode", ["Debit"])
    st.success("💡 Tips: Coba berbagai metode biar lihat perbedaan debitnya!")

    if pilihan == "Debit":
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Data", len(df))
        c2.metric("Status", "Active")
        c3.metric("Mode", "Watery")

        st.write("### 📌 Ringkasan Sistem")

        # ===== VISUAL KONSEP =====
        st.markdown("POLITEKNIK AKA BOGOR - SISTEM SIMULASI DEBIT AIR")
        url_gambar = "gevika.jpeg"
        st.image(url_gambar, caption="Sistem Simulasi Debit Air - Mahasiswa/i Kelompok 11", width=500)

        st.markdown("""
        ### ⚡ Cara Kerja Sistem
        1. Pilih metode perhitungan di menu **Hitung Debit**
        2. Masukkan parameter (Diameter, Lebar, Kecepatan, dll)
        3. Sistem menghitung debit secara *real-time*
        4. Data hasil hitung disimpan otomatis ke database
        5. Grafik tren visualisasi diperbarui otomatis
        """)

        st.markdown("<h2>📘 Tentang Sistem Ini</h2>", unsafe_allow_html=True)
        st.info("""
        Water Flow System adalah aplikasi simulasi untuk menghitung dan menganalisis debit air secara cepat, tepat, dan interaktif.
        
        💡 Sistem ini membantu pengguna untuk:
        - Menghitung debit air dari berbagai tipe penampang (Pipa lingkaran & Sungai kotak)
        - Memahami perilaku kontinuitas aliran fluida
        - Menyimpan dan melacak data historis tanpa takut hilang
        - Melihat visualisasi perubahan debit dalam bentuk grafik dinamis
        """)

        st.markdown("### ⚙️ Fitur Utama")
        st.markdown("""
        💧 **Perhitungan Debit Otomatis** Mendukung metode Volume & Waktu, Pipa & Kecepatan, dan Sungai  

        📊 **Analisis Data** Menampilkan nilai maksimum, minimum, dan rata-rata secara otomatis  

        📈 **Visualisasi Interaktif** Grafik garis (*Line Chart*) perubahan debit terhadap waktu menggunakan Plotly  

        💾 **Penyimpanan Data lokal** Data tersimpan aman di database SQLite internal  

        ⬇️ **Export Data** Hasil rekapan data bisa diunduh langsung dalam bentuk file Excel (`.xlsx`)  
        """)

# ================= HITUNG =================
elif menu == "💧 Hitung Debit":
    st.subheader("💧 Kalkulator Debit Air")

    metode = st.selectbox("Metode", [
        "Perhitungan Debit Air",
        "Perhitungan Debit Air Pipa",
        "Perhitungan Debit Air Sungai"
    ])

    with st.form("form"):
        if metode == "Perhitungan Debit Air":
            v_vol = st.number_input("Volume (m³)", min_value=0.0, max_value=1000000.0, value=1.0)
            t_waktu = st.number_input("Waktu (s)", min_value=0.1, max_value=1000000.0, value=1.0)
        elif metode == "Perhitungan Debit Air Pipa":
            d_pipa = st.number_input("Diameter Pipa (m)", min_value=0.0, max_value=1000000.0, value=0.001, step=0.001, format="%.3f")
            v_kecepatan = st.number_input("Kecepatan Aliran Pipa (m/s)", min_value=0.0, max_value=100.0, value=1.0, step=0.00001, format="%.1f")
        else:
            l_sungai = st.number_input("Lebar Sungai (m)", min_value=0.0, max_value=100000.0, value=1.0)
            k_sungai = st.number_input("Kedalaman Sungai (m)", min_value=0.0, max_value=10000.0, value=1.0)
            v_sungai = st.number_input("Kecepatan Aliran Sungai (m/s)", min_value=0.0, max_value=100000.0, value=1.0)

        hitung = st.form_submit_button("🔥 HITUNG DEBIT")

    if hitung:
        if metode == "Perhitungan Debit Air":
            debit = v_vol / t_waktu
            rumus = "Q = V / t"
        elif metode == "Perhitungan Debit Air Sungai":
            a = math.pi * (d_pipa / 2) ** 2
            debit = a * v_kecepatan
            rumus = "Q = A × v  (Di mana A = π × r²)"
        else:
            a = l_sungai * k_sungai
            debit = a * v_sungai
            rumus = "Q = A × v  (Di mana A = Lebar × Kedalaman)"

        waktu = datetime.now().strftime("%H:%M:%S")
        save(waktu, metode, debit)

        st.success(f"💧 Debit Air ({metode}) = {debit:.7f} m³/s")
        st.info(f"📌 Rumus yang digunakan: {rumus}")

        if debit < 1:
            level = "Rendah 🌱"
        elif debit < 5:
            level = "Sedang 🌊"
        else:
            level = "Tinggi 🌪️"

        st.markdown(f"""
        ### 🧠 Analisis Otomatis
        - Level aliran saat ini: **{level}**
        - Status: Nilai ini menunjukkan parameter laju aliran fluida pada kondisi input Anda.
        - *Insight*: Semakin besar penampang atau kecepatan aliran, nilai debit ($Q$) akan meningkat secara linear.
        """)

# ================= ANALISIS =================
elif menu == "📊 Analisis":
    st.subheader("📊 Analisis Data Statistik")
    if not df.empty:
        st.dataframe(df)
        st.markdown("### 📊 Statistik Log")
        c1, c2, c3 = st.columns(3)
        c1.metric("Debit Maksimum", f"{df['debit'].max():.4f} m³/s")
        c2.metric("Debit Minimum", f"{df['debit'].min():.4f} m³/s")
        c3.metric("Rata-rata Debit", f"{df['debit'].mean():.4f} m³/s")
    else:
        st.warning("Belum ada data di database untuk dianalisis. Silakan lakukan perhitungan terlebih dahulu!")

# ================= VISUALISASI =================
elif menu == "📈 Visualisasi":
    st.subheader("📈 Visualisasi Grafik Perubahan")
    if not df.empty:
        fig = px.line(
            df,
            x="waktu",
            y="debit",
            color="metode",
            markers=True,
            title="Grafik Fluktuasi Debit Air terhadap Waktu"
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("### 📌 Interpretasi Grafik")
        st.info("Grafik di atas merekam tren naik-turunnya debit air berdasarkan log waktu penyimpanan. Titik lonjakan menandakan adanya perubahan signifikan pada luas area penampang atau kecepatan fluida yang dimasukkan.")
    else:
        st.warning("Tidak ada data untuk divisualisasikan. Yuk, hitung debit dulu!")

# ================= DATA =================
elif menu == "📋 Data":
    st.subheader("📋 Manajemen Log Tabel Data")
    st.dataframe(df)
    if not df.empty:
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            df.to_excel(writer, index=False)
        st.download_button(
            "⬇️ Export Data ke Excel",
            buffer.getvalue(),
            "waterflow_final.xlsx"
        )

# ================= RESET =================
elif menu == "🔄 Reset":
    st.subheader("🔄 Reset Database Sistem")
    st.warning("Peringatan! Tindakan ini akan menghapus semua riwayat data secara permanen dari database.")
    if st.button("🗑 HAPUS SEMUA DATA PERMANEN"):
        reset()
        st.success("Database berhasil dikosongkan! Silakan segarkan halaman.")

st.markdown("---")
st.markdown("<center style='color:white'>💧 WATER FLOW SYSTEM 2026</center>", unsafe_allow_html=True)
