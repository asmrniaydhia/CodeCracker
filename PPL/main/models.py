from django.db import models

# ----- PUNNYAA RANIIII ------
class Pengguna(models.Model):
    # Definisi Kolom Tabel
    id_pengguna = models.AutoField(primary_key=True)
    nama_lengkap = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    kata_sandi = models.CharField(max_length=255) # Disimpan plain text sesuai request (sebaiknya di-hash nanti)
    
    # Pilihan Peran (Enum)
    PERAN_CHOICES = [
        ('siswa', 'Siswa'),
        ('guru', 'Guru'),
    ]
    peran = models.CharField(max_length=10, choices=PERAN_CHOICES)

    def __str__(self):
        return f"{self.nama_lengkap} ({self.peran})"

    class Meta:
        db_table = 'pengguna'


class Kelas(models.Model):
    id_kelas = models.AutoField(primary_key=True)
    # Menggunakan ForeignKey ke Pengguna (khusus yg perannya guru)
    guru = models.ForeignKey(Pengguna, on_delete=models.CASCADE, db_column='id_guru') 
    nama_kelas = models.CharField(max_length=45)
    token = models.CharField(max_length=45, unique=True)

    class Meta:
        db_table = 'kelas'

class AnggotaKelas(models.Model):
    id_anggota = models.AutoField(primary_key=True)
    kelas = models.ForeignKey(Kelas, on_delete=models.CASCADE, db_column='id_kelas')
    siswa = models.ForeignKey(Pengguna, on_delete=models.CASCADE, db_column='id_siswa')

    class Meta:
        db_table = 'anggota_kelas'

# ----- Batas punya Rani ----- 

# ============================
#            KUIS
# ============================
class Kuis(models.Model):
    id_kuis = models.AutoField(primary_key=True)
    nama_kuis = models.CharField(max_length=45)

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
#      RINCIAN JAWABAN SISWA
# ============================
class RincianJawaban(models.Model):
    id_rincian = models.AutoField(primary_key=True)
    # Ubah related_name menjadi 'rincian_jawaban'
    id_hasil_kuis = models.ForeignKey(
        HasilKuis, on_delete=models.CASCADE, related_name="rincian_jawaban" 
    ) 

    # Field untuk menyimpan ID/kunci dari JSON
    id_pertanyaan_json = models.CharField(max_length=50) 
    teks_pertanyaan = models.TextField(default="")
    jawaban_benar = models.CharField(max_length=255)
    jawaban_siswa = models.CharField(max_length=255)
    is_benar = models.BooleanField(default=False)

    def __str__(self):
        return f"Hasil Kuis {self.id_hasil_kuis.id_hasil_kuis} - ID JSON {self.id_pertanyaan_json}"


# ============================
#        TABEL PERTANYAAN
# ============================
# Model ini diasumsikan ada di proyek Anda
# Jika belum ada, Anda harus membuatnya. Contoh:
class Pertanyaan(models.Model):
    id_pertanyaan = models.AutoField(primary_key=True)
    id_kuis = models.ForeignKey(Kuis, on_delete=models.CASCADE)
    teks_pertanyaan = models.TextField()
    jawaban_benar = models.CharField(max_length=255)  # Jawaban yang benar
    # Anda bisa tambahkan field lain seperti jenis, pilihan_a, pilihan_b, dll.

    def __str__(self):
        return self.teks_pertanyaan


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
        ("teks", "Teks"),
        ("kuis", "Kuis"),
        ("latihan", "Latihan"),
    )

    id_item = models.AutoField(primary_key=True)
    id_section = models.ForeignKey(
        Section, on_delete=models.CASCADE, related_name="items"
    )
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
        ("belum", "Belum Selesai"),
        ("proses", "Sedang Dikerjakan"),
        ("selesai", "Selesai"),
    )

    id_progres_item = models.AutoField(primary_key=True)
    id_siswa = models.ForeignKey(Pengguna, on_delete=models.CASCADE)
    id_item = models.ForeignKey(SectionItem, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.id_siswa} - {self.id_item} ({self.status})"


# ============================
#         STAGE GAME
# ============================
class StageGame(models.Model):
    id_stage = models.AutoField(primary_key=True)
    nama_stage = models.CharField(max_length=45)

    def __str__(self):
        return self.nama_stage


# ============================
#          HASIL GAME
# ============================
class HasilGame(models.Model):
    id_hasil_game = models.AutoField(primary_key=True)
    id_siswa = models.ForeignKey(Pengguna, on_delete=models.CASCADE)
    id_stage = models.ForeignKey(StageGame, on_delete=models.CASCADE)
    skor_game = models.IntegerField()
    waktu_game = models.IntegerField()
    percobaan_game = models.IntegerField()

    def __str__(self):
        return f"{self.id_siswa} - {self.id_stage}"


# ============================
#        HASIL EVALUASI
# ============================
class HasilEvaluasi(models.Model):
    id_hasil_evaluasi = models.AutoField(primary_key=True)
    id_siswa = models.ForeignKey(Pengguna, on_delete=models.CASCADE)
    nilai = models.IntegerField()
    total_benar = models.IntegerField(default=0) 
    waktu_evaluasi_detik = models.IntegerField(default=0) 

    def __str__(self):
        return f"{self.id_siswa} - Nilai {self.nilai}"


# ============================
#   SISTEM PERINGKAT (BARU)
#   Digunakan untuk Leaderboard
# ============================
class PeringkatFinal(models.Model):
    # PERBAIKAN: Menggunakan Pengguna (model kamu), BUKAN User (bawaan Django)
    siswa = models.OneToOneField(Pengguna, on_delete=models.CASCADE, primary_key=True, related_name='peringkat_final')
    
    total_skor = models.IntegerField(default=0)
    total_waktu_detik = models.IntegerField(default=0)
    waktu_selesai = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-total_skor', 'total_waktu_detik']

    def __str__(self):
        return f"{self.siswa.nama_lengkap} - {self.total_skor} Poin"
    
