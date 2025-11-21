from django.urls import path
from . import views

urlpatterns = [
    # Evaluasi
    path('evaluasi/', views.evaluasi_petunjuk, name='evaluasi_petunjuk'),
    path('evaluasi/pengerjaan/', views.evaluasi_pengerjaan, name='evaluasi_pengerjaan'),
    path('evaluasi/nilai/', views.evaluasi_nilai, name='evaluasi_nilai'),

    # Halaman guru
    path('guru/dashboard/', views.dashboard, name='dashboard'),
    path('guru/data-nilai/', views.data_nilai, name='data_nilai'),
    path('guru/data-siswa/', views.data_siswa, name='data_siswa'),

    # Kuis
    path('kuis/', views.kuis_petunjuk, name='kuis_petunjuk'),
    path('kuis/pengerjaan/', views.kuis_pengerjaan, name='kuis_pengerjaan'),
    path('kuis/nilai/', views.kuis_nilai, name='kuis_nilai'),

    # Materi
    path('materi/aktivitas1/', views.aktivitas1, name='aktivitas1'),
    path('materi/aktivitas2/', views.aktivitas2, name='aktivitas2'),
    path('materi/aktivitas3/', views.aktivitas3, name='aktivitas3'),
    path('materi/aktivitas4/', views.aktivitas4, name='aktivitas4'),
    path('materi/caesar/', views.caesar, name='caesar'),
    path('materi/caesar2/', views.caesar2, name='caesar2'),
    path('materi/dekripsi/', views.dekripsi, name='dekripsi'),
    path('materi/dekripsi2/', views.dekripsi2, name='dekripsi2'),
    path('materi/enkripsi/', views.enkripsi, name='enkripsi'),
    path('materi/pengenalan/', views.pengenalan, name='pengenalan'),

    # Tantangan
    path('tantangan/stage1/', views.stage1, name='stage1'),
    path('tantangan/stage2/', views.stage2, name='stage2'),
    path('tantangan/stage3/', views.stage3, name='stage3'),
    path('tantangan/stage4/', views.stage4, name='stage4'),
    path('tantangan/stage5/', views.stage5, name='stage5'),
    path('tantangan/stage6/', views.stage6, name='stage6'),
    path('tantangan/stage7/', views.stage7, name='stage7'),
    path('tantangan/stage8/', views.stage8, name='stage8'),
    path('tantangan/stage9/', views.stage9, name='stage9'),
    path('tantangan/stage10/', views.stage10, name='stage10'),
    path('tantangan/tantangan/', views.tantangan, name='tantangan'),

    # Otentikasi & Umum
    path('', views.landing, name='landing'),
    path('guru-daftar/', views.guru_daftar, name='guru_daftar'), # Menggunakan fungsi register_user(peran='guru')
    path('siswa-daftar/', views.siswa_daftar, name='siswa_daftar'), # Menggunakan fungsi register_user(peran='siswa')
    path('pilihan-daftar/', views.pilihan_daftar, name='pilihan_daftar'),

    # --- PATH BARU ---
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    # ------------------

    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('tes/', views.tes, name='tes'),

    path('api/simpan-skor-final/', views.simpan_skor_final_view, name='simpan_skor_final'),
]