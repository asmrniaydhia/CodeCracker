from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import PeringkatFinal
import json

# ---------- EVALUASI ----------
def evaluasi_petunjuk(request):
    return render(request, "evaluasi/evaluasi.html")

def evaluasi_pengerjaan(request):
    return render(request, "evaluasi/evaluasi_pengerjaan.html")

def evaluasi_nilai(request):
    return render(request, "evaluasi/nilaiEval.html")

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

    if jenis not in ["enkripsi", "caesar", "dekripsi"]:
        return render(
            request, "kuis/kuis_invalid.html", {"error": "Jenis kuis tidak valid."}
        )
    return render(request, "kuis/kuis_pengerjaan.html", {"jenis": jenis})

from .models import Pengguna, Kuis, HasilKuis

def kuis_nilai(request):
    # Ambil user dari session
    siswa = get_logged_in_user(request)
    # if not siswa:
    #     return redirect("login")  # wajib login
    jenis = request.GET.get("jenis")
    nilai = request.GET.get("nilai")

    if jenis not in ["enkripsi", "caesar", "dekripsi"]:
        return render(request, "kuis/kuis_invalid.html", {"error": "Jenis kuis tidak valid."})

    if nilai:
        nilai_int = int(nilai)

        # Mapping jenis kuis ke ID kuis di database
        kuis_map = {"enkripsi": 1, "caesar": 2, "dekripsi": 3}
        kuis_obj = Kuis.objects.get(id_kuis=kuis_map[jenis])

        # Hitung percobaan sebelumnya
        existing_attempts = HasilKuis.objects.filter(id_siswa=siswa, id_kuis=kuis_obj).count()
        percobaan_ke = existing_attempts + 1

        # Simpan nilai
        HasilKuis.objects.create(
            id_siswa=siswa,
            id_kuis=kuis_obj,
            skor_kuis=nilai_int,
            waktu_kuis=20,
            percobaan_kuis=percobaan_ke,
        )

        context = {
            "jenis": jenis,
            "nilai": nilai_int,
            "percobaan": percobaan_ke,
            "nama": siswa.nama_lengkap
        }
        return render(request, "kuis/nilaiKuis.html", context)
    return render(request, "kuis/nilaiKuis.html", {"jenis": jenis})

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
    if request.method == 'POST':
        nama_lengkap = request.POST.get('nama_lengkap')
        email = request.POST.get('email')
        kata_sandi = request.POST.get('kata_sandi')
        konfirmasi_sandi = request.POST.get('konfirmasi_sandi')

        # 1. Validasi input
        if kata_sandi != konfirmasi_sandi:
            messages.error(request, 'Kata sandi dan konfirmasi kata sandi tidak cocok.')
            # Kembali ke halaman formulir yang sesuai
            template = "guru-daftar.html" if peran == 'guru' else "siswa-daftar.html"
            return render(request, template, request.POST)

        # 2. Cek apakah email sudah terdaftar
        if Pengguna.objects.filter(email=email).exists():
            messages.error(request, f'Email "{email}" sudah terdaftar. Silakan login.')
            template = "guru-daftar.html" if peran == 'guru' else "siswa-daftar.html"
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
                peran=peran
            )
            messages.success(request, 'Pendaftaran berhasil! Silakan login.')
            return redirect('login') # Arahkan ke halaman login

        except Exception as e:
            messages.error(request, f'Terjadi kesalahan saat menyimpan data: {e}')
            template = "guru-daftar.html" if peran == 'guru' else "siswa-daftar.html"
            return render(request, template, request.POST)

    # Untuk permintaan GET, tampilkan formulir
    template = "guru-daftar.html" if peran == 'guru' else "siswa-daftar.html"
    return render(request, template)

def guru_daftar(request):
    # Panggil fungsi register_user dengan peran 'guru'
    return register_user(request, peran='guru')

def siswa_daftar(request):
    # Panggil fungsi register_user dengan peran 'siswa'
    return register_user(request, peran='siswa')

def pilihan_daftar(request):
    return render(request, "pilihan-daftar.html")

def login_user(request):
    """
    Menangani proses login pengguna.
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        kata_sandi = request.POST.get('kata_sandi')

        try:
            user = Pengguna.objects.get(email=email)

            # Verifikasi Kata Sandi dengan Hashing
            # Menggunakan check_password untuk membandingkan kata sandi yang dimasukkan
            # dengan kata sandi yang di-hash di database.
            if check_password(kata_sandi, user.kata_sandi):
                # Login Berhasil
                request.session['user_id'] = user.id_pengguna
                request.session['user_role'] = user.peran
                messages.success(request, f'Selamat datang, {user.nama_lengkap}!')

                # Arahkan (Redirect) sesuai peran
                if user.peran == 'guru':
                    # Guru diarahkan ke dashboard guru
                    return redirect('dashboard')
                else:
                    # Siswa diarahkan ke landing page
                    return redirect('landing')

            else:
                # Kata Sandi Salah
                messages.error(request, 'Kata sandi salah.')
                return render(request, 'login.html', {'email': email})

        except Pengguna.DoesNotExist:
            # Email Tidak Ditemukan
            messages.error(request, 'Email tidak terdaftar.')
            return render(request, 'login.html', {'email': email})

        except Exception as e:
            messages.error(request, f'Terjadi kesalahan saat login: {e}')
            return render(request, 'login.html')

    # Untuk permintaan GET, tampilkan formulir login
    return render(request, 'login.html')

def logout_user(request):
    """
    Menghapus data session dan melakukan logout.
    """
    if 'user_id' in request.session:
        del request.session['user_id']
    if 'user_role' in request.session:
        del request.session['user_role']
    messages.info(request, 'Anda telah berhasil logout.')
    return redirect('landing')

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
        return JsonResponse({
            'status': 'sudah_ada', 
            'message': 'Skor PERTAMA kali Anda sudah tercatat di Leaderboard. Percobaan ini tidak akan mengubah peringkat.'
        }, status=200)

    try:
        data = json.loads(request.body)
        skor = int(data.get('total_skor'))
        waktu = int(data.get('total_waktu'))

        PeringkatFinal.objects.create(
            siswa=request.user,
            total_skor=skor,
            total_waktu_detik=waktu
        )
        return JsonResponse({'status': 'sukses', 'message': 'Selamat! Skor pertama Anda berhasil dicatat ke Leaderboard!'}, status=201)
    
    except Exception as e:
        return JsonResponse({'status': 'gagal', 'message': str(e)}, status=500)

@login_required 
def leaderboard_view(request):
    peringkat_list = PeringkatFinal.objects.all().order_by('-total_skor', 'total_waktu_detik')
    context = {
        'peringkat_list': peringkat_list
    }
    return render(request, 'leaderboard.html', context)