from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import PeringkatFinal
import json

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
@login_required
def stage1(request):
    return render(request, 'tantangan/stage1.html')

@login_required
def stage2(request):
    return render(request, 'tantangan/stage2.html')

@login_required
def stage3(request):
    return render(request, 'tantangan/stage3.html')

@login_required
def stage4(request):
    return render(request, 'tantangan/stage4.html')

@login_required
def stage5(request):
    return render(request, 'tantangan/stage5.html')

@login_required
def stage6(request):
    return render(request, 'tantangan/stage6.html')

@login_required
def stage7(request):
    return render(request, 'tantangan/stage7.html')

@login_required
def stage8(request):
    return render(request, 'tantangan/stage8.html')

@login_required
def stage9(request):
    return render(request, 'tantangan/stage9.html')

@login_required
def stage10(request):
    return render(request, 'tantangan/stage10.html')

@login_required
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