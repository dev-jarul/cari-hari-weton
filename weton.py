import streamlit as st
import datetime as dt
from datetime import datetime, timedelta
import plotly.graph_objects as go

# Setup halaman utama web app agar responsif di HP
st.set_page_config(
    page_title="Prediksi Weton & Jodoh", 
    page_icon="🔮", 
    layout="centered"
)

# Judul Aplikasi Utama
st.title("🔮 Primbon Digital: Weton & Cek Jodoh")
st.markdown("Cek weton, watak lahir, hari peruntungan, grafik karakter, hingga kecocokan jodoh Anda berdasarkan kalender Jawa kuno.")
st.markdown("---")

# --- DATABASE & LOGIKA DASAR ---
NEPTU_HARI = {"Senin": 4, "Selasa": 3, "Rabu": 7, "Kamis": 8, "Jumat": 6, "Sabtu": 9, "Minggu": 5}
NEPTU_PASARAN = {"Legi": 5, "Pahing": 9, "Pon": 7, "Wage": 4, "Kliwon": 8}
DAFTAR_HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
DAFTAR_PASARAN = ["Legi", "Pahing", "Pon", "Wage", "Kliwon"]

PRIMBON_WATAK_DETAIL = {
    "Senin Legi": {"positif": "Tegas, mandiri, suka berargumen yang sehat, berpegang teguh pada prinsip, serta memiliki hati yang lembut dan mudah iba.", "negatif": "Cenderung keras kepala, sulit menerima masukan, dan suka mencampuri urusan orang lain."},
    "Senin Pahing": {"positif": "Pekerja keras, jujur, sangat optimis dalam menatap masa depan, dan memiliki cita-cita yang tinggi.", "negatif": "Cenderung kaku dalam bergaul, mudah tersinggung jika dikritik, dan suka memendam masalah."},
    "Senin Pon": {"positif": "Cerdas, berwawasan luas, pandai bicara atau bernegosiasi, serta memiliki jiwa sosial yang tinggi.", "negatif": "Terkadang suka pamer kelebihan, agak angkuh, dan mudah goyah pendiriannya."},
    "Senin Wage": {"positif": "Sabar, penurut, setia, suka kedamaian, dan pandai merawat hubungan baik.", "negatif": "Kurang ambisius, jika sudah terlanjur marah besar akan sangat sulit ditenangkan."},
    "Senin Kliwon": {"positif": "Penuh kehormatan, ambisius dalam karier, suka menolong tanpa pamrih, dan setia pada janji.", "negatif": "Hatinya mudah goyah, sering merasa cemas atau khawatir berlebihan."},
    "Selasa Legi": {"positif": "Ceria, pandai bergaul, mudah beradaptasi, dan memiliki bakat kepemimpinan.", "negatif": "Suka membantah perintah, emosinya meledak-ledak, dan agak boros."},
    "Selasa Pahing": {"positif": "Cerdas, mandiri, rela berkorban demi teman, serta punya daya juang tinggi.", "negatif": "Pencemburu berat, suka membalas perbuatan orang, dan sulit melupakan kesalahan."},
    "Selasa Pon": {"positif": "Setia, murah hati, berwibawa, dan suka melindungi orang yang lebih lemah.", "negatif": "Suka kemewahan, agak keras kepala, dan sulit dinasihati."},
    "Selasa Wage": {"positif": "Sederhana, hemat, tekun dalam bekerja, pandai menyimpan rahasia, dan tidak suka pamer.", "negatif": "Cenderung kaku, agak penyendiri, dan kurang pandai mengekspresikan perasaan."},
    "Selasa Kliwon": {"positif": "Dikenal sebagai 'Anggoro Kasih', bicaranya berwibawa, memikat, dan dikagumi.", "negatif": "Keras kepala, sulit menerima kritik, dan bicaranya terlalu tajam tanpa sengaja."},
    "Rabu Legi": {"positif": "Menghormati tata krama, berpegang teguh pada prinsip hidup, adil, dan setia pada kawan.", "negatif": "Suka mencampuri urusan orang lain, suka dipuji, dan sulit mengalah."},
    "Rabu Pahing": {"positif": "Tenang, suka menolong, penuh perhitungan yang matang, dan berwibawa.", "negatif": "Jika dikhianati akan sangat pendendam, kaku, dan sulit memberikan kesempatan kedua."},
    "Rabu Pon": {"positif": "Sopan santun, pandai beradaptasi, berjiwa sosial tinggi, dan kreatif.", "negatif": "Suka dipuji, agak boros, dan mudah tersinggung."},
    "Rabu Wage": {"positif": "Sabar, suka mengalah demi kebaikan bersama, protektif, dan sayang keluarga.", "negatif": "Kurang percaya diri dalam mengambil keputusan besar dan cenderung peragu."},
    "Rabu Kliwon": {"positif": "Pemikir yang dalam, pandai berbicara, berhati lembut, dan punya bakat jadi pendidik.", "negatif": "Sangat peka atau sensitif, mudah tersinggung, dan sering berpikir terlalu dalam."},
    "Kamis Legi": {"positif": "Bercita-cita tinggi, bijaksana, mandiri, dan suka mempelajari hal baru.", "negatif": "Emosinya suka naik turun (moody), suka dipuji, dan terkadang kurang sabar."},
    "Kamis Pahing": {"positif": "Gagah berani, cerdas, tidak mudah menyerah, dan sangat mencintai keluarganya.", "negatif": "Agak angkuh, tidak suka mengalah meskipun salah, dan bicaranya blak-blakan."},
    "Kamis Pon": {"positif": "Hemat, rajin bekerja, bicaranya penuh arti, serta pandai menyimpan rahasia.", "negatif": "Pendiam, suka curigaan pada orang baru, dan sulit menaruh kepercayaan."},
    "Kamis Wage": {"positif": "Suka dengan kerapian dan kebersihan, penurut, setia, serta sangat telaten.", "negatif": "Hatinya cenderung mudah dendam jika disakiti, kurang suka perubahan mendadak."},
    "Kamis Kliwon": {"positif": "Sabar, murah hati, memiliki lingkaran pertemanan luas, dan pandai menghidupkan suasana.", "negatif": "Suka membantah jika merasa benar dan sulit mengalah dalam argumen."},
    "Jumat Legi": {"positif": "Dikenal sakral, taat beragama, teguh pada pendirian, jujur, dan berwibawa besar.", "negatif": "Jarang mau mengalah, cenderung kaku, dan menganggap prinsipnya paling benar."},
    "Jumat Pahing": {"positif": "Cerdas, tenang menghadapi masalah, pandai mencari peluang rezeki, dan mandiri.", "negatif": "Suka memendam amarah yang besar, jika meledak bisa menakutkan, dan agak kikir."},
    "Jumat Pon": {"positif": "Rendah hati, welas asih, tutur katanya menyejukkan, disukai banyak orang.", "negatif": "Mudah dipengaruhi lingkungan (kurang teguh) dan gampang ditipu karena kasihan."},
    "Jumat Wage": {"positif": "Penuh kasih sayang, jujur, setia, dan suka menolong orang kesusahan.", "negatif": "Terlalu mudah iba hingga sering dimanfaatkan, serta sering mengorbankan diri sendiri."},
    "Jumat Kliwon": {"positif": "Memiliki pesona kuat, berjiwa pemimpin, pandai bergaul, dan murah rezeki.", "negatif": "Agak malas jika tidak diberi motivasi, suka membantah, dan gampang marah."},
    "Sabtu Legi": {"positif": "Pandai bergaul, ceria, suka menolong, memiliki selera seni bagus, dan mudah memaafkan.", "negatif": "Cenderung boros, suka pamer atau menjadi pusat perhatian, dan kurang menabung."},
    "Sabtu Pahing": {"positif": "Berani, ambisius, mudah memaafkan, berwibawa, dan berjiwa penolong.", "negatif": "Emosinya sangat meledak-ledak, mudah tersinggung, dan suka menguasai percakapan."},
    "Sabtu Pon": {"positif": "Sabar, bertanggung jawab penuh, teliti, dan suka menolong sesama.", "negatif": "Sangat keras kepala, sulit dibilangi jika sudah mengambil keputusan."},
    "Sabtu Wage": {"positif": "Mandiri, hemat, suka menolong sesama yang membutuhkan, dan pendiam.", "negatif": "Cenderung kaku, mudah curiga pada niat baik orang, dan agak penyendiri."},
    "Sabtu Kliwon": {"positif": "Ramah, sopan santun, bijaksana, berjiwa pelindung, dan mengayomi.", "negatif": "Hatinya mudah tersinggung, gampang merasa kecewa jika ekspektasi tidak terpenuhi."},
    "Minggu Legi": {"positif": "Tegas, tenang dalam situasi sulit, cerdas, dan pandai menyembunyikan masalah.", "negatif": "Agak licik atau penuh taktik rahasia untuk mencapai tujuan, serta sulit ditebak."},
    "Minggu Pahing": {"positif": "Wawasan luas, cerdas berpikir logis, kuat mental, dan sangat mandiri.", "negatif": "Suka memendam perasaan, sangat sensitif, dan sulit membuka diri."},
    "Minggu Pon": {"positif": "Penuh keberuntungan hidup, pekerja keras, berwibawa, dan tidak mudah menyerah.", "negatif": "Suka membantah pendapat orang lain, agak boros, dan suka dipuji."},
    "Minggu Wage": {"positif": "Sederhana, berwawasan luas, penurut, suka kedamaian, dan pandai menenangkan.", "negatif": "Pencemburu, kurang memiliki inisiatif memimpin, dan mudah merasa minder."},
    "Minggu Kliwon": {"positif": "Sopan, pandai berbicara, berjiwa pemimpin, murah hati, dan pandai bergaul.", "negatif": "Suka membantah, gampang tersinggung, dan sering tidak sabaran."}
}

PRIMBON_JODOH = {
    1: {"status": "PEGAT (💔)", "arti": "Menurut perhitungan, hubungan cenderung sering menemui masalah di kemudian hari, baik karena masalah sepele, ekonomi, maupun faktor eksternal. Diperlukan kesabaran ekstra tinggi dan komunikasi yang kuat agar hubungan tetap kokoh."},
    2: {"status": "RATU (👑)", "arti": "Luar biasa! Pasangan ini dianggap sebagai jodoh sejati. Kehidupan rumah tangga akan sangat harmonis, disegani oleh tetangga dan kerabat, serta penuh ketenteraman."},
    3: {"status": "JODOH (💖)", "arti": "Sangat cocok! Pasangan ini diprediksi bisa saling menerima kelebihan dan kekurangan masing-masing. Rumah tangga berjalan rukun, adem ayem, dan awet sampai tua."},
    4: {"status": "TOPO (⛰️)", "arti": "Di awal pernikahan, rumah tangga kemungkinan akan mengalami pasang surut atau rintangan terlebih dahulu (misal penyesuaian sifat atau ekonomi). Namun jangan khawatir, seiring berjalannya waktu hubungan akan berakhir bahagia dan sukses."},
    5: {"status": "TINARI (💰)", "arti": "Penuh keberuntungan rezeki! Pasangan ini diprediksi akan mudah mencari nafkah, sering mendapat keberuntungan mengejutkan, dan hidupnya berkecukupan."},
    6: {"status": "PADANAN (⚖️)", "arti": "Rumah tangga akan sering diuji oleh percekcokan atau perbedaan pendapat yang cukup intens. Namun selama kedua pihak mau mengalah dan menurunkan ego, hubungan bisa tetap dipertahaman dengan baik."},
    7: {"status": "SUJANAN (🔥)", "arti": "Harus berhati-hati terhadap potensi konflik atau rasa cemburu yang berlebihan dalam rumah tangga. Kunci keharmonisan pasangan ini adalah keterbukaan total dan menjaga kepercayaan satu sama lain."},
    0: {"status": "PESTHI (🕊️)", "arti": "Sangat damai! Rumah tangga diprediksi berjalan lempeng, rukun, minim konflik besar, dan dinaungi kebahagiaan yang konsisten sepanjang perjalanan pernikahan."}
}

def hitung_weton_core(tgl, waktu_malam):
    tanggal_lahir = datetime.combine(tgl, datetime.min.time())
    if waktu_malam:
        tanggal_lahir += timedelta(days=1)
    
    tanggal_patokan = datetime(1900, 1, 1)
    selisih_hari = (tanggal_lahir - tanggal_patokan).days
    
    idx_h = (0 + selisih_hari) % 7
    idx_p = (1 + selisih_hari) % 5
    
    hari = DAFTAR_HARI[idx_h]
    pasaran = DAFTAR_PASARAN[idx_p]
    
    return hari, pasaran, NEPTU_HARI[hari], NEPTU_PASARAN[pasaran]

def cari_hari_baik_nahas(hari_lahir, pasaran_lahir):
    idx_h = DAFTAR_HARI.index(hari_lahir)
    idx_p = DAFTAR_PASARAN.index(pasaran_lahir)
    
    hari_nahas_1 = f"{DAFTAR_HARI[(idx_h + 3) % 7]} {DAFTAR_PASARAN[(idx_p + 3) % 5]}"
    hari_nahas_2 = f"{DAFTAR_HARI[(idx_h + 4) % 7]} {DAFTAR_PASARAN[(idx_p + 4) % 5]}"
    hari_baik_1 = f"{DAFTAR_HARI[(idx_h + 1) % 7]} {DAFTAR_PASARAN[(idx_p + 2) % 5]}"
    hari_baik_2 = f"{DAFTAR_HARI[(idx_h + 2) % 7]} {DAFTAR_PASARAN[(idx_p + 0) % 5]}"
    
    return [hari_nahas_1, hari_nahas_2], [hari_baik_1, hari_baik_2]

# --- MENU NAVIGASI UTAMA ---
menu = st.tabs(["👤 Cek Weton Pribadi", "👩‍❤️‍👨 Cek Kecocokan Jodoh"])

min_date = dt.date(1920, 1, 1)
max_date = dt.date(2040, 12, 31)

# ================= TAB 1: CEK WETON PRIBADI =================
with menu[0]:
    st.subheader("📅 Data Kelahiran Anda")
    tgl_pilih = st.date_input("Pilih Tanggal Lahir Anda:", value=dt.date(2000, 1, 1), min_value=min_date, max_value=max_date, format="DD/MM/YYYY", key="pribadi_tgl")
    waktu = st.radio("Kapan Waktu Jam Kelahiran Anda?", ("Siang / Pagi / Sore (06.00 - 17.59 WIB)", "Malam Hari (Setelah Magrib / 18.00 - 05.59 WIB)"), key="pribadi_waktu")
    
    st.markdown("---")
    
    if tgl_pilih:
        malam_hari = "Malam Hari" in waktu
        h_weton, p_weton, n_h, n_p = hitung_weton_core(tgl_pilih, malam_hari)
        weton_lengkap = f"{h_weton} {p_weton}"
        total_neptu = n_h + n_p
        
        # Perhitungan sisa hari selapanan
        hari_ini = datetime.now()
        selisih_hari_ini = (hari_ini - datetime(1900, 1, 1)).days
        idx_hari_kini = (0 + selisih_hari_ini) % 7
        idx_pas_kini = (1 + selisih_hari_ini) % 5
        
        target_h = DAFTAR_HARI.index(h_weton)
        target_p = DAFTAR_PASARAN.index(p_weton)
        
        sisa_hari_selapan = 0
        for i in range(36):
            if (idx_hari_kini + i) % 7 == target_h and (idx_pas_kini + i) % 5 == target_p:
                sisa_hari_selapan = i
                break
        if sisa_hari_selapan == 0:
            sisa_hari_selapan = 35

        st.subheader("📊 Hasil Analisis Primbon")
        st.success(f"**Weton Anda: {weton_lengkap}**")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Tanggal Input", value=tgl_pilih.strftime("%d/%m/%Y"))
            st.info(f"🎂 **{sisa_hari_selapan} hari lagi** menuju Hari Ulang Tahun Weton (*Selapanan*) Anda.")
        with col2:
            st.metric(label="Total Angka Neptu", value=str(total_neptu))
            st.write(f"🔢 **Detail:** {h_weton} ({n_h}) + {p_weton} ({n_p})")
            
        st.markdown("---")
        st.markdown("### 📊 Visualisasi Karakter & Watak Lahir")
        
        karakter_skor = {
            "Kepemimpinan": 60 + ((n_h * 5) % 40),
            "Kesabaran": 55 + ((n_p * 6) % 45),
            "Kejujuran": 65 + (((n_h + n_p) * 2) % 35),
            "Keuangan / Rezeki": 50 + ((total_neptu * 4) % 50),
            "Kecerdasan Emosi": 55 + (((n_p - n_h) * 7) % 45)
        }
        
        categories = list(karakter_skor.keys())
        values = list(karakter_skor.values())
        values.append(values[0])
        categories.append(categories[0])
        
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            fillcolor='rgba(131, 201, 255, 0.4)',
            line=dict(color='#1f77b4', width=2),
            name='Potensi Diri'
        ))
        
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=False,
            margin=dict(l=40, r=40, t=20, b=20),
            height=320
        )
        
        st.plotly_chart(fig, use_container_width=True)

        watak_data = PRIMBON_WATAK_DETAIL.get(weton_lengkap, {"positif": "Belum terdaftar.", "negatif": "Belum terdaftar."})
        with st.expander("🔮 Detail Watak & Tabiat (Menurut Kitab Primbon)", expanded=False):
            st.markdown("##### 🟩 Sisi Positif / Kelebihan:")
            st.write(watak_data['positif'])
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("##### 🟥 Sisi Negatif / Kekurangan:")
            st.write(watak_data['negatif'])

        st.markdown("### 📅 Kalender Peruntungan Jawa")
        daftar_nahas, daftar_baik = cari_hari_baik_nahas(h_weton, p_weton)
        st.error(f"⚠️ **Hari Nahas Anda:** {daftar_nahas[0]} & {daftar_nahas[1]}")
        st.info(f"✨ **Hari Baik Anda:** {daftar_baik[0]} & {daftar_baik[1]}")
        
        st.markdown("---")
        st.markdown("### 📜 Simpan Hasil Analisis")
        st.markdown("Klik tombol di bawah untuk mencetak atau menyimpan dokumen hasil ramalan weton resmi Anda dalam format PDF.")
        
        # --- TEMPLATE HTML/CSS PADA SERTIFIKAT DENGAN WATERMARK / TANDA TANGAN ---
        html_sertifikat = f"""
        <html>
        <head>
        <style>
            @media print {{
                body {{ background: white; color: black; }}
                .no-print {{ display: none !important; }}
            }}
            .cert-container {{
                border: 6px double #b58900;
                padding: 30px;
                background-color: #fdfaf2;
                font-family: 'Georgia', serif;
                color: #333;
                text-align: center;
                border-radius: 10px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.1);
                margin: 20px auto;
                max-width: 600px;
                position: relative;
            }}
            .cert-title {{
                font-size: 24px;
                font-weight: bold;
                color: #856404;
                text-transform: uppercase;
                letter-spacing: 2px;
                margin-bottom: 5px;
            }}
            .cert-subtitle {{
                font-size: 13px;
                font-style: italic;
                color: #666;
                margin-bottom: 25px;
            }}
            .cert-table {{
                width: 100%;
                margin: 15px 0;
                border-collapse: collapse;
            }}
            .cert-table td {{
                padding: 8px;
                text-align: left;
                font-size: 14px;
                border-bottom: 1px dashed #ddd;
            }}
            .cert-table td.label {{
                font-weight: bold;
                color: #555;
                width: 40%;
            }}
            .badge-weton {{
                font-size: 20px;
                font-weight: bold;
                color: #fff;
                background-color: #856404;
                padding: 10px;
                display: inline-block;
                margin: 15px 0;
                border-radius: 5px;
                letter-spacing: 1px;
            }}
            .watermark-container {{
                margin-top: 35px;
                padding-top: 15px;
                border-top: 1px dashed #b58900;
                text-align: right;
            }}
            .watermark-text {{
                font-family: 'Courier New', Courier, monospace;
                font-size: 14px;
                font-weight: bold;
                color: #856404;
                letter-spacing: 2px;
                opacity: 0.85;
            }}
            .watermark-sub {{
                font-size: 10px;
                color: #888;
                letter-spacing: 1px;
                font-family: sans-serif;
            }}
            .print-btn {{
                background-color: #28a745;
                color: white;
                border: none;
                padding: 12px 24px;
                font-size: 16px;
                font-weight: bold;
                border-radius: 5px;
                cursor: pointer;
                width: 100%;
                box-shadow: 0 2px 5px rgba(0,0,0,0.2);
                transition: 0.3s;
            }}
            .print-btn:hover {{
                background-color: #218838;
            }}
        </style>
        </head>
        <body>
            <div class="cert-container" id="printable-area">
                <div class="cert-title">📜 Sertifikat Primbon Jawa 📜</div>
                <div class="cert-subtitle">Hasil Analisis Perhitungan Weton Digital</div>
                
                <table class="cert-table">
                    <tr><td class="label">Tanggal Lahir</td><td>: {tgl_pilih.strftime('%d/%m/%Y')}</td></tr>
                    <tr><td class="label">Waktu Kelahiran</td><td>: {waktu.split('(')[0]}</td></tr>
                </table>
                
                <div class="badge-weton">{weton_lengkap.upper()}</div>
                
                <table class="cert-table">
                    <tr><td class="label">Jumlah Neptu</td><td>: <b>{total_neptu}</b> (Hari {n_h} + Pasaran {n_p})</td></tr>
                    <tr><td class="label">Kepemimpinan</td><td>: {karakter_skor['Kepemimpinan']}/100</td></tr>
                    <tr><td class="label">Kesabaran</td><td>: {karakter_skor['Kesabaran']}/100</td></tr>
                    <tr><td class="label">Kejujuran</td><td>: {karakter_skor['Kejujuran']}/100</td></tr>
                    <tr><td class="label">Keuangan / Rezeki</td><td>: {karakter_skor['Keuangan / Rezeki']}/100</td></tr>
                    <tr><td class="label">✨ Hari Baik</td><td>: {daftar_baik[0]} & {daftar_baik[1]}</td></tr>
                    <tr><td class="label">⚠️ Hari Nahas</td><td>: {daftar_nahas[0]} & {daftar_nahas[1]}</td></tr>
                </table>
                
                <!-- BLOK WATERMARK / SIGNATURE DIGITAL -->
                <div class="watermark-container">
                    <div class="watermark-text">✍️ JARULISME.DEV-APP</div>
                    <div class="watermark-sub">Verified Digital Signature</div>
                </div>
                
                <div class="no-print" style="margin-top: 25px;">
                    <button class="print-btn" onclick="window.print()">📥 Download / Cetak Sebagai PDF</button>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Tampilkan komponen sertifikat HTML interaktif di Streamlit
        st.components.v1.html(html_sertifikat, height=620, scrolling=False)

# ================= TAB 2: CEK KECOCOKAN JODOH =================
with menu[1]:
    st.subheader("👩‍❤️‍👨 Analisis Keserasian Pasangan")
    st.markdown("Masukkan tanggal lahir Anda dan Pasangan Anda untuk melihat tingkat kecocokan berdasarkan kitab Primbon Jawa.")
    
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.markdown("### **Data Anda:**")
        tgl_p1 = st.date_input("Tanggal Lahir Anda:", value=dt.date(2000, 1, 1), min_value=min_date, max_value=max_date, format="DD/MM/YYYY", key="jodoh_tgl1")
        waktu_p1 = st.radio("Waktu Lahir Anda:", ("Siang", "Malam (Habis Magrib)"), key="jodoh_waktu1")
        
    with col_p2:
        st.markdown("### **Data Pasangan:**")
        tgl_p2 = st.date_input("Tanggal Lahir Pasangan:", value=dt.date(2000, 1, 1), min_value=min_date, max_value=max_date, format="DD/MM/YYYY", key="jodoh_tgl2")
        waktu_p2 = st.radio("Waktu Lahir Pasangan:", ("Siang", "Malam (Habis Magrib)"), key="jodoh_waktu2")
        
    if st.button("🔮 Hitung Keserasian Jodoh", type="primary", use_container_width=True):
        h1, p1, n_h1, n_p1 = hitung_weton_core(tgl_p1, "Malam" in waktu_p1)
        nep1 = n_h1 + n_p1
        
        h2, p2, n_h2, n_p2 = hitung_weton_core(tgl_p2, "Malam" in waktu_p2)
        nep2 = n_h2 + n_p2
        
        total_neptu_jodoh = nep1 + nep2
        sisa_jodoh = total_neptu_jodoh % 8
        hasil_ramalan = PRIMBON_JODOH[sisa_jodoh]
        
        st.markdown("---")
        st.subheader("💘 Hasil Perhitungan Jodoh")
        st.info(f"**Weton Anda:** {h1} {p1} (Neptu {nep1})   |   **Weton Pasangan:** {h2} {p2} (Neptu {nep2})")
        
        st.warning(f"### Kategori Hasil: {hasil_ramalan['status']}")
        st.write(hasil_ramalan['arti'])
