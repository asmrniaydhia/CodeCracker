from django.contrib import admin
from .models import (
    Pengguna, Kelas, AnggotaKelas, Kuis, StageGame, 
    HasilGame, HasilKuis, HasilEvaluasi, Section, 
    SectionItem, ProgresItem
)

# --- 1. Pengguna (Users) ---

@admin.register(Pengguna)
class PenggunaAdmin(admin.ModelAdmin):
    list_display = ('id_pengguna', 'nama_lengkap', 'email', 'peran')
    list_filter = ('peran',)
    search_fields = ('nama_lengkap', 'email')
    ordering = ('peran', 'nama_lengkap')

# --- 2. Kelas (Classes) ---

@admin.register(Kelas)
class KelasAdmin(admin.ModelAdmin):
    list_display = ('id_kelas', 'nama_kelas', 'id_guru', 'token')
    search_fields = ('nama_kelas', 'token', 'id_guru__nama_lengkap')
    raw_id_fields = ('id_guru',) # Memungkinkan pencarian guru menggunakan ID/Pop-up

# --- 3. Anggota Kelas (Class Membership) ---

@admin.register(AnggotaKelas)
class AnggotaKelasAdmin(admin.ModelAdmin):
    list_display = ('id_anggota', 'id_kelas', 'id_siswa')
    list_filter = ('id_kelas',)
    search_fields = ('id_kelas__nama_kelas', 'id_siswa__nama_lengkap')
    raw_id_fields = ('id_kelas', 'id_siswa')

# --- 4. Kuis (Quizzes) ---

class SectionInline(admin.TabularInline):
    model = Section
    extra = 1 # Menambahkan 1 field section kosong secara default

@admin.register(Kuis)
class KuisAdmin(admin.ModelAdmin):
    list_display = ('id_kuis', 'nama_kuis', 'id_pengguna', 'durasi')
    search_fields = ('nama_kuis', 'id_pengguna__nama_lengkap')
    raw_id_fields = ('id_pengguna',)
    inlines = [SectionInline]

# --- 5. Stage Game (Game Stages) ---

@admin.register(StageGame)
class StageGameAdmin(admin.ModelAdmin):
    list_display = ('id_stage', 'nama_stage')
    search_fields = ('nama_stage',)

# --- 6. Section (Sections within a Quiz) & SectionItem Inline ---

class SectionItemInline(admin.TabularInline):
    model = SectionItem
    extra = 1
    fields = ('nama_item', 'jenis_item', 'urutan')

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('id_section', 'nama_section', 'id_kuis', 'urutan')
    list_filter = ('id_kuis',)
    inlines = [SectionItemInline]
    search_fields = ('nama_section', 'id_kuis__nama_kuis')
    ordering = ('id_kuis', 'urutan')

# --- 7. Section Item (Quiz Items/Questions) ---

@admin.register(SectionItem)
class SectionItemAdmin(admin.ModelAdmin):
    list_display = ('id_item', 'nama_item', 'id_section', 'jenis_item', 'urutan')
    list_filter = ('jenis_item', 'id_section__id_kuis')
    search_fields = ('nama_item', 'id_section__nama_section')
    raw_id_fields = ('id_section',)

# --- 8. Progres Item (User Progress) ---

@admin.register(ProgresItem)
class ProgresItemAdmin(admin.ModelAdmin):
    list_display = ('id_progres', 'id_pengguna', 'id_item', 'status')
    list_filter = ('status', 'id_item__id_section__id_kuis')
    search_fields = ('id_pengguna__nama_lengkap', 'id_item__nama_item')
    raw_id_fields = ('id_pengguna', 'id_item')

# --- 9. Hasil Kuis (Quiz Results) ---

@admin.register(HasilKuis)
class HasilKuisAdmin(admin.ModelAdmin):
    list_display = ('id_hasil_kuis', 'id_siswa', 'id_kuis', 'skor_kuis', 'waktu_kuis', 'percobaan_kuis')
    list_filter = ('id_kuis',)
    search_fields = ('id_siswa__nama_lengkap', 'id_kuis__nama_kuis')
    raw_id_fields = ('id_siswa', 'id_kuis')

# --- 10. Hasil Game (Game Results) ---

@admin.register(HasilGame)
class HasilGameAdmin(admin.ModelAdmin):
    list_display = ('id_hasil_game', 'id_siswa', 'id_stage', 'skor_game', 'waktu_game', 'percobaan_game')
    list_filter = ('id_stage',)
    search_fields = ('id_siswa__nama_lengkap', 'id_stage__nama_stage')
    raw_id_fields = ('id_siswa', 'id_stage')

# --- 11. Hasil Evaluasi (Evaluation Results) ---

@admin.register(HasilEvaluasi)
class HasilEvaluasiAdmin(admin.ModelAdmin):
    list_display = ('id_hasil_evaluasi', 'id_siswa', 'id_kuis', 'nilai')
    list_filter = ('id_kuis',)
    search_fields = ('id_siswa__nama_lengkap', 'id_kuis__nama_kuis')
    raw_id_fields = ('id_siswa', 'id_kuis')