from django.shortcuts import render, redirect

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
def stage1(request):
    return render(request, "tantangan/stage1.html")


def stage2(request):
    return render(request, "tantangan/stage2.html")


def stage3(request):
    return render(request, "tantangan/stage3.html")


def stage4(request):
    return render(request, "tantangan/stage4.html")


def stage5(request):
    return render(request, "tantangan/stage5.html")


def stage6(request):
    return render(request, "tantangan/stage6.html")


def stage7(request):
    return render(request, "tantangan/stage7.html")


def stage8(request):
    return render(request, "tantangan/stage8.html")


def stage9(request):
    return render(request, "tantangan/stage9.html")


def stage10(request):
    return render(request, "tantangan/stage10.html")


def tantangan(request):
    return render(request, "tantangan/tantangan.html")


# ---------- HALAMAN UMUM ----------
def landing(request):
    return render(request, "landing.html")


def guru_daftar(request):
    return render(request, "guru-daftar.html")


def siswa_daftar(request):
    return render(request, "siswa-daftar.html")


def pilihan_daftar(request):
    return render(request, "pilihan-daftar.html")


def leaderboard(request):
    return render(request, "leaderboard.html")


def tes(request):
    return render(request, "tes.html")


# ---------- HELPER ----------
from .models import Pengguna

def get_logged_in_user(request):
    user_id = request.session.get("user_id")  # ambil dari session
    if user_id is None:
        return None
    try:
        return Pengguna.objects.get(id_pengguna=user_id)
    except Pengguna.DoesNotExist:
        return None
