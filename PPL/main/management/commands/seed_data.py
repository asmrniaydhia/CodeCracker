from django.core.management.base import BaseCommand
from faker import Faker
from main.models import Pengguna, Kelas, AnggotaKelas
import random
import string

class Command(BaseCommand):
    help = 'Mengisi database dengan data dummy (Seeding) Khusus Kelas 7'

    def handle(self, *args, **kwargs):
        self.stdout.write('🔄 Memulai proses seeding (Mode: Kelas 7 Only)...')
        fake = Faker('id_ID')

        # --- 1. BUAT DATA GURU (5 Orang) ---
        guru_list = []
        for _ in range(5):
            guru = Pengguna.objects.create(
                nama_lengkap=fake.prefix() + " " + fake.last_name() + ", S.Pd", 
                email=fake.unique.email(),
                kata_sandi='123',
                peran='guru'
            )
            guru_list.append(guru)
        
        self.stdout.write(self.style.SUCCESS(f'✓ Berhasil membuat {len(guru_list)} Guru.'))

        # --- 2. BUAT DATA SISWA (30 Orang) ---
        siswa_list = []
        for _ in range(30):
            siswa = Pengguna.objects.create(
                nama_lengkap=fake.name(),
                email=fake.unique.email(),
                kata_sandi='123',
                peran='siswa'
            )
            siswa_list.append(siswa)
            
        self.stdout.write(self.style.SUCCESS(f'✓ Berhasil membuat {len(siswa_list)} Siswa.'))

        # --- 3. BUAT DATA KELAS (15 Kelas - HANYA KELAS 7) ---
        kelas_created_count = 0
        all_kelas = []

        # HANYA KELAS 7
        prefix_kelas = "VII" 
        huruf_kelas = ['A', 'B', 'C', 'D', 'E', 'F', 'G'] # VII A s/d VII G
        
        for _ in range(15): 
            guru_pilih = random.choice(guru_list)
            
            # Generate Nama Kelas Unik untuk Guru Ini
            nama_kelas_dummy = ""
            for i in range(20): 
                # Format PASTI: VII [Huruf]
                calon_nama = f"{prefix_kelas} {random.choice(huruf_kelas)}"
                
                # Cek Database: Apakah guru ini sudah punya kelas dengan nama ini?
                if not Kelas.objects.filter(guru=guru_pilih, nama_kelas=calon_nama).exists():
                    nama_kelas_dummy = calon_nama
                    break
            
            # Jika gagal dapat nama unik (skip iterasi ini)
            if not nama_kelas_dummy:
                continue 

            # Generate Token Unik
            token_acak = ""
            while True:
                token_calon = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
                if not Kelas.objects.filter(token=token_calon).exists():
                    token_acak = token_calon
                    break
            
            # Simpan Kelas
            kelas_baru = Kelas.objects.create(
                guru=guru_pilih,
                nama_kelas=nama_kelas_dummy,
                token=token_acak
            )
            all_kelas.append(kelas_baru)
            kelas_created_count += 1
            
        self.stdout.write(self.style.SUCCESS(f'✓ Berhasil membuat {kelas_created_count} Kelas (Semua Kelas VII).'))

        # --- 4. MASUKKAN SISWA KE KELAS ---
        enrollment_count = 0
        
        if all_kelas:
            for siswa in siswa_list:
                # Pilih 1 kelas acak untuk setiap siswa
                k = random.choice(all_kelas)
                
                # Pastikan tidak double data
                if not AnggotaKelas.objects.filter(siswa=siswa).exists():
                    AnggotaKelas.objects.create(
                        kelas=k,
                        siswa=siswa
                    )
                    enrollment_count += 1

        self.stdout.write(self.style.SUCCESS(f'✓ Berhasil mendaftarkan siswa (Total {enrollment_count} data anggota).'))
        self.stdout.write(self.style.SUCCESS('=== SEEDING SELESAI ==='))