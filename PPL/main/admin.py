from django.contrib import admin
from .models import (
    Pengguna, Kelas, AnggotaKelas,
    Kuis, HasilKuis, Section, SectionItem,
    ProgresItem, StageGame, HasilGame,
    HasilEvaluasi
)


# ============================
#       ADMIN PENGGUNA
# ============================
@admin.register(Pengguna)
class PenggunaAdmin(admin.ModelAdmin):
    list_display = ('id_pengguna', 'nama_lengkap', 'email', 'peran')
    search_fields = ('nama_lengkap', 'email')
    list_filter = ('peran',)


# ============================
#       ADMIN KELAS
# ============================
@admin.register(Kelas)
class KelasAdmin(admin.ModelAdmin):
    list_display = ('id_kelas', 'nama_kelas', 'id_guru', 'token')
    search_fields = ('nama_kelas', 'token')
    list_filter = ('id_guru',)


# ============================
#   ADMIN ANGGOTA KELAS
# ============================
@admin.register(AnggotaKelas)
class AnggotaKelasAdmin(admin.ModelAdmin):
    list_display = ('id_anggota', 'id_kelas', 'id_siswa')
    search_fields = ('id_kelas__nama_kelas', 'id_siswa__nama_lengkap')


# ============================
#       ADMIN KUIS
# ============================
@admin.register(Kuis)
class KuisAdmin(admin.ModelAdmin):
    list_display = ('id_kuis', 'nama_kuis', 'durasi')
    search_fields = ('nama_kuis',)


# ============================
#     ADMIN HASIL KUIS
# ============================
@admin.register(HasilKuis)
class HasilKuisAdmin(admin.ModelAdmin):
    list_display = ('id_hasil_kuis', 'id_siswa', 'id_kuis', 'skor_kuis', 'waktu_kuis', 'percobaan_kuis')
    list_filter = ('id_kuis', 'id_siswa')
    search_fields = ('id_siswa__nama_lengkap', 'id_kuis__nama_kuis')


# ============================
#      ADMIN SECTION
# ============================
@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('id_section', 'nama_section', 'urutan')
    search_fields = ('nama_section',)
    ordering = ('urutan',)


# ============================
#    ADMIN SECTION ITEM
# ============================
@admin.register(SectionItem)
class SectionItemAdmin(admin.ModelAdmin):
    list_display = ('id_item', 'nama_item', 'id_section', 'jenis_item', 'urutan', 'id_kuis')
    list_filter = ('jenis_item', 'id_section')
    search_fields = ('nama_item',)


# ============================
#    ADMIN PROGRES ITEM
# ============================
@admin.register(ProgresItem)
class ProgresItemAdmin(admin.ModelAdmin):
    list_display = ('id_progres_item', 'id_siswa', 'id_item', 'status')
    list_filter = ('status', 'id_siswa')
    search_fields = ('id_siswa__nama_lengkap', 'id_item__nama_item')


# ============================
#     ADMIN STAGE GAME
# ============================
@admin.register(StageGame)
class StageGameAdmin(admin.ModelAdmin):
    list_display = ('id_stage', 'nama_stage')
    search_fields = ('nama_stage',)


# ============================
#     ADMIN HASIL GAME
# ============================
@admin.register(HasilGame)
class HasilGameAdmin(admin.ModelAdmin):
    list_display = ('id_hasil_game', 'id_siswa', 'id_stage', 'skor_game', 'waktu_game', 'percobaan_game')
    list_filter = ('id_stage', 'id_siswa')
    search_fields = ('id_siswa__nama_lengkap',)


# ============================
#    ADMIN HASIL EVALUASI
# ============================
@admin.register(HasilEvaluasi)
class HasilEvaluasiAdmin(admin.ModelAdmin):
    list_display = ('id_hasil_evaluasi', 'id_siswa', 'nilai')
    list_filter = ('nilai',)
    search_fields = ('id_siswa__nama_lengkap',)
