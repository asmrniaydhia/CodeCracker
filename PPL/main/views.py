from django.shortcuts import render

# ---------- EVALUASI ----------
def evaluasi(request):
    return render(request, 'evaluasi/evaluasi.html')

def nilai_eval(request):
    return render(request, 'evaluasi/nilaiEval.html')


# ---------- HALAMAN GURU ----------
def dashboard(request):
    return render(request, 'halaman guru/dashboard.html')

def data_nilai(request):
    return render(request, 'halaman guru/data-nilai.html')

def data_siswa(request):
    return render(request, 'halaman guru/data-siswa.html')


# ---------- KUIS ----------
def kuis(request):
    return render(request, 'kuis/kuis.html')

def kuis1(request):
    return render(request, 'kuis/kuis1.html')

def kuis2(request):
    return render(request, 'kuis/kuis2.html')

def kuis3(request):
    return render(request, 'kuis/kuis3.html')

def kuis4(request):
    return render(request, 'kuis/kuis4.html')

def nilai_kuis(request):
    return render(request, 'kuis/nilaiKuis.html')


# ---------- MATERI ----------
def aktivitas1(request):
    return render(request, 'materi/aktivitas1.html')

def aktivitas2(request):
    return render(request, 'materi/aktivitas2.html')

def aktivitas3(request):
    return render(request, 'materi/aktivitas3.html')

def aktivitas4(request):
    return render(request, 'materi/aktivitas4.html')

def caesar(request):
    return render(request, 'materi/caesarcipher.html')

def caesar2(request):
    return render(request, 'materi/caesarcipher2.html')

# Jika kamu punya file tambahan seperti enkripsi/deskripsi/pengenalan:
def deskripsi(request):
    return render(request, 'materi/deskripsi.html')

def deskripsi2(request):
    return render(request, 'materi/deskripsi2.html')

def enkripsi(request):
    return render(request, 'materi/enkripsi.html')

def pengenalan(request):
    return render(request, 'materi/pengenalan.html')


# ---------- TANTANGAN ----------
def stage1(request):
    return render(request, 'tantangan/stage1.html')

def stage2(request):
    return render(request, 'tantangan/stage2.html')

def stage3(request):
    return render(request, 'tantangan/stage3.html')

def stage4(request):
    return render(request, 'tantangan/stage4.html')

def stage5(request):
    return render(request, 'tantangan/stage5.html')

def stage6(request):
    return render(request, 'tantangan/stage6.html')

def stage7(request):
    return render(request, 'tantangan/stage7.html')

def stage8(request):
    return render(request, 'tantangan/stage8.html')

def stage9(request):
    return render(request, 'tantangan/stage9.html')

def stage10(request):
    return render(request, 'tantangan/stage10.html')

def tantangan(request):
    return render(request, 'tantangan/tantangan.html')


# ---------- HALAMAN UMUM ----------
def landing(request):
    return render(request, 'landing.html')

def guru_daftar(request):
    return render(request, 'guru-daftar.html')

def siswa_daftar(request):
    return render(request, 'siswa-daftar.html')

def pilihan_daftar(request):
    return render(request, 'pilihan-daftar.html')

def leaderboard(request):
    return render(request, 'leaderboard.html')

def tes(request):
    return render(request, 'tes.html')
