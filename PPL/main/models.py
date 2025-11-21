from django.db import models
from django.contrib.auth.models import User


# ============================
#        TABEL PENGGUNA
# ============================
class Pengguna(models.Model):
    PERAN_CHOICES = (
        ('guru', 'Guru'),
        ('siswa', 'Siswa'),
    )
    id_pengguna = models.AutoField(primary_key=True)
    nama_lengkap = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    kata_sandi = models.CharField(max_length=255)
    peran = models.CharField(max_length=10, choices=PERAN_CHOICES)

    @property
    def is_guru(self):
        return self.peran == 'guru'
    
    @property
    def is_siswa(self):
        return self.peran == 'siswa'
    
    def __str__(self):
        return self.nama_lengkap


# ============================
#        TABEL KELAS
# ============================
class Kelas(models.Model):
    id_kelas = models.AutoField(primary_key=True)
    id_guru = models.ForeignKey(Pengguna, on_delete=models.CASCADE, related_name='kelas_guru')
    nama_kelas = models.CharField(max_length=45)
    token = models.CharField(max_length=45)

    def __str__(self):
        return self.nama_kelas

# ============================
#     ANGGOTA_KELAS (RELASI)
# ============================
class AnggotaKelas(models.Model):
    id_anggota = models.AutoField(primary_key=True)
    id_kelas = models.ForeignKey(Kelas, on_delete=models.CASCADE, related_name='anggota')
    id_siswa = models.ForeignKey(Pengguna, on_delete=models.CASCADE, related_name='kelas_siswa', null=True)
    def __str__(self):
        return f"{self.id_siswa} di {self.id_kelas}"

# ============================
#            KUIS
# ============================
class Kuis(models.Model):
    id_kuis = models.AutoField(primary_key=True)
    nama_kuis = models.CharField(max_length=45)
    durasi = models.IntegerField()

    def __str__(self):
        return self.nama_kuis

# ============================
#         HASIL KUIS
# ============================
class HasilKuis(models.Model):
    id_hasil_kuis = models.AutoField(primary_key=True)
    id_siswa = models.ForeignKey(Pengguna, on_delete=models.CASCADE)
    id_kuis = models.ForeignKey(Kuis, on_delete=models.CASCADE)
    skor_kuis = models.IntegerField()
    waktu_kuis = models.IntegerField()
    percobaan_kuis = models.IntegerField()

    def __str__(self):
        return f"{self.id_siswa} - {self.id_kuis}"

# ============================
#           SECTION
# ============================
class Section(models.Model):
    id_section = models.AutoField(primary_key=True)
    nama_section = models.CharField(max_length=45)
    urutan = models.IntegerField()

    def __str__(self):
        return self.nama_section

# ============================
#        SECTION ITEM
# ============================
class SectionItem(models.Model):
    JENIS_ITEM_CHOICES = (
        ('video', 'Video'),
        ('teks', 'Teks'),
        ('kuis', 'Kuis'),
        ('game', 'Game'),
    )

    id_item = models.AutoField(primary_key=True)
    id_section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='items')
    nama_item = models.CharField(max_length=45)
    jenis_item = models.CharField(max_length=10, choices=JENIS_ITEM_CHOICES)
    urutan = models.IntegerField()
    id_kuis = models.ForeignKey(Kuis, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nama_item

# ============================
#         PROGRES ITEM
# ============================
class ProgresItem(models.Model):
    STATUS_CHOICES = (
        ('belum', 'Belum Selesai'),
        ('proses', 'Sedang Dikerjakan'),
        ('selesai', 'Selesai'),
    )

    id_progres_item = models.AutoField(primary_key=True)
    id_siswa = models.ForeignKey(Pengguna, on_delete=models.CASCADE)
    id_item = models.ForeignKey(SectionItem, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.id_siswa} - {self.id_item} ({self.status})"

# # ============================
# #         STAGE GAME
# # ============================
# class StageGame(models.Model):
#     id_stage = models.AutoField(primary_key=True)
#     nama_stage = models.CharField(max_length=45)

#     def __str__(self):
#         return self.nama_stage

# # ============================
# #          HASIL GAME
# # ============================
# class HasilGame(models.Model):
#     id_hasil_game = models.AutoField(primary_key=True)
#     id_siswa = models.ForeignKey(Pengguna, on_delete=models.CASCADE)
#     id_stage = models.ForeignKey(StageGame, on_delete=models.CASCADE)
#     skor_game = models.IntegerField()
#     waktu_game = models.IntegerField()
#     percobaan_game = models.IntegerField()

#     def __str__(self):
#         return f"{self.id_siswa} - {self.id_stage}"

# ============================
#        HASIL EVALUASI
# ============================
class HasilEvaluasi(models.Model):
    id_hasil_evaluasi = models.AutoField(primary_key=True)
    id_siswa = models.ForeignKey(Pengguna, on_delete=models.CASCADE)
    nilai = models.IntegerField()

    def __str__(self):
        return f"{self.id_siswa} - Nilai {self.nilai}"
    
# ============================
#   SISTEM PERINGKAT (BARU)
#   Digunakan untuk Leaderboard
# ============================
class PeringkatFinal(models.Model):
    # Menggunakan User bawaan Django agar sinkron dengan login/logout sistem
    siswa = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='peringkat_final')
    
    # Default 0 untuk menghindari error
    total_skor = models.IntegerField(default=0)
    total_waktu_detik = models.IntegerField(default=0)
    
    # Mencatat kapan siswa menyelesaikan tantangan
    waktu_selesai = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Otomatis mengurutkan berdasarkan Skor Tertinggi, lalu Waktu Tercepat
        ordering = ['-total_skor', 'total_waktu_detik']

    def __str__(self):
        return f"{self.siswa.username} - {self.total_skor} Poin ({self.total_waktu_detik}s)"