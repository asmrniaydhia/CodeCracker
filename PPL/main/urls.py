from django.urls import path
from main import views

urlpatterns = [
    # Evaluasi
    path('evaluasi/', views.evaluasi_petunjuk, name='evaluasi_petunjuk'),
    path('evaluasi/pengerjaan/', views.evaluasi_pengerjaan, name='evaluasi_pengerjaan'),
    path('evaluasi/simpan/', views.simpan_evaluasi_nilai, name='simpan_evaluasi_nilai'),
    path('evaluasi/nilai/<int:hasil_id>/', views.evaluasi_nilai_detail, name='evaluasi_nilai_detail'),

    # Kuis
    path('kuis/', views.kuis_petunjuk, name='kuis_petunjuk'),
    path('kuis/pengerjaan/', views.kuis_pengerjaan, name='kuis_pengerjaan'),
    path('kuis/simpan/', views.simpan_kuis_nilai, name='simpan_kuis_nilai'),
    path('kuis/nilai/<int:hasil_id>/', views.kuis_nilai_detail, name='kuis_nilai_detail'),

    # Materi
    path('siswa/belajar/aktivitas1/', views.aktivitas1, name='aktivitas1'),
    path('siswa/belajar/enkripsi/aktivitas/', views.aktivitas2, name='aktivitas2'),
    path('materi/aktivitas3/', views.aktivitas3, name='aktivitas3'),
    path('materi/aktivitas4/', views.aktivitas4, name='aktivitas4'),
    path('materi/caesar/', views.caesar, name='caesar'),
    path('materi/caesar2/', views.caesar2, name='caesar2'),
    path('materi/dekripsi/', views.dekripsi, name='dekripsi'),
    path('materi/dekripsi2/', views.dekripsi2, name='dekripsi2'),
    path('siswa/belajar/enkripsi/', views.enkripsi, name='enkripsi'),
    path('siswa/belajar/pengenalan/', views.pengenalan_view, name='pengenalan'),
    
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

    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('manajemen-nilai/', views.rekap_nilai_siswa, name='rekap_nilai_siswa'),
    path('export-nilai-pdf/', views.export_rekap_nilai_pdf, name='export_rekap_nilai_pdf'),
    path('hapus-nilai/<int:id_siswa>/<str:jenis>/', views.hapus_nilai_siswa, name='hapus_nilai_siswa'),
    path('export-nilai/pilih-kelas/', views.halaman_download_per_kelas, name='halaman_download_per_kelas'),
    path('api/simpan-skor-final/', views.simpan_skor_final_view, name='simpan_skor_final_view'),
    path('tantangan/unlock/<int:stage_selesai>/', views.unlock_next_stage, name='unlock_next_stage'),
    path('profil/', views.profil_view, name='profil'),
    path('', views.index, name='index'),  
    path('daftar/', views.pilihan_daftar, name='pilihan_daftar'),
    path('daftar/siswa/', views.siswa_daftar, name='siswa_daftar'),
    path('daftar/guru/', views.guru_daftar, name='guru_daftar'),  
    path('login/', views.login_view, name='login'),
    path('lupa-sandi/', views.lupa_sandi_view, name='lupa_sandi'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('join-kelas/', views.input_token_view, name='input_token'), 
    path('logout/', views.logout_view, name='logout'),
    path('manajemen-kelas/', views.kelola_kelas, name='kelola_kelas'),
    path('edit-kelas/<int:id_kelas>/', views.edit_kelas, name='edit_kelas'),
    path('hapus-kelas/<int:id_kelas>/', views.hapus_kelas, name='hapus_kelas'),
    path('data-siswa/', views.data_siswa, name='data_siswa'),
    path('hapus-anggota/<int:id_anggota>/', views.hapus_anggota_kelas, name='hapus_anggota_kelas'),
    path('api/progres-item/', views.update_progres_item, name='update_progres_item'),
]