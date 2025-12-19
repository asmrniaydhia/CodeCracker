from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import random, string
from .models import Pengguna, Kelas, AnggotaKelas, Kuis, HasilKuis, RincianJawaban,HasilEvaluasi, PeringkatFinal, SectionItem, ProgresItem  
from functools import wraps
import json
import time
from django.db.models import Max, Avg, Count, Q
from .utils import render_to_pdf
from .decorators import butuh_login_siswa 

# --- DECORATOR KHUSUS TANTANGAN ---
def butuh_login_siswa(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        # GANTI 'user_id' MENJADI 'id_pengguna'
        if 'id_pengguna' not in request.session:
            return redirect('login') 
        return function(request, *args, **kwargs)
    return wrap

# ==========================================
#  LOGIKA HELPER TANTANGAN (BARU)
# ==========================================

def cek_akses_stage(request, stage_ke):
    """
    Mengecek apakah user boleh mengakses stage tertentu berdasarkan session.
    """
    # Ambil progress terakhir dari session, default Stage 1
    max_stage = request.session.get('max_stage', 1)
    if max_stage < stage_ke:
        return False
    return True

@butuh_login_siswa
def unlock_next_stage(request, stage_selesai):
    """
    Fungsi ini dipanggil ketika siswa MENYELESAIKAN sebuah stage.
    Misal: Selesai stage 1 -> panggil url unlock/1 -> system buka stage 2.
    """
    current_max = request.session.get('max_stage', 1)
    
    # Hanya naikkan level jika stage yang diselesaikan adalah stage terakhir yg terbuka
    if stage_selesai >= current_max:
        request.session['max_stage'] = stage_selesai + 1
        request.session.modified = True
        
    messages.success(request, f"Hebat! Stage {stage_selesai + 1} terbuka.")
    return redirect('tantangan')

# ---------- EVALUASI ----------
@butuh_login_siswa
def evaluasi_petunjuk(request):
    """
    Menampilkan halaman petunjuk evaluasi. 
    Jika sudah selesai (Evaluasi tidak bisa diulang), langsung alihkan ke hasil nilai detail.
    """
    siswa = get_logged_in_user(request)
    if not siswa:
        return redirect('login')
    
    # 1. Cek apakah sudah ada hasil evaluasi untuk siswa ini
    # Ambil hasil yang paling baru (asumsi hanya ada satu hasil permanen)
    hasil_evaluasi = HasilEvaluasi.objects.filter(id_siswa=siswa).order_by('-id_hasil_evaluasi').first()
    
    if hasil_evaluasi:
        # **LOGIKA BYPASS**: Jika sudah selesai, langsung redirect ke halaman nilai
        return redirect('evaluasi_nilai_detail', hasil_id=hasil_evaluasi.id_hasil_evaluasi)
    else:
        # 2. Ambil Status Sidebar (Jika belum selesai, untuk sidebar)
        sidebar_status = get_sidebar_status(siswa.id_pengguna)
        
        context = {
            'sidebar_status': sidebar_status
        }
        
        # 3. Kirim ke template (evaluasi.html)
        return render(request, "evaluasi/evaluasi.html", context)


def evaluasi_pengerjaan(request):
    return render(request, "evaluasi/evaluasi_pengerjaan.html")

# ⚠️ DATA SOAL EVALUASI UNTUK VALIDASI SERVER
EVALUASI_QUESTIONS_SERVER = [
    {"question":"Saat kamu melakukan login ke akun media sosial melalui jaringan Wi-Fi publik yang tidak aman, risiko pencurian data pribadi oleh peretas dapat dikurangi jika aplikasi tersebut telah mengubah kata sandimu menjadi deretan karakter acak yang disebut ....","options":["Plain Text","Glosarium","Ciphertext","Password asli"],"correct":2,"type":"mcq"},
    {"question":"Di sebuah perusahaan, seorang admin sistem menerapkan enkripsi pada data karyawan yang disimpan di dalam hard drive agar jika perangkat tersebut dicuri, pencuri tetap tidak bisa membaca informasi sensitif karena data berada dalam kondisi ....","options":["Data in transit","Data at rest","Data in process","Data deleted"],"correct":1,"type":"mcq"},
    {"question":"Seorang detektif menemukan potongan kertas berisi instruksi militer kuno yang menggunakan metode substitution cipher. Prinsip kerja algoritma ini adalah mengganti setiap huruf asli dengan huruf lain berdasarkan ....","options":["Panjang kalimat","Simbol acak","Posisi tetap dalam alfabet","Frekuensi suara"],"correct":2,"type":"mcq"},
    {"question":"Jika kamu ingin mengirim pesan rahasia \"AMAN\" menggunakan kunci pergeseran Geser 2 ke Kanan, maka hasil perubahan huruf yang diterima adalah ....","options":["BOCP","CPBQ","COCP","BNDO"],"correct":2,"type":"mcq"},
    {"question":"Kata \"BUKU\" berubah menjadi \"EXNX\". Hal ini menunjukkan bahwa pengirim pesan menggunakan kunci pergeseran sebanyak ....","options":["1 langkah ke kanan","2 langkah ke kanan","3 langkah ke kanan","4 langkah ke kanan"],"correct":2,"type":"mcq"},
    {"question":"Dalam sebuah aktivitas simulasi, kamu harus mengenkripsi kata \"ZOO\" dengan kunci Geser 1 ke Kanan. Setelah huruf Z berputar kembali ke awal alfabet, hasil sandi yang benar adalah ....","options":["APP","BPP","YNN","AQQ"],"correct":0,"type":"mcq"},
    {"question":"Seorang siswa menerima pesan sandi \"EDCB\" dan mengetahui bahwa pengirim menggunakan kunci Geser 1 ke Kanan. Untuk mendapatkan kembali pesan asli \"DCBA\", siswa tersebut harus menerapkan ....","options":["Enkripsi 1 langkah ke kanan","Dekripsi 1 langkah ke kiri","Enkripsi 2 langkah ke kanan","Dekripsi 2 langkah ke kiri"],"correct":1,"type":"mcq"},
    {"question":"Kamu mendapatkan ciphertext berupa huruf \"D\" dan mengetahui bahwa kunci enkripsi aslinya adalah Geser 3 ke Kanan. Pesan asli setelah digeser manual 3 langkah ke kiri adalah ....","options":["A","B","G","H"],"correct":0,"type":"mcq"},
    {"question":"Saat seorang analis keamanan tidak mengetahui kunci yang digunakan pada sebuah pesan sandi Caesar, ia mencoba seluruh kemungkinan pergeseran dari 1 hingga 25 secara sistematis. Teknik ini dikenal dengan ....","options":["Substitusi","Algoritma","Brute Force","Glosarium"],"correct":2,"type":"mcq"},
    {"question":"Penggunaan Caesar Cipher di era digital saat ini dianggap tidak cukup aman untuk melindungi data perbankan karena peretas dapat memecahkan kodenya dengan sangat cepat menggunakan teknik ....","options":["Manual","Acak","Brute Force","Rahasia"],"correct":2,"type":"mcq"},

    {"question":"Proses mengubah pesan asli (Plain Text) menjadi pesan rahasia (Ciphertext) disebut dengan proses ....","answer":"enkripsi","type":"fill"},
    {"question":"Pesan asli yang masih dalam wujud orisinal, mudah dibaca, dan dapat dipahami oleh siapa saja disebut dengan ....","answer":"plaintext","type":"fill"},
    {"question":"Pada algoritma Caesar Cipher, elemen rahasia yang menentukan seberapa jauh posisi alfabet akan digeser disebut dengan ....","answer":"kunci","type":"fill"},
    {"question":"Jika proses enkripsi menggunakan arah kanan, maka menurut Aturan Emas proses dekripsi harus menggunakan arah ....","answer":"kiri","type":"fill"},
    {"question":"Teknik pemecahan sandi dengan mencoba semua kemungkinan pergeseran alfabet hingga menemukan kata yang bermakna disebut ....","answer":"brute force","type":"fill"}
]



# views.py (Revisi fungsi simpan_evaluasi_nilai)

@require_POST
def simpan_evaluasi_nilai(request):
    siswa = get_logged_in_user(request) # Asumsikan helper ini ada
    if not siswa:
        messages.error(request, "Anda harus login untuk menyimpan hasil evaluasi.")
        return redirect("login")

    # ASUMSI: EVALUASI_QUESTIONS_SERVER sudah didefinisikan (misalnya, list of dict)
    questions = EVALUASI_QUESTIONS_SERVER
    total_soal = len(questions)

    waktu_pengerjaan_detik = int(request.POST.get("waktu_pengerjaan", 0))

    # 1. Hitung Nilai Evaluasi
    skor_sebenarnya = 0
    total_benar = 0 
    poin_per_soal = 100 // total_soal 
    
    # Logika Perhitungan Skor (diasumsikan sudah benar)
    for i, q in enumerate(questions):
        q_num = i + 1
        jawaban_siswa = request.POST.get(f"jawaban_{q_num}", "").strip()
        is_benar = False
        
        # Logika pengecekan MCQ dan Fill-in
        if q["type"] == "mcq":
            jawaban_benar = q["options"][q["correct"]]
            is_benar = (jawaban_siswa == jawaban_benar)
        elif q["type"] == "fill":
            jawaban_benar = q["answer"]
            is_benar = (jawaban_siswa.lower() == jawaban_benar.lower())

        if is_benar:
            skor_sebenarnya += poin_per_soal
            total_benar += 1
            
    # Koreksi skor agar genap 100 jika ada sisa pembagian
    if total_soal > 0:
        skor_sebenarnya += (100 % total_soal) 
    
    # 2. Simpan Hasil Evaluasi Ringkasan
    hasil_evaluasi_obj = HasilEvaluasi.objects.create(
        id_siswa=siswa,
        nilai=skor_sebenarnya,
        total_benar=total_benar,
        waktu_evaluasi_detik=waktu_pengerjaan_detik,
    )

    # 3. LOGIKA UPDATE PROGRES (Selalu Selesai)
    try:
        item_evaluasi = SectionItem.objects.filter(
            id_section__nama_section__iexact='Evaluasi', 
            nama_item__iexact='Evaluasi Akhir'           
        ).first()
        
        if item_evaluasi:
            # Update status menjadi 'selesai' tanpa perlu cek skor
            ProgresItem.objects.get_or_create(
                id_siswa=siswa, 
                id_item=item_evaluasi,
            )
            ProgresItem.objects.filter(id_siswa=siswa, id_item=item_evaluasi).update(status='selesai')
            
    except Exception as e:
        # Menangani error update progres secara pasif
        pass

    # 4. Redirect ke halaman nilai
    # Ini yang membuat halaman hasil muncul setelah submit, seperti kuis.
    return redirect("evaluasi_nilai_detail", hasil_id=hasil_evaluasi_obj.id_hasil_evaluasi)


# --- Fungsi untuk Menampilkan Nilai Evaluasi ---
def evaluasi_nilai_detail(request, hasil_id):
    """Menampilkan detail nilai evaluasi dengan konteks sidebar."""
    siswa = get_logged_in_user(request) 
    if not siswa:
        return redirect("login")
    
    # ASUMSI: EVALUASI_QUESTIONS_SERVER sudah didefinisikan (Total soal 15)
    questions = EVALUASI_QUESTIONS_SERVER 
    
    try:
        # Ambil hasil evaluasi berdasarkan ID dan pastikan milik siswa yang login
        hasil_evaluasi = HasilEvaluasi.objects.get(id_hasil_evaluasi=hasil_id, id_siswa=siswa)
        
        total_soal = len(questions) # Total soal 15
        jawaban_salah = total_soal - hasil_evaluasi.total_benar

        # Dapatkan Konteks Sidebar (PENTING)
        sidebar_context = get_sidebar_status(siswa.id_pengguna)

        context = {
            "hasil_evaluasi": hasil_evaluasi,
            "total_soal": total_soal,
            "jawaban_salah": jawaban_salah, 
            "nama_user": siswa.nama_lengkap, 
            "sidebar_status": sidebar_context, # Kirim status sidebar
        }
        
        if 'mode_fokus' in request.session:
            del request.session['mode_fokus']

        return render(request, "evaluasi/nilaiEval.html", context)

    except HasilEvaluasi.DoesNotExist:
        messages.error(request, "Hasil evaluasi tidak ditemukan atau bukan milik Anda.")
        return redirect("dashboard")

    except HasilEvaluasi.DoesNotExist:
        messages.error(request, "Hasil evaluasi tidak ditemukan atau bukan milik Anda.")
        return redirect("dashboard")

# ---------- KUIS ----------
def kuis_petunjuk(request):
    """
    Halaman petunjuk kuis.
    Memastikan sidebar sinkron dan mengecek apakah siswa sudah pernah mengerjakan.
    """
    # 1. Cek Login
    # Ganti 'get_logged_in_user' dengan logika manual jika helper belum diimport
    if 'id_pengguna' not in request.session:
        return redirect('login')
    
    # Ambil object user
    user_id = request.session.get('id_pengguna')
    try:
        siswa = Pengguna.objects.get(id_pengguna=user_id)
    except Pengguna.DoesNotExist:
        return redirect('login')

    jenis = request.GET.get("jenis")
    mode = request.GET.get("mode") # Menangkap parameter ?mode=ulangi

    # Validasi Jenis Kuis
    if jenis not in ["enkripsi", "caesar", "dekripsi"]:
        return render(request, "kuis/kuis.html", {"error": "Jenis kuis tidak valid."})

    # 2. LOGIKA REDIRECT KE HASIL (Jika sudah pernah & bukan mode ulangi)
    NAMA_KUIS_DB = {
        "enkripsi": "Kuis Enkripsi",
        "caesar": "Kuis Caesar Cipher",
        "dekripsi": "Kuis Dekripsi"
    }

    # Jika BUKAN sedang mengulang, cek apakah sudah ada nilai?
    if mode != 'ulangi':
        try:
            nama_db = NAMA_KUIS_DB.get(jenis)
            kuis_obj = Kuis.objects.get(nama_kuis=nama_db)
            
            # Cek apakah ada hasil kuis untuk siswa ini
            last_result = HasilKuis.objects.filter(id_siswa=siswa, id_kuis=kuis_obj).last()
            
            if last_result:
                # Jika sudah ada, lempar langsung ke halaman nilai
                return redirect('kuis_nilai_detail', hasil_id=last_result.id_hasil_kuis)
                
        except Kuis.DoesNotExist:
            pass 
        except Exception as e:
            print(f"Error cek history kuis: {e}")

    status_sidebar = get_sidebar_status(user_id) 

    context = {
        "jenis": jenis,
        "sidebar_status": status_sidebar  # <--- WAJIB DIKIRIM KE TEMPLATE
    }

    return render(request, "kuis/kuis.html", context)


def kuis_pengerjaan(request):
    """
    Halaman pengerjaan kuis.
    """
    # 1. Cek Login
    if 'id_pengguna' not in request.session:
        return redirect('login')

    jenis = request.GET.get("jenis")
    current_time_stamp = int(time.time())

    if jenis not in ["enkripsi", "caesar", "dekripsi"]:
        return render(
            request, "kuis/kuis.html", {"error": "Jenis kuis tidak valid."}
        )
    
    list_soal = QUIZ_QUESTIONS_SERVER.get(jenis, [])

    # 2. 👇 TAMBAHKAN INI: Ambil Status Sidebar
    user_id = request.session.get('id_pengguna')
    status_sidebar = get_sidebar_status(user_id)

    context = {
        "jenis": jenis,
        "time": current_time_stamp,
        "questions": list_soal,
        "sidebar_status": status_sidebar # 3. 👇 Kirim ke HTML
    }

    return render(request, "kuis/kuis_pengerjaan.html", context)


def get_logged_in_user(request):
    """Mengambil objek Pengguna dari session jika ada."""
    # GANTI 'user_id' MENJADI 'id_pengguna' (Sesuai login_view)
    user_id = request.session.get("id_pengguna") 
    if user_id:
        try:
            return Pengguna.objects.get(id_pengguna=user_id)
        except Pengguna.DoesNotExist:
            return None
    return None

# ⚠️ DATA SOAL KUIS UNTUK VALIDASI SERVER
QUIZ_QUESTIONS_SERVER={
    "enkripsi":[
        {"question":"Agus mengirimkan foto kartu pelajar berisi data sensitif melalui aplikasi chat dengan fitur End-to-End Encryption. Jika data disadap di tengah jalan, penyadap hanya akan melihat kode acak tidak bermakna yang disebut ....","options":["Plain Text","Password","Ciphertext","Glosarium"],"correct":2},
        {"question":"Saat membuka sebuah file dokumen di komputer sekolah, kamu hanya menemukan deretan karakter aneh seperti \"Xy29!#amZ\" yang tidak dapat dipahami. File tersebut sedang berada dalam wujud ....","options":["Pesan asli","Data orisinal","Ciphertext","Plain Text"],"correct":2},
        {"question":"Sebuah bank mengganti sebagian nomor rekening pada struk ATM menjadi tanda bintang (contoh: 123XXXX890). Tindakan ini merupakan penerapan prinsip ....","options":["Transparansi data","Kerahasiaan (confidentiality)","Kecepatan transaksi","Penghapusan data"],"correct":1},
        {"question":"Saat menggunakan Wi-Fi publik untuk aktivitas perbankan, risiko terbesar jika data tidak dienkripsi adalah data dikirimkan dalam bentuk ....","options":["Plain Text","Ciphertext","Kode rahasia","Algoritma"],"correct":0},
        {"question":"Dalam alur komunikasi digital, proses mengubah pesan asli menjadi kode acak menggunakan algoritma tertentu disebut ....","options":["Deskripsi","Dekripsi","Enkripsi","Glosarium"],"correct":2}
    ],
    "caesar":[
        {"question":"Pesan asli \"DUNIA\" dienkripsi dengan kunci Geser 3 ke Kanan. Hasil perubahannya adalah ....","options":["GVQLD","FWPKC","GXQLD","HWQLE"],"correct":2},
        {"question":"Kata \"DATA\" dienkripsi menggunakan kunci Geser 2 ke Kanan. Hasil alfabet sandinya adalah ....","options":["FCVD","FCVC","EBVB","GDWD"],"correct":1},
        {"question":"Jika huruf \"B\" berubah menjadi \"E\", maka pesan \"MUKA\" dengan kunci yang sama akan menjadi ....","options":["PXND","QYOE","OWMC","PVNC"],"correct":0},
        {"question":"Jika huruf \"K\" digeser 5 langkah ke kanan menjadi \"P\", maka hasil enkripsi kata \"BOLA\" adalah ....","options":["CPMA","DQNB","GTQF","FSPE"],"correct":2},
        {"question":"Jika huruf \"Z\" dienkripsi dengan Geser 1 ke Kanan, maka huruf hasilnya adalah ....","options":["A","B","Y","X"],"correct":0}
    ],
    "dekripsi":[
        {"question":"Pesan rahasia \"FDVD\" dienkripsi dengan Geser 3 ke Kanan. Untuk mendapatkan pesan asli, hasil dekripsinya adalah ....","options":["BOLA","CASA","DATA","GAGA"],"correct":1},
        {"question":"Dengan teknik Brute Force, kode \"PHVD\" menghasilkan kata \"MESA\" setelah dilakukan pergeseran sebanyak ....","options":["1 langkah ke kiri","2 langkah ke kiri","3 langkah ke kiri","4 langkah ke kiri"],"correct":2},
        {"question":"Pesan terenkripsi \"LUL\" diketahui menggunakan kunci Geser 1 ke Kanan. Pesan aslinya adalah ....","options":["MUM","KTK","JSK","LVL"],"correct":1},
        {"question":"Jika huruf sandi \"V\" berasal dari huruf asli \"T\", maka proses dekripsi dilakukan dengan menggeser ke kiri sebanyak ....","options":["1 langkah","2 langkah","3 langkah","4 langkah"],"correct":1},
        {"question":"Kode \"WKDQ\" setelah digeser 3 langkah ke kiri menghasilkan kata \"THANK\". Kunci enkripsi awal yang digunakan adalah ....","options":["Geser 1 ke Kanan","Geser 2 ke Kanan","Geser 3 ke Kanan","Geser 4 ke Kanan"],"correct":2}
    ]
}

KUIST_ID_MAP = {"enkripsi": 1, "caesar": 2, "dekripsi": 3}


# main/views.py

@require_POST
def simpan_kuis_nilai(request):
    siswa = get_logged_in_user(request)
    if not siswa:
        messages.error(request, "Anda harus login untuk menyimpan hasil kuis.")
        return redirect("login")

    jenis = request.POST.get("jenis")
    waktu_pengerjaan = int(request.POST.get("waktu_pengerjaan", 0))

    # PETA NAMA KUIS
    NAMA_KUIS_DB = {
        "enkripsi": "Kuis Enkripsi",
        "caesar": "Kuis Caesar Cipher",
        "dekripsi": "Kuis Dekripsi"
    }

    if jenis not in NAMA_KUIS_DB:
        messages.error(request, "Jenis kuis tidak valid.")
        return redirect("landing")

    try:
        nama_db = NAMA_KUIS_DB[jenis]
        kuis_obj = Kuis.objects.get(nama_kuis=nama_db)
    except Kuis.DoesNotExist:
        messages.error(request, f"Data kuis '{nama_db}' tidak ditemukan di database.")
        return redirect("dashboard")

    questions = QUIZ_QUESTIONS_SERVER.get(jenis, [])

    # 1. Hitung Skor
    skor_sebenarnya = 0
    rincian_jawaban_list = []

    for i, q in enumerate(questions):
        q_num = i + 1
        jawaban_siswa_text = request.POST.get(f"jawaban_{q_num}", "(kosong)")
        jawaban_benar_text = q["options"][q["correct"]]

        is_benar = jawaban_siswa_text == jawaban_benar_text
        if is_benar:
            skor_sebenarnya += 20 
        
        rincian_jawaban_list.append(
            RincianJawaban(
                id_pertanyaan_json=str(q_num),
                teks_pertanyaan=q["question"],
                jawaban_siswa=jawaban_siswa_text,
                jawaban_benar=jawaban_benar_text,
                is_benar=is_benar,
            )
        )

    # 2. Simpan Hasil Kuis
    existing_attempts = HasilKuis.objects.filter(id_siswa=siswa, id_kuis=kuis_obj).count()
    
    hasil_kuis_obj = HasilKuis.objects.create(
        id_siswa=siswa,
        id_kuis=kuis_obj,
        skor_kuis=skor_sebenarnya,
        waktu_kuis=waktu_pengerjaan,
        percobaan_kuis=existing_attempts + 1,
    )

    # 3. Simpan Rincian
    for rincian in rincian_jawaban_list:
        rincian.id_hasil_kuis = hasil_kuis_obj
    RincianJawaban.objects.bulk_create(rincian_jawaban_list)

    # 4. Update Progres Item (BUKA GEMBOK)
    # ⚠️ LOGIKA BARU: Hanya tandai 'selesai' jika NILAI >= 70 (KKM)
    KKM = 70
    if skor_sebenarnya >= KKM:
        try:
            item_materi = SectionItem.objects.filter(id_kuis=kuis_obj).first()
            if item_materi:
                ProgresItem.objects.get_or_create(
                    id_siswa=siswa, 
                    id_item=item_materi,
                    defaults={'status': 'selesai'}
                )
                ProgresItem.objects.filter(id_siswa=siswa, id_item=item_materi).update(status='selesai')
        except Exception as e:
            print(f"Gagal update progres kuis: {e}")

    return redirect("kuis_nilai_detail", hasil_id=hasil_kuis_obj.id_hasil_kuis)


def kuis_nilai_detail(request, hasil_id):
    siswa = get_logged_in_user(request)
    if not siswa:
        return redirect("login")

    try:
        hasil_kuis = HasilKuis.objects.get(id_hasil_kuis=hasil_id, id_siswa=siswa)
        rincian_jawaban = hasil_kuis.rincian_jawaban.all()

        jenis_kuis = hasil_kuis.id_kuis.nama_kuis.lower()
        
        # Inisialisasi jenis kuis pendek
        jenis_kuis_pendek = ""
        next_url_name = "dashboard"
        prev_url_name = "dashboard" 

        # Tentukan Link Selanjutnya, Sebelumnya, dan Jenis Kuis Pendek
        if "enkripsi" in jenis_kuis:
            jenis_kuis_pendek = "enkripsi"
            next_url_name = "caesar"        
            prev_url_name = "enkripsi"   
        elif "caesar" in jenis_kuis:
            jenis_kuis_pendek = "caesar"
            next_url_name = "dekripsi"
            prev_url_name = "aktivitas3"    
        elif "dekripsi" in jenis_kuis:
            jenis_kuis_pendek = "dekripsi"
            next_url_name = "evaluasi_petunjuk"
            prev_url_name = "aktivitas4"    

        correct_count = rincian_jawaban.filter(is_benar=True).count()
        is_lulus = hasil_kuis.skor_kuis >= 70

        # 👇 TAMBAHAN PENTING: Ambil Status Sidebar agar menu terbuka sesuai progres
        user_id = request.session.get('id_pengguna')
        status_sidebar = get_sidebar_status(user_id)

        context = {
            "hasil_kuis": hasil_kuis,
            "rincian_jawaban": rincian_jawaban,
            "correct_count": correct_count,
            "next_url_name": next_url_name,
            "prev_url_name": prev_url_name,
            "is_lulus": is_lulus,
            "jenis_kuis_pendek": jenis_kuis_pendek, 
            "sidebar_status": status_sidebar, 
        }
        return render(request, "kuis/nilaiKuis.html", context)

    except HasilKuis.DoesNotExist:
        messages.error(request, "Hasil kuis tidak ditemukan.")
        return redirect("dashboard")


# ---------- MATERI ----------
# main/views.py

def aktivitas1(request):
    if 'id_pengguna' not in request.session: 
        return redirect('login')
    
    user_id = request.session['id_pengguna']
    
    # 1. Ambil Status Sidebar (untuk menu gembok)
    sidebar_status = get_sidebar_status(user_id)

    # 2. Cek Status Pengerjaan Item Ini
    status_pengerjaan = "belum"
    try:
        # Cari Item "Aktivitas" di Section "Pengenalan"
        item_obj = SectionItem.objects.get(
            nama_item__iexact="Aktivitas",
            id_section__nama_section__iexact="Pengenalan"
        )
        
        # Cek di tabel Progres
        progres = ProgresItem.objects.filter(
            id_siswa__id_pengguna=user_id,
            id_item=item_obj
        ).first()
        
        if progres and progres.status == 'selesai':
            status_pengerjaan = "selesai"
            
    except SectionItem.DoesNotExist:
        print("Item Aktivitas (Pengenalan) tidak ditemukan di database")

    context = {
        'sidebar_status': sidebar_status,
        'status_pengerjaan': status_pengerjaan  # Kirim ke template
    }
    return render(request, 'dashboard/siswa/aktivitas1.html', context)

def aktivitas2(request):
    if 'id_pengguna' not in request.session: 
        return redirect('login')
    
    user_id = request.session['id_pengguna']
    
    # 1. Cek Status Gembok Sidebar (Kode Lama)
    sidebar_status = get_sidebar_status(user_id)
    if not sidebar_status['enkripsi_buka']:
        return redirect('dashboard')

    # 2. [BARU] Cek Apakah Item Ini Sudah Selesai?
    status_pengerjaan = "belum" # Default
    try:
        # Cari Item "Aktivitas" di Section "Enkripsi"
        item_obj = SectionItem.objects.get(
            nama_item__iexact="Aktivitas",
            id_section__nama_section__iexact="Enkripsi"
        )
        
        # Cek Progres User
        progres = ProgresItem.objects.filter(
            id_siswa__id_pengguna=user_id,
            id_item=item_obj
        ).first()
        
        if progres and progres.status == 'selesai':
            status_pengerjaan = "selesai"
            
    except SectionItem.DoesNotExist:
        print("Item tidak ditemukan di database")

    context = {
        'sidebar_status': sidebar_status,
        'status_pengerjaan': status_pengerjaan # Kirim ke HTML
    }
    return render(request, 'dashboard/siswa/aktivitas2.html', context)


def aktivitas3(request):
    if 'id_pengguna' not in request.session: 
        return redirect('login')
    
    user_id = request.session['id_pengguna']
    
    # 1. Cek Status Gembok Sidebar
    sidebar_status = get_sidebar_status(user_id)
    # Anda mungkin ingin menambahkan cek gembok di sini, misal:
    # if not sidebar_status['caesar_buka']: return redirect('dashboard')

    # 2. [BARU] Cek Apakah Item Ini Sudah Selesai?
    status_pengerjaan = "belum" # Default
    try:
        # Cari Item "Aktivitas" di Section "Caesar Cipher"
        item_obj = SectionItem.objects.get(
            nama_item__iexact="Aktivitas",
            id_section__nama_section__iexact="Caesar Cipher" # <- PENTING: Section Caesar Cipher
        )
        
        # Cek Progres User
        progres = ProgresItem.objects.filter(
            id_siswa__id_pengguna=user_id,
            id_item=item_obj
        ).first()
        
        if progres and progres.status == 'selesai':
            status_pengerjaan = "selesai"
            
    except SectionItem.DoesNotExist:
        print("Item Aktivitas Caesar Cipher tidak ditemukan di database")

    context = {
        'sidebar_status': sidebar_status,
        'status_pengerjaan': status_pengerjaan # Kirim ke HTML
    }
    return render(request, 'dashboard/siswa/aktivitas3.html', context)


# views.py (Ganti fungsi aktivitas4 dengan kode ini)

def aktivitas4(request):
    if 'id_pengguna' not in request.session: return redirect('login')
    
    user_id = request.session['id_pengguna']
    
    # 1. Cek Status Gembok Sidebar
    sidebar_status = get_sidebar_status(user_id)
    # Anda mungkin ingin menambahkan cek gembok di sini agar aktivitas tidak bisa diakses jika Bab Dekripsi belum terbuka.
    # if not sidebar_status['dekripsi_buka']: return redirect('dashboard')

    # 2. [BARU] Cek Apakah Item Ini Sudah Selesai?
    status_pengerjaan = "belum" # Default
    try:
        # Cari Item "Aktivitas" di Section "Dekripsi"
        item_obj = SectionItem.objects.get(
            nama_item__iexact="Aktivitas",
            id_section__nama_section__iexact="Dekripsi" # <- PENTING: Section Dekripsi
        )
        
        # Cek Progres User
        progres = ProgresItem.objects.filter(
            id_siswa__id_pengguna=user_id,
            id_item=item_obj
        ).first()
        
        if progres and progres.status == 'selesai':
            status_pengerjaan = "selesai"
            
    except SectionItem.DoesNotExist:
        print("Item Aktivitas Dekripsi tidak ditemukan di database. Pastikan seeder sudah dijalankan!")

    context = {
        'sidebar_status': sidebar_status,
        'status_pengerjaan': status_pengerjaan # Kirim ke HTML
    }
    return render(request, 'dashboard/siswa/aktivitas4.html', context)

def pengenalan_view(request):
    if 'id_pengguna' not in request.session: return redirect('login')
    
    context = {
        'sidebar_status': get_sidebar_status(request.session['id_pengguna'])
    }
    return render(request, 'dashboard/siswa/pengenalan.html', context)

def caesar(request):
    # 1. Cek Login
    siswa = get_logged_in_user(request) # atau logika cek session manual Anda
    if not siswa:
        return redirect('login')
    
    # 2. Ambil Status Sidebar
    user_id = request.session.get('id_pengguna')
    status_sidebar = get_sidebar_status(user_id)

    context = {
        'sidebar_status': status_sidebar
    }
    
    # 3. Render ke lokasi file BARU
    return render(request, 'dashboard/siswa/caesarcipher.html', context)

def caesar2(request):
    # 1. Cek Login
    siswa = get_logged_in_user(request) # atau logika cek session manual Anda
    if not siswa:
        return redirect('login')
    
    # 2. Ambil Status Sidebar
    user_id = request.session.get('id_pengguna')
    status_sidebar = get_sidebar_status(user_id)

    context = {
        'sidebar_status': status_sidebar
    }
    
    # 3. Render ke lokasi file BARU
    return render(request, 'dashboard/siswa/caesarcipher2.html', context)

def dekripsi(request):
    siswa = get_logged_in_user(request) # atau logika cek session manual Anda
    if not siswa:
        return redirect('login')
    
    # 2. Ambil Status Sidebar
    user_id = request.session.get('id_pengguna')
    status_sidebar = get_sidebar_status(user_id)

    context = {
        'sidebar_status': status_sidebar
    }
    
    # 3. Render ke lokasi file BARU
    return render(request, 'dashboard/siswa/dekripsi.html', context)

def dekripsi2(request):
    if 'id_pengguna' not in request.session: return redirect('login')
    
    context = {
        'sidebar_status': get_sidebar_status(request.session['id_pengguna'])
    }
    return render(request, 'dashboard/siswa/dekripsi2.html', context)

def enkripsi(request):
    if 'id_pengguna' not in request.session: return redirect('login')
    
    context = {
        'sidebar_status': get_sidebar_status(request.session['id_pengguna'])
    }
    return render(request, 'dashboard/siswa/enkripsi.html', context)

# ---------- TANTANGAN (LOGIKA DIPERBAIKI) ----------
@butuh_login_siswa
def tantangan(request):
    # Ambil stage terakhir dari session, jika tidak ada, mulai dari 1
    current_max_stage = request.session.get('max_stage', 1)
    
    context = {
        'max_stage': current_max_stage
    }
    return render(request, "tantangan/tantangan.html", context)

@butuh_login_siswa
def stage1(request):
    # Stage 1 selalu terbuka
    return render(request, "tantangan/stage1.html")

@butuh_login_siswa
def stage2(request):
    if not cek_akses_stage(request, 2):
        messages.warning(request, "Selesaikan Stage 1 terlebih dahulu!")
        return redirect('tantangan')
    return render(request, "tantangan/stage2.html")

@butuh_login_siswa
def stage3(request):
    if not cek_akses_stage(request, 3):
        messages.warning(request, "Stage ini masih terkunci!")
        return redirect('tantangan')
    return render(request, "tantangan/stage3.html")

@butuh_login_siswa
def stage4(request):
    if not cek_akses_stage(request, 4):
        messages.warning(request, "Stage ini masih terkunci!")
        return redirect('tantangan')
    return render(request, "tantangan/stage4.html")

@butuh_login_siswa
def stage5(request):
    if not cek_akses_stage(request, 5):
        messages.warning(request, "Stage ini masih terkunci!")
        return redirect('tantangan')
    return render(request, "tantangan/stage5.html")

@butuh_login_siswa
def stage6(request):
    if not cek_akses_stage(request, 6):
        messages.warning(request, "Stage ini masih terkunci!")
        return redirect('tantangan')
    return render(request, "tantangan/stage6.html")

@butuh_login_siswa
def stage7(request):
    if not cek_akses_stage(request, 7):
        messages.warning(request, "Stage ini masih terkunci!")
        return redirect('tantangan')
    return render(request, "tantangan/stage7.html")

@butuh_login_siswa
def stage8(request):
    if not cek_akses_stage(request, 8):
        messages.warning(request, "Stage ini masih terkunci!")
        return redirect('tantangan')
    return render(request, "tantangan/stage8.html")

@butuh_login_siswa
def stage9(request):
    if not cek_akses_stage(request, 9):
        messages.warning(request, "Stage ini masih terkunci!")
        return redirect('tantangan')
    return render(request, "tantangan/stage9.html")

@butuh_login_siswa
def stage10(request):
    if not cek_akses_stage(request, 10):
        messages.warning(request, "Stage ini masih terkunci!")
        return redirect('tantangan')
    return render(request, "tantangan/stage10.html")

# ---------- HALAMAN UMUM ----------
def landing(request):
    return render(request, "landing.html")

def leaderboard(request):
    return render(request, "tantangan/leaderboard.html")

@butuh_login_siswa
@require_POST
def simpan_skor_final_view(request):
    user_id = request.session.get('id_pengguna')
    try:
        siswa_sekarang = Pengguna.objects.get(id_pengguna=user_id)
        data = json.loads(request.body)
        skor_baru = int(data.get('total_skor', 0))
        waktu_baru = int(data.get('total_waktu', 0))

        obj, created = PeringkatFinal.objects.get_or_create(siswa=siswa_sekarang)

        updated = False
        if created:
            obj.total_skor = skor_baru
            obj.total_waktu_detik = waktu_baru
            updated = True
        else:
            if skor_baru > obj.total_skor: updated = True
            elif skor_baru == obj.total_skor and waktu_baru < obj.total_waktu_detik: updated = True
            
        if updated:
            obj.total_skor = skor_baru
            obj.total_waktu_detik = waktu_baru
            obj.save()
            return JsonResponse({'status': 'sukses', 'message': 'Rekor baru!'})
        else:
            return JsonResponse({'status': 'sudah_ada', 'message': 'Skor tersimpan.'})

    except Exception as e:
        return JsonResponse({"status": "gagal", "message": str(e)}, status=500)

@butuh_login_siswa
def leaderboard(request):
    peringkat_list = PeringkatFinal.objects.select_related('siswa').all().order_by('-total_skor', 'total_waktu_detik')
    context = {'peringkat_list': peringkat_list}
    return render(request, "tantangan/leaderboard.html", context)

def siswa_daftar(request):
    if request.method == 'POST':
        nama = request.POST.get('nama_lengkap')
        email_input = request.POST.get('email')
        sandi = request.POST.get('kata_sandi')
        konfirmasi = request.POST.get('konfirmasi_sandi')

        # 2. Validasi
        if sandi != konfirmasi:
            print("ERROR: Password tidak cocok!") # Debug
            messages.error(request, 'Kata sandi tidak cocok!')
            return render(request, 'auth/register_guru.html')

        if Pengguna.objects.filter(email=email_input).exists():
            print("ERROR: Email sudah ada!") # Debug
            messages.error(request, 'Email sudah terdaftar!')
            return render(request, 'auth/register_siswa.html')

        # 3. Simpan
        try:
            Pengguna.objects.create(
                nama_lengkap=nama,
                email=email_input,
                kata_sandi=sandi,
                peran='siswa'
            )
            messages.success(request, 'Akun kamu berhasil dibuat! Silakan masuk.')
            return redirect('login')
        except Exception as e:
            print(f"ERROR DATABASE: {e}") # Debug Penting!
            messages.error(request, f'Terjadi kesalahan: {e}')

    return render(request, 'auth/register_siswa.html')

def guru_daftar(request):
    if request.method == 'POST':
        nama = request.POST.get('nama_lengkap')
        email_input = request.POST.get('email')
        sandi = request.POST.get('kata_sandi')
        konfirmasi = request.POST.get('konfirmasi_sandi')

        # 2. Validasi
        if sandi != konfirmasi:
            print("ERROR: Password tidak cocok!") # Debug
            messages.error(request, 'Kata sandi tidak cocok!')
            return render(request, 'auth/register_guru.html')

        if Pengguna.objects.filter(email=email_input).exists():
            print("ERROR: Email sudah ada!") # Debug
            messages.error(request, 'Email sudah terdaftar!')
            return render(request, 'auth/register_guru.html')

        # 3. Simpan
        try:
            Pengguna.objects.create(
                nama_lengkap=nama,
                email=email_input,
                kata_sandi=sandi,
                peran='guru'
            )
            messages.success(request, 'Akun Guru berhasil dibuat! Silakan masuk.')
            return redirect('login')
        except Exception as e:
            print(f"ERROR DATABASE: {e}") # Debug Penting!
            messages.error(request, f'Terjadi kesalahan: {e}')

    return render(request, 'auth/register_guru.html')

def login_view(request):
    if request.method == 'POST':
        email_input = request.POST.get('email') 
        password_input = request.POST.get('password')

        try:
            # 1. Cari pengguna berdasarkan email
            user = Pengguna.objects.get(email=email_input)

            # 2. Cek Password (Plain text matching sesuai database anda)
            if user.kata_sandi == password_input:
                # 3. SUKSES: Simpan data ke SESSION (Kantung Saku Browser)
                request.session['id_pengguna'] = user.id_pengguna
                request.session['nama_lengkap'] = user.nama_lengkap
                request.session['peran'] = user.peran
                
                messages.success(request, f'Selamat datang, {user.nama_lengkap}!')
                
                # Redirect sesuai peran (Nanti bisa diarahkan ke dashboard khusus)
                return redirect('dashboard') 
            
            else:
                messages.error(request, 'Kata sandi salah!')
        
        except Pengguna.DoesNotExist:
            messages.error(request, 'Email tidak terdaftar!')

    return render(request, 'auth/login.html')

def logout_view(request):
    request.session.flush()
    return redirect('login')

def dashboard(request):
    # Cek session menggunakan 'id_pengguna' (sesuai login_view)
    if 'id_pengguna' not in request.session:
        return redirect('login')
    
    user_id = request.session['id_pengguna']
    role_user = request.session.get('peran')

    if role_user == 'guru':
        return render(request, 'dashboard/index.html')

    # Cek Siswa
    sudah_punya_kelas = AnggotaKelas.objects.filter(siswa_id=user_id).exists()

    if sudah_punya_kelas:
        # --- PERBAIKAN UTAMA DI SINI ---
        # Kita harus mengambil status gembok dan mengirimnya ke template
        context = {
            'sidebar_status': get_sidebar_status(user_id) 
        }
        return render(request, 'dashboard/index.html', context)
    else:
        return redirect('input_token')

def input_token_view(request):
    if 'id_pengguna' not in request.session:
        return redirect('login')

    user_id = request.session['id_pengguna']
    if AnggotaKelas.objects.filter(siswa_id=user_id).exists():
        return redirect('dashboard')

    if request.method == 'POST':
        token_input = request.POST.get('token_kelas')
        
        try:
            kelas_ditemukan = Kelas.objects.get(token=token_input)
            
            siswa_login = Pengguna.objects.get(id_pengguna=user_id)

            AnggotaKelas.objects.create(
                kelas=kelas_ditemukan,
                siswa=siswa_login
            )

            messages.success(request, f'Berhasil bergabung ke kelas {kelas_ditemukan.nama_kelas}!')
            return redirect('dashboard')
            
        except Kelas.DoesNotExist:
            messages.error(request, 'Token tidak ditemukan! Pastikan kode benar.')
        except Exception as e:
            messages.error(request, f'Terjadi kesalahan: {e}')

    return render(request, 'auth/input_token.html')

def generate_token(length=6):
    # Menghasilkan huruf besar + angka acak (Misal: 4F9JA2)
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def kelola_kelas(request):
    # 1. CEK LOGIN MANUAL (Sesuai style kode Anda)
    if 'id_pengguna' not in request.session:
        return redirect('login')

    # 2. CEK PERAN (Hanya Guru)
    if request.session.get('peran') != 'guru':
        messages.error(request, "Akses ditolak. Halaman ini khusus Guru.")
        return redirect('dashboard')

    id_guru = request.session['id_pengguna']
    obj_guru = get_object_or_404(Pengguna, id_pengguna=id_guru)

    # --- LOGIKA TAMBAH KELAS ---
    if request.method == 'POST':
        nama_kelas_input = request.POST.get('nama_kelas')
        
        # Cek apakah guru ini sudah punya kelas dengan nama yang sama (case-insensitive)
        cek_duplikat = Kelas.objects.filter(
            guru=obj_guru, 
            nama_kelas__iexact=nama_kelas_input
        ).exists()

        if cek_duplikat:
            # Kirim pesan error (nanti ditangkap SweetAlert)
            messages.error(request, f'Gagal! Kelas dengan nama "{nama_kelas_input}" sudah ada.')
            return redirect('kelola_kelas')

        # Jika lolos validasi, lanjut buat token dan simpan
        token_unik = generate_token()
        while Kelas.objects.filter(token=token_unik).exists():
            token_unik = generate_token()

        try:
            Kelas.objects.create(
                guru=obj_guru,
                nama_kelas=nama_kelas_input,
                token=token_unik
            )
            messages.success(request, 'Kelas berhasil dibuat!')
            return redirect('kelola_kelas')
        except Exception as e:
            messages.error(request, f'Gagal membuat kelas: {e}')

    # --- TAMPILKAN DATA ---
    daftar_kelas = Kelas.objects.filter(guru=obj_guru).order_by('-id_kelas')

    context = {
        'daftar_kelas': daftar_kelas
    }
    return render(request, 'dashboard/guru/data_kelas.html', context)


def hapus_kelas(request, id_kelas):
    # 1. CEK LOGIN MANUAL
    if 'id_pengguna' not in request.session:
        return redirect('login')

    if request.session.get('peran') != 'guru':
        return redirect('dashboard')
        
    try:
        # Pastikan hanya menghapus kelas milik guru yang sedang login
        kelas = Kelas.objects.get(id_kelas=id_kelas, guru__id_pengguna=request.session['id_pengguna'])
        kelas.delete()
        messages.success(request, 'Kelas berhasil dihapus.')
    except Kelas.DoesNotExist:
        messages.error(request, 'Kelas tidak ditemukan atau bukan milik Anda.')
    
    return redirect('kelola_kelas')


def edit_kelas(request, id_kelas):
    if 'id_pengguna' not in request.session:
        return redirect('login')

    if request.session.get('peran') != 'guru':
        return redirect('dashboard')
    
    # Ambil data kelas spesifik
    kelas_target = get_object_or_404(Kelas, id_kelas=id_kelas, guru__id_pengguna=request.session['id_pengguna'])

    if request.method == 'POST':
        nama_baru = request.POST.get('nama_kelas')
        
        kelas_target.nama_kelas = nama_baru
        kelas_target.save()
        
        messages.success(request, 'Nama kelas berhasil diperbarui!')
    
    return redirect('kelola_kelas')

def data_siswa(request):
    # 1. Cek Login & Peran
    if 'id_pengguna' not in request.session:
        return redirect('login')
    
    if request.session.get('peran') != 'guru':
        return redirect('dashboard')

    id_guru = request.session['id_pengguna']
    
    # 2. Ambil parameter Filter & Search dari URL (GET request)
    filter_kelas_id = request.GET.get('kelas') # ID kelas dari dropdown
    search_query = request.GET.get('q')        # Kata kunci pencarian nama

    # 3. Query Dasar: Ambil semua anggota kelas yang gurunya adalah user saat ini
    data_anggota = AnggotaKelas.objects.filter(kelas__guru__id_pengguna=id_guru).select_related('siswa', 'kelas')

    # 4. Terapkan Filter Kelas (Jika ada)
    if filter_kelas_id:
        data_anggota = data_anggota.filter(kelas__id_kelas=filter_kelas_id)

    # 5. Terapkan Pencarian Nama (Jika ada)
    if search_query:
        data_anggota = data_anggota.filter(siswa__nama_lengkap__icontains=search_query)

    # 6. Urutkan berdasarkan Nama Kelas lalu Nama Siswa
    data_anggota = data_anggota.order_by('kelas__nama_kelas', 'siswa__nama_lengkap')

    # 7. Ambil daftar semua kelas guru ini (Untuk isi opsi Dropdown Filter)
    daftar_kelas_guru = Kelas.objects.filter(guru__id_pengguna=id_guru).order_by('nama_kelas')

    context = {
        'data_anggota': data_anggota,
        'daftar_kelas_guru': daftar_kelas_guru,
        'selected_kelas': int(filter_kelas_id) if filter_kelas_id else None,
        'search_query': search_query
    }

    return render(request, 'dashboard/guru/data_siswa.html', context)

def hapus_anggota_kelas(request, id_anggota):
    # 1. Cek Login
    if 'id_pengguna' not in request.session:
        return redirect('login')
    
    # 2. Cek Peran Guru
    if request.session.get('peran') != 'guru':
        return redirect('dashboard')

    try:
        # 3. Cari data keanggotaan
        # Kita juga cek 'kelas__guru__id_pengguna' untuk keamanan
        # Supaya guru A tidak bisa menghapus siswa dari kelas milik guru B
        anggota = get_object_or_404(AnggotaKelas, 
                                    id_anggota=id_anggota, 
                                    kelas__guru__id_pengguna=request.session['id_pengguna'])
        
        nama_siswa = anggota.siswa.nama_lengkap
        nama_kelas = anggota.kelas.nama_kelas
        
        # 4. Hapus data (Siswa keluar dari kelas, tapi akun tetap ada)
        anggota.delete()
        
        messages.success(request, f'Berhasil mengeluarkan {nama_siswa} dari kelas {nama_kelas}.')
        
    except Exception as e:
        messages.error(request, 'Gagal menghapus siswa atau Anda tidak memiliki akses.')

    return redirect('data_siswa')

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import SectionItem, ProgresItem, Pengguna
import json

def get_sidebar_status(user_id):
    # Ambil semua item yang SUDAH SELESAI
    item_selesai = ProgresItem.objects.filter(
        id_siswa__id_pengguna=user_id,
        status='selesai'
    ).values_list('id_item__id_section__nama_section', 'id_item__nama_item')
    
    selesai_set = set(item_selesai) # Contoh: {('Pengenalan', 'Aktivitas'), ...}

    status = {
        'pengenalan_buka': True,
        
        # Syarat Buka Bab Enkripsi: Aktivitas di Pengenalan selesai
        'enkripsi_buka': ('Pengenalan', 'Aktivitas') in selesai_set,
        
        # Syarat Buka Kuis Enkripsi: Aktivitas di Enkripsi selesai
        'enkripsi_kuis_buka': ('Enkripsi', 'Aktivitas') in selesai_set,

        # Syarat Buka Bab Caesar: Kuis Enkripsi selesai
        'caesar_buka': ('Enkripsi', 'Kuis Enkripsi') in selesai_set,
        
        # Syarat Buka Kuis Caesar: Aktivitas di Caesar selesai
        'caesar_kuis_buka': ('Caesar Cipher', 'Aktivitas') in selesai_set,

        # Syarat Buka Bab Dekripsi: Kuis Caesar Cipher selesai
        'dekripsi_buka': ('Caesar Cipher', 'Kuis Caesar Cipher') in selesai_set,
        
        # Syarat Buka Kuis Dekripsi: Aktivitas di Dekripsi selesai
        'dekripsi_kuis_buka': ('Dekripsi', 'Aktivitas') in selesai_set,
        
        # Syarat Buka Evaluasi: Kuis Dekripsi selesai
        'evaluasi_buka': ('Dekripsi', 'Kuis Dekripsi') in selesai_set,
    }
    return status

# --- API SIMPAN PROGRES ---
@csrf_exempt
def update_progres_item(request):
    if request.method == 'POST' and 'id_pengguna' in request.session:
        try:
            data = json.loads(request.body)
            req_section = data.get('section')
            req_item = data.get('item')
            
            user_id = request.session['id_pengguna']
            siswa = Pengguna.objects.get(id_pengguna=user_id)

            # Cari Item di Database (iexact = tidak peduli huruf besar/kecil)
            item_target = SectionItem.objects.filter(
                id_section__nama_section__iexact=req_section, 
                nama_item__iexact=req_item
            ).first()

            if item_target:
                progres, created = ProgresItem.objects.get_or_create(
                    id_siswa=siswa,
                    id_item=item_target
                )
                progres.status = 'selesai'
                progres.save()
                
                return JsonResponse({'status': 'success', 'message': 'Tersimpan!'})
            else:
                print(f"GAGAL: {req_section} - {req_item} tidak ditemukan di DB")
                return JsonResponse({'status': 'error', 'message': 'Item tidak valid'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Akses ditolak'})

from django.db.models import Max

@butuh_login_siswa
def rekap_nilai_siswa(request):
    # 1. Cek Akses Guru
    if request.session.get('peran') != 'guru':
        return redirect('dashboard')

    id_guru = request.session['id_pengguna']
    
    # 2. Filter Kelas
    filter_kelas_id = request.GET.get('kelas')
    data_anggota = AnggotaKelas.objects.filter(kelas__guru__id_pengguna=id_guru).select_related('siswa', 'kelas')
    
    if filter_kelas_id:
        data_anggota = data_anggota.filter(kelas__id_kelas=filter_kelas_id)
        
    data_anggota = data_anggota.order_by('kelas__nama_kelas', 'siswa__nama_lengkap')

    # 3. Struktur Data
    rekap_list = []

    for anggota in data_anggota:
        siswa = anggota.siswa
        
        # --- Helper Function untuk Mengambil Data Per Kategori ---
        def get_quiz_data(keyword):
            # Ambil semua riwayat urut dari percobaan pertama
            histori = HasilKuis.objects.filter(
                id_siswa=siswa, 
                id_kuis__nama_kuis__icontains=keyword
            ).order_by('percobaan_kuis')
            
            # Cari percobaan TERBAIK (Skor Tertinggi, Waktu Tercepat)
            terbaik = histori.order_by('-skor_kuis', 'waktu_kuis').first()
            
            return {
                'histori': histori,
                'total_coba': histori.count(),
                'terbaik': terbaik, # Objek HasilKuis (bisa ambil skor & waktu)
            }

        # --- EVALUASI (Hanya 1 kali) ---
        hasil_eval = HasilEvaluasi.objects.filter(id_siswa=siswa).first()

        rekap_list.append({
            'siswa': siswa,
            'kelas': anggota.kelas.nama_kelas,
            'enkripsi': get_quiz_data("Enkripsi"),
            'caesar': get_quiz_data("Caesar"),
            'dekripsi': get_quiz_data("Dekripsi"),
            'evaluasi': hasil_eval
        })

    # Dropdown Kelas
    daftar_kelas_guru = Kelas.objects.filter(guru__id_pengguna=id_guru).order_by('nama_kelas')

    context = {
        'rekap_list': rekap_list,
        'daftar_kelas_guru': daftar_kelas_guru,
        'selected_kelas': int(filter_kelas_id) if filter_kelas_id else None,
    }

    return render(request, 'dashboard/guru/rekap_nilai.html', context)

@butuh_login_siswa
def hapus_nilai_siswa(request, id_siswa, jenis):
    # 1. Cek Akses Guru
    if request.session.get('peran') != 'guru':
        return redirect('dashboard')

    try:
        siswa = Pengguna.objects.get(id_pengguna=id_siswa)
        
        # 2. Logika Hapus Berdasarkan Jenis
        if jenis == 'evaluasi':
            # Hapus Evaluasi Akhir
            HasilEvaluasi.objects.filter(id_siswa=siswa).delete()
            # Opsional: Reset status progres jika perlu
            # ...
            messages.success(request, f"Data Evaluasi {siswa.nama_lengkap} berhasil direset.")
            
        else:
            # Hapus Kuis (Enkripsi, Caesar, Dekripsi)
            keyword_map = {
                'enkripsi': 'Enkripsi',
                'caesar': 'Caesar',
                'dekripsi': 'Dekripsi'
            }
            keyword = keyword_map.get(jenis)
            
            if keyword:
                # Hapus semua riwayat kuis tersebut
                HasilKuis.objects.filter(
                    id_siswa=siswa, 
                    id_kuis__nama_kuis__icontains=keyword
                ).delete()
                
                messages.success(request, f"Data Kuis {keyword} {siswa.nama_lengkap} berhasil direset.")

    except Exception as e:
        messages.error(request, f"Gagal menghapus data: {e}")

    # Redirect kembali ke rekap nilai
    return redirect('rekap_nilai_siswa')

@butuh_login_siswa
def halaman_download_per_kelas(request):
    if request.session.get('peran') != 'guru':
        return redirect('dashboard')

    id_guru = request.session['id_pengguna']
    jenis = request.GET.get('jenis', 'enkripsi') # Tangkap jenis dari URL
    
    daftar_kelas = Kelas.objects.filter(guru__id_pengguna=id_guru).order_by('nama_kelas')
    
    context = {
        'daftar_kelas': daftar_kelas,
        'jenis': jenis, # Kirim jenis ke template agar link downloadnya benar
        'judul_halaman': f"Download Nilai {jenis.title()}"
    }
    return render(request, 'dashboard/guru/list_download_kelas.html', context)

from .utils import render_to_pdf # Import helper yang tadi dibuat
from django.db.models import Max
import datetime

@butuh_login_siswa
def export_rekap_nilai_pdf(request):
    if request.session.get('peran') != 'guru':
        return redirect('dashboard')

    id_guru = request.session['id_pengguna']
    
    # 1. TANGKAP FILTER DARI URL
    jenis = request.GET.get('jenis', 'enkripsi')  # Default enkripsi jika tidak ada param
    filter_kelas_id = request.GET.get('kelas')    # Jika ada, berarti mode "Download Per Kelas"
    
    # Helper Format Waktu (Detik -> HH:MM:SS)
    def format_hms(seconds):
        if not seconds: return "00:00:00"
        m, s = divmod(int(seconds), 60)
        h, m = divmod(m, 60)
        return f"{h:02d}:{m:02d}:{s:02d}"

    # 2. JUDUL LAPORAN
    judul_map = {
        'enkripsi': 'Hasil Kuis Enkripsi',
        'caesar': 'Hasil Kuis Caesar Cipher',
        'dekripsi': 'Hasil Kuis Dekripsi',
        'evaluasi': 'Hasil Evaluasi Akhir'
    }
    judul_laporan = judul_map.get(jenis, 'Laporan Nilai')

    # 3. AMBIL DAFTAR KELAS GURU
    daftar_kelas = Kelas.objects.filter(guru__id_pengguna=id_guru).order_by('nama_kelas')
    
    # Jika mode "Per Kelas", filter hanya satu kelas itu saja
    if filter_kelas_id:
        daftar_kelas = daftar_kelas.filter(id_kelas=filter_kelas_id)
        # Update nama file agar spesifik
        if daftar_kelas.exists():
            judul_laporan += f" - {daftar_kelas.first().nama_kelas}"

    # 4. SUSUN DATA HIERARKI (KELAS -> SISWA)
    laporan_data = []

    for kelas in daftar_kelas:
        # Ambil siswa di kelas ini
        anggota_kelas = AnggotaKelas.objects.filter(kelas=kelas).select_related('siswa').order_by('siswa__nama_lengkap')
        
        list_siswa = []
        for idx, anggota in enumerate(anggota_kelas, 1):
            siswa = anggota.siswa
            
            # Cari Nilai Sesuai Jenis
            nilai = 0
            waktu_str = "00:00:00"
            percobaan = 0

            if jenis == 'evaluasi':
                res = HasilEvaluasi.objects.filter(id_siswa=siswa).first()
                if res:
                    nilai = res.nilai
                    waktu_str = format_hms(res.waktu_evaluasi_detik)
                    percobaan = 1 # Evaluasi cuma 1x
            else:
                # Kuis (Enkripsi/Caesar/Dekripsi)
                keyword = jenis.title() # "Enkripsi", "Caesar", "Dekripsi"
                if jenis == 'caesar': keyword = "Caesar" # Pastikan sesuai nama di DB

                # Ambil histori terbaik
                # Kita perlu objek lengkap untuk ambil waktu, bukan cuma Max skor
                histori = HasilKuis.objects.filter(
                    id_siswa=siswa, 
                    id_kuis__nama_kuis__icontains=keyword
                ).order_by('-skor_kuis', 'waktu_kuis') # Prioritas: Skor tinggi, Waktu cepat (kecil)
                
                terbaik = histori.first()
                total_coba = histori.count()

                if terbaik:
                    nilai = terbaik.skor_kuis
                    waktu_str = format_hms(terbaik.waktu_kuis)
                    percobaan = total_coba

            list_siswa.append({
                'no': idx,
                'nama': siswa.nama_lengkap,
                'nilai': nilai,
                'waktu': waktu_str,
                'percobaan': percobaan
            })

        # Masukkan ke list utama jika kelas ada siswanya (opsional: atau tetap tampilkan meski kosong)
        laporan_data.append({
            'nama_kelas': kelas.nama_kelas,
            'siswa_list': list_siswa
        })

    # 5. RENDER PDF
    context = {
        'judul_laporan': judul_laporan,
        'nama_guru': request.session.get('nama_lengkap'),
        'laporan_data': laporan_data,
        'tanggal_cetak': datetime.datetime.now()
    }

    pdf = render_to_pdf('dashboard/guru/pdf_rekap_nilai.html', context)
    
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = f"{judul_laporan.replace(' ', '_')}.pdf"
        content = f"inline; filename='{filename}'"
        response['Content-Disposition'] = content
        return response
    
    return HttpResponse("Gagal membuat PDF")

@butuh_login_siswa # Atau decorator manual jika untuk guru juga
def profil_view(request):
    # 1. Ambil data user yang sedang login
    user_id = request.session.get('id_pengguna')
    if not user_id:
        return redirect('login')
    
    try:
        pengguna = Pengguna.objects.get(id_pengguna=user_id)
    except Pengguna.DoesNotExist:
        return redirect('logout')

    # 2. Logika Ganti Password (POST)
    if request.method == 'POST':
        password_baru = request.POST.get('password_baru')
        
        if password_baru:
            # Langsung timpa password lama (Sesuai permintaan: tanpa konfirmasi/pass lama)
            pengguna.kata_sandi = password_baru
            pengguna.save()
            messages.success(request, 'Kata sandi berhasil diperbarui!')
        else:
            messages.error(request, 'Password tidak boleh kosong.')
        
        return redirect('profil')

    # 3. Tampilkan Halaman
    context = {
        'user': pengguna,
        # Ambil status sidebar agar menu tetap sinkron (khusus siswa)
        'sidebar_status': get_sidebar_status(user_id) if pengguna.peran == 'siswa' else None
    }
    return render(request, 'dashboard/profile.html', context)
    
# main/views.py (Pastikan ini menggantikan fungsi dashboard & index lama Anda)

@butuh_login_siswa
def dashboard(request):
    peran = request.session.get('peran')
    id_pengguna = request.session.get('id_pengguna')
    nama_lengkap = request.session.get('nama_lengkap')

    # ==========================
    # LOGIKA GURU (Tidak Berubah)
    # ==========================
    if peran == 'guru':
        total_kelas = Kelas.objects.filter(guru__id_pengguna=id_pengguna).count()
        siswa_guru_qs = AnggotaKelas.objects.filter(kelas__guru__id_pengguna=id_pengguna)
        total_siswa = siswa_guru_qs.count()
        
        evaluasi_qs = HasilEvaluasi.objects.filter(
            id_siswa__anggotakelas__kelas__guru__id_pengguna=id_pengguna
        )
        rata_rata_evaluasi = evaluasi_qs.aggregate(Avg('nilai'))['nilai__avg'] or 0
        siswa_remedial = evaluasi_qs.filter(nilai__lt=70).count()

        def get_materi_stats(keyword):
            if total_siswa == 0: return 0, 0
            base_qs = HasilKuis.objects.filter(
                id_siswa__anggotakelas__kelas__guru__id_pengguna=id_pengguna,
                id_kuis__nama_kuis__icontains=keyword
            )
            siswa_lulus = base_qs.values('id_siswa').annotate(max_skor=Max('skor_kuis')).filter(max_skor__gte=70).count()
            progress_persen = round((siswa_lulus / total_siswa) * 100, 1)
            
            data_max = base_qs.values('id_siswa').annotate(max_skor=Max('skor_kuis'))
            if data_max.exists():
                total_skor = sum(item['max_skor'] for item in data_max)
                avg_score = round(total_skor / data_max.count(), 1)
            else:
                avg_score = 0
            return progress_persen, avg_score

        prog_enkripsi, avg_enkripsi = get_materi_stats('Enkripsi')
        prog_caesar, avg_caesar = get_materi_stats('Caesar')
        prog_dekripsi, avg_dekripsi = get_materi_stats('Dekripsi')
        
        lulus_eval = evaluasi_qs.filter(nilai__gte=70).count()
        prog_eval = round((lulus_eval / total_siswa) * 100, 1) if total_siswa > 0 else 0

        top_siswa = evaluasi_qs.select_related('id_siswa').order_by('-nilai')[:5]

        context = {
            'role': 'guru',
            'nama_guru': nama_lengkap,
            'total_kelas': total_kelas,
            'total_siswa': total_siswa,
            'rata_rata_evaluasi': round(rata_rata_evaluasi, 1),
            'siswa_remedial': siswa_remedial,
            'materi': {
                'enkripsi': {'progress': prog_enkripsi, 'avg': avg_enkripsi},
                'caesar':   {'progress': prog_caesar,   'avg': avg_caesar},
                'dekripsi': {'progress': prog_dekripsi, 'avg': avg_dekripsi},
                'evaluasi': {'progress': prog_eval,     'avg': round(rata_rata_evaluasi, 1)}
            },
            'top_siswa': top_siswa,
        }
        return render(request, 'dashboard/index.html', context)


    # ==========================
    # LOGIKA SISWA
    # ==========================
    else:
        # 1. Info Kelas
        try:
            anggota = AnggotaKelas.objects.get(siswa__id_pengguna=id_pengguna)
            nama_kelas = anggota.kelas.nama_kelas
        except AnggotaKelas.DoesNotExist:
            nama_kelas = "Belum masuk kelas"
        
        # 2. Nilai Evaluasi Akhir
        try:
            hasil = HasilEvaluasi.objects.get(id_siswa__id_pengguna=id_pengguna)
            nilai_evaluasi = hasil.nilai
        except HasilEvaluasi.DoesNotExist:
            nilai_evaluasi = "-"

        # 3. DATA RIWAYAT PER KATEGORI (Dipisah-pisah)
        # Helper kecil untuk mengambil riwayat berdasarkan nama kuis
        def get_histori_kuis(keyword):
            return HasilKuis.objects.filter(
                id_siswa__id_pengguna=id_pengguna,
                id_kuis__nama_kuis__icontains=keyword
            ).order_by('percobaan_kuis') # Urutkan dari percobaan ke-1, 2, dst.

        histori_enkripsi = get_histori_kuis('Enkripsi')
        histori_caesar = get_histori_kuis('Caesar')
        histori_dekripsi = get_histori_kuis('Dekripsi')

        context = {
            'role': 'siswa',
            'nama_siswa': nama_lengkap,
            'kelas': nama_kelas,
            'nilai_evaluasi': nilai_evaluasi,
            
            # Kirim data yang sudah dipisah ke HTML
            'histori_enkripsi': histori_enkripsi,
            'histori_caesar': histori_caesar,
            'histori_dekripsi': histori_dekripsi,
            
            'sidebar_status': get_sidebar_status(id_pengguna)
        }
        return render(request, 'dashboard/index.html', context)
    
def index(request):
    return render(request, 'landing/index.html')

def pilihan_daftar(request):
    return render(request, 'auth/role_selection.html')

