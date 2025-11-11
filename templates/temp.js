// SIDEBAR
const app = document.getElementById('lessonApp');
const toggleBtn = document.getElementById('sidebarToggle');

function toggleSidebar() {
    const collapsed = app.classList.toggle('is-collapsed');
    // ARIA untuk aksesibilitas
    toggleBtn.setAttribute('aria-expanded', String(!collapsed));
    toggleBtn.setAttribute('aria-label', collapsed ? 'Buka sidebar' : 'Tutup sidebar');
}
toggleBtn.addEventListener('click', toggleSidebar);

document.addEventListener('DOMContentLoaded', function () {
  // ambil nama file dari URL saat ini (contoh: 'enkripsi.html')
  const currentFile = (location.pathname.split('/').pop() || 'index.html').toLowerCase();

  // cari link di sidebar yang cocok
  const links = document.querySelectorAll('.sidebar a[href]');
  let activeLink = null;

  links.forEach(a => {
    const href = a.getAttribute('href');
    if (!href) return;

    // normalisasi: ambil bagian file di akhir (handle path seperti /templates/quiz/quiz1.html)
    const hrefFile = href.split('/').pop().toLowerCase();
    if (hrefFile === currentFile) {
      activeLink = a;
    }
  });

  if (!activeLink) return;

  // tandai link sebagai aktif (akan diwarnai oleh CSS di atas)
  activeLink.classList.add('active');

  // buka collapsible section (accordion) yang menaungi link aktif
  const collapse = activeLink.closest('.accordion-collapse');
  if (collapse) {
    // tambahkan kelas 'show' agar tetap terbuka
    collapse.classList.add('show');
    collapse.setAttribute('aria-expanded', 'true');

    // ubah state tombol header accordion
    const headerBtn = collapse.previousElementSibling?.querySelector('.accordion-button');
    if (headerBtn) {
      headerBtn.classList.remove('collapsed');
      headerBtn.setAttribute('aria-expanded', 'true');
      headerBtn.classList.add('active-head'); // untuk highlight judul section
    }
  }

  // (opsional) jika kamu punya tombol burger untuk sembunyikan sidebar,
  // pastikan default-nya terbuka:
  const sidebarToggle = document.getElementById('sidebarToggle');
  if (sidebarToggle) {
    sidebarToggle.setAttribute('aria-expanded', 'true');
  }
});