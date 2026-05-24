import streamlit as st
import numpy as np
import pandas as pd
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="SPK Kolesterol",
    page_icon="🥗",
    layout="wide"
)

# ==================================================
# CUSTOM CSS
# ==================================================
st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}

.block-container {
    padding-top: 2rem;
}

.hero-card {
    background: black;
    border-radius: 20px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.1);

    min-height: 220px;

    display: flex;
    flex-direction: column;
    justify-content: center;

    padding: 0 40px;

    margin-bottom: 20px;
    margin-top: 30px;
}

.hero-card h1,
.hero-card h4 {
    margin: 0;
}

.nutrisi-card {
    background: black;
    border-radius: 18px;
    overflow: hidden;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.1);
    margin-bottom: 20px;
}

.nutrisi-header-green {
    background: #0f766e;
    color: white;
    padding: 12px;
    font-weight: bold;
    font-size: 18px;
}

.nutrisi-header-orange {
    background: #f59e0b;
    color: white;
    padding: 12px;
    font-weight: bold;
    font-size: 18px;
}

.nutrisi-body {
    padding: 20px;
}

.food-card {
    background: white;
    border-radius: 18px;
    overflow: hidden;
    box-shadow: 0px 3px 10px rgba(0,0,0,0.1);
    margin-bottom: 20px;
    color: black;
}

.food-card img {
    width: 100%;
    height: 220px;
    object-fit: cover;
}

.food-content {
    padding: 15px;
}

.score-badge {
    background: #0f766e;
    color: black;
    padding: 6px 14px;
    border-radius: 20px;
    display: inline-block;
    font-size: 14px;
    margin-top: 10px;
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# LOAD DATASET
# ==================================================
df = pd.read_csv("nutrition.csv", on_bad_lines='skip')

foods = df[[
    'Food_Item',
    'Fat (g)',
    'Fiber (g)',
    'Sodium (mg)',
    'Cholesterol (mg)'
]]

foods = foods.dropna()

# ==================================================
# KATEGORI DINAMIS
# ==================================================
def kategori_fat(val):
    if val <= 5:
        return "LOW"
    elif val <= 15:
        return "MED"
    else:
        return "HIGH"

def kategori_fiber(val):
    if val <= 2:
        return "LOW"
    elif val <= 5:
        return "MED"
    else:
        return "HIGH"

def kategori_sodium(val):
    if val <= 150:
        return "LOW"
    elif val <= 500:
        return "MED"
    else:
        return "HIGH"

def kategori_cholesterol(val):
    if val <= 20:
        return "LOW"
    elif val <= 80:
        return "MED"
    else:
        return "HIGH"

# ==================================================
# HERO SECTION
# ==================================================
st.markdown("""
<div class="hero-card">
<h1>
🥗 Sistem Pendukung Keputusan Pemilihan
Makanan untuk Penderita Kolesterol
</h1>

<h4>
Rekomendasi Makanan Cerdas Berbasis
Metode Fuzzy Mamdani
</h4>
</div>
""", unsafe_allow_html=True)

# ==================================================
# SIDEBAR INPUT
# ==================================================
fat_input = 15
fiber_input = 2
sodium_input = 500
kolesterol_input = 50

if "show_form" not in st.session_state:
    st.session_state.show_form = False

# bikin tombol di tengah
left, center, right = st.columns([1, 2, 1])
with center:
    if st.button(
        "🔍 Mulai Analisis Nutrisi",
        use_container_width=True
    ):
        st.session_state.show_form = True

if st.session_state.show_form:
    st.markdown("## ⚙️ Input Parameter Nutrisi")
    col1, col2 = st.columns(2)
    with col1:
        fat_input = st.slider("Kadar Lemak (g)",0,40,15)
        fiber_input = st.slider("Kadar Serat (g)",0,14,2)

    with col2:
        sodium_input = st.slider("Kadar Sodium (mg)",0,1600,500)
        kolesterol_input = st.slider("Kadar Kolesterol (mg)",0,450,50)

    left2, center2, right2 = st.columns([1, 2, 1])

    with center2:
        proses = st.button("✨ Tampilkan Hasil",use_container_width=True)

    if proses:
        # ==================================================
        # CARD PARAMETER NUTRISI
        # ==================================================
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="nutrisi-card">
                <div class="nutrisi-header-green">
                    Kategori: LEMAK ({kategori_fat(fat_input)})
                </div>
                <div class="nutrisi-body">
                    <h3>{fat_input} g</h3>
                    <p>
                    Asupan lemak Anda berada
                    dalam batas yang dipilih.
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="nutrisi-card">
                <div class="nutrisi-header-green">
                    Kategori: SODIUM ({kategori_sodium(sodium_input)})
                </div>
                <div class="nutrisi-body">
                    <h3>{sodium_input} mg</h3>
                    <p>
                    Sodium perlu dijaga untuk
                    kesehatan jantung.
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="nutrisi-card">
                <div class="nutrisi-header-orange">
                    Kategori: SERAT ({kategori_fiber(fiber_input)})
                </div>
                <div class="nutrisi-body">
                    <h3>{fiber_input} g</h3>
                    <p>
                    Serat membantu mengontrol
                    kadar kolesterol tubuh.
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="nutrisi-card">
                <div class="nutrisi-header-orange">
                    Kategori: KOLESTEROL ({kategori_cholesterol(kolesterol_input)})
                </div>
                <div class="nutrisi-body">
                    <h3>{kolesterol_input} mg</h3>
                    <p>
                    Kolesterol rendah lebih baik
                    untuk kesehatan tubuh.
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        # ==================================================
        # FUZZY VARIABLE
        # ==================================================
        fat = ctrl.Antecedent(np.arange(0, 41, 1), 'fat')
        fiber = ctrl.Antecedent(np.arange(0, 15, 1), 'fiber')
        sodium = ctrl.Antecedent(np.arange(0, 1601, 1), 'sodium')
        cholesterol = ctrl.Antecedent(np.arange(0, 451, 1), 'cholesterol')

        recommendation = ctrl.Consequent(np.arange(0, 101, 1),'recommendation')

        # ==================================================
        # MEMBERSHIP FUNCTION
        # ==================================================
        fat['low'] = fuzz.trimf(fat.universe, [0, 0, 5])
        fat['medium'] = fuzz.trimf(fat.universe, [3, 10, 15])
        fat['high'] = fuzz.trapmf(fat.universe, [10, 25, 40, 40])

        fiber['low'] = fuzz.trimf(fiber.universe, [0, 0, 2])
        fiber['medium'] = fuzz.trimf(fiber.universe, [1, 3, 5])
        fiber['high'] = fuzz.trapmf(fiber.universe, [5, 8, 14, 14])

        sodium['low'] = fuzz.trimf(sodium.universe, [0, 0, 150])
        sodium['medium'] = fuzz.trimf(sodium.universe, [100, 350, 500])
        sodium['high'] = fuzz.trapmf(sodium.universe, [400, 900, 1600, 1600])

        cholesterol['low'] = fuzz.trimf(cholesterol.universe, [0, 0, 20])
        cholesterol['medium'] = fuzz.trimf(cholesterol.universe, [10, 50, 80])
        cholesterol['high'] = fuzz.trapmf(cholesterol.universe, [50, 200, 450, 450])

        # OUTPUT
        recommendation['not_recommended'] = fuzz.trimf(recommendation.universe,[0, 20, 40])
        recommendation['moderate'] = fuzz.trimf(recommendation.universe,[30, 50, 70])
        recommendation['recommended'] = fuzz.trimf(recommendation.universe,[60, 80, 100])

        # ==================================================
        # RULE FUZZY
        # ==================================================
        rule1 = ctrl.Rule(fat['high'] & cholesterol['high'],recommendation['not_recommended'])
        rule2 = ctrl.Rule(sodium['high'] & fiber['low'],recommendation['not_recommended'])
        rule3 = ctrl.Rule(fat['low'] & cholesterol['low'] & fiber['high'],recommendation['recommended'])
        rule4 = ctrl.Rule(fat['medium'] & sodium['medium'],recommendation['moderate'])
        rule5 = ctrl.Rule(fiber['high'] & cholesterol['low'],recommendation['recommended'])
        rule6 = ctrl.Rule(fat['low'] & sodium['low'],recommendation['recommended'])
        rule7 = ctrl.Rule(cholesterol['medium'],recommendation['moderate'])
        rule8 = ctrl.Rule(fat['high'],recommendation['not_recommended'])
        rule9 = ctrl.Rule(sodium['high'],recommendation['not_recommended'])
        rule10 = ctrl.Rule(fiber['medium'],recommendation['moderate'])

        # ==================================================
        # CONTROL SYSTEM
        # ==================================================
        recommendation_ctrl = ctrl.ControlSystem([rule1,rule2,rule3,rule4,rule5,rule6,rule7,rule8,rule9,rule10])

        # ==================================================
        # FUNCTION KATEGORI MAKANAN
        # ==================================================
        def kategori_makanan(score):
            if score <= 40:
                return "Tidak Direkomendasikan"
            elif score <= 70:
                return "Cukup Aman"
            else:
                return "Direkomendasikan"

        # ==================================================
        # FUNCTION KATEGORI PASIEN
        # ==================================================
        def kategori_pasien(score):
            if score <= 40:
                return "Risiko Tinggi"
            elif score <= 70:
                return "Risiko Sedang"
            else:
                return "Risiko Rendah"

        # ==================================================
        # PROSES FUZZY UNTUK SEMUA MAKANAN
        # ==================================================
        results = []
        for index, row in foods.iterrows():
            try:
                simulation = ctrl.ControlSystemSimulation(recommendation_ctrl)
                simulation.input['fat'] = row['Fat (g)']
                simulation.input['fiber'] = row['Fiber (g)']
                simulation.input['sodium'] = row['Sodium (mg)']
                simulation.input['cholesterol'] = row['Cholesterol (mg)']
                simulation.compute()
                score = simulation.output['recommendation']
                results.append([
                    row['Food_Item'],
                    round(score, 2)
                ])
            except:
                pass

        # ==================================================
        # DATAFRAME HASIL
        # ==================================================
        result_df = pd.DataFrame(
            results,
            columns=['Food', 'Score']
        )

        # HANDLE DATA KOSONG
        if result_df.empty:
            st.error("Tidak ada makanan yang berhasil dianalisis.")
            st.stop()

        result_df['Kategori'] = result_df['Score'].apply(kategori_makanan)
        kategori_order = {
            "Direkomendasikan": 3,
            "Cukup Aman": 2,
            "Tidak Direkomendasikan": 1
        }

        result_df['Kategori_Order'] = result_df['Kategori'].map(kategori_order)
        result_df = result_df.sort_values(by=['Kategori_Order', 'Score'],ascending=False)
        result_df = result_df.drop(columns=['Kategori_Order'])

        # ==================================================
        # ANALISIS KONDISI PASIEN
        # ==================================================
        simulation_user = ctrl.ControlSystemSimulation(recommendation_ctrl)
        simulation_user.input['fat'] = fat_input
        simulation_user.input['fiber'] = fiber_input
        simulation_user.input['sodium'] = sodium_input
        simulation_user.input['cholesterol'] = kolesterol_input
        simulation_user.compute()
        patient_score = simulation_user.output['recommendation']
        patient_category = kategori_pasien(patient_score)

        # ==================================================
        # HASIL ANALISIS PASIEN
        # ==================================================
        st.markdown("## 🩺 Analisis Kondisi Nutrisi Pasien")
        if patient_category == "Risiko Rendah":
            st.success(f"""
            ✅ Skor Kondisi: {patient_score:.2f}

            Kategori Risiko: {patient_category}
            
            Kondisi nutrisi pasien masih tergolong baik.
            
            Nilai lemak, sodium, dan kolesterol relatif terkendali,
            serta asupan serat cukup baik.
            """)
        elif patient_category == "Risiko Sedang":
            st.warning(f"""
            ⚠️ Skor Kondisi: {patient_score:.2f}
            
            Kategori Risiko: {patient_category}
            
            Kondisi nutrisi pasien perlu diperhatikan.
            
            Beberapa parameter nutrisi masih berada
            pada tingkat sedang dan perlu dikontrol.
            """)
        else:
            st.error(f"""
            ❌ Skor Kondisi: {patient_score:.2f}
            
            Kategori Risiko: {patient_category}
            
            Kondisi nutrisi pasien kurang baik.
            
            Sistem menyarankan untuk lebih menjaga
            pola makan dan memilih makanan
            dengan kandungan nutrisi lebih sehat.
            """)

        # ==================================================
        # REKOMENDASI MAKANAN
        # ==================================================
        st.markdown("## 🍽️ Rekomendasi Makanan")
        recommended = result_df[result_df['Kategori'] == "Direkomendasikan"]
        moderate = result_df[result_df['Kategori'] == "Cukup Aman"]

        bad = result_df[result_df['Kategori'] == "Tidak Direkomendasikan"]

        st.success(f"✅ Direkomendasikan: {len(recommended)} makanan")
        st.dataframe(recommended,use_container_width=True)
        st.warning(f"⚠️ Cukup Aman: {len(moderate)} makanan")
        st.dataframe(moderate,use_container_width=True)
        st.error(f"❌ Tidak Direkomendasikan: {len(bad)} makanan")
        st.dataframe(bad,use_container_width=True)

        # ==================================================
        # VISUALISASI FUZZY
        # ==================================================
        st.markdown("## 🧠 Visualisasi Analisis Fuzzy")

        # LEMAK
        st.subheader("1️⃣ Membership Lemak")

        fat.view(sim=simulation_user)
        fig = plt.gcf()
        st.pyplot(fig)

        st.info(f"""
        Input lemak pasien = {fat_input} g

        Kategori dominan:
        {kategori_fat(fat_input)}
        """)

        # SERAT
        st.subheader("2️⃣ Membership Serat")

        fiber.view(sim=simulation_user)
        fig = plt.gcf()
        st.pyplot(fig)

        st.info(f"""
        Input serat pasien = {fiber_input} g

        Kategori dominan:
        {kategori_fiber(fiber_input)}
        """)

        # SODIUM
        st.subheader("3️⃣ Membership Sodium")

        sodium.view(sim=simulation_user)
        fig = plt.gcf()
        st.pyplot(fig)

        st.info(f"""
        Input sodium pasien = {sodium_input} mg

        Kategori dominan:
        {kategori_sodium(sodium_input)}
        """)

        # KOLESTEROL
        st.subheader("4️⃣ Membership Kolesterol")

        cholesterol.view(sim=simulation_user)
        fig = plt.gcf()
        st.pyplot(fig)

        st.info(f"""
        Input kolesterol pasien = {kolesterol_input} mg

        Kategori dominan:
        {kategori_cholesterol(kolesterol_input)}
        """)

        # OUTPUT
        st.subheader("5️⃣ Output Fuzzy Recommendation")

        recommendation.view(sim=simulation_user)
        fig = plt.gcf()
        st.pyplot(fig)