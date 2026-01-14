# =============================================================================
# JALU - Platform Analisis MBG (Makan Bergizi Gratis)
# Streamlit App with Tailwind CSS Integration
# =============================================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from PIL import Image, ImageDraw, ImageFont
from ultralytics import YOLO
import io
import random
import streamlit.components.v1 as components

# =============================================================================
# CONFIGURATION
# =============================================================================
st.set_page_config(
    page_title="JALU - Platform Analisis MBG",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- MOCK DATA GENERATOR (Jika CSV tidak ada) ---
def get_nutrition_data():
    data = {
        "FoodType": ["Banana", "Apple", "Orange", "Broccoli", "Carrot", "Sandwich", "Pizza", "Cake", "Bowl", "Milk"],
        "Quantity": ["1 medium", "1 medium", "1 medium", "100g", "100g", "1 serving", "1 slice", "1 slice", "1 bowl", "1 bottle"],
        "Protein": [1.3, 0.5, 1.2, 2.8, 0.9, 12.0, 11.0, 3.0, 5.0, 8.0],
        "Carbs": [27.0, 25.0, 15.0, 7.0, 10.0, 30.0, 36.0, 50.0, 20.0, 12.0],
        "Fat": [0.3, 0.3, 0.2, 0.4, 0.2, 10.0, 12.0, 15.0, 2.0, 5.0],
        "Calories": [105, 95, 62, 34, 41, 250, 285, 350, 150, 120]
    }
    return pd.DataFrame(data)

# --- LOAD MODELS & DATA ---
@st.cache_resource
def load_yolo_model():
    return YOLO("yolov8n.pt") # Menggunakan nano agar lebih ringan

@st.cache_data
def load_mbg_data():
    provinces = ["DKI Jakarta", "Jawa Barat", "Jawa Tengah", "Jawa Timur", "Banten"]
    levels = ["SD", "SMP", "SMA"]
    data = []
    for prov in provinces:
        for lvl in levels:
            data.append({
                "Provinsi": prov,
                "Jenjang_Pendidikan": lvl,
                "Jumlah_Siswa_Penerima": random.randint(50000, 200000),
                "Tingkat_Kepuasan": random.uniform(70, 95),
                "Penurunan_Stunting": random.uniform(5, 15),
                "Indeks_Keberhasilan": random.uniform(75, 98),
                "Anggaran_Terserap": random.uniform(80, 100),
                "Kabupaten_Kota": f"Kota {prov}",
                "Jumlah_Sekolah": random.randint(100, 500),
                "Rata_Rata_Berat_Badan": random.uniform(25, 35),
                "Persentase_Gizi_Baik": random.uniform(60, 90),
                "Jumlah_Kantin_Sehat": random.randint(50, 200),
                "Efisiensi_Distribusi": random.uniform(75, 95),
                "Tingkat_Partisipasi_Orang_Tua": random.uniform(70, 95),
                "Jumlah_Guru_Terbina": random.randint(200, 800),
                "Persentase_Kehadiran_Siswa": random.uniform(85, 98),
                "Biaya_Per_Siswa": random.uniform(15000, 25000),
                "Jumlah_Paket_Makanan": random.randint(1000, 5000),
                "Tingkat_Kualitas_Makanan": random.uniform(75, 95),
                "Persentase_Siswa_Aktif": random.uniform(80, 95),
                "Jumlah_Monitoring_Bulanan": random.randint(10, 30),
                "Indeks_Kesehatan_Sekolah": random.uniform(70, 95),
                "Persentase_Program_Lanjutan": random.uniform(60, 90),
                "Jumlah_Kemitraan": random.randint(5, 20)
            })
    return pd.DataFrame(data)

# Inisialisasi Data
yolo_model = load_yolo_model()
nutrition_data = get_nutrition_data()
mbg_data = load_mbg_data()
food_mapping = {k.lower(): k for k in nutrition_data["FoodType"].values}

# =============================================================================
# TAILWIND CSS INTEGRATION
# =============================================================================
st.markdown("""
<link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
<style>
    /* Custom overrides for Streamlit */
    .stApp { background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%); }
    .sidebar .sidebar-content { background: rgba(255,255,255,0.95); box-shadow: 2px 0 10px rgba(0,0,0,0.3); }
    .metric-card {
        @apply p-6 rounded-xl shadow-lg text-center transform hover:scale-105 transition-all duration-300;
        background: linear-gradient(135deg, rgba(255,255,255,0.98) 0%, rgba(248,250,252,0.95) 50%, rgba(241,245,249,0.92) 100%);
        border: 2px solid rgba(59,130,246,0.1);
        backdrop-filter: blur(15px);
        box-shadow: 0 8px 32px rgba(0,0,0,0.08), 0 2px 8px rgba(0,0,0,0.04);
        position: relative;
        overflow: hidden;
    }
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #3b82f6, #06b6d4, #10b981);
        border-radius: 12px 12px 0 0;
    }
    .metric-card:hover {
        box-shadow: 0 25px 50px rgba(0,0,0,0.15), 0 10px 25px rgba(0,0,0,0.1);
        transform: translateY(-8px) scale(1.03);
        border-color: rgba(59,130,246,0.2);
    }
    .metric-card .text-3xl {
        filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));
    }
    .hero-gradient { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
    .glass-effect { @apply bg-white bg-opacity-20 backdrop-blur-lg border border-white border-opacity-20; }
    .white-bg-text { @apply text-gray-800; }

    /* Ensure all text on white backgrounds is dark */
    .bg-white, .bg-white * { color: #1f2937 !important; }
    .bg-gray-50, .bg-gray-50 * { color: #1f2937 !important; }
    .metric-card, .metric-card * { color: #1f2937 !important; }
</style>
""", unsafe_allow_html=True)

# --- FUNCTIONS ---
def draw_detections(image, results):
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.load_default() # Hindari error arial.ttf
    except:
        font = None
    
    detections = []
    for box in results[0].boxes:
        coords = box.xyxy[0].tolist()
        conf = float(box.conf[0])
        cls_id = int(box.cls[0])
        label = yolo_model.names[cls_id]
        
        draw.rectangle(coords, outline="red", width=3)
        draw.text((coords[0], coords[1]-10), f"{label} {conf:.2f}", fill="red")
        detections.append(label)
    return image, detections

def calculate_nutrients(detected_labels):
    summary = {"Protein": 0, "Carbs": 0, "Fat": 0, "Calories": 0, "Items": []}
    for item in detected_labels:
        item_lower = item.lower()
        if item_lower in food_mapping:
            food_name = food_mapping[item_lower]
            row = nutrition_data[nutrition_data["FoodType"] == food_name].iloc[0]
            summary["Protein"] += row["Protein"]
            summary["Carbs"] += row["Carbs"]
            summary["Fat"] += row["Fat"]
            summary["Calories"] += row["Calories"]
            summary["Items"].append(food_name)
    return summary

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("JALU Platform")
page = st.sidebar.radio("Navigasi", ["Beranda Website", "Dashboard Analisis", "Deteksi AI Vision"])

# =============================================================================
# PAGE 1: BERANDA WEBSITE
# =============================================================================
if page == "Beranda Website":
    # Hero Section with Tailwind
    st.markdown("""
    <div class="text-center py-12">
        <h1 class="text-5xl font-bold text-blue-600 mb-4">🚀 JALU - Platform MBG Terpadu</h1>
        <p class="text-xl text-gray-600 mb-8">Membangun Generasi Emas dengan Gizi Seimbang</p>
    </div>
    """, unsafe_allow_html=True)

    # Hero Card
    st.markdown("""
    <div class="hero-gradient rounded-2xl p-12 text-white text-center mb-8 shadow-2xl">
        <h2 class="text-3xl font-bold mb-4">🌟 Platform Monitoring & Analisis</h2>
        <p class="text-lg opacity-90">Program Makan Bergizi Gratis berbasis AI untuk memantau dan menganalisis distribusi nutrisi di sekolah-sekolah Indonesia.</p>
    </div>
    """, unsafe_allow_html=True)

    # Metrics Section
    st.markdown("### 📈 Statistik Program MBG", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="text-3xl mb-2">👥</div>
            <div class="text-2xl font-bold text-blue-600">55.1 Juta</div>
            <div class="text-sm text-gray-600">Penerima Manfaat</div>
            <div class="text-green-500 font-semibold">+12%</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="text-3xl mb-2">💰</div>
            <div class="text-2xl font-bold text-green-600">Rp 335 T</div>
            <div class="text-sm text-gray-600">Anggaran</div>
            <div class="text-blue-500 font-semibold">Tahun 2026</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="text-3xl mb-2">🎯</div>
            <div class="text-2xl font-bold text-red-600">14%</div>
            <div class="text-sm text-gray-600">Target Stunting</div>
            <div class="text-orange-500 font-semibold">Target Nasional</div>
        </div>
        """, unsafe_allow_html=True)

# =============================================================================
# PAGE 2: DASHBOARD ANALISIS
# =============================================================================
elif page == "Dashboard Analisis":
    st.markdown("""
    <div class="text-center py-8">
        <h1 class="text-4xl font-bold text-gray-800 mb-2">📊 Dashboard Analitik MBG</h1>
        <p class="text-lg text-gray-600">Analisis mendalam program Makan Bergizi Gratis di seluruh Indonesia</p>
    </div>
    """, unsafe_allow_html=True)

    # Filter Section with better styling
    st.markdown("""
    <div class="bg-white p-6 rounded-xl shadow-lg mb-6">
        <h3 class="text-xl font-semibold text-gray-800 mb-4">🔍 Filter Data</h3>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("⚙️ Pengaturan Filter", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            selected_prov = st.multiselect(
                "🏛️ Pilih Provinsi",
                mbg_data["Provinsi"].unique(),
                default=mbg_data["Provinsi"].unique(),
                help="Pilih provinsi yang ingin dianalisis"
            )
        with col2:
            selected_lvl = st.multiselect(
                "🎓 Jenjang Sekolah",
                mbg_data["Jenjang_Pendidikan"].unique(),
                default=mbg_data["Jenjang_Pendidikan"].unique(),
                help="Pilih jenjang pendidikan yang ingin dianalisis"
            )

    filtered = mbg_data[(mbg_data["Provinsi"].isin(selected_prov)) & (mbg_data["Jenjang_Pendidikan"].isin(selected_lvl))]

    # Summary Cards
    st.markdown("### 📈 Ringkasan Data", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        total_students = filtered["Jumlah_Siswa_Penerima"].sum()
        st.metric("👥 Total Siswa", f"{total_students:,.0f}")
    with col2:
        avg_satisfaction = filtered["Tingkat_Kepuasan"].mean()
        st.metric("😊 Kepuasan Rata-rata", f"{avg_satisfaction:.1f}%")
    with col3:
        avg_success = filtered["Indeks_Keberhasilan"].mean()
        st.metric("🎯 Keberhasilan Rata-rata", f"{avg_success:.1f}%")
    with col4:
        avg_budget = filtered["Anggaran_Terserap"].mean()
        st.metric("💰 Anggaran Terserap", f"{avg_budget:.1f}%")

    # Charts Section
    st.markdown("### 📊 Visualisasi Data", unsafe_allow_html=True)

    # Row 1: Bar Chart and Scatter Plot
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class="bg-white p-4 rounded-xl shadow-lg mb-4">
            <h4 class="text-lg font-semibold text-gray-800 mb-2">📊 Distribusi Siswa per Provinsi</h4>
        </div>
        """, unsafe_allow_html=True)
        fig1 = px.bar(
            filtered,
            x="Provinsi",
            y="Jumlah_Siswa_Penerima",
            color="Jenjang_Pendidikan",
            title="",
            template="plotly_white"
        )
        fig1.update_layout(showlegend=True, height=400)
        st.plotly_chart(fig1, width='stretch')

    with c2:
        st.markdown("""
        <div class="bg-white p-4 rounded-xl shadow-lg mb-4">
            <h4 class="text-lg font-semibold text-gray-800 mb-2">🎯 Kepuasan vs Keberhasilan</h4>
        </div>
        """, unsafe_allow_html=True)
        fig2 = px.scatter(
            filtered,
            x="Tingkat_Kepuasan",
            y="Indeks_Keberhasilan",
            size="Jumlah_Siswa_Penerima",
            color="Provinsi",
            title="",
            template="plotly_white"
        )
        fig2.update_layout(height=400)
        st.plotly_chart(fig2, width='stretch')

    # Row 2: Pie Chart and Box Plot
    c3, c4 = st.columns(2)
    with c3:
        st.markdown("""
        <div class="bg-white p-4 rounded-xl shadow-lg mb-4">
            <h4 class="text-lg font-semibold text-gray-800 mb-2">💰 Anggaran Terserap per Provinsi</h4>
        </div>
        """, unsafe_allow_html=True)
        # Aggregate data by province for pie chart
        prov_budget = filtered.groupby("Provinsi")["Anggaran_Terserap"].mean().reset_index()
        fig3 = px.pie(
            prov_budget,
            values="Anggaran_Terserap",
            names="Provinsi",
            title="",
            template="plotly_white",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig3.update_layout(height=400)
        st.plotly_chart(fig3, width='stretch')

    with c4:
        st.markdown("""
        <div class="bg-white p-4 rounded-xl shadow-lg mb-4">
            <h4 class="text-lg font-semibold text-gray-800 mb-2">📈 Distribusi Tingkat Kepuasan</h4>
        </div>
        """, unsafe_allow_html=True)
        fig4 = px.box(
            filtered,
            x="Jenjang_Pendidikan",
            y="Tingkat_Kepuasan",
            color="Jenjang_Pendidikan",
            title="",
            template="plotly_white"
        )
        fig4.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig4, width='stretch')

    # Row 3: Line Chart and Heatmap
    c5, c6 = st.columns(2)
    with c5:
        st.markdown("""
        <div class="bg-white p-4 rounded-xl shadow-lg mb-4">
            <h4 class="text-lg font-semibold text-gray-800 mb-2">📉 Tren Indeks Keberhasilan</h4>
        </div>
        """, unsafe_allow_html=True)
        fig5 = px.line(
            filtered.sort_values("Indeks_Keberhasilan"),
            x="Provinsi",
            y="Indeks_Keberhasilan",
            color="Jenjang_Pendidikan",
            markers=True,
            title="",
            template="plotly_white"
        )
        fig5.update_layout(height=400)
        st.plotly_chart(fig5, use_container_width=True)

    with c6:
        st.markdown("""
        <div class="bg-white p-4 rounded-xl shadow-lg mb-4">
            <h4 class="text-lg font-semibold text-gray-800 mb-2">🔥 Korelasi Metrik Program</h4>
        </div>
        """, unsafe_allow_html=True)
        # Create correlation matrix for key metrics
        corr_data = filtered[["Tingkat_Kepuasan", "Penurunan_Stunting", "Indeks_Keberhasilan", "Anggaran_Terserap"]]
        corr_matrix = corr_data.corr()
        fig6 = px.imshow(
            corr_matrix,
            text_auto=True,
            aspect="auto",
            title="",
            template="plotly_white",
            color_continuous_scale="RdBu_r"
        )
        fig6.update_layout(height=400)
        st.plotly_chart(fig6, width='stretch')

    # Data Table
    st.markdown("### 📋 Detail Data", unsafe_allow_html=True)
    st.markdown("""
    <div class="bg-white p-4 rounded-xl shadow-lg">
        <p class="text-gray-600 mb-4">Data lengkap program MBG berdasarkan filter yang dipilih</p>
    </div>
    """, unsafe_allow_html=True)
    st.dataframe(
        filtered.style.highlight_max(axis=0),
        width='stretch',
        height=400
    )

# =============================================================================
# PAGE 3: DETEKSI AI VISION
# =============================================================================
elif page == "Deteksi AI Vision":
    st.markdown("""
    <div class="text-center py-8">
        <h1 class="text-4xl font-bold text-gray-800 mb-2">🤖 Deteksi Nutrisi AI</h1>
        <p class="text-lg text-gray-600">Unggah foto makanan untuk mendapatkan estimasi kandungan nutrisi secara real-time</p>
    </div>
    """, unsafe_allow_html=True)

    # Upload Section
    st.markdown("""
    <div class="bg-white p-6 rounded-xl shadow-lg mb-6">
        <h3 class="text-xl font-semibold text-gray-800 mb-4">📤 Upload Gambar Makanan</h3>
        <p class="text-gray-600">Pilih gambar makanan yang ingin dianalisis nutrisi nya</p>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Pilih file gambar (JPG, PNG, JPEG)",
        type=["jpg", "png", "jpeg"],
        help="Upload gambar makanan untuk deteksi nutrisi"
    )

    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGB")

        # Processing Section
        st.markdown("### 🔍 Proses Analisis", unsafe_allow_html=True)

        with st.spinner("🤖 AI sedang menganalisis gambar..."):
            results = yolo_model(image)
            processed_img, labels = draw_detections(image.copy(), results)
            nutrisi = calculate_nutrients(labels)

        # Results Section
        st.markdown("### 📊 Hasil Analisis", unsafe_allow_html=True)

        col_img, col_res = st.columns([2, 1])

        with col_img:
            st.markdown("""
            <div class="bg-white p-4 rounded-xl shadow-lg">
                <h4 class="text-lg font-semibold text-gray-800 mb-2">🖼️ Gambar Hasil Deteksi</h4>
            </div>
            """, unsafe_allow_html=True)
            st.image(processed_img, caption="Hasil Deteksi AI", use_container_width=True)

        with col_res:
            # Detection Summary
            if len(labels) > 0:
                st.success(f"✅ Ditemukan {len(labels)} objek makanan")
            else:
                st.warning("⚠️ Tidak ada objek makanan terdeteksi")

            # Nutrition Results
            st.markdown("""
            <div class="bg-white p-4 rounded-xl shadow-lg mb-4">
                <h4 class="text-lg font-semibold text-gray-800 mb-3">🥗 Estimasi Nutrisi</h4>
            </div>
            """, unsafe_allow_html=True)

            # Nutrition Metrics in a grid
            nutr_cols = st.columns(2)
            with nutr_cols[0]:
                st.metric("🔥 Kalori", f"{nutrisi['Calories']:.0f} kcal")
                st.metric("🍗 Protein", f"{nutrisi['Protein']:.1f} g")
            with nutr_cols[1]:
                st.metric("🍞 Karbohidrat", f"{nutrisi['Carbs']:.1f} g")
                st.metric("🥑 Lemak", f"{nutrisi['Fat']:.1f} g")

            # Detected Items
            if nutrisi["Items"]:
                st.markdown("""
                <div class="bg-green-50 p-4 rounded-xl border-l-4 border-green-500 mt-4">
                    <h5 class="font-semibold text-green-800 mb-2">✅ Item Terdeteksi:</h5>
                    <p class="text-green-700">{}</p>
                </div>
                """.format(", ".join(set(nutrisi["Items"]))), unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="bg-blue-50 p-4 rounded-xl border-l-4 border-blue-500 mt-4">
                    <h5 class="font-semibold text-blue-800 mb-2">💡 Tips:</h5>
                    <p class="text-blue-700">Gunakan objek seperti: Banana, Apple, Sandwich, Pizza untuk tes nutrisi.</p>
                </div>
                """, unsafe_allow_html=True)
    else:
        # Placeholder when no image uploaded
        st.markdown("""
        <div class="text-center py-12 bg-gray-50 rounded-xl">
            <div class="text-6xl mb-4">📷</div>
            <h3 class="text-xl font-semibold text-gray-700 mb-2">Belum ada gambar diupload</h3>
            <p class="text-gray-500">Silakan upload gambar makanan untuk mulai analisis nutrisi</p>
        </div>
        """, unsafe_allow_html=True)

# =============================================================================
# FOOTER
# =============================================================================
st.markdown("""
<div class="text-center py-8 mt-12 bg-white rounded-t-2xl shadow-lg">
    <div class="max-w-4xl mx-auto">
        <h3 class="text-2xl font-bold text-gray-800 mb-4">🌟 JALU - Platform MBG Terpadu</h3>
        <p class="text-gray-600 mb-6">Membangun Generasi Emas dengan Gizi Seimbang melalui Teknologi AI</p>
        <div class="flex justify-center space-x-6 text-sm text-gray-500">
            <span>🔬 Berbasis YOLOv8</span>
            <span>📊 Powered by Streamlit</span>
            <span>🎨 Styled with Tailwind CSS</span>
        </div>
        <div class="mt-4 text-xs text-gray-400">
            © 2025 JALU Analytics Platform. All rights reserved.
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
