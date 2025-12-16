from django.core.management.base import BaseCommand
from main.models import Section, SectionItem, Kuis

class Command(BaseCommand):
    help = 'Mengisi database Materi dan 3 Kuis Utama (Termasuk Item Evaluasi Akhir)'

    def handle(self, *args, **kwargs):
        self.stdout.write('🔄 Reset Data Materi & Kuis...')
        
        # 1. BERSIHKAN DATA LAMA
        SectionItem.objects.all().delete()
        Section.objects.all().delete()
        Kuis.objects.all().delete()
        self.stdout.write('   (Data lama dibersihkan)')

        # 2. BUAT DATA KUIS (HANYA 3 UTAMA)
        k_enkripsi = Kuis.objects.create(nama_kuis="Kuis Enkripsi")
        k_caesar = Kuis.objects.create(nama_kuis="Kuis Caesar Cipher")
        k_dekripsi = Kuis.objects.create(nama_kuis="Kuis Dekripsi")
        self.stdout.write(self.style.SUCCESS('   ✓ 3 Data Kuis berhasil dibuat'))

        # 3. BUAT SECTION & ITEM (MATERI)
        
        # --- BAB 1: PENGENALAN (urutan 1) ---
        sec_pengenalan, _ = Section.objects.get_or_create(nama_section="Pengenalan", urutan=1)
        SectionItem.objects.create(id_section=sec_pengenalan, nama_item="Definisi", jenis_item='teks', urutan=1)
        SectionItem.objects.create(id_section=sec_pengenalan, nama_item="Aktivitas", jenis_item='latihan', urutan=2)

        # --- BAB 2: ENKRIPSI (urutan 2) ---
        sec_enkripsi, _ = Section.objects.get_or_create(nama_section="Enkripsi", urutan=2)
        SectionItem.objects.create(id_section=sec_enkripsi, nama_item="Teori Enkripsi", jenis_item='teks', urutan=1)
        SectionItem.objects.create(id_section=sec_enkripsi, nama_item="Aktivitas", jenis_item='latihan', urutan=2)
        SectionItem.objects.create(id_section=sec_enkripsi, nama_item="Kuis Enkripsi", jenis_item='kuis', urutan=3, id_kuis=k_enkripsi)

        # --- BAB 3: CAESAR CIPHER (urutan 3) ---
        sec_caesar, _ = Section.objects.get_or_create(nama_section="Caesar Cipher", urutan=3)
        SectionItem.objects.create(id_section=sec_caesar, nama_item="Konsep Caesar Cipher 1", jenis_item='teks', urutan=1)
        SectionItem.objects.create(id_section=sec_caesar, nama_item="Konsep Caesar Cipher 2", jenis_item='teks', urutan=2)
        SectionItem.objects.create(id_section=sec_caesar, nama_item="Aktivitas", jenis_item='latihan', urutan=3)
        SectionItem.objects.create(id_section=sec_caesar, nama_item="Kuis Caesar Cipher", jenis_item='kuis', urutan=4, id_kuis=k_caesar)

        # --- BAB 4: DEKRIPSI (urutan 4) ---
        sec_dekripsi, _ = Section.objects.get_or_create(nama_section="Dekripsi", urutan=4)
        SectionItem.objects.create(id_section=sec_dekripsi, nama_item="Konsep Dekripsi 1", jenis_item='teks', urutan=1)
        SectionItem.objects.create(id_section=sec_dekripsi, nama_item="Konsep Dekripsi 2", jenis_item='teks', urutan=2)
        SectionItem.objects.create(id_section=sec_dekripsi, nama_item="Aktivitas", jenis_item='latihan', urutan=3)
        SectionItem.objects.create(id_section=sec_dekripsi, nama_item="Kuis Dekripsi", jenis_item='kuis', urutan=4, id_kuis=k_dekripsi)

        # ==========================================
        # 4. BUAT SECTION ITEM UNTUK EVALUASI AKHIR (urutan 5)
        # ==========================================
        
        sec_evaluasi, _ = Section.objects.get_or_create(nama_section="Evaluasi", urutan=5)
        
        SectionItem.objects.create(
            id_section=sec_evaluasi, 
            nama_item="Evaluasi Akhir", 
            jenis_item='kuis', # Menggunakan jenis 'kuis' atau 'latihan'
            urutan=1,
            id_kuis=None # Evaluasi Akhir tidak terikat ke Kuis bab manapun
        )

        self.stdout.write(self.style.SUCCESS('   ✓ Section Evaluasi dan Item berhasil ditambahkan'))
        self.stdout.write(self.style.SUCCESS('✅ SEEDING SELESAI!'))