from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

from .models import Pengguna, Kuis, HasilKuis, RincianJawaban   
from .models import HasilEvaluasi 
from .models import PeringkatFinal

import json
import time


# ---------- EVALUASI ----------
def evaluasi_petunjuk(request):
    return render(request, "evaluasi/evaluasi.html")


def evaluasi_pengerjaan(request):
    return render(request, "evaluasi/evaluasi_pengerjaan.html")

# ⚠️ DATA SOAL EVALUASI UNTUK VALIDASI SERVER
EVALUASI_QUESTIONS_SERVER = [
    # 🔹 PILIHAN GANDA (MCQ)
    {
        "question": "Enkripsi disebut berhasil jika …",
        "options": [
            "Ciphertext tidak dapat dimengerti tanpa kunci",
            "Plaintext dan ciphertext memiliki arti yang sama",
            "Semua orang bisa membaca ciphertext",
            "Pesan berubah tetapi tetap mudah ditebak",
        ],
        "correct": 0,  # Index 0 adalah jawaban benar
        "type": "mcq",
    },
    {
        "question": "Caesar Cipher termasuk kriptografi simetris karena …",
        "options": [
            "Menggunakan dua kunci berbeda",
            "Kunci enkripsi dan dekripsi sama",
            "Tidak membutuhkan kunci",
            "Menggunakan kunci acak setiap kali",
        ],
        "correct": 1,
        "type": "mcq",
    },
    {
        "question": "Gunakan kunci 3 untuk mengenkripsi kata “DATA”.",
        "options": ["GDXD", "EDWD", "FDXD", "GDWD"],
        "correct": 3,
        "type": "mcq",
    },
    {
        "question": "Dekripsilah ciphertext “WKH” dengan kunci 3.",
        "options": ["THE", "QEB", "ZKH", "TXE"],
        "correct": 0,
        "type": "mcq",
    },
    {
        "question": "Seseorang mengenkripsi pesan “SEHAT” dengan kunci 5, tetapi penerima melakukan dekripsi dengan kunci 4. Apa akibatnya?",
        "options": [
            "Pesan tetap terbaca benar",
            "Pesan rusak karena pergeseran tidak sesuai",
            "Pesan berubah menjadi plaintext semula",
            "Pesan hilang seluruhnya",
        ],
        "correct": 1,
        "type": "mcq",
    },
    {
        "question": "Mengapa Caesar Cipher dianggap lemah dari sisi keamanan modern?",
        "options": [
            "Karena terlalu banyak kunci yang mungkin",
            "Karena hasil enkripsinya selalu sama",
            "Karena hanya memiliki 25 kemungkinan kunci",
            "Karena tidak bisa mengenkripsi angka",
        ],
        "correct": 2,
        "type": "mcq",
    },
    {
        "question": "Dalam komunikasi digital, dekripsi dilakukan oleh pihak …",
        "options": ["Pengirim", "Server", "Penerima", "Penyedia layanan"],
        "correct": 2,
        "type": "mcq",
    },
    {
        "question": "Urutan yang benar dari proses komunikasi aman adalah …",
        "options": [
            "Dekripsi → Enkripsi → Pengiriman",
            "Enkripsi → Pengiriman → Dekripsi",
            "Pengiriman → Dekripsi → Enkripsi",
            "Enkripsi → Dekripsi → Pengiriman",
        ],
        "correct": 1,
        "type": "mcq",
    },
    {
        "question": "Seorang siswa menulis ciphertext “YMNX NX F YJXY” hasil dari plaintext “THIS IS A TEST”. Kunci yang digunakan adalah …",
        "options": ["2", "3", "4", "5"],
        "correct": 3,
        "type": "mcq",
    },
    {
        "question": "Ciphertext “JCU” jika didekripsi dengan kunci 2 menjadi “HAS”. Jika ingin mengirim kembali pesan yang sama, tetapi hasil ciphertext-nya berbeda, maka tindakan yang paling logis adalah …",
        "options": [
            "Mengganti algoritma enkripsi",
            "Mengubah posisi huruf secara acak tanpa kunci",
            "Menambah kunci menjadi 4",
            "Menghapus proses dekripsi",
        ],
        "correct": 0,
        "type": "mcq",
    },
    # 🔹 ISIAN SINGKAT (FILL)
    {
        "question": "Proses mengubah ciphertext menjadi bentuk asli disebut ____________.",
        "answer": "Dekripsi",
        "type": "fill",
    },
    {
        "question": "Enkripsilah “KOMPUTER” dengan kunci 2 → hasil ciphertext: ____________.",
        "answer": "MQORWVGT",
        "type": "fill",
    },
    {
        "question": "Dekripsilah ciphertext “ZRUOG” dengan kunci 3 → plaintext: ____________.",
        "answer": "WORLD",
        "type": "fill",
    },
    {
        "question": "Jumlah maksimum kemungkinan kunci dalam Caesar Cipher adalah ____________.",
        "answer": "25",
        "type": "fill",
    },
    {
        "question": "Dalam Caesar Cipher, huruf digeser sejauh jumlah langkah yang disebut ____________.",
        "answer": "Kunci",
        "type": "fill",
    },
]


@require_POST
def simpan_evaluasi_nilai(request):
    siswa = get_logged_in_user(request)
    if not siswa:
        messages.error(request, "Anda harus login untuk menyimpan hasil evaluasi.")
        return redirect("login")

    questions = EVALUASI_QUESTIONS_SERVER
    total_soal = len(questions)

    # ⚠️ AMBIL WAKTU PENGERJAAN DARI POST
    # Asumsi frontend mengirim data waktu (misal dari JavaScript) dengan nama 'waktu_pengerjaan'
    waktu_pengerjaan_detik = int(request.POST.get("waktu_pengerjaan", 0))

    # 1. Hitung Nilai Evaluasi di Server
    skor_sebenarnya = 0
    total_benar = 0 # ⚠️ VARIABEL BARU
    poin_per_soal = 100 // total_soal 
    
    for i, q in enumerate(questions):
        q_num = i + 1
        jawaban_siswa = request.POST.get(f"jawaban_{q_num}", "").strip()
        is_benar = False
        
        if q["type"] == "mcq":
            jawaban_benar = q["options"][q["correct"]]
            is_benar = (jawaban_siswa == jawaban_benar)
        elif q["type"] == "fill":
            jawaban_benar = q["answer"]
            is_benar = (jawaban_siswa.lower() == jawaban_benar.lower())

        if is_benar:
            skor_sebenarnya += poin_per_soal
            total_benar += 1 # ⚠️ HITUNG BENAR
    
    # 2. Simpan Hasil Evaluasi Ringkasan (MENGGUNAKAN FIELD BARU)
    
    hasil_evaluasi_obj = HasilEvaluasi.objects.create(
        id_siswa=siswa,
        nilai=skor_sebenarnya,
        total_benar=total_benar, # ⚠️ SIMPAN TOTAL BENAR
        waktu_evaluasi_detik=waktu_pengerjaan_detik, # ⚠️ SIMPAN WAKTU
    )

    # 3. Redirect
    return redirect("evaluasi_nilai_detail", hasil_id=hasil_evaluasi_obj.id_hasil_evaluasi)

# B. Ubah `evaluasi_nilai_detail` (Mengirimkan Konteks):

def evaluasi_nilai_detail(request, hasil_id):
    siswa = get_logged_in_user(request)
    if not siswa:
        return redirect("login")
    
    from .models import HasilEvaluasi
    questions = EVALUASI_QUESTIONS_SERVER # Muat soal untuk hitung total
    
    try:
        hasil_evaluasi = HasilEvaluasi.objects.get(id_hasil_evaluasi=hasil_id, id_siswa=siswa)
        
        context = {
            "hasil_evaluasi": hasil_evaluasi,
            "total_soal": len(questions),
             "nama_user": siswa.nama_lengkap,
        }
        return render(request, "evaluasi/nilaiEval.html", context)

    except HasilEvaluasi.DoesNotExist:
        messages.error(request, "Hasil evaluasi tidak ditemukan atau bukan milik Anda.")
        return redirect("landing")


# ---------- HALAMAN GURU ----------
def dashboard(request):
    return render(request, "halaman guru/dashboard.html")


def data_nilai(request):
    return render(request, "halaman guru/data-nilai.html")


def data_siswa(request):
    return render(request, "halaman guru/data-siswa.html")


# ---------- KUIS ----------
def kuis_petunjuk(request):
    """
    Halaman petunjuk kuis.
    Parameter: ?jenis=enkripsi / caesar / dekripsi
    """
    jenis = request.GET.get("jenis")

    # Validasi agar ?jenis wajib ada
    if jenis not in ["enkripsi", "caesar", "dekripsi"]:
        return render(
            request, "kuis/kuis_invalid.html", {"error": "Jenis kuis tidak valid."}
        )

    return render(request, "kuis/kuis.html", {"jenis": jenis})


def kuis_pengerjaan(request):
    """
    Halaman pengerjaan kuis.
    Parameter: ?jenis=enkripsi / caesar / dekripsi
    """
    jenis = request.GET.get("jenis")

    # Ambil timestamp saat ini
    current_time_stamp = int(time.time())

    if jenis not in ["enkripsi", "caesar", "dekripsi"]:
        return render(
            request, "kuis/kuis_invalid.html", {"error": "Jenis kuis tidak valid."}
        )
    return render(request, "kuis/kuis_pengerjaan.html", {"jenis": jenis})

    context = {
        "jenis": jenis,
        "time": current_time_stamp,  # Teruskan timestamp ke template
    }

    return render(request, "kuis/kuis_pengerjaan.html", context)



def get_logged_in_user(request):
    """Mengambil objek Pengguna dari session jika ada."""
    user_id = request.session.get("user_id")
    if user_id:
        try:
            return Pengguna.objects.get(id_pengguna=user_id)
        except Pengguna.DoesNotExist:
            # Jika user_id ada di session tetapi objek tidak ada di DB
            return None
    return None


# ⚠️ DATA SOAL KUIS UNTUK VALIDASI SERVER
QUIZ_QUESTIONS_SERVER = {
    "enkripsi": [
        {
            "question": "Sebuah aplikasi sekolah mengirimkan pesan nilai rapor melalui server pusat. Agar data tidak mudah dibaca jika terjadi kebocoran jaringan, aplikasi tersebut menambahkan proses khusus sebelum pengiriman. Langkah apakah yang paling tepat dilakukan?",
            "options": [
                "Mengubah format file menjadi PDF",
                "Mengganti nama file sebelum dikirim",
                "Melakukan enkripsi pada data rapor",
                "Menghapus sebagian data penting",
            ],
            "correct": 2,
        },
        {
            "question": "Rina membuat aplikasi pengaduan anonim. Ia ingin memastikan setiap laporan aman walaupun database dicuri orang. Apa alasan utama ia perlu menerapkan enkripsi?",
            "options": [
                "Agar laporan lebih cepat diproses",
                "Agar laporan tetap bisa dibaca hanya oleh pihak berwenang",
                "Agar database tidak bisa dihapus",
                "Agar server tidak cepat penuh",
            ],
            "correct": 1,
        },
        {
            "question": "Sebuah pesan terenkripsi dapat dikirim dengan aman melalui jaringan sekolah yang sering mengalami gangguan keamanan. Mengapa enkripsi tetap penting meskipun jaringan sudah dilindungi firewall?",
            "options": [
                "Firewall tidak menjamin data selalu aman",
                "Enkripsi membuat pesan jadi lebih pendek",
                "Firewall tidak boleh digunakan bersamaan dengan enkripsi",
                "Firewall menghapus pesan asli",
            ],
            "correct": 0,
        },
        {
            "question": "Guru ingin berbagi file kunci ujian. Ia melakukan enkripsi, tetapi tidak mengirimkan kunci dekripsinya kepada siswa. Apa akibatnya?",
            "options": [
                "File akan terbaca otomatis",
                "File tetap aman dan tidak dapat dibaca",
                "Siswa dapat menebak isinya dengan mudah",
                "File berubah ukuran menjadi lebih besar",
            ],
            "correct": 1,
        },
        {
            "question": "Anto membuat sistem presensi otomatis. Ia menyadari data siswa dapat dilihat oleh admin jaringan. Untuk mencegah penyalahgunaan data, langkah apa yang harus ia tambahkan?",
            "options": [
                "Mengganti warna tampilan aplikasi",
                "Menyimpan data di folder berbeda",
                "Menyembunyikan aplikasi dari layar utama",
                "Menyandikan data saat disimpan (enkripsi)",
            ],
            "correct": 3,
        },
    ],
    "caesar": [
        {
            "question": "Sebuah pesan: “DRO AESMU LBYGX” ditemukan di kelas komputer. Siswa menduga ini adalah Caesar Cipher dengan geser +10. Apa isi pesannya?",
            "options": [
                "THE QUICK BROWN",
                "THE QUICK ROBOT",
                "THE CLOUD BROWN",
                "THE BROWN HOUSE",
            ],
            "correct": 0,
        },
        {
            "question": "Guru memberikan pesan terenkripsi “KHOOR ZRUOG” kepada siswa, namun lupa memberi petunjuk geseran. Siswa mencoba menebak pola pergeseran. Manakah teknik paling efektif?",
            "options": [
                "Menebak acak hingga muncul kata “WOW”",
                "Menggeser huruf satu per satu sampai pesan terbaca",
                "Mengganti huruf vokal saja",
                "Menghapus spasi lalu mencoba gabungan kata baru",
            ],
            "correct": 1,
        },
        {
            "question": "Aplikasi belajar membuat fitur tantangan Caesar Cipher. Pesan “ZL AOLYPUF” muncul saat kunci geser tidak diketahui. Siswa menyadari kata terakhir kemungkinan “HAPPY”. Maka geseran yang benar adalah…",
            "options": ["+5", "+7", "–7", "–5"],
            "correct": 2,
        },
        {
            "question": "Aldi membuat program Caesar Cipher. Namun saat pesan terdiri dari angka, program malah mengubah angka menjadi huruf. Apa perbaikan yang paling tepat?",
            "options": [
                "Mematikan fitur enkripsi",
                "Menambahkan aturan untuk membiarkan angka tetap sama",
                "Mengubah semua angka menjadi simbol",
                "Menghapus angka dari pesan",
            ],
            "correct": 1,
        },
        {
            "question": "Pesan “WKLV LV D VHFUHW” dikirimkan namun tampak mencurigakan. Siswa melihat pola huruf tidak biasa. Apa langkah paling tepat untuk memeriksa apakah itu Caesar Cipher?",
            "options": [
                "Mengirim pesan kembali ke pengirim",
                "Menguji beberapa pergeseran untuk melihat apakah menghasilkan kata yang bermakna",
                "Mengganti semua huruf dengan vokal",
                "Menghapus huruf pertama dan terakhir",
            ],
            "correct": 1,
        },
    ],
    "dekripsi": [
        {
            "question": "Pesan rahasia siswa berbunyi “RIJVS UYVJN”. Setelah dianalisis, ternyata ini hasil enkripsi tertentu. Apa tujuan proses dekripsi?",
            "options": [
                "Mengubah pesan menjadi lebih sulit dibaca",
                "Mengembalikan pesan ke bentuk aslinya",
                "Menghasilkan pesan baru untuk dikirim",
                "Menghapus pesan dari sistem",
            ],
            "correct": 1,
        },
        {
            "question": "Guru menerima file nilai yang terenkripsi, tetapi kunci dekripsinya hilang. Apa risiko yang terjadi?",
            "options": [
                "File dapat dibuka siapa saja",
                "File tidak bisa dibaca meskipun datanya benar",
                "File berubah ukuran dan rusak",
                "File otomatis terhapus",
            ],
            "correct": 1,
        },
        {
            "question": "Dalam simulasi keamanan, siswa mencoba membuka pesan yang disandikan. Namun ketika dekripsi dilakukan dengan kunci salah, hasilnya tidak masuk akal. Apa yang bisa disimpulkan?",
            "options": [
                "Sistem enkripsi tidak berfungsi",
                "Dekripsi hanya bisa dilakukan dengan kunci yang tepat",
                "Pesan tidak perlu didekripsi",
                "Semua kunci menghasilkan pesan yang sama",
            ],
            "correct": 1,
        },
        {
            "question": "Sebuah aplikasi melakukan enkripsi saat mengirim data, tetapi tidak melakukan dekripsi saat menerima. Apa dampaknya?",
            "options": [
                "Data yang diterima tetap terenkripsi dan tidak terbaca",
                "Data menjadi lebih cepat terkirim",
                "Data otomatis berubah menjadi teks asli",
                "Data tersimpan dua kali lebih besar",
            ],
            "correct": 0,
        },
        {
            "question": "Rani mencoba mendekripsi pesan yang digeser 8 langkah ke kanan. Ia ingin mengembalikannya ke teks asli. Apa yang harus ia lakukan?",
            "options": [
                "Menggeser huruf maju 8 langkah",
                "Menggeser huruf mundur 8 langkah",
                "Menggeser huruf maju 16 langkah",
                "Menghapus huruf vokal lalu membaca ulang",
            ],
            "correct": 1,
        },
    ],
}
KUIST_ID_MAP = {"enkripsi": 1, "caesar": 2, "dekripsi": 3}


@require_POST
def simpan_kuis_nilai(request):
    siswa = get_logged_in_user(request)
    if not siswa:
        messages.error(request, "Anda harus login untuk menyimpan hasil kuis.")
        return redirect("login")

    jenis = request.POST.get("jenis")
    waktu_pengerjaan = int(request.POST.get("waktu_pengerjaan", 0))

    if jenis not in KUIST_ID_MAP:
        messages.error(request, "Jenis kuis tidak valid.")
        return redirect("landing")

    kuis_id = KUIST_ID_MAP[jenis]
    kuis_obj = Kuis.objects.get(id_kuis=kuis_id)
    questions = QUIZ_QUESTIONS_SERVER.get(jenis, [])

    # 1. Hitung Ulang dan Validasi Skor di Server
    skor_sebenarnya = 0
    rincian_jawaban_list = []

    for i, q in enumerate(questions):
        q_num = i + 1
        # Mengambil jawaban siswa (berbentuk teks/pilihan)
        jawaban_siswa_text = request.POST.get(f"jawaban_{q_num}", "(kosong)")

        # Mengambil jawaban benar (teks/pilihan) dari data soal server
        jawaban_benar_text = q["options"][q["correct"]]

        is_benar = jawaban_siswa_text == jawaban_benar_text
        if is_benar:
            skor_sebenarnya += 20
        rincian_jawaban_list.append(
            {
                "id_pertanyaan_json": str(q_num),  # ID di JSON adalah nomor urut
                "teks_pertanyaan": q["question"],
                "jawaban_siswa": jawaban_siswa_text,
                "is_benar": is_benar,
            }
        )

    # 2. Simpan Hasil Kuis Ringkasan
    existing_attempts = HasilKuis.objects.filter(
        id_siswa=siswa, id_kuis=kuis_obj
    ).count()
    percobaan_ke = existing_attempts + 1

    hasil_kuis_obj = HasilKuis.objects.create(
        id_siswa=siswa,
        id_kuis=kuis_obj,
        skor_kuis=skor_sebenarnya,
        waktu_kuis=waktu_pengerjaan,
        percobaan_kuis=percobaan_ke,
    )

    # 3. Simpan Rincian Jawaban
    rincian_batch = []
    for rincian in rincian_jawaban_list:
        rincian_batch.append(
            RincianJawaban(
                id_hasil_kuis=hasil_kuis_obj,
                id_pertanyaan_json=rincian["id_pertanyaan_json"],
                teks_pertanyaan=rincian["teks_pertanyaan"],
                jawaban_siswa=rincian["jawaban_siswa"],
                is_benar=rincian["is_benar"],
            )
        )
    RincianJawaban.objects.bulk_create(rincian_batch)

    # 4. Redirect ke Halaman Nilai
    # Redirect ke fungsi baru dengan ID hasil kuis
    return redirect("kuis_nilai_detail", hasil_id=hasil_kuis_obj.id_hasil_kuis)


def kuis_nilai_detail(request, hasil_id):
    siswa = get_logged_in_user(request)
    if not siswa:
        return redirect("login")

    try:
        hasil_kuis = HasilKuis.objects.get(id_hasil_kuis=hasil_id, id_siswa=siswa)
        rincian_jawaban = hasil_kuis.rincian_jawaban.all()

        jenis_kuis = hasil_kuis.id_kuis.nama_kuis.lower()
        next_url_name = (
            "landing"  # Default kembali ke landing jika tidak ada yang cocok
        )

        if jenis_kuis == "enkripsi":
            # Jika dari kuis enkripsi, lanjutkan ke materi caesar
            next_url_name = "caesar"
        elif jenis_kuis == "caesar":
            # Jika dari kuis caesar, lanjutkan ke materi dekripsi
            next_url_name = "dekripsi"
        elif jenis_kuis == "dekripsi":
            # Jika dari kuis dekripsi, lanjutkan ke petunjuk evaluasi
            next_url_name = "evaluasi_petunjuk"

        correct_count = rincian_jawaban.filter(is_benar=True).count()

        context = {
            "hasil_kuis": hasil_kuis,
            "rincian_jawaban": rincian_jawaban,
            "correct_count": correct_count,
            "next_url_name": next_url_name,  # Kirim Named URL ke template
        }
        return render(request, "kuis/nilaiKuis.html", context)

    except HasilKuis.DoesNotExist:
        messages.error(request, "Hasil kuis tidak ditemukan atau bukan milik Anda.")
        return redirect("landing")


# ---------- MATERI ----------
def aktivitas1(request):
    return render(request, "materi/aktivitas1.html")


def aktivitas2(request):
    return render(request, "materi/aktivitas2.html")


def aktivitas3(request):
    return render(request, "materi/aktivitas3.html")


def aktivitas4(request):
    return render(request, "materi/aktivitas4.html")


def caesar(request):
    return render(request, "materi/caesarcipher.html")


def caesar2(request):
    return render(request, "materi/caesarcipher2.html")


# Jika kamu punya file tambahan seperti enkripsi/deskripsi/pengenalan:
def dekripsi(request):
    return render(request, "materi/dekripsi.html")


def dekripsi2(request):
    return render(request, "materi/dekripsi2.html")


def enkripsi(request):
    return render(request, "materi/enkripsi.html")


def pengenalan(request):
    return render(request, "materi/pengenalan.html")


# ---------- TANTANGAN ----------
@login_required
def stage1(request):
    return render(request, "tantangan/stage1.html")


@login_required
def stage2(request):
    return render(request, "tantangan/stage2.html")


@login_required
def stage3(request):
    return render(request, "tantangan/stage3.html")


@login_required
def stage4(request):
    return render(request, "tantangan/stage4.html")


@login_required
def stage5(request):
    return render(request, "tantangan/stage5.html")


@login_required
def stage6(request):
    return render(request, "tantangan/stage6.html")


@login_required
def stage7(request):
    return render(request, "tantangan/stage7.html")


@login_required
def stage8(request):
    return render(request, "tantangan/stage8.html")


@login_required
def stage9(request):
    return render(request, "tantangan/stage9.html")


@login_required
def stage10(request):
    return render(request, "tantangan/stage10.html")


@login_required
def tantangan(request):
    return render(request, "tantangan/tantangan.html")


# ---------- HALAMAN UMUM ----------
def landing(request):
    return render(request, "landing.html")


def register_user(request, peran):
    """
    Fungsi helper untuk menangani logic pendaftaran Guru atau Siswa.
    """
    if request.method == "POST":
        nama_lengkap = request.POST.get("nama_lengkap")
        email = request.POST.get("email")
        kata_sandi = request.POST.get("kata_sandi")
        konfirmasi_sandi = request.POST.get("konfirmasi_sandi")

        # 1. Validasi input
        if kata_sandi != konfirmasi_sandi:
            messages.error(request, "Kata sandi dan konfirmasi kata sandi tidak cocok.")
            # Kembali ke halaman formulir yang sesuai
            template = "guru-daftar.html" if peran == "guru" else "siswa-daftar.html"
            return render(request, template, request.POST)

        # 2. Cek apakah email sudah terdaftar
        if Pengguna.objects.filter(email=email).exists():
            messages.error(request, f'Email "{email}" sudah terdaftar. Silakan login.')
            template = "guru-daftar.html" if peran == "guru" else "siswa-daftar.html"
            return render(request, template, request.POST)

        # 3. Proses Hashing Kata Sandi dan Simpan
        try:
            # Hashing kata sandi sebelum disimpan
            hashed_password = make_password(kata_sandi)

            Pengguna.objects.create(
                nama_lengkap=nama_lengkap,
                email=email,
                # Simpan kata sandi yang sudah di-hash
                kata_sandi=hashed_password,
                peran=peran,
            )
            messages.success(request, "Pendaftaran berhasil! Silakan login.")
            return redirect("login")  # Arahkan ke halaman login

        except Exception as e:
            messages.error(request, f"Terjadi kesalahan saat menyimpan data: {e}")
            template = "guru-daftar.html" if peran == "guru" else "siswa-daftar.html"
            return render(request, template, request.POST)

    # Untuk permintaan GET, tampilkan formulir
    template = "guru-daftar.html" if peran == "guru" else "siswa-daftar.html"
    return render(request, template)


def guru_daftar(request):
    # Panggil fungsi register_user dengan peran 'guru'
    return register_user(request, peran="guru")


def siswa_daftar(request):
    # Panggil fungsi register_user dengan peran 'siswa'
    return register_user(request, peran="siswa")


def pilihan_daftar(request):
    return render(request, "pilihan-daftar.html")


def login_user(request):
    """
    Menangani proses login pengguna.
    """
    if request.method == "POST":
        email = request.POST.get("email")
        kata_sandi = request.POST.get("kata_sandi")

        try:
            user = Pengguna.objects.get(email=email)

            # Verifikasi Kata Sandi dengan Hashing
            # Menggunakan check_password untuk membandingkan kata sandi yang dimasukkan
            # dengan kata sandi yang di-hash di database.
            if check_password(kata_sandi, user.kata_sandi):
                # Login Berhasil
                request.session["user_id"] = user.id_pengguna
                request.session["user_role"] = user.peran
                messages.success(request, f"Selamat datang, {user.nama_lengkap}!")

                # Arahkan (Redirect) sesuai peran
                if user.peran == "guru":
                    # Guru diarahkan ke dashboard guru
                    return redirect("dashboard")
                else:
                    # Siswa diarahkan ke landing page
                    return redirect("landing")

            else:
                # Kata Sandi Salah
                messages.error(request, "Kata sandi salah.")
                return render(request, "login.html", {"email": email})

        except Pengguna.DoesNotExist:
            # Email Tidak Ditemukan
            messages.error(request, "Email tidak terdaftar.")
            return render(request, "login.html", {"email": email})

        except Exception as e:
            messages.error(request, f"Terjadi kesalahan saat login: {e}")
            return render(request, "login.html")

    # Untuk permintaan GET, tampilkan formulir login
    return render(request, "login.html")


def logout_user(request):
    """
    Menghapus data session dan melakukan logout.
    """
    if "user_id" in request.session:
        del request.session["user_id"]
    if "user_role" in request.session:
        del request.session["user_role"]
    messages.info(request, "Anda telah berhasil logout.")
    return redirect("landing")


def leaderboard(request):
    # ... (tidak berubah)
    return render(request, "leaderboard.html")


def tes(request):
    # ... (tidak berubah)
    return render(request, "tes.html")


@login_required
@require_POST
def simpan_skor_final_view(request):
    if PeringkatFinal.objects.filter(siswa=request.user).exists():
        return JsonResponse(
            {
                "status": "sudah_ada",
                "message": "Skor PERTAMA kali Anda sudah tercatat di Leaderboard. Percobaan ini tidak akan mengubah peringkat.",
            },
            status=200,
        )

    try:
        data = json.loads(request.body)
        skor = int(data.get("total_skor"))
        waktu = int(data.get("total_waktu"))

        PeringkatFinal.objects.create(
            siswa=request.user, total_skor=skor, total_waktu_detik=waktu
        )
        return JsonResponse(
            {
                "status": "sukses",
                "message": "Selamat! Skor pertama Anda berhasil dicatat ke Leaderboard!",
            },
            status=201,
        )

    except Exception as e:
        return JsonResponse({"status": "gagal", "message": str(e)}, status=500)


@login_required
def leaderboard_view(request):
    peringkat_list = PeringkatFinal.objects.all().order_by(
        "-total_skor", "total_waktu_detik"
    )
    context = {"peringkat_list": peringkat_list}
    return render(request, "leaderboard.html", context)
