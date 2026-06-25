import streamlit as st
from datetime import datetime, timedelta

# Setup halaman utama web app agar responsif di HP
st.set_page_config(
    page_title="Prediksi Weton & Watak Lahir", 
    page_icon="🔮", 
    layout="vertical"
)

# Judul Aplikasi Utama
st.title("🔮 Primbon Digital: Cari Hari Kelahiran & Weton")
st.markdown("Cek weton, neptu, watak, serta hari baik/nahas Anda berdasarkan kalender primbon Jawa kuno.")
st.markdown("---")

# 1. Nilai Neptu Hari dan Pasaran
NEPTU_HARI = {"Senin": 4, "Selasa": 3, "Rabu": 7, "Kamis": 8, "Jumat": 6, "Sabtu": 9, "Minggu": 5}
NEPTU_PASARAN = {"Legi": 5, "Pahing": 9, "Pon": 7, "Wage": 4, "Kliwon": 8}

# Daftar Hari dan Pasaran untuk Perhitungan Rotasi
DAFTAR_HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
DAFTAR_PASARAN = ["Legi", "Pahing", "Pon", "Wage", "Kliwon"]

# 2. Database Watak & Tabiat Detail
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

def cari_hari_baik_nahas(hari_lahir, pasaran_lahir):
    idx_h = DAFTAR_HARI.index(hari_lahir)
    idx_p = DAFTAR_PASARAN.index(pasaran_lahir)
    
    hari_nahas_1 = f"{DAFTAR_HARI[(idx_h + 3) % 7]} {DAFTAR_PASARAN[(idx_p + 3) % 5]}"
    hari_nahas_2 = f"{DAFTAR_HARI[(idx_h + 4) % 7]} {DAFTAR_PASARAN[(idx_p + 4) % 5]}"
    
    hari_baik_1 = f"{DAFTAR_HARI[(idx_h + 1) % 7]} {DAFTAR_PASARAN[(idx_p + 2) % 5]}"
    hari_baik_2 = f"{DAFTAR_HARI[(idx_h + 2) % 7]} {DAFTAR_PASARAN[(idx_p + 0) % 5]}"
    
    return [hari_nahas_1, hari_nahas_2], [hari_baik_1, hari_baik_2]

# --- AREA INPUT FORM (Ramah Tampilan Mobile/HP) ---
with st.container():
    st.subheader("📅 Data Kelahiran")
    
    # Input tanggal bawaan widget kalender (Default diset ke hari ini)
    tgl_pilih = st.date_input("Pilih Tanggal Lahir Anda:", datetime.now())
    
    # Input waktu siang/malam (Mengganti input teks manual menjadi tombol pilihan)
    waktu = st.radio(
        "Kapan Waktu Jam Kelahiran Anda?",
        ("Siang / Pagi / Sore (06.00 - 17.59 WIB)", "Malam Hari (Setelah Magrib / 18.00 - 05.59 WIB)")
    )

st.markdown("---")

# --- PROSES PERHITUNGAN LOGIKA ---
if tgl_pilih:
    # Salin objek datetime dasar
    tanggal_lahir = datetime.combine(tgl_pilih, datetime.min.time())
    tanggal_asli_str = tgl_pilih.strftime("%d-%m-%Y")

    # Jalankan logika pergeseran hari Jawa untuk kelahiran malam hari
    if "Malam Hari" in waktu:
        tanggal_lahir = tanggal_lahir + timedelta(days=1)
        keterangan_waktu = "Malam (Masuk Hari Berikutnya)"
    else:
        keterangan_waktu = "Siang"

    # Algoritma Patokan 1 Januari 1900 asli milik Anda
    tanggal_patokan = datetime(1900, 1, 1)
    selisih_hari = (tanggal_lahir - tanggal_patokan).days

    index_hari_baru = (0 + selisih_hari) % 7
    index_pasaran_baru = (1 + selisih_hari) % 5

    hari_weton = DAFTAR_HARI[index_hari_baru]
    pasaran_weton = DAFTAR_PASARAN[index_pasaran_baru]
    weton_lengkap = f"{hari_weton} {pasaran_weton}"

    # Hitung Jumlah Neptu
    n_hari = NEPTU_HARI[hari_weton]
    n_pasaran = NEPTU_PASARAN[pasaran_weton]
    total_neptu = n_hari + n_pasaran

    # Ekstrak data watak
    watak_data = PRIMBON_WATAK_DETAIL.get(weton_lengkap, {"positif": "Belum terdaftar.", "negatif": "Belum terdaftar."})
    daftar_nahas, daftar_baik = cari_hari_baik_nahas(hari_weton, pasaran_weton)

    # --- TAMPILAN OUTPUT FINAL (Sangat Rapi di HP) ---
    st.subheader("📊 Hasil Analisis Primbon")
    
    # Ringkasan data utama
    st.success(f"**Weton Anda: {weton_lengkap}**")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Tanggal Input", value=tanggal_asli_str)
        st.write(f"⏱️ **Waktu:** {keterangan_waktu}")
    with col2:
        st.metric(label="Total Angka Neptu", value=str(total_neptu))
        st.write(f"🔢 **Detail:** {hari_weton} ({n_hari}) + {pasaran_weton} ({n_pasaran})")
        
    st.markdown("---")
    
    # Bagian Watak & Karakter menggunakan Expander agar hemat ruang layar HP
    with st.expander("🔮 Watak & Tabiat (Menurut Primbon)", expanded=True):
        st.markdown("##### 🟩 Sisi Positif / Kelebihan:")
        st.write(watak_data['positif'])
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("##### 🟥 Sisi Negatif / Kekurangan:")
        st.write(watak_data['negatif'])

    # Bagian Peruntungan Kalender Jawa
    st.markdown("### 📅 Kalender Peruntungan Jawa")
    
    st.error(f"⚠️ **Hari Nahas Anda:** {daftar_nahas[0]} & {daftar_nahas[1]}")
    st.caption("Sebaiknya hindari hari-hari ini untuk mengadakan urusan besar, transaksi penting, maupun hajat pernikahan.")
    
    st.info(f"✨ **Hari Baik Anda:** {daftar_baik[0]} & {daftar_baik[1]}")
    st.caption("Sangat baik digunakan untuk memulai usaha baru, melakukan perjalanan jauh, atau membuka hajat acara.")