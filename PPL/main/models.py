from django.db import models

# --- Tipe ENUM yang digunakan ---

class PeranPengguna(models.TextChoices):
    ADMIN = 'admin', 'Admin'
    GURU = 'guru', 'Guru'
    SISWA = 'siswa', 'Siswa'

class JenisItem(models.TextChoices):
    PILIHAN_GANDA = 'pilihan_ganda', 'Pilihan Ganda'
    ESAI = 'esai', 'Esai'

class StatusProgres(models.TextChoices):
    BELUM_SELESAI = 'belum_selesai', 'Belum Selesai'
    SELESAI = 'selesai', 'Selesai'

# --- 1. Pengguna (Users) ---

class Pengguna(models.Model):
    id_pengguna = models.AutoField(primary_key=True)
    nama_lengkap = models.CharField(max_length=45)
    email = models.CharField(max_length=45, unique=True) # Diasumsikan email unik
    kata_sandi = models.CharField(max_length=45) # Sebaiknya gunakan tipe yang lebih panjang untuk hash kata sandi
    peran = models.CharField(
        max_length=10,
        choices=PeranPengguna.choices,
        default=PeranPengguna.SISWA,
    )

    class Meta:
        db_table = 'pengguna'
        verbose_name_plural = 'Pengguna'

    def __str__(self):
        return self.nama_lengkap

# --- 2. Kelas (Classes) ---

class Kelas(models.Model):
    id_kelas = models.AutoField(primary_key=True)
    id_guru = models.ForeignKey(
        Pengguna, 
        on_delete=models.CASCADE, 
        limit_choices_to={'peran': PeranPengguna.GURU}, # Diasumsikan id_guru merujuk ke Pengguna dengan peran 'guru'
        related_name='kelas_diajar'
    )
    nama_kelas = models.CharField(max_length=45)
    token = models.CharField(max_length=45, unique=True) # Diasumsikan token unik

    class Meta:
        db_table = 'kelas'
        verbose_name_plural = 'Kelas'

    def __str__(self):
        return self.nama_kelas

# --- 3. Anggota Kelas (Class Membership - Many-to-Many through explicit table) ---

class AnggotaKelas(models.Model):
    id_anggota = models.AutoField(primary_key=True)
    id_kelas = models.ForeignKey(Kelas, on_delete=models.CASCADE, related_name='anggota')
    id_siswa = models.ForeignKey(
        Pengguna, 
        on_delete=models.CASCADE, 
        limit_choices_to={'peran': PeranPengguna.SISWA}, # Diasumsikan id_siswa merujuk ke Pengguna dengan peran 'siswa'
        related_name='keanggotaan_kelas'
    )

    class Meta:
        db_table = 'anggota_kelas'
        unique_together = ('id_kelas', 'id_siswa') # Agar satu siswa hanya bisa terdaftar sekali di satu kelas
        verbose_name_plural = 'Anggota Kelas'

    def __str__(self):
        return f'{self.id_siswa.nama_lengkap} di {self.id_kelas.nama_kelas}'

# --- 4. Kuis (Quizzes) ---

class Kuis(models.Model):
    id_kuis = models.AutoField(primary_key=True)
    id_pengguna = models.ForeignKey( # Diasumsikan pembuat kuis adalah Pengguna (Guru/Admin)
        Pengguna, 
        on_delete=models.SET_NULL, # Misal: Jika pengguna dihapus, kuis tetap ada, tapi id_pengguna menjadi NULL
        null=True, 
        related_name='kuis_dibuat'
    )
    nama_kuis = models.CharField(max_length=45)
    durasi = models.IntegerField() # Diasumsikan durasi dalam menit/detik (INT)

    class Meta:
        db_table = 'kuis'
        verbose_name_plural = 'Kuis'

    def __str__(self):
        return self.nama_kuis

# --- 5. Stage Game (Game Stages) ---

class StageGame(models.Model):
    id_stage = models.AutoField(primary_key=True)
    nama_stage = models.CharField(max_length=45)

    class Meta:
        db_table = 'stage_game'
        verbose_name_plural = 'Stage Game'

    def __str__(self):
        return self.nama_stage

# --- 6. Hasil Game (Game Results) ---

class HasilGame(models.Model):
    id_hasil_game = models.AutoField(primary_key=True)
    id_stage = models.ForeignKey(StageGame, on_delete=models.CASCADE, related_name='hasil_game')
    id_siswa = models.ForeignKey(
        Pengguna, 
        on_delete=models.CASCADE, 
        limit_choices_to={'peran': PeranPengguna.SISWA}, 
        related_name='hasil_game'
    )
    skor_game = models.IntegerField()
    waktu_game = models.TimeField() # Atau DateTimeField, tergantung kebutuhan
    percobaan_game = models.IntegerField()

    class Meta:
        db_table = 'hasil_game'
        verbose_name_plural = 'Hasil Game'

# --- 7. Hasil Kuis (Quiz Results) ---

class HasilKuis(models.Model):
    id_hasil_kuis = models.AutoField(primary_key=True)
    id_siswa = models.ForeignKey(
        Pengguna, 
        on_delete=models.CASCADE, 
        limit_choices_to={'peran': PeranPengguna.SISWA}, 
        related_name='hasil_kuis'
    )
    id_kuis = models.ForeignKey(Kuis, on_delete=models.CASCADE, related_name='hasil_kuis')
    skor_kuis = models.IntegerField()
    waktu_kuis = models.TimeField() # Atau DateTimeField, tergantung kebutuhan
    percobaan_kuis = models.IntegerField()

    class Meta:
        db_table = 'hasil_kuis'
        verbose_name_plural = 'Hasil Kuis'

# --- 8. Hasil Evaluasi (Evaluation Results) ---

class HasilEvaluasi(models.Model):
    id_hasil_evaluasi = models.AutoField(primary_key=True)
    id_siswa = models.ForeignKey(
        Pengguna, 
        on_delete=models.CASCADE, 
        limit_choices_to={'peran': PeranPengguna.SISWA}, 
        related_name='hasil_evaluasi'
    )
    id_kuis = models.ForeignKey(Kuis, on_delete=models.CASCADE, related_name='hasil_evaluasi')
    nilai = models.DecimalField(max_digits=5, decimal_places=2) # Menggunakan DecimalField untuk nilai yang mungkin desimal

    class Meta:
        db_table = 'hasil_evaluasi'
        verbose_name_plural = 'Hasil Evaluasi'

# --- 9. Section (Sections within a Quiz) ---

class Section(models.Model):
    id_section = models.AutoField(primary_key=True)
    id_kuis = models.ForeignKey(Kuis, on_delete=models.CASCADE, related_name='sections')
    nama_section = models.CharField(max_length=45)
    urutan = models.IntegerField()

    class Meta:
        db_table = 'section'
        ordering = ['urutan'] # Mengatur urutan default
        unique_together = ('id_kuis', 'urutan') # Urutan harus unik dalam satu kuis
        verbose_name_plural = 'Sections'

    def __str__(self):
        return f'{self.nama_section} ({self.id_kuis.nama_kuis})'

# --- 10. Section Item (Quiz Items/Questions) ---

class SectionItem(models.Model):
    id_item = models.AutoField(primary_key=True)
    id_section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='items')
    nama_item = models.CharField(max_length=45) # Mungkin teks singkat dari soal
    jenis_item = models.CharField(
        max_length=20,
        choices=JenisItem.choices,
        default=JenisItem.PILIHAN_GANDA,
    )
    urutan = models.IntegerField()

    class Meta:
        db_table = 'section_item'
        ordering = ['urutan']
        unique_together = ('id_section', 'urutan')
        verbose_name_plural = 'Section Items'

    def __str__(self):
        return self.nama_item

# --- 11. Progres Item (User Progress on Quiz Items) ---

class ProgresItem(models.Model):
    id_progres = models.AutoField(primary_key=True)
    id_pengguna = models.ForeignKey(Pengguna, on_delete=models.CASCADE, related_name='progres_item')
    id_item = models.ForeignKey(SectionItem, on_delete=models.CASCADE, related_name='progres_item')
    status = models.CharField(
        max_length=15,
        choices=StatusProgres.choices,
        default=StatusProgres.BELUM_SELESAI,
    )

    class Meta:
        db_table = 'progres_item'
        unique_together = ('id_pengguna', 'id_item') # Agar progres untuk satu item oleh satu pengguna unik
        verbose_name_plural = 'Progres Item'